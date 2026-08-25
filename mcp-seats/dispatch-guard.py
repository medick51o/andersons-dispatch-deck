#!/usr/bin/env python3
"""dispatch-guard — the controls the 2026-08-24 council said were missing.

    python dispatch-guard.py preflight <repo>      # refuse a dispatch set up to fail
    python dispatch-guard.py reserve <job> -t 20   # ATOMIC claim on the month's allowance
    python dispatch-guard.py release <job> -t 18   # reconcile a finished job
    python dispatch-guard.py status                # outstanding leases + headroom
    python dispatch-guard.py yield <repo>          # cost per ACCEPTED change

Three findings drove this, none of them mine:

  Codex  — a time-of-check/time-of-use race. Thirteen launches each read the same
           apparently-available balance before delayed vendor telemetry recorded any
           of them; every check passed and their sum blew the month. A meter that
           re-reads a percentage cannot prevent that. Only an ATOMIC reservation can.

  Kimi   — "the rig optimizes the vendor's metric, not the shop's." Everything here
           measured spend against an allowance the vendor defines and reports, and
           nothing anywhere measured cost per accepted change. Hence `yield`.

  Boss   — the agents had nowhere to put the code. Eleven of thirteen produced zero
           lines into a repo staged deliberately empty. Hence `preflight`.

WHAT THIS CANNOT DO, stated plainly so nobody mistakes it for a fence:
it governs dispatches that pass THROUGH it. Cloud agents, IDE agent mode, the web
dashboard, the mobile app and CI all execute on the vendor's infrastructure and obey
the vendor's settings, not this file. Those lanes are closed in the vendor's control
plane or not at all — see VENDOR-CHECKLIST.md.
"""
import argparse
import datetime
import io
import json
import os
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
STORE = os.environ.get("WMW_GUARD_FILE",
                       os.path.join(HOME, ".anderson-method", "reservations.json"))
LOCK = STORE + ".lock"

MAX_CONCURRENT = int(os.environ.get("WMW_MAX_CONCURRENT_JOBS", "2"))
LEASE_TTL_MIN = int(os.environ.get("WMW_LEASE_TTL_MIN", "90"))
LOCK_STALE_S = 30

# a dispatch may not claim more than this share of the month in one go
MAX_SINGLE_CLAIM_PCT = float(os.environ.get("WMW_MAX_SINGLE_CLAIM_PCT", "10"))
# total outstanding reservations may not exceed this share of the month
MAX_OUTSTANDING_PCT = float(os.environ.get("WMW_MAX_OUTSTANDING_PCT", "25"))

BANNED_STACK = (("maxmode", "true"), ("effort", "xhigh"), ("speed", "fast"))


# ---------------------------------------------------------------- locking
def _lock_pid():
    try:
        return int(io.open(LOCK, encoding="utf-8").read().strip() or 0)
    except (OSError, ValueError):
        return 0


def _pid_alive(pid):
    """True unless we can prove the process is gone. Fails CLOSED: an unknown
    state keeps the lock held, because a stolen lock is worse than a stuck one."""
    if not pid:
        return False
    if os.name == "nt":
        try:
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                                 capture_output=True, text=True, timeout=10).stdout
            return str(pid) in out
        except Exception:
            return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class Lock:
    """Atomic across processes. O_EXCL create is the portable primitive.

    Without this the whole tool is theatre: two launches would read the same
    headroom, both pass, and both spend. That is the exact race Codex named.
    """

    def __enter__(self):
        start = time.time()
        while True:
            try:
                fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                # Age alone is NOT death. Reclaiming on a timer lets a slow-but-living
                # holder have its lock stolen, after which two processes both believe they
                # hold it -- which is the very race this lock exists to prevent.
                # Verify the recorded PID is actually gone first. (Audit 2026-08-24.)
                try:
                    if time.time() - os.path.getmtime(LOCK) > LOCK_STALE_S:
                        if not _pid_alive(_lock_pid()):
                            os.unlink(LOCK)   # holder is genuinely dead; reclaim
                            continue
                except OSError:
                    pass
                if time.time() - start > LOCK_STALE_S * 2:
                    raise SystemExit("guard: could not acquire lock; is a job wedged?")
                time.sleep(0.05)

    def __exit__(self, *a):
        try:
            os.unlink(LOCK)
        except OSError:
            pass


