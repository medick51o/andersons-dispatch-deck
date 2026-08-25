# ROUND 3 — COMBINE AND SHRINK. Not delete.

You are one seat. Others read this independently and are not told your answer.

**Two delete rounds have already run today. This is the opposite job.** Do not propose
deletions — that question is closed and the easy wins are gone. **Propose MERGES.**

---

## The owner's words for this round

> *"The second scan will be more of what can we do to 'fix' the code or **combine things to
> shrink it down** — basically **combine parts or rewrite it in the name of combining**."*

And his standing spec for the whole system:

> *"The orchestrator is supposed to have a **lean mean machine** of understanding **where** it
> needs to summon, **how** it gets things summoned, put the work **in front of** the model that
> got summoned, and take that output and **bring it back to the user**."*

## Where things stand

```
per-summon load   ~21,600  ->  ~13,797 tokens   (36% cut today)
SPINE             877  ->  ~660 lines
SKILL.md          3,557  ->  ~1,500 tokens
dispatch-guard    543  ->  ~300 lines
```

Already deleted today: Six Doctrines · plan card / postures / routing ledger · Amendment Law ·
Meter Law methodology · the whole reservation subsystem · episode folder / visuals ·
`bench-burn.py` · SKILL's persistent-seats, reserve-bench, running-the-deck, non-negotiables
and legend blocks · every dated scar and ruling attribution · a `MAX_FRAME` check that fired
after the damage it claimed to prevent.

## YOUR JOB — find what should become ONE thing

For each proposal:

```
[MERGE] <what combines with what>
WHY:     what makes them the same thing wearing two names
SHAPE:   what the combined version looks like — concretely enough to build
SAVES:   ~N tokens per summon, or ~N lines of code
RISK:    what gets harder or less clear once they are one
```

Look hardest at:

**1. The three seat wrappers.** `wmw_grok_mcp.py`, `wmw_gemini_mcp.py` and `wmw_cursor_mcp.py`
share a JSON-RPC loop, tool dispatch, path safety, argument validation and spend logging.
An earlier seat estimated a shared transport could reduce each vendor layer to 50–150 lines.
**Is that right?** What genuinely differs per vendor, and what is copy-paste? Note that today
proved the real cost of the duplication: a fix applied to one seat was never propagated to its
siblings, and the Gemini seat still carried bugs the others had fixed months earlier.

**2. Laws in SPINE that are one law wearing two names.** Where do two sections govern the same
decision from different angles? Merging beats cross-referencing.

**3. The small tools.** `allowance.py`, `read-meters.py`, `dispatch-guard.py`,
`calibrate-pool.py` — four files, four CLIs, overlapping concerns. What is the honest shape?

**4. Anything where a rewrite makes it smaller AND clearer**, not just smaller.

## Rules
- Quote exact anchors. An unanchored proposal cannot be evaluated.
- **A merge must reduce total size.** "Reorganised, same length" is not a finding.
- Say plainly when two things only LOOK alike and must stay apart — a defended separation is a
  real finding, and merging things that differ is how subtle bugs are born.
- The decision rule: **3+ seats proposing the same merge → it gets built.**
- Do not write any file. Report only.

## Output
```
MERGE LIST — ranked, in the format above
KEEP APART — what only looks mergeable, and why merging it would hurt
THE ONE MERGE worth doing if only one happens
CONFIDENCE
```
