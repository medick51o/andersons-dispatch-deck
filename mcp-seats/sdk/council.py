#!/usr/bin/env python3
"""council — the fan-out the shop runs by hand, as one callable.

WHY THIS EXISTS
Six councils ran on 2026-08-24. Every one was assembled by hand: write the packet, copy
it per seat, dispatch each vendor CLI with its own flags, poll for completion, dig the
reply out of a different JSON shape per vendor, tally votes, synthesize. Fifteen-plus tool
calls of loop work done in prose.

That hand-assembly is not free of consequence. One experiment that evening passed
`write_capable` to a seat expecting `always_approve`; the seat ignored the unknown key,
ran twelve REAL dispatches, and reported them as refusals. A coded harness does not drift
between the control arm and the test arm.

WHAT IT ENCODES — the shop's own council law, not a generic fan-out:
  * BLIND        no seat sees another's answer, within a run OR across runs.
  * DISTINCT     a carry is counted in LABS, not seats. Two seats fronting one lab are
                 one lineage and one vote. "A pool is not a vendor."
  * BOUNDED      the seat cap is declared BEFORE the run, never "as many as it takes".
  * PRE-COMMITTED  the decision rule is fixed before any seat reports, so the council
                 converges instead of becoming another round of proposals.
  * METER-HONEST  free and subscription seats are preferred; a seat that spends is
                 labelled 💸 and must be asked for by name.

WHAT IT IS NOT
It does not decide anything. It gathers independent reads and applies arithmetic the
operator fixed in advance. The synthesis, and the ruling, stay human.

HOW THIS FILE GOT ITS SHAPE — two self-reviews, 2026-08-25
Round 1: five seats, blind, reviewing the program that dispatched them. Ten carried. The
sharpest came from `cgrok`, an xAI seat noting the default bench held xAI TWICE, so a
carry could be one lab agreeing with itself. It flagged its own redundancy and got ONE
vote — which the counting rule of the day would have discarded. That is why carries now
count labs, and why vote count is documented as a noise filter, never a ranking.

Round 2 reviewed the fixes and refused most of them. Three seats independently graded the
containment fix FALSE ASSURANCE: it set a working directory, called that "read-only
enforced for every transport", and closed the ticket. A guard that makes an operator
believe they are protected when they are not is worse than no guard. Nothing below claims
containment it does not have; the honest limits are printed at dispatch time, not buried.
"""
import argparse
import asyncio
import io
import json
import os
import random
import re
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seat_core as core  # noqa: E402

HOME = os.path.expanduser("~")
LOCAL = os.environ.get("LOCALAPPDATA", os.path.join(HOME, "AppData", "Local"))
PLAYPEN = os.path.abspath(os.environ.get(
    "WMW_CURSOR_PLAYPEN", os.path.join("C:" + os.sep, "Sync", "_playpen", "cursor")))
ANCHOR = re.compile(r"\[(?:DELETE|MERGE|CUT|FINDING)\]\s*([^\n]{6,90})")

# --------------------------------------------------------------------------
# THE BENCH. Each seat names its transport, its LINEAGE, and what it costs.
# `vendor` is the lab whose brain actually thinks — never the brand of the pipe
# it arrives through. `cgrok` is Cursor-hosted but xAI-blooded, and the tally
# counts it as xAI. `meter` is the honest part: 'sub' bills a flat subscription,
# 'free' rides the plan's included tier, 'credit' spends real money and is never
# chosen for you. `hard_ro` says whether the TRANSPORT can be locked read-only by
# vendor flags — the only containment that actually holds. See _argv.
# --------------------------------------------------------------------------
SEATS = {
    "grok":     dict(vendor="xAI",      mark="⚫",   meter="sub",    transport="grok",
                     hard_ro=True),
    "gemini":   dict(vendor="Google",   mark="🟢",   meter="sub",    transport="agy",
                     hard_ro=False),
    "composer": dict(vendor="Cursor",   mark="🎼",   meter="free",   transport="cursor",
                     model="composer-2.5", hard_ro=False),
    "cgrok":    dict(vendor="xAI",      mark="🟣⚫", meter="free",   transport="cursor",
                     model="cursor-grok-4.6-high", hard_ro=False),
    "kimi":     dict(vendor="Moonshot", mark="🌙",   meter="credit", transport="cursor",
                     model="kimi-k3-max", hard_ro=False),
    "glm":      dict(vendor="Zhipu",    mark="🔷",   meter="credit", transport="cursor",
                     model="glm-5.2-high", hard_ro=False),
    "claude":   dict(vendor="Anthropic", mark="🟠",  meter="credit", transport="cursor",
                     model="claude-opus-5-thinking-high", hard_ro=False),
}
FREE = [k for k, v in SEATS.items() if v["meter"] in ("sub", "free")]


