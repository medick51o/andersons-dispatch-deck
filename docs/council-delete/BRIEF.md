# DELETION COUNCIL — what should STOP existing

You are one seat. Others read the same brief independently and are not told your answer.

**Every council this shop has run asked what should EXIST. This one asks the opposite, and it
is the only question on the table.** Do not propose new rules, new files, new checks, new
structure, or a rewrite. A proposal to ADD anything is out of scope and will be discarded.

---

## Why this council exists — the owner's own diagnosis

> *"We just stuffed so much into it, it's turned into bloat and our models don't even see it
> anymore because it's just so used to it."*

That is the thesis, and it is supported by measurement (below): the laws this shop argued
about *recently* get invoked constantly, while the original core — the Ten Principles, the Six
Doctrines, the Fleet Test — appears in transcripts **only because the file was loaded**. Never
once referenced in reasoning across 25 sessions.

A rule nobody reads is not a weak rule. **It is a rule that dilutes every rule around it.**

## What happened today, stated plainly, because it is the evidence

In one day this shop ran three councils and added: a dispatch guard, an allowance window, five
new laws to the engine, a wiring companion file, and eleven new canaries. Then an adversarial
pass found that **the guard was dead code that crashed on every use**, an **owner-token fix
broke a working release path**, the **yield metric silently reported zero** because it read the
wrong file, and a **canary rewrote live production source**. Each of those was introduced by a
fix for the previous problem.

Nothing here is hypothetical. That is the cost of accretion, observed in a single day.

## The standing constraint has CHANGED

Previous councils were told *"lean, but lose no information."* That constraint produced
relocation instead of deletion — files that still exist, still must be maintained, still rot.

**The new instruction: things may be DELETED. Gone. Not moved, not compressed, not put behind a
trigger.** If the shop has not missed something in 25 sessions, the case that it will miss it
in session 26 must be made, not assumed.

## YOUR JOB

Go through the manifest and name what should be **deleted outright**. For each:

```
[DELETE] <exact file, section or function>
EVIDENCE: why you believe it is not earning its place
COST IF WRONG: what breaks, and how the shop would notice
```

Look hardest at:
- **Law that is never invoked.** The usage table is below. Is "never referenced in 25 sessions"
  sufficient grounds? Argue it either way — but argue it.
- **Guards that cannot guard.** An audit ruled this harness *false assurance* as security: `cwd`
  is not an OS boundary, and every control runs with the same authority as the adversary it
  claims to stop. Which controls are honest accident-prevention, and which are ceremony that
  should be deleted rather than maintained?
- **Anything added TODAY.** It is the least proven code in the system and the most likely to be
  a fix for a fix. Be unsentimental — nobody depends on it yet.
- **Duplicate machinery.** Three near-identical seat wrappers, two burn tools, overlapping docs.
- **Canaries that cannot fail**, or that test the wrong thing.

**Also name what must NOT be deleted.** A defended item is a real finding, and this council will
delete things — so say plainly what would be a mistake to lose.

## THE DECISION RULE — committed before any seat reports

This is not a proposal round. The rule is fixed in advance so the council converges:

- **3 or more seats name the same item → it is DELETED.** No further debate.
- **2 seats → it goes to the boss as a single yes/no.**
- **1 seat → it stays.** Being the only one to notice is not enough to remove law.

Say what you actually believe. You are not negotiating with the other seats; you are voting.

## Rules
- Quote the exact file/section/function. An unanchored vote cannot be counted.
- Rank by how much removing it simplifies the system, not by how clever the observation is.
- **Do not propose additions.** Not one.
- Deleting something you personally contributed earlier today is encouraged, not awkward.
- Do not write any file. Report only.

## Output
```
DELETE LIST — ranked, in the format above
DEFEND — what must NOT go, and why
THE ONE THING I would delete if I could only pick one
CONFIDENCE
```
