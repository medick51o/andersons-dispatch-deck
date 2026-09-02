#!/usr/bin/env python3
"""Round-2 batch B — the restatement cuts BOTH cross-vendor seats found independently.

Every cut here was raised by Composer AND Gemini, blind to each other. Each one collapses
a restatement into a pointer at the section that actually owns the rule. No rule, number,
condition or exception is removed — only the second and third telling of it.
"""
import io
import shutil

BASE = r"C:\Users\<you>\.claude\skills\team-rocket-takes-over\SPINE.md"
TARGETS = [
    r"C:\Users\<you>\.claude\skills\trm\SPINE.md",
    r"C:\Users\<you>\.claude\skills\dispatch\SPINE.md",
    r"C:\Sync\Projects\andersons-dispatch-deck\SPINE.md",
    r"C:\Sync\Projects\team-rocket-method-public\SPINE.md",
    r"C:\Sync\Projects\team-rocket-takes-over\SPINE.md",
]

s = io.open(BASE, encoding="utf-8").read()
before = s.count("\n")
applied, skipped = [], []


def sub(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        skipped.append(f"{label} (matched {n}x)")
        return
    s = s.replace(old, new)
    applied.append(label)


# --- B1: Doctrine 2 restates Part I §3's bug fork in full (both seats) ---
sub("""### Doctrine 2 · INSTRUMENT, DON'T GUESS
The bug-side of the Diagnose/Design fork, promoted to reflex. When theory stalls, build the
instrument. One honest measurement beats a splash of hypotheses. *(The boss asked for this himself
— make it reflex.)*""",
    """### Doctrine 2 · INSTRUMENT, DON'T GUESS
Part I §3's bug fork, promoted to reflex at the boss's own request.""",
    "B1 Doctrine 2 -> pointer")

# --- B2: Doctrine 3 restates Reality Contract terms 2 & 4 (both seats) ---
sub("""### Doctrine 3 · SELF-VERIFY + HONEST DEFERRALS
Build things that check their OWN end-state and report requested-vs-achieved, loud, with rollback
(Reality Contract terms 2 & 4). When a piece can't land safely, FLAG it, never fake it. A guard
that reverts itself beats a fix that bricks the box. Silent slop is the crime.""",
    """### Doctrine 3 · SELF-VERIFY + HONEST DEFERRALS
Reality Contract terms 2 & 4, promoted to reflex: an artifact reports its own requested-vs-achieved,
and a piece that can't land safely is FLAGGED, never faked. **Silent slop is the crime.**""",
    "B2 Doctrine 3 -> pointer")

# --- B3: Part VI dispatch gate repeats Part I §2 verbatim (both seats) ---
# Keep the crew-scaling clause here, since it is the ONLY place a number appears --
# but bind it to Part I's consent rule, which resolves CONTRA-1 (see below).
sub("""### The dispatch gate (before every task)
Two questions: (1) multiple stages, files, or surfaces? (2) would doing it inline burn frontier
quota on non-judgment work? Both no → just do it, signed by whoever did it. Any yes → delegate with
a ticket. Scale the crew to the job (one worker for a contained task; two-to-four for genuinely
independent workstreams; more only on the boss's explicit ask) and always inside the five-prong
fleet test. **Fan-outs cost multiples, not increments.**""",
    """### The dispatch gate (before every task)
Part I §2's two questions, applied per task. Both no → just do it, signed by whoever did it. Any
yes → delegate with a ticket. **Seat count is governed by Part I §2 and the Part IV fleet test:**
one worker for a contained task; the canon shape of one builder + one cross-vendor reviewer for real
code; **anything wider — parallel workstreams included — dispatches only on the boss's explicit go.**""",
    "B3 dispatch gate -> pointer (+CONTRA-1 fix)")

# --- B4: Doctrine 1 gate 4 restates the Ladder's top rung (both seats) ---
sub("""4. **BOSS IN-HAND — the TOP gate, above all of it.** The bench catches CODE""",
    """4. **BOSS IN-HAND — the TOP gate** (Ladder of Truth, Part I §1). The bench catches CODE""",
    "B4 Doctrine 1 gate 4 -> pointer")

# --- B5: Principle 5 restates the oracle/RED rule (both seats) ---
sub("""5. **Gates referee, but a gate is only an arbiter if it can FAIL.** Automated tests are the most
   reproducible evidence available, and opinion yields to them **once the oracle is checked against
   the task**. Nothing is "done" until gates are green. **A regression test is not evidence until
   proven to fail against the unfixed code.** (See Ladder of Truth.)""",
    """5. **Gates referee, but a gate is only an arbiter if it can FAIL** (Ladder of Truth, Part I §1,
   which owns the oracle check and the RED-first rule). Automated tests are the most reproducible
   evidence available, and opinion yields to them. Nothing is "done" until gates are green.""",
    "B5 Principle 5 -> pointer")

# --- B6: Part IV repeats Part I §2's earn-a-head line verbatim (both seats) ---
sub("""
*If a fan-out cannot be justified in one sentence, it is decoration.*
""", "\n", "B6 Part IV earn-a-head echo")

# --- B7: Part VI section preamble carries no rule (both seats) ---
sub("""> These are the operating mechanics the principles require. Higher tiers may bind a""",
    """> Operating mechanics for the principles. Higher tiers may bind a""",
    "B7 Part VI preamble")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")
