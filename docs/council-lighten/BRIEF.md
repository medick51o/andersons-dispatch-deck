# COUNCIL BRIEF — make the engine as light as possible without losing anything

You are one seat on a multi-vendor council. Others are reading this same document with
different lenses, blind to you. Two seats are **invited guests** who have never seen this
method before — if you are one, that outside eye is exactly why you were asked.

---

## What SPINE.md is, and why weight matters

SPINE is the method engine for a one-person AI-orchestration shop. It is **law, not
documentation**: an orchestrator reads it and is bound by it.

**It is loaded into context on every single summon of three different skills.** So every line
is billed again on every task, forever, for every person who installs the method — not just its
author. A wasted line is a tax on strangers.

Current shape, measured:

```
SPINE total                920 lines   ~17,549 tokens
  the engine (law)         ~15,433 tokens   88%
  APPENDIX A (wiring)       ~1,380 tokens    8%
  APPENDIX B (field notes)    ~735 tokens    4%
plus SKILL.md (the loader)  ~4,048 tokens
────────────────────────────────────────────────
every summon costs roughly 21,600 tokens before any work happens
```

## What has already been done, so you do not re-propose it

A council trimmed this document **this morning**. It went 920 → 889 lines, then back to 920
when five new laws were added. Already applied, do not suggest again:

- The inline changelog was collapsed to one clause; git carries history.
- Six war stories were **moved, not deleted**, to `SPINE-PROVENANCE.md`, which no summon loads.
- Restatements of Doctrines 2, 3, 5, Principle 5 and the dispatch gate became pointers.
- The amendment-scar narrative moved to provenance; its one operative law stayed.
- Nine internal contradictions were repaired.

**The standing constraint from the owner, unchanged: "as lean as possible WITHOUT LOSING ANY
INFORMATION."** Relocating text to a file that is not auto-loaded counts as keeping it.
Deleting a rule does not.

## The specific proposal on the table

Split **Appendix A** ("current wiring, NOT law — verify") and **Appendix B** ("append-only;
proven capabilities & gotchas") out of SPINE into a companion file that is read on demand,
exactly as the war stories were. Both appendices already describe themselves as
non-law. Estimated saving: **~2,116 tokens per summon, for every installer, forever.**

**Q1. Is that split right?** What breaks if wiring is not present at load time? An orchestrator
that must *know it can check* something is different from one that must *have it memorised* —
which is this? Name the failure mode.

**Q2. Where else is the weight?** The engine is 88% of the load and nobody has attacked it
structurally. Look for:
- Sections that could be one table instead of prose.
- Law that is genuinely dead — a rule for a situation that no longer occurs.
- Whole subsystems that could be **summarised in the trunk and detailed on demand**, the way
  the appendices would be. What are the best candidates, and what is the load-bearing minimum
  that must stay behind?
- Repetition the earlier pass missed, now that the obvious cases are gone.

**Q3. Is the STRUCTURE wrong?** The deepest question. Right now one file carries: four
load-bearing structures, six doctrines, ten principles, a fleet test, an adjudication protocol,
orchestration mechanics, review culture, an invariant block, four standalone laws, and two
appendices. Everything loads, every time, whether the task needs it or not.

Is a single always-loaded monolith the right shape at all? If you would restructure it —
a small always-loaded core plus on-demand modules, or something else entirely — **say so
concretely**, and say what the core must contain to keep an orchestrator honest before it has
read anything else. Be specific about the risk: a rule nobody loads is a rule nobody follows,
and the whole point of an always-loaded engine is that compliance cannot be optional.

## Rules

- **Quote anchors exactly.** Copy 8–15 words verbatim from any passage you propose changing.
  An approximate anchor is a useless finding.
- Give a **token estimate** per proposal.
- **Defending a section is a real finding.** If something looks cuttable and is not, say why.
- Disagreeing with the premise of this brief is welcome and useful.
- No flattery. The owner wants uncomfortable truths stated plainly.
- Do not write any file. Report only.

## Output format

```
VERDICT (3 sentences max)

Q1 THE APPENDIX SPLIT — yes/no + the failure mode you are worried about
Q2 WHERE THE WEIGHT IS
   [CUT n] <name> (~N tokens)
   ANCHOR:  <exact words>
   WHY SAFE: <where the surviving statement lives>
   ACTION:  MOVE to on-demand | COMPRESS to <text> | DELETE
Q3 STRUCTURE — keep the monolith, or restructure? Concretely.
DEFENDED — what must NOT move, and why
TOTAL: ~N tokens recoverable per summon
CONFIDENCE + what would change your mind
```