def _exe(kind):
    if kind == "grok":
        # grok.exe was missing here until the first self-review; on a box where the shim
        # resolves to the .exe, the seat simply reported "grok CLI not found".
        return core.discover_executable(
            (os.path.join(HOME, ".grok", "bin", "grok"),
             os.path.join(HOME, ".grok", "bin", "grok.cmd"),
             os.path.join(HOME, ".grok", "bin", "grok.exe")), "grok")
    if kind == "agy":
        return core.discover_executable((os.path.join(LOCAL, "agy", "bin", "agy.exe"),), "agy")
    return core.discover_executable(
        (os.path.join(LOCAL, "cursor-agent", "cursor-agent.cmd"),
         os.path.join(HOME, ".local", "bin", "cursor-agent")), "cursor-agent")


def _argv(seat, packet_path, sandbox):
    """Per-vendor invocation. A council READS; no seat is ever write-capable here.

    WHAT CONTAINS A SEAT, HONESTLY:
      grok        vendor --deny flags on every write tool. This is real enforcement.
      agy         --mode plan is the vendor's own read-only mode. Real, but it is one
                  mode flag, not a deny list.
      cursor      --mode ask. No deny list is available. NOT hard containment.

    The sandbox cwd below is defence in depth on top of that, and nothing more. It stops
    a well-behaved relative write; it does not stop an absolute path. An earlier version
    of this file called the sandbox "read-only enforced for every transport" — three seats
    graded that FALSE ASSURANCE, correctly, because the operator would believe the harness
    contained a seat that only the vendor flags were containing. The sandbox is now placed
    OUTSIDE the repo and outside the artifact tree, which is the part it genuinely buys:
    a seat's relative file tools land in an empty temp folder with no council answers in
    reach. `hard_ro` in SEATS records which transports have the real barrier, and the run
    prints the seats that do not.
    """
    s = SEATS[seat]
    exe = _exe(s["transport"])
    if not exe:
        return None, f"{s['transport']} CLI not found"
    ask = (f"Read the file {packet_path} in FULL and follow it exactly. "
           f"Output only your findings in the format the brief specifies.")

    if s["transport"] == "grok":
        ptr = os.path.join(sandbox, "ask.txt")
        io.open(ptr, "w", encoding="utf-8", newline="").write(ask)
        # --cwd MUST be absolute. A relative path here made grok exit 1 with
        # "Failed to set working directory" on every dispatch of the 23:17 run.
        return [exe, "--prompt-file", ptr, "--cwd", os.path.abspath(sandbox),
                "--deny", "Write", "--deny", "Edit", "--deny", "MultiEdit",
                "--deny", "NotebookEdit", "--deny", "Bash", "--deny", "MCPTool",
                "--disallowed-tools", "Agent", "--permission-mode", "default",
                "--no-memory", "--disable-web-search", "--output-format", "json"], None
    if s["transport"] == "agy":
        # Antigravity auto-denies any tool needing `command` permission in headless mode,
        # because it cannot prompt for one -- and that killed this seat in two of three
        # councils on 2026-08-25. Its allow-list already covers read_file/cat/type/rg, so
        # it was reaching for a shell it did not need. Telling it plainly not to is the
        # cheap fix; the expensive one is guessing at allow-rules for a tool the log
        # never named.
        return [exe, "--mode", "plan", "--effort", "high", "--print-timeout", "25m",
                "-p", ask + " Use your file-reading tool only. Do NOT run shell commands "
                "of any kind — they are auto-denied here and will end your run.",
                "--output-format", "json"], None
    # --trust auto-approves inside the cwd, which is why the cwd is a throwaway temp dir
    # holding one packet. Without it the seat stalls on a prompt it cannot answer headless.
    return [exe, "--model", s["model"], "--mode", "ask", "--trust",
            "-p", ask, "--output-format", "json"], None


