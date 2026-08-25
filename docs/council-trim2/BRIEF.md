# TRIM COUNCIL, ROUND 2 — fresh eyes, same question: what should be DELETED

You are one seat. Others read this independently and are not told your answer.

**This is a DELETE scan. Not a refactor scan.** Do not propose combining files, rewriting
modules, extracting shared helpers, or restructuring anything. A follow-up pass will ask
exactly that question — this one does not. **Anything that isn't "remove this" is out of scope
and will be discarded.**

---

## Why you are here

Four earlier councils have already cut hard today. You are being brought in *after* the
obvious wins, deliberately, because the shop wants to know **what a fresh reader still finds
that people who have been staring at it all day cannot see.**

The owner's standard, in his own words:

> *"The orchestrator is supposed to have a **lean mean machine** of understanding **where** it
> needs to summon, **how** it gets things summoned, put the work **in front of** the model that
> got summoned, and take that output and **bring it back to the user**."*

> *"I don't want people to download our method and find out they burned all of their usage from
> our setup because we are just running in circles half the time before any work gets pushed to
> the MCP or the seats."*

**Every token of engine that loads is a token a stranger paid before a single model was
summoned.** That is the cost you are minimising.

## Already cut today — do NOT re-propose these

Six Doctrines · the plan card, posture map and routing ledger · the Amendment Law · the Meter
Law's methodology · `bench-burn.py` · **the entire reservation subsystem** (Lock/reserve/release)
· SKILL.md's persistent-seats, reserve-bench, running-the-deck and non-negotiables sections ·
every dated scar, `(boss ruling YYYY-MM-DD)` attribution and *this shop's wiring* aside ·
armcheck's checks that could never fail.

```
per-summon load    ~21,600  ->  ~14,400 tokens
SPINE              877      ->  ~690 lines
dispatch-guard.py  543      ->  323 lines
```

**Assume nothing that remains is sacred.** Four councils have already agreed on the easy calls;
if you only rediscover those, you have added nothing.

## YOUR JOB

Name what should be **deleted outright**. For each:

```
[DELETE] <exact file, section or function>
EVIDENCE: why it is not earning its place
COST IF WRONG: what breaks, and how the shop would notice
```

Hunt specifically for:
- **Law a competent orchestrator would follow without being told.**
- **Rules stated twice** in different words — the earlier passes found five such, there are
  likely more.
- **Code that exists to support something already deleted.**
- **Anything that describes the shop rather than instructing the reader.**
- **Guards that cannot guard.** An audit ruled this harness *false assurance* as security:
  `cwd` is not an OS boundary, and every control runs with the same authority as the adversary
  it claims to stop. Which remaining controls are honest accident-prevention, and which are
  ceremony?

**Also name what must NOT go.** This council deletes things; say plainly what would be a
mistake to lose.

## The decision rule, fixed before any seat reports
- **3+ seats name the same item → DELETED.** No debate.
- **2 seats → the owner decides.**
- **1 seat → it stays.**

You are voting, not negotiating.

## Rules
- Quote exact anchors. An unanchored vote cannot be counted.
- **No additions. No refactors. No rewrites.** Deletions only.
- Do not write any file. Report only.

## Output
```
DELETE LIST — ranked, in the format above
DEFEND — what must NOT go
THE ONE THING I would delete if I could only pick one
CONFIDENCE
```