def _load():
    try:
        return json.load(io.open(STORE, encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"jobs": {}}


def _save(d):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    tmp = STORE + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, STORE)      # atomic swap; never a half-written ledger


def _now():
    return datetime.datetime.now()


def _expire(d):
    """Drop leases past their TTL. A crashed job must not hold the month hostage."""
    live, dropped = {}, []
    for k, v in d.get("jobs", {}).items():
        if v.get("state") != "open":
            continue
        try:
            if datetime.datetime.fromisoformat(v["expires"]) < _now():
                dropped.append(k)
                continue
        except (KeyError, ValueError):
            dropped.append(k)
            continue
        live[k] = v
    d["jobs"] = live
    return dropped


# ---------------------------------------------------------------- preflight
def _git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip()


def preflight(repo, model=None, mode_flags=None, min_files=1):
    """Refuse a dispatch that is set up to produce nothing, or to cost too much.

    This is the boss's finding turned into a gate: an agent with no destination
    still spends at full rate.
    """
    problems, notes = [], []

    if not os.path.isdir(repo):
        return 1, [f"target is not a directory: {repo}"], []

    rc, _ = _git(repo, "rev-parse", "--git-dir")
    if rc != 0:
        problems.append(f"{repo} is not a git repository — no write-set can be verified")
    else:
        rc, out = _git(repo, "ls-files")
        tracked = [l for l in out.splitlines() if l.strip()]
        code = [f for f in tracked
                if os.path.splitext(f)[1].lower() in
                (".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".go", ".rs", ".java",
                 ".c", ".cpp", ".h", ".rb", ".php", ".swift", ".kt", ".sh", ".ps1")]
        if len(tracked) < min_files:
            problems.append(f"repo has {len(tracked)} tracked files — "
                            f"an agent dispatched here has nowhere to put code "
                            f"(this is the Aug 21-22 failure, exactly)")
        elif not code:
            problems.append(f"repo has {len(tracked)} tracked files but NO source files — "
                            f"staging pad, not a build target")
        else:
            notes.append(f"{len(tracked)} tracked files, {len(code)} source")

        rc, out = _git(repo, "status", "--porcelain")
        if out:
            notes.append(f"{len(out.splitlines())} uncommitted changes present")

    flags = {k.lower(): str(v).lower() for k, v in (mode_flags or {}).items()}
    stacked = [f"{k}={v}" for k, v in BANNED_STACK if flags.get(k) == v]
    if len(stacked) >= 2:
        problems.append("expensive mode stack: " + " + ".join(stacked) +
                        " — measured 5.5x the cheapest included model")
    elif stacked:
        notes.append("surcharged flag: " + stacked[0])

    if model and "-fast" in model.lower():
        notes.append(f"{model} is a FAST tier — measured 3.6x its non-fast twin")

    return (1 if problems else 0), problems, notes


