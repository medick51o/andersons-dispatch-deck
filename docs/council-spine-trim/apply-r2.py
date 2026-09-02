#!/usr/bin/env python3
"""Apply the round-2 council trim to SPINE, moving provenance instead of deleting it.

The boss's constraint was exact: "as lean as possible WITHOUT LOSING ANY INFORMATION."
So the war stories behind the laws are not deleted — they are RELOCATED, verbatim, to
SPINE-PROVENANCE.md, which is never loaded on a summon. SPINE keeps the law; the story
keeps its home. Nothing is lost; the per-summon bill drops.
"""
import io
import shutil

BASE = r"C:\Users\<you>\.claude\skills\team-rocket-takes-over\SPINE.md"
PROV = r"C:\Sync\Projects\andersons-dispatch-deck\SPINE-PROVENANCE.md"

TARGETS = [
    r"C:\Users\<you>\.claude\skills\trm\SPINE.md",
    r"C:\Users\<you>\.claude\skills\dispatch\SPINE.md",
    r"C:\Sync\Projects\andersons-dispatch-deck\SPINE.md",
    r"C:\Sync\Projects\team-rocket-method-public\SPINE.md",
    r"C:\Sync\Projects\team-rocket-takes-over\SPINE.md",
]

s = io.open(BASE, encoding="utf-8").read()
before = s.count("\n")
applied, skipped, moved = [], [], []


def sub(old, new, label, provenance=None):
    """Replace exactly-once, or refuse and report. Never guess an anchor."""
    global s
    n = s.count(old)
    if n != 1:
        skipped.append(f"{label} (anchor matched {n}x)")
        return
    s = s.replace(old, new)
    applied.append(label)
    if provenance:
        moved.append((label, provenance))


# =====================================================================
# A. PROVENANCE MOVES — the war stories leave SPINE, verbatim, to PROV
# =====================================================================

sub("""RED against the unfixed code. State, per test, what it would catch if the fix were reverted; a
  test that cannot answer that is deleted and rewritten, not kept for the count. *(Earned in a
  validation run where a fully green suite hid live bugs, and one test asserted a bug was correct.
  An untested test is an opinion with a green checkmark.)*""",
    """RED against the unfixed code. State, per test, what it would catch if the fix were reverted; a
  test that cannot answer that is deleted and rewritten, not kept for the count. **An untested test
  is an opinion with a green checkmark.**""",
    "P1 oracle anecdote -> provenance",
    "**The oracle rule.** Earned in a validation run where a fully green suite hid live bugs, and "
    "one test asserted a bug was correct.")

sub("""- **The bench catches CODE bugs; the boss catches REALITY bugs — and reality outranks the review.**
  *(The day's hardest-won law: a four-model review council MISSED the bug one real use surfaced in
  a sentence — "no virtual controller spawns." Green gates + passed bench + working in-hand =
  shipped. Any two without the third = not yet.)*""",
    """- **The bench catches CODE bugs; the boss catches REALITY bugs — and reality outranks the review.**
  Green gates + passed bench + working in-hand = shipped. **Any two without the third = not yet.**""",
    "P2 four-model anecdote -> provenance",
    "**Reality outranks the review.** The day's hardest-won law: a four-model review council MISSED "
    'the bug one real use surfaced in a sentence — "no virtual controller spawns." This is the '
    "origin of the top rung of the Ladder, and of the rule that a council widens coverage without "
    "ever reaching reality.")

sub("""  BUILD AN INSTRUMENT to see reality — a tap, a probe, a debug mode that shows the actual data.
  *(A packet tap on the fleet wire ended hours of "maybe it's the session / the slot / the gate"
  by* proving *the input was arriving — collapsing the search space in one read. A splash of""",
    """  BUILD AN INSTRUMENT to see reality — a tap, a probe, a debug mode that shows the actual data.
  *(A splash of""",
    "P3 packet-tap anecdote -> provenance",
    '**Instrument, don\'t guess.** A packet tap on the fleet wire ended hours of "maybe it\'s the '
    'session / the slot / the gate" by *proving* the input was arriving — collapsing the search '
    "space in one read.")

sub("""
*(A toggle's honest self-status once caught the orchestrator's own ACL bug before the boss could —
that is the contract paying for itself.)*
""", "", "P4 toggle-ACL anecdote -> provenance",
    "**The Reality Contract.** A toggle's honest self-status once caught the orchestrator's own ACL "
    "bug before the boss could — the contract paying for itself.")

sub("""The engine-level rules that keep review from becoming a debate club. *(Born from a true cautionary
tale: a two-agent shop where every review spawned a six-minute all-hands argument about whether a
color was red or pink, and no work ever shipped.)*""",
    "The engine-level rules that keep review from becoming a debate club.",
    "P5 red-or-pink anecdote -> provenance",
    "**Review culture.** Born from a two-agent shop where every review spawned a six-minute "
    "all-hands argument about whether a color was red or pink, and no work ever shipped.")

sub("""telling).** When the shop runs unattended these are ABSOLUTE — born from a true horror story (four
agents argued for hours, tokens torched, each restart burning more):""",
    "telling).** When the shop runs unattended these are ABSOLUTE:",
    "P6 token-inferno anecdote -> provenance",
    "**Autonomous-hours discipline.** Born from a horror story: four agents argued for hours, "
    "tokens torched, each restart burning more. This is why the bell exists.")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match exactly — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")

# write the provenance companion
if moved:
    out = ["# SPINE — PROVENANCE",
           "",
           "*The war stories behind the laws.* Every entry here was once a paragraph inside SPINE.md.",
           "They were moved out — verbatim in substance — because SPINE is loaded into context on",
           "**every summon**, and a story that has already done its teaching should not be re-billed",
           "forever. The law it produced still lives in SPINE. Nothing was deleted.",
           "",
           "**This file is never auto-loaded.** Read it when you want to know *why* a rule exists,",
           "or when someone proposes repealing one.",
           "",
           "---",
           ""]
    for label, text in moved:
        out.append(text)
        out.append("")
    io.open(PROV, "w", encoding="utf-8", newline="").write("\n".join(out))
    print(f"\nprovenance: {len(moved)} stories preserved -> {PROV}")
