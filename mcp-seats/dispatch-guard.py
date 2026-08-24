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
                try:
                    if time.time() - os.path.getmtime(LOCK) > LOCK_STALE_S:
                        os.unlink(LOCK)       # holder died; reclaim
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

        open_jobs[job] = {
            "est_pct": est_pct,
            "state": "open",
            "note": note,
            "opened": _now().isoformat(timespec="seconds"),
            "expires": (_now() + datetime.timedelta(minutes=LEASE_TTL_MIN)
                        ).isoformat(timespec="seconds"),
        }
        _save(d)
        msg = (f"RESERVED  {job}  {est_pct}% for up to {LEASE_TTL_MIN} min "
               f"({len(open_jobs)}/{MAX_CONCURRENT} leases, {outstanding + est_pct}% committed)")
        if dropped:
            msg += f"\n  (expired and reclaimed: {', '.join(dropped)})"
        return True, msg


def release(job, actual_pct=None, lines=None):
    with Lock():
        d = _load()
        _expire(d)
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
def yield_report(repo, days=7):
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
    spent = sum(h.get("actual_pct") or 0 for h in hist)
    zero = [h for h in hist if h.get("lines") == 0 and (h.get("actual_pct") or 0) > 0]

    L = [f"YIELD — {os.path.basename(os.path.abspath(repo))}, last {days} days",
         "",
         f"  accepted:  {commits} commits, +{added}/-{removed} lines",
         f"  dispatched: {len(hist)} guarded jobs, {spent:.3f}% of the month's allowance"]
    if added and spent:
        L.append(f"  COST PER ACCEPTED LINE: {spent/added:.5f}% of the month")
    if spent and not added:
        L.append("  COST PER ACCEPTED LINE: undefined — spend with NO accepted output.")
    if zero:
        L.append(f"  ZERO-OUTPUT JOBS: {len(zero)} "
                 f"({sum(h['actual_pct'] for h in zero):.3f}% burned for nothing)")
        for h in zero[:5]:
            L.append(f"     - {h['job']}: {h['actual_pct']}%  {h.get('note','')}")
    if not hist:
        L += ["", "  No guarded jobs recorded. Either nothing ran through the guard,",
              "  or dispatches are bypassing it — which is the thing to check."]
    L += ["", "  Note: only dispatches that passed through this guard are counted.",
          "  Cloud/IDE/web lanes are invisible here by construction."]
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
        rc, out = yield_report(a.repo, a.days)
        print(out)
        return rc

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
