#!/usr/bin/env python3
"""Round-2 batch G — Grok's contradictions. The sharpest findings of the round.

G1 is the one that mattered most: the dispatch gate was an escape hatch from the review
law. An orchestrator could answer "no" to both gate questions, build real code itself,
and ship it unreviewed while citing SPINE for the right to do so.
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


# --- G1: THE HOLE. The dispatch gate governs who BUILDS. It never governed
# whether the result gets reviewed -- but read alone it says "just do it,
# signed, done", and SHOESTRING pushes almost everything down that fork.
# Principle 3 could be skipped by classification. Name the boundary.
sub("""  signed by whoever did it. Most small tasks deserve no orchestration at all. Any yes → delegate
  with a ticket.""",
    """  signed by whoever did it. Most small tasks deserve no orchestration at all. Any yes → delegate
  with a ticket. **The gate decides who BUILDS — never whether the result is REVIEWED.** An
  orchestrator that builds is a builder like any other: if the change is nontrivial and accepted,
  Principle 3 still fires. Only trivial non-artifact work is genuinely review-free, and it is named
  as such out loud.""",
    "G1 dispatch gate is not an escape hatch from Principle 3")

# --- G2: the same hole from the Part VI side ---
sub("""Part I §2's two questions, applied per task. Both no → just do it, signed by whoever did it. Any
yes → delegate with a ticket. **Seat count is governed by Part I §2 and the Part IV fleet test:**
one worker for a contained task; the canon shape of one builder + one cross-vendor reviewer for real
code; **anything wider — parallel workstreams included — dispatches only on the boss's explicit go.**""",
    """Part I §2's two questions, applied per task — they decide who BUILDS, never whether the result is
reviewed (Principle 3 fires either way). Both no → just do it, signed. Any yes → delegate with a
ticket. **Seat count, two cases, so neither hides behind the other:**
- **Parallel BUILDERS on provably disjoint write-sets** — the fleet test governs: Declared and
  Bounded before it runs. The boss is TOLD the shape; he need not be asked.
- **An N-way PANEL on one question** (council, bake-off, multi-lens review) — Part I §2 governs:
  it dispatches only on the boss's **explicit go**, never self-authorized.""",
    "G2 seat count split: disjoint builders vs N-way panel")

# --- G3: "every ELIGIBLE seat at once" reads as a roster instruction that
# overrides the cap the fleet test requires. My own v2.5 phrasing.
sub("""orchestrator convenes **every ELIGIBLE seat at once** (eligibility and the spend gate are owned by
THE COUNCIL SEAT LAW) — one per seat, each a genuinely different effective-model lineage — for""",
    """orchestrator convenes **the boss-approved, fleet-BOUNDED set of eligible seats** (eligibility and
the spend gate are owned by THE COUNCIL SEAT LAW; the cap is set in advance, per Part IV — "as many
as it takes" is not a number) — one per seat, each a genuinely different effective-model lineage — for""",
    "G3 council roster is bounded, not 'everyone'")

# --- G4: "TWO ROUNDS EACH" -- EACH was never defined. Ruling 2 defined ROUND
# but left this. Per debate or per participant changes the cap by 2x or more.
sub("""   tone and nits → ONE EXCHANGE** (Part VII); **unattended debates → TWO ROUNDS EACH, then the bell**""",
    """   tone and nits → ONE EXCHANGE** (Part VII); **unattended debates → TWO ROUNDS PER DEBATE (not per
   participant), then the bell**""",
    "G4 'EACH' defined: per debate, not per participant")

sub("""  two rounds each, then the bell. Resolved → proceed. Unresolved → the dispute goes to the DECISION""",
    """  two rounds per debate — not per participant — then the bell. Resolved → proceed. Unresolved →
  the dispute goes to the DECISION""",
    "G4b autonomous bell unit matched")

# --- G5: a free seat may sit, but Meter Law 4 says a subsidy is never a
# foundation. Both are right; they govern different things. Say which.
sub("""4. **A subsidy is never a foundation.** Vendors buying market share grant far more than sticker
   price, genuinely and in writing. Take the deal; never put a load-bearing lane on it.""",
    """4. **A subsidy is never a foundation.** Vendors buying market share grant far more than sticker
   price, genuinely and in writing. Take the deal; never put a load-bearing lane on it. **A free or
   subsidized seat may hold an EXTRA council vote; it may not be the SOLE build or review path for a
   lane the shop depends on** — that is the line between using a gift and betting on one.""",
    "G5 subsidy: extra vote yes, sole load-bearing lane no")

# --- G6: the pointer promises two paths, then names three statuses that live
# in a different Part.
sub("3. **INDEPENDENT BENCH before merge (Part IV's two paths).** Reviewed from OUTSIDE the builder's",
    "3. **INDEPENDENT BENCH before merge** (Part IV's two legal paths; Part VI's preflight names the\n"
    "   three statuses, including fail-closed `REVIEW UNAVAILABLE`). Reviewed from OUTSIDE the builder's",
    "G6 pointer names the right owner for the statuses")

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