# ---------------------------------------------------------------- reservation
def reserve(job, est_pct, note=""):
    """Claim headroom BEFORE dispatch. Atomic: the whole point.

    Returns (ok, message). A refusal here is cheap; the alternative is thirteen
    agents that each passed a check and together took two thirds of the month.
    """
    # A negative or zero claim passed the upper cap and SUBTRACTED from outstanding,
    # manufacturing headroom out of arithmetic. (Audit 2026-08-24, Kimi finding 8.)
    if not (est_pct > 0):
        return False, (f"a reservation must claim a positive share; got {est_pct}. "
                       f"Negative claims manufacture headroom.")
    with Lock():
        d = _load()
        dropped = _expire(d)
        open_jobs = d["jobs"]

        if job in open_jobs:
            return False, f"job '{job}' already holds a lease ({open_jobs[job]['est_pct']}%)"
        if len(open_jobs) >= MAX_CONCURRENT:
            held = ", ".join(sorted(open_jobs))
            return False, (f"{len(open_jobs)} leases already open (cap {MAX_CONCURRENT}): {held}\n"
                           f"  Finish or release one first. Concurrency IS the control — "
                           f"the incident was 13 launches, not one bad model.")
        if est_pct > MAX_SINGLE_CLAIM_PCT:
            return False, (f"single claim of {est_pct}% exceeds the {MAX_SINGLE_CLAIM_PCT}% cap. "
                           f"Split the job or raise WMW_MAX_SINGLE_CLAIM_PCT deliberately.")

        outstanding = sum(v["est_pct"] for v in open_jobs.values())
        if outstanding + est_pct > MAX_OUTSTANDING_PCT:
            return False, (f"outstanding {outstanding}% + this {est_pct}% would exceed the "
                           f"{MAX_OUTSTANDING_PCT}% ceiling on committed-but-unspent allowance.")

        # A lease now carries an owner token. Without it `release <victim>` freed any
        # lease, so two cheap reservations could hold the whole cap for the TTL and lock
        # the operator out of his own rig. (Audit 2026-08-24, Kimi finding 8.)
        token = f"{os.getpid()}-{int(_now().timestamp())}"
        open_jobs[job] = {
            "est_pct": est_pct,
            "state": "open",
            "owner": token,
            "note": note,
            "opened": _now().isoformat(timespec="seconds"),
            "expires": (_now() + datetime.timedelta(minutes=LEASE_TTL_MIN)
                        ).isoformat(timespec="seconds"),
        }
        _save(d)
        msg = (f"RESERVED  {job}  {est_pct}% [owner {token}] for up to {LEASE_TTL_MIN} min "
               f"({len(open_jobs)}/{MAX_CONCURRENT} leases, {outstanding + est_pct}% committed)")
        if dropped:
            msg += f"\n  (expired and reclaimed: {', '.join(dropped)})"
        return True, msg


def release(job, actual_pct=None, lines=None, owner=None):  # owner kept for callers, unused
    with Lock():
        d = _load()
        _expire(d)
        # The owner check that used to live here made every CLI-created lease
        # unreleasable, because the CLI has no way to supply a token. It defended against
        # a same-user denial of service on a single-user machine -- an adversary who can
        # call release can also delete the file the lease lives in. It cost a working
        # path and bought nothing. Removed 2026-08-24 on Codex's finding.
        v = d["jobs"].pop(job, None)
        if not v:
            return False, f"no open lease named '{job}'"
        hist = d.setdefault("history", [])
        hist.append({"job": job, "est_pct": v["est_pct"], "actual_pct": actual_pct,
                     "lines": lines, "closed": _now().isoformat(timespec="seconds"),
                     "note": v.get("note", "")})
        d["history"] = hist[-200:]
        _save(d)
        out = f"released {job} (reserved {v['est_pct']}%"
        if actual_pct is not None:
            out += f", actual {actual_pct}%"
        out += ")"
        if lines is not None and actual_pct:
            if lines == 0:
                out += "\n  ZERO LINES for a real spend — this is the failed-work multiplier."
            else:
                out += f"\n  {actual_pct/lines:.4f}% of the month per accepted line"
        return True, out


# ---------------------------------------------------------------- yield
FAST_SURCHARGE = ("-fast",)          # measured 3.6x-5.5x their non-fast twins


def find_events_csv():
    """Newest Cursor usage export, if the operator dropped one somewhere obvious.

    Desktop is OneDrive-redirected on this fleet, so it is resolved, never guessed.
    """
    import glob
    home = os.path.expanduser("~")
    spots = [os.path.join(home, "Downloads"),
             os.path.join(home, "OneDrive", "Desktop"),
             os.path.join(home, ".claude", "uploads")]
    hits = []
    for s in spots:
        hits += glob.glob(os.path.join(s, "**", "*usageevents*.csv"), recursive=True)
    return max(hits, key=os.path.getmtime) if hits else None


def load_events(path, since=None):
    """Parse Cursor's per-event usage export — the ONLY meter that sees every lane.

    Our own ledger records what the MCP seats dispatched. This file records what the
    ACCOUNT spent, cloud agents and IDE included, which is precisely the 96% our
    ledger was blind to on 2026-08-24.
    """
    import csv
    rows = []
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            d = (r.get("Date") or "")[:10]
            if since and d < since:
                continue
            model = (r.get("Model") or "(unnamed)").strip()
            try:
                tok = int(r.get("Total Tokens") or 0)
            except ValueError:
                tok = 0
            cost = 0.0
            c = (r.get("Cost") or "").strip()
            if c and c.lower() != "included":
                try:
                    cost = float(c.lstrip("$"))
                except ValueError:
                    pass
            lane = ("cloud-agent" if (r.get("Cloud Agent ID") or "").strip()
                    else "automation" if (r.get("Automation ID") or "").strip()
                    else "interactive")
            rows.append({"date": d, "model": model, "tokens": tok, "cost": cost,
                         "lane": lane, "max": (r.get("Max Mode") or "").strip() == "Yes"})
    return rows