def _reply(raw):
    """Every vendor buries the answer under a different key. This is the tax the
    hand-run version paid six times a day, in my head, with a fresh mistake available
    each time.

    Scans TOP-LEVEL objects only, keeping the last one that carries content. Two separate
    bugs live here and both were found by review, not by me:
      * taking the FIRST match let a startup banner become a seat's entire review;
      * scanning every `{` let a NESTED object shadow its parent, because the child
        starts later than the parent does. Advancing past each decoded object — rather
        than one character — makes nested objects unreachable.
    """
    out, i, dec, n = None, 0, json.JSONDecoder(), len(raw)
    while i < n:
        j = raw.find("{", i)
        if j == -1:
            break
        try:
            v, end = dec.raw_decode(raw, j)
        except json.JSONDecodeError:
            i = j + 1
            continue
        if isinstance(v, dict) and (v.get("text") or v.get("result") or v.get("response")):
            out = v
        i = max(end, j + 1)
    if not out:
        return ""
    return str(out.get("text") or out.get("result") or out.get("response") or "")


def anchors(text):
    """The findings a reply actually raised.

    A bare `[FINDING]` match is not a vote. The brief itself prints a template line, so a
    seat that restates the instructions used to be counted as a lab that had voted —
    inflating turnout with a reply containing no finding at all. A real finding names
    something and explains it, so it must carry a WHY within reach and must not be the
    template.
    """
    out = []
    for m in ANCHOR.finditer(text):
        name = m.group(1).strip(" *`")
        if name.startswith("<") or "under 60 chars" in name.lower():
            continue                                     # the brief's own example line
        if not re.search(r"\bWHY\s*:", text[m.end():m.end() + 400], re.I):
            continue
        out.append(name)
    return out


async def _run_seat(seat, packet_path, sandbox, timeout_s, retries=1):
    """Returns (seat, text, err, secs, warn). `warn` is a nonzero exit that still
    produced parseable text — kept, because the content is usually real, but recorded
    so it degrades the run instead of voting at full strength in silence.

    ONE RETRY ON A CROAK, none on a timeout. Across three councils every seat croaked at
    least once and each time a whole LAB left the bench silently, which is far more
    damaging to a lineage-counted tally than to a seat-counted one. A crash is often
    transient and worth a second attempt; a timeout already consumed the operator's
    patience budget and retrying it just spends it twice.
    """
    for attempt in range(retries + 1):
        res = await _dispatch_once(seat, packet_path, sandbox, timeout_s)
        err = res[2]
        if not err or "timed out" in err or "not found" in err or attempt == retries:
            return res
        print(f"   ↻ {seat} croaked ({err[:52]}) — one retry")
    return res


async def _dispatch_once(seat, packet_path, sandbox, timeout_s):
    argv, err = _argv(seat, packet_path, sandbox)
    if err:
        return seat, "", err, 0.0, None
    t0 = time.perf_counter()
    proc = await asyncio.create_subprocess_exec(
        *argv, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL, cwd=sandbox)
    try:
        out, errb = await asyncio.wait_for(proc.communicate(), timeout=timeout_s)
    except asyncio.TimeoutError:
        proc.kill()
        return seat, "", f"timed out after {timeout_s}s", time.perf_counter() - t0, None
    secs = time.perf_counter() - t0
    text = _reply((out or b"").decode("utf-8", "replace"))
    tail = (errb or b"").decode("utf-8", "replace").strip()[-300:]
    if not text:
        rc = f"exit {proc.returncode}. " if proc.returncode else ""
        return seat, "", f"{rc}no parseable reply. {tail}", secs, None
    warn = f"exit {proc.returncode}: {tail[:110]}" if proc.returncode else None
    return seat, text, None, secs, warn


SYNTH_BRIEF = """# SYNTHESIS — group these findings. Do not judge them.

Several reviewers examined the same material blind and raised the findings listed below,
one per line, each with an ID. **Your only job is to say which IDs name THE SAME finding.**

You are not deciding what is right, what matters, or what should be done. You are not
adding findings. You are not dropping findings. You are grouping.

Reviewers are anonymous, in an order chosen at random, and you are given only their
finding TITLES — never their prose. One of them may be you, and you are not meant to be
able to tell.

## Rules
- **Every ID below must appear in exactly one group.** If an ID matches nothing else, it
  is its own group of one. Dropping an ID is the one unforgivable error.
- Group only when the titles name the SAME underlying problem. Two findings about the
  same function naming different defects are TWO groups.
- Name each group in the clearest words any reviewer used, not a blend of all of them.
- **Never invent an ID.** Only IDs printed below exist.

## Output — this exact format, one line per group, and nothing else
```
[GROUP] <name, under 70 chars> | ids: <comma-separated IDs, e.g. S1-2, S3-1>
```

---

# THE FINDINGS

"""


