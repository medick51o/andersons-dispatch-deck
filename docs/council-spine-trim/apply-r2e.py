#!/usr/bin/env python3
"""Round-2 batch E — remaining convergent cuts. Stories relocate; echoes become pointers.

Everything here was raised by at least two of the three seats that reported, and every
anecdote removed from SPINE is appended verbatim to SPINE-PROVENANCE.md.
"""
import io
import shutil

BASE = r"C:\Users\andre\.claude\skills\team-rocket-takes-over\SPINE.md"
PROV = r"C:\Sync\Projects\andersons-dispatch-deck\SPINE-PROVENANCE.md"
TARGETS = [
    r"C:\Users\andre\.claude\skills\trm\SPINE.md",
    r"C:\Users\andre\.claude\skills\dispatch\SPINE.md",
    r"C:\Sync\Projects\andersons-dispatch-deck\SPINE.md",
    r"C:\Sync\Projects\team-rocket-method-public\SPINE.md",
    r"C:\Sync\Projects\team-rocket-takes-over\SPINE.md",
]

s = io.open(BASE, encoding="utf-8").read()
before = s.count("\n")
applied, skipped, moved = [], [], []


def sub(old, new, label, prov=None):
    global s
    n = s.count(old)
    if n != 1:
        skipped.append(f"{label} (matched {n}x)")
        return
    s = s.replace(old, new)
    applied.append(label)
    if prov:
        moved.append(prov)


# --- E1: the repealed-default scar (Gemini + Codex) ---
sub("""  Scaling seat count is the boss's call to make loud, never a habit. *(This REPLACES the old
  "whip-crack parallel delegation as default" — that instinct contradicts Gate-0. Fence and
  right-size first; parallelism is earned per task, not assumed.)*""",
    "  Scaling seat count is the boss's call to make loud, never a habit.",
    "E1 whip-crack scar -> provenance",
    '**Right-size FIRST.** This rule REPLACED an earlier default of "whip-crack parallel delegation" '
    "— an instinct that contradicted Gate-0. Fence and right-size first; parallelism is earned per "
    "task, not assumed.")

# --- E2: bench anecdote inside Doctrine 1 gate 3 (Composer + Codex) ---
sub("""   keep finding the paths that "looked clean." *(It once caught a feature quietly re-introducing the
   exact bug it was built to kill.)*""",
    """   keep finding the paths that "looked clean.\"""",
    "E2 bench anecdote -> provenance",
    "**The independent bench.** It once caught a feature quietly re-introducing the exact bug it was "
    "built to kill.")

# --- E3: unfenced-swarm anecdote (Gemini + Codex) ---
sub("""   No hidden sub-agent swarms, no self-appointed "verify the whole codebase" sweeps. *(The
   anti-pattern that motivated the whole method: an unfenced instance spawning a swarm and torching
   a day of frontier budget.)*""",
    """   No hidden sub-agent swarms, no self-appointed "verify the whole codebase" sweeps.""",
    "E3 unfenced-swarm anecdote -> provenance",
    "**One seat, one job.** The anti-pattern that motivated the whole method: an unfenced instance "
    "spawning a swarm and torching a day of frontier budget.")

# --- E4: council recap paragraph. Codex flagged it twice: as a pure recap AND as
# carrying stale pre-v2.5 phrasing that demotes EVERY same-vendor read to a
# self-check, contradicting Part IV's second legal path.
sub("""This is adversarial verification at full width — the one cross-lineage-review law (a review comes
from a different effective-model vendor than the build — a same-vendor read is a labeled degraded
self-check, never disguised as cross-vendor), scaled to N independent perspectives. Each tier dresses it
differently — a plain **panel** (report by model name), a signed **crew council**, or a puppeteered
**set-piece** — but the engine underneath is this single procedure. *(A four-model council once MISSED
a bug that one real use surfaced instantly — Part I §1. The council widens coverage; it does not
replace in-hand validation.)*""",
    """Adversarial verification at full width — Part IV's review law scaled to N independent
perspectives. Each tier dresses it differently (a plain **panel**, a signed **crew council**, a
puppeteered **set-piece**); the engine underneath is this one procedure. **The council widens
coverage; it never replaces in-hand validation.**""",
    "E4 council recap compressed (+CONTRA fix: stale same-vendor phrasing)")

# --- E5: builder-ticket ambiguity restatement (all three seats) ---
sub("""builder ticket carries the load-bearing line: *"'I could not tell what you meant' is a good
outcome. Propose, don't guess."* Ambiguity is a finding, not an input.""",
    """builder ticket carries the load-bearing line: *"'I could not tell what you meant' is a good
outcome. Propose, don't guess."*""",
    "E5 builder-ticket ambiguity echo")

# --- E6: three-flips history compressed (Codex). The three causes and the
# invariant survive; the worked examples go to provenance. The practical scars
# stay -- they carry instructions found nowhere else.
sub("""The builder seat has flipped for three causes: **capability** (the vendor with local file/shell/git
access got the hammer), **price** (one vendor's budget ran dry, the other had headroom),
**infrastructure** (a sandbox broke; the seat that could still write files built). In each flip the
cold reviewer surfaced defects the builder missed — including guard tests that would pass even with
their callback deleted, and a reviewer's own overclaims discarded under the NOT PROVEN rule. **The
seat map is mission state, never method state. The only fixed point is that the lineage which produced
the work does not approve it.**""",
    """The builder seat has flipped for three causes — **capability**, **price**, **infrastructure** —
and in each flip the cold reviewer surfaced defects the builder missed. **The seat map is mission
state, never method state. The only fixed point is that the lineage which produced the work does not
approve it.**""",
    "E6 three-flips compressed",
    "**The three flips.** Capability: the vendor with local file/shell/git access got the hammer. "
    "Price: one vendor's budget ran dry, the other had headroom. Infrastructure: a sandbox broke, so "
    "the seat that could still write files built. In each flip the cold reviewer surfaced defects the "
    "builder missed — including guard tests that would pass even with their callback deleted, and a "
    "reviewer's own overclaims discarded under the NOT PROVEN rule.")

# --- E7: the v2.5 rationale paragraph is provenance, not law (Codex) ---
sub("""The earlier version of this law admitted only flat-rate subscription seats. That was a proxy for the
real concern and it was wrong in both directions: it barred a free seat that happened to be granted
through a metered transport, and it would have waved through a house seat someone later attached an
API key to. The thing being protected is the boss's money, so the test is his consent.

""", "", "E7 v2.5 rationale -> provenance",
    "**Why the Council Seat Law gates spending, not vendor class.** The earlier version admitted only "
    "flat-rate subscription seats. That was a proxy for the real concern and it was wrong in both "
    "directions: it barred a free seat that happened to be granted through a metered transport, and it "
    "would have waved through a house seat someone later attached an API key to. The thing being "
    "protected is the boss's money, so the test is his consent.")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

if moved:
    with io.open(PROV, "a", encoding="utf-8", newline="") as f:
        for m in moved:
            f.write("\n" + m + "\n")

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")