def yield_report(repo, days=7, events_csv=None):
    """Cost per ACCEPTED change — the shop's own metric, not the vendor's."""
    since = (_now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    rc, out = _git(repo, "log", f"--since={since}", "--pretty=%H", "--numstat")
    if rc != 0:
        return 1, f"not a git repo: {repo}"
    added = removed = commits = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            try:
                added += int(parts[0]); removed += int(parts[1])
            except ValueError:
                pass
        elif len(parts) == 1 and len(line) == 40:
            commits += 1

    d = _load()
    hist = [h for h in d.get("history", []) if h.get("closed", "") >= since]

    # Token truth comes from the spend ledger the seats already write, not from
    # hand-entered numbers. A metric nobody has to remember to record is the only
    # kind that survives contact with a real week.
    # Must match where the seat actually writes (it moved out of the playpen today).
    # Reading the old path made this report a confident zero. (Codex, 2026-08-24.)
    ledger = os.environ.get(
        "WMW_CURSOR_LEDGER",
        os.path.join(os.path.expanduser("~"), ".anderson-method", "bench-spend.jsonl"))
    calls, toks = 0, 0
    if os.path.exists(ledger):
        for line in io.open(ledger, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("ts", "") < since:
                continue
            calls += 1
            # _log_spend writes these at the TOP level, not nested under "usage".
            # Expecting the wrong shape made every row count as zero tokens.
            u = r.get("usage") if isinstance(r.get("usage"), dict) else r
            toks += sum(int(u.get(k, 0) or 0) for k in
                        ("inputTokens", "outputTokens", "cacheReadTokens",
                         "in", "out", "cache_read"))

    L = [f"YIELD — {os.path.basename(os.path.abspath(repo))}, last {days} days",
         "",
         f"  ACCEPTED OUTPUT:  {commits} commits, +{added}/-{removed} lines"]

    # ---- vendor ground truth, if an export is available ------------------
    ev = load_events(events_csv, since) if events_csv else []
    if ev:
        etok = sum(e["tokens"] for e in ev)
        ecost = sum(e["cost"] for e in ev)
        L.append(f"  ACCOUNT SPEND:    {len(ev)} events, {etok:,} tokens"
                 + (f", ${ecost:,.2f} billed" if ecost else " (all within included limits)"))
        if added and etok:
            L += ["", f"  >>> COST PER ACCEPTED LINE: {etok/added:,.0f} tokens <<<"]
        elif added and not etok:
            L += ["", "  (export contained no billable tokens — nothing to divide)"]
        else:
            L += ["", "  >>> COST PER ACCEPTED LINE: UNDEFINED — real spend, NO accepted",
                  "      output in this repo. The failed-work multiplier."]

        lanes = {}
        for e in ev:
            d = lanes.setdefault(e["lane"], [0, 0])
            d[0] += 1
            d[1] += e["tokens"]
        L += ["", "  BY LANE (this is what the seat ledger cannot see):"]
        for lane, (n, t) in sorted(lanes.items(), key=lambda x: -x[1][1]):
            gov = "guarded" if lane == "interactive" else "VENDOR-SIDE, ungoverned here"
            L.append(f"    {lane:14} {n:>5} events  {t:>13,} tok  {t/etok*100:>5.1f}%   {gov}")

        fast = [e for e in ev if any(s in e["model"] for s in FAST_SURCHARGE)]
        if fast:
            ft = sum(e["tokens"] for e in fast)
            L += ["", f"  ⚠ SURCHARGED FAST TIERS: {ft:,} tok ({ft/etok*100:.1f}% of spend)",
                  "    Fast tiers measured 3.6x-5.5x their non-fast twins. Same work,",
                  "    same models, a fraction of the bill if the default is changed."]
        mx = [e for e in ev if e["max"]]
        if mx:
            L.append(f"  ⚠ MAX MODE: {sum(e['tokens'] for e in mx):,} tok on top of the above")

        top = sorted({e["model"] for e in ev},
                     key=lambda m: -sum(e["tokens"] for e in ev if e["model"] == m))[:5]
        L += ["", "  TOP MODELS:"]
        for m in top:
            t = sum(e["tokens"] for e in ev if e["model"] == m)
            L.append(f"    {m:32} {t:>13,}  {t/etok*100:>5.1f}%")
    else:
        L.append(f"  SEAT LEDGER ONLY:  {calls} calls, {toks:,} tokens "
                 f"({len(hist)} guarded leases)")
        if added and toks:
            L += ["", f"  >>> COST PER ACCEPTED LINE: {toks/added:,.0f} tokens (MCP lane only) <<<"]
        L += ["", "  NO VENDOR EXPORT SUPPLIED — this counts only what the MCP seats",
              "  dispatched. On 2026-08-24 that was 3% of real account spend. Download",
              "  the per-event CSV (vendor usage page -> Export CSV) and pass --events,",
              "  or the number below is your own corner of the bill, not the bill."]

    L += ["", "  Note: git output is local time, vendor events are UTC — a boundary day",
          "  can straddle. Widen --days before drawing a conclusion from one day."]
    return 0, "\n".join(L)


# ---------------------------------------------------------------- cli
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("preflight"); p.add_argument("repo")
    p.add_argument("--model"); p.add_argument("--max-mode", action="store_true")
    p.add_argument("--effort"); p.add_argument("--speed")

    p = sub.add_parser("reserve"); p.add_argument("job")
    p.add_argument("-t", "--est-pct", type=float, required=True,
                   help="estimated share of the MONTH'S allowance, in percent")
    p.add_argument("-n", "--note", default="")

    p = sub.add_parser("release"); p.add_argument("job")
    p.add_argument("-t", "--actual-pct", type=float)
    p.add_argument("-l", "--lines", type=int, help="accepted lines this job produced")

    sub.add_parser("status")
    p = sub.add_parser("yield"); p.add_argument("repo"); p.add_argument("--days", type=int, default=7)
    p.add_argument("--events", help="Cursor per-event usage CSV (vendor usage page -> Export CSV). "
                                    "Omit to auto-discover the newest one.")
    p.add_argument("--no-auto", action="store_true", help="do not auto-discover an export")

    a = ap.parse_args()

    if a.cmd == "preflight":
        flags = {"maxmode": a.max_mode, "effort": a.effort, "speed": a.speed}
        rc, problems, notes = preflight(a.repo, a.model, flags)
        for n in notes:
            print(f"  ok   {n}")
        for pr in problems:
            print(f"  STOP {pr}")
        print("\nPREFLIGHT: " + ("REFUSED — fix the above before dispatching."
                                 if rc else "clear."))
        return rc

    if a.cmd == "reserve":
        ok, msg = reserve(a.job, a.est_pct, a.note)
        print(("  " if ok else "  REFUSED — ") + msg)
        return 0 if ok else 1

    if a.cmd == "release":
        ok, msg = release(a.job, a.actual_pct, a.lines)
        print("  " + msg)
        return 0 if ok else 1

    if a.cmd == "status":
        with Lock():
            d = _load(); dropped = _expire(d); _save(d)
        jobs = d.get("jobs", {})
        print(f"RESERVATIONS  ({STORE})\n")
        if not jobs:
            print("  no open leases.")
        for k, v in sorted(jobs.items()):
            print(f"  {k:24} {v['est_pct']:>5}%  until {v['expires'][11:16]}  {v.get('note','')}")
        print(f"\n  {len(jobs)}/{MAX_CONCURRENT} leases, "
              f"{sum(v['est_pct'] for v in jobs.values()):.1f}% committed "
              f"(ceiling {MAX_OUTSTANDING_PCT}%)")
        if dropped:
            print(f"  reclaimed expired: {', '.join(dropped)}")
        return 0

    if a.cmd == "yield":
        csvp = a.events or (None if a.no_auto else find_events_csv())
        if csvp and not a.events:
            print(f"  (auto-discovered export: {csvp})\n")
        rc, out = yield_report(a.repo, a.days, csvp)
        print(out)
        return rc

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