async def synthesize(items, seat, rundir, sandbox_root, timeout_s):
    """One extra blind call that GROUPS findings before they are counted.

    Round 1 proved this is not optional: four seats found the same bug in four different
    sentences, and string-matching scored it as four findings with one vote each --
    reporting unanimous agreement as nothing carried. A tally that cannot recognise
    agreement is worse than none, because it reads as disagreement.

    THE SYNTHESISER IS OFTEN ALSO A VOTER, which round 1 carried 4/4 as real bias. A
    non-voting seat is preferred and tried first. When none is available the bias is
    reduced, not erased, and the run says so:
      * labels are a RANDOM permutation, not alphabetical -- the old `sorted()` scheme
        was a deterministic map off the public seat list that a voter could invert;
      * the synthesiser receives finding TITLES ONLY, never the prose, so there is no
        writing style to recognise as its own. Grouping by title is slightly coarser
        than grouping by full text. That is the price of removing the tell, and it is
        cheaper than the bias it buys off.
    """
    ids = list(items)                       # items: {"S1-2": (seat, title)}
    rnd = random.Random(os.urandom(8))
    rnd.shuffle(ids)

    lines = [SYNTH_BRIEF]
    for i in ids:
        lines.append(f"{i}   {items[i][1]}")
    sandbox = os.path.join(sandbox_root, "SYNTH")
    os.makedirs(sandbox, exist_ok=True)
    path = os.path.join(sandbox, "pkt.md")
    io.open(path, "w", encoding="utf-8", newline="").write("\n".join(lines))

    _s, text, err, _secs, warn = await _run_seat(seat, path, sandbox, timeout_s)
    if err:
        return None, err, {}
    io.open(os.path.join(rundir, "SIGNED-SYNTH.md"), "w",
            encoding="utf-8", newline="").write(text)
    if warn:
        # A crashing synthesiser that still emitted [GROUP] lines used to be treated as
        # clean grouping, because the exit code was never threaded through to here.
        return None, f"synthesiser exited nonzero ({warn})", {}

    groups, placed = [], {}
    for m in re.finditer(r"\[GROUP\]\s*([^|\n]{4,90})\|\s*ids:\s*([^\n]+)", text):
        gname = m.group(1).strip(" *`")
        raw = {x.strip().upper() for x in m.group(2).split(",") if x.strip()}
        real = {x for x in raw if x in items}       # invented IDs cannot vote
        if not gname or not real:
            continue
        for x in real:
            placed[x] = placed.get(x, 0) + 1
        groups.append((gname, {items[x][0] for x in real}))
    if not groups:
        return None, "synthesis returned no parseable [GROUP] lines", {}

    # AUDIT BY IDENTITY, NOT BY COUNT. The first audit compared how many findings a seat
    # raised against how many groups mentioned it -- so a dropped finding plus one
    # spurious placement netted to zero and printed nothing. IDs make it exact: every ID
    # must be placed exactly once, and both directions are reported.
    audit = {"dropped": sorted(i for i in items if i not in placed),
             "duplicated": sorted(i for i, n in placed.items() if n > 1)}
    audit = {k: v for k, v in audit.items() if v}
    return sorted(groups, key=lambda g: -len(g[1])), None, audit


def tally(findings):
    """Fallback counter: group on a normalized title and count distinct seats.

    Deliberately dumb, and KNOWN INADEQUATE -- it cannot see that two differently-worded
    findings are the same finding, which is exactly how a unanimous result once printed as
    nothing carried. It runs only when synthesis is unavailable, and the run is marked
    DEGRADED when it does, because silently falling back to the broken counter would
    reintroduce the original bug wearing the fixed one's output format.
    """
    votes = {}
    for seat, text in findings.items():
        for name in anchors(text):
            key = re.sub(r"[`*_\"']", "", name).strip().lower()[:70]
            votes.setdefault(key, set()).add(seat)
    return sorted(votes.items(), key=lambda x: -len(x[1]))


def _labs(seat_set):
    """A carry is counted in LABS, not seats. Two seats fronting the same lab are one
    lineage and one vote -- the shop's standing law, previously written down everywhere
    except in the code that does the counting."""
    return {SEATS[s]["vendor"] for s in seat_set}


async def run_council(brief, material=(), seats=None, rule=3, timeout_s=1800,
                      outdir=None, synth=None, keep_sandboxes=False):
    """Dispatch a blind council and tally it against a rule fixed before the run."""
    seats = list(seats or FREE)
    unknown = [s for s in seats if s not in SEATS]
    if unknown:
        raise ValueError(f"unknown seats: {unknown}")
    if rule < 1:
        raise ValueError("rule must be at least 1; a rule of 0 carries everything")
    labs = _labs(seats)
    # A rule no bench can satisfy is a run that cannot succeed. Refuse at the door rather
    # than dispatching everyone and printing a foregone "nothing carried".
    if rule > len(labs):
        raise ValueError(
            f"rule {rule} is unreachable: this bench holds {len(labs)} distinct lab(s) "
            f"({', '.join(sorted(labs))}). Carries count labs, not seats.")
    metered = [s for s in seats if SEATS[s]["meter"] == "credit"]

    # ARTIFACTS and SANDBOXES live in different trees, on purpose. When seat working
    # directories sat inside the artifact tree, a seat's own file tools could walk up to
    # `../../SIGNED-*.md` and read a sibling's or a previous council's answers -- blindness
    # broken by the harness's own layout. Sandboxes are now throwaway temp dirs; the
    # answers are never in reach of a relative path.
    stamp = time.strftime("%Y%m%d-%H%M%S")
    base = os.path.abspath(outdir or os.path.join(PLAYPEN, "council"))
    rundir, n = None, 0
    while rundir is None:                    # same-second councils must not share a dir
        cand = os.path.join(base, f"run-{stamp}-{os.getpid()}" + (f"-{n}" if n else ""))
        try:
            os.makedirs(cand, exist_ok=False)
            rundir = cand
        except FileExistsError:
            n += 1
    sandbox_root = tempfile.mkdtemp(prefix="council-")

    body = [brief, ""]
    for path in material:
        body += ["", f"# ===== {os.path.basename(path)} =====", "```",
                 io.open(path, encoding="utf-8", errors="replace").read(), "```"]
    packet = "\n".join(body)

    dupes = [v for v in labs if sum(1 for s in seats if SEATS[s]["vendor"] == v) > 1]
    soft = [s for s in seats if not SEATS[s]["hard_ro"]]
    print(f"🌈 COUNCIL — {len(seats)} seats · {len(labs)} labs, rule: {rule}+ LABS carry "
          f"(declared before the run)")
    for s in seats:
        d = SEATS[s]
        print(f"   {d['mark']} {s:10} {d['vendor']:10} "
              f"{'💸 CREDIT' if d['meter'] == 'credit' else d['meter']}"
              f"{'' if d['hard_ro'] else '   (no vendor read-only flags)'}")
    if dupes:
        print(f"   ⚠ same lab seated twice: {', '.join(sorted(dupes))} — those seats share "
              f"a lineage\n     and count as ONE vote toward a carry.")
    if rule == len(labs):
        print(f"   ⚠ rule {rule} equals the bench's lab count — this council requires "
              f"UNANIMITY to carry anything.")
    if soft:
        print(f"   ⚠ containment is best-effort on: {', '.join(soft)}. Their read-only "
              f"rests on one\n     vendor mode flag plus a throwaway cwd, NOT a deny list. "
              f"Do not treat it as a sandbox.")
    if metered:
        print(f"   ⚠ metered seats present: {', '.join(metered)} — these SPEND")
    print()

    jobs = []
    for s in seats:                      # one packet, one private sandbox, per seat
        sb = os.path.join(sandbox_root, s)
        os.makedirs(sb, exist_ok=True)
        p = os.path.join(sb, "pkt.md")
        io.open(p, "w", encoding="utf-8", newline="").write(packet)
        jobs.append(_run_seat(s, p, sb, timeout_s))

    t0 = time.perf_counter()
    results = await asyncio.gather(*jobs)
    findings, failures, malformed, warns = {}, {}, {}, {}
    for seat, text, err, secs, warn in results:
        if err:
            failures[seat] = err
            print(f"   {SEATS[seat]['mark']} {seat:10} FAILED after {secs:.0f}s — {err[:70]}")
            continue
        io.open(os.path.join(rundir, f"SIGNED-{seat}.md"), "w",
                encoding="utf-8", newline="").write(text)
        found = anchors(text)
        if not found:
            # A seat that answers in prose has not voted. It used to count as turnout and
            # contribute nothing, quietly inflating how well-attended a council was.
            malformed[seat] = "replied without a usable [FINDING] anchor"
            print(f"   {SEATS[seat]['mark']} {seat:10} {len(text):>7,} chars  {secs:>5.0f}s"
                  f"  ⚠ NO FINDINGS — not counted")
            continue
        findings[seat] = text
        if warn:
            warns[seat] = warn
        print(f"   {SEATS[seat]['mark']} {seat:10} {len(text):>7,} chars  {secs:>5.0f}s"
              f"  {len(found):>2} findings" + (f"  ⚠ {warn[:40]}" if warn else ""))

    heard = _labs(findings)
    print(f"\n   {len(findings)}/{len(seats)} seats voted "
          f"({len(heard)} labs) in {time.perf_counter() - t0:.0f}s")

    degraded = [f"{s} exited nonzero but its reply was counted" for s in warns]
    rows, audit, synth_used = None, {}, None
    if len(findings) >= 2:
        items, tries = {}, []
        # THE SEAT INDEX ITSELF IS A TELL. Round 2 randomised the ORDER the findings are
        # printed in, but kept `S{i}` numbered off `sorted(findings)` -- so S1 was always
        # the alphabetically-first seat, and a synthesiser that knows the bench could
        # decode its own label from the number alone. Three seats caught it. The seat ->
        # index map is now itself randomised per run.
        snames = sorted(findings)
        random.Random(os.urandom(8)).shuffle(snames)
        for si, s in enumerate(snames, 1):
            for ai, name in enumerate(anchors(findings[s]), 1):
                items[f"S{si}-{ai}"] = (s, name)
        # Prefer a seat that did not vote; never one that spends without being asked.
        # If the preferred synthesiser dies, TRY THE NEXT rather than dropping straight
        # to the broken string counter -- gemini's headless croak took out a whole tally
        # that a second attempt would have saved.
        # Candidate order: the operator's pick, then free seats that were never dispatched,
        # then seats that WERE dispatched but did not vote (a timeout on a long review says
        # little about a short title-grouping job, and they are genuinely neutral), then the
        # voters. An explicit --synth no longer ENDS the chain -- naming a preferred
        # synthesiser used to mean one attempt and a degraded run if it croaked.
        tries = [synth] if synth else []
        tries += [k for k in SEATS if k not in seats and SEATS[k]["meter"] != "credit"]
        tries += [k for k in seats if k not in findings]
        tries += sorted(findings)
        seen = set()
        tries = [k for k in tries if not (k in seen or seen.add(k))]
        for cand in tries:
            voted = cand in findings
            print(f"\n   {SEATS[cand]['mark']} synthesising with {cand}"
                  + (" — A VOTER; titles only, labels randomised, so it should not be able"
                     " to\n     recognise its own findings. Bias reduced, not removed."
                     if voted else " — did not vote (neutral)"))
            rows, synth_err, audit = await synthesize(items, cand, rundir,
                                                      sandbox_root, timeout_s)
            if rows:
                synth_used = cand
                if voted:
                    degraded.append(f"grouped by {cand}, which also voted")
                break
            print(f"   ✗ {cand} could not synthesise: {synth_err[:100]}")
    if rows is None:
        print(f"   ⚠ SYNTHESIS FAILED on every candidate.\n"
              f"     Falling back to raw title matching, which CANNOT see agreement across "
              f"differing wording —\n     the exact bug synthesis exists to fix. Treat the "
              f"counts below as a floor, not a result.")
        degraded.append("synthesis unavailable on every candidate seat")
        rows = tally(findings)
    if audit.get("dropped"):
        print(f"   ⚠ grouping DROPPED {len(audit['dropped'])} finding(s): "
              f"{', '.join(audit['dropped'][:8])}")
        degraded.append(f"{len(audit['dropped'])} findings dropped in grouping")
    if audit.get("duplicated"):
        print(f"   ⚠ grouping placed {len(audit['duplicated'])} finding(s) in more than one "
              f"group: {', '.join(audit['duplicated'][:8])}")
        degraded.append(f"{len(audit['duplicated'])} findings double-placed in grouping")

    # An UNGROUPED tally must not wear the grouped tally's clothes. The fallback counter
    # printed the identical "** CARRIED **" marker, so a degraded run read exactly like a
    # clean one two lines below the warning that said it wasn't -- and the warning is the
    # part a tired operator skips.
    grouped = synth_used is not None
    mark = "** CARRIED **" if grouped else "~~ CARRIED, UNGROUPED ~~"
    carried = []
    if rows:
        if not grouped:
            print(f"\n   (counts below are RAW TITLE MATCHES. Seats that found the same "
                  f"thing in different\n    words appear as separate rows, each undercounted. "
                  f"This is a floor, not a result.)")
        print(f"\n   {'ITEM':54}{'v':>3}{'labs':>6}  seats")
        for item, ss in rows[:25]:
            n = len(_labs(ss))
            tag = f"  {mark}" if n >= rule else ""
            print(f"   {item[:52]:54}{len(ss):>3}{n:>6}  {','.join(sorted(ss))}{tag}")
        if len(rows) > 25:
            hidden = [i for i, ss in rows[25:] if len(_labs(ss)) >= rule]
            print(f"   … {len(rows) - 25} further rows not shown; {len(hidden)} of them "
                  f"CARRIED. Full list in the artifacts.")
        carried = [i for i, ss in rows if len(_labs(ss)) >= rule]
    else:
        print("\n   No usable [FINDING] anchors — the brief should ask for them, with a "
              "WHY line, if you want an automatic tally.")

    # TURNOUT IS NOT A VERDICT. "Nothing carried" and "not enough labs showed up" used to
    # print identically, so a council that never convened read as a council that disagreed.
    if len(heard) < rule:
        verdict = "INCONCLUSIVE"
        print(f"\n   ⛔ INCONCLUSIVE — {len(heard)} lab(s) voted, rule needs {rule}. "
              f"Nothing could carry\n      regardless of content. This is NOT disagreement.")
    elif degraded:
        verdict = "DEGRADED"
        print(f"\n   CARRIED at {rule}+ labs: {len(carried)}")
    elif failures or malformed:
        verdict = "PARTIAL"          # quorum met, but part of the bench never reported
        print(f"\n   CARRIED at {rule}+ labs: {len(carried)}")
    else:
        verdict = "OK"
        print(f"\n   CARRIED at {rule}+ labs: {len(carried)}")
    if degraded:
        print(f"   ⚠ DEGRADED — {'; '.join(degraded)}")
    for s, e in list(failures.items()) + list(malformed.items()):
        print(f"   ✗ {s}: {e[:90]}")

    if keep_sandboxes:
        print(f"   sandboxes kept: {sandbox_root}")
    else:
        shutil.rmtree(sandbox_root, ignore_errors=True)
    print(f"\n   verdict: {verdict}   artifacts: {rundir}")
    return {"verdict": verdict, "findings": findings, "failures": failures,
            "malformed": malformed, "warns": warns, "tally": rows, "carried": carried,
            "labs": sorted(heard), "degraded": degraded, "synth": synth_used,
            "audit": audit, "outdir": rundir}


def main():
    ap = argparse.ArgumentParser(description="Run a blind multi-vendor council.")
    ap.add_argument("brief", help="path to the brief file")
    ap.add_argument("-m", "--material", nargs="*", default=[], help="files the seats read")
    ap.add_argument("-s", "--seats", nargs="*", default=None,
                    help=f"default: the free/subscription bench ({', '.join(FREE)})")
    ap.add_argument("-r", "--rule", type=int, default=3,
                    help="distinct LABS that carry a finding (default 3)")
    ap.add_argument("-t", "--timeout", type=int, default=1800)
    ap.add_argument("-o", "--outdir", default=None)
    ap.add_argument("--synth", default=None,
                    help="seat that groups the findings (default: a free non-voter)")
    ap.add_argument("--keep-sandboxes", action="store_true",
                    help="do not delete the per-seat temp working directories")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    brief = io.open(a.brief, encoding="utf-8").read()
    out = asyncio.run(run_council(brief, a.material, a.seats, a.rule, a.timeout,
                                  a.outdir, a.synth, a.keep_sandboxes))
    # The exit code carries the verdict. A council that never convened, whose grouping was
    # degraded, or that lost part of its bench must not look like a clean pass downstream.
    return 0 if out["verdict"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
