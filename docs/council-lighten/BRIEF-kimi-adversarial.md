# ADVERSARIAL REVIEW — 🌙 Kimi K3, second pass, deep

You reviewed this engine once today as an invited outsider. Your carve-out was adopted: you
argued the notation and meter-mark grammar are **memorise-not-lookup**, that a grammar applied
per line cannot be fetched per line, and that splitting it out would cause silent
non-compliance. Two other seats independently reached the same conclusion from different
angles. **That finding changed the design.**

You are now brought back with a different job. **Attack the result.**

Changes have been APPLIED to the live engine since you last saw it. Your task is to break them,
and to break the bigger proposal that has NOT been applied. Assume the author is pleased with
himself and is therefore at his least careful. Assume every consensus in this council is
suspect precisely because it was unanimous — including your own earlier finding.

## What was APPLIED (attack these)

1. **The appendices were split into `SPINE-WIRING.md`**, which is never auto-loaded, with the
   NOTATION and meter-mark grammar deliberately carved back into the trunk per your ruling.
   In their place the trunk now carries three load triggers: before a seat preflight or the
   session's first dispatch; before selecting a vendor capability; when a vendor-specific
   failure appears.
2. Three duplicated statements became pointers: a ship-rule restatement, the consent gate
   (Part I §2 now declared its owner), and a repeated stdin instruction.
3. Four cross-references that pointed at the now-moved "Appendix A" were repointed.

**Questions:** Are those three triggers actually sufficient and actually reflexive? Name a
realistic session where an orchestrator needs the wiring and NONE of the three fires. Does
declaring one clause "the owner" of a rule genuinely work when the other sites now say less —
or has the rule become weaker at four sites to be stronger at one? Did the repoint miss a
semantic dependency that a text search would not catch?

## What was NOT applied, and why (attack this too)

Three seats proposed a full **core + on-demand modules** restructure, worth an estimated
3,300–12,400 tokens per summon. It was NOT applied. The stated reason:

> Every seat made it conditional on a loader that can **fail closed** when a required module is
> missing. This shop's loader is prose read by an agent — it cannot resolve a module, cannot
> record which modules were read, and cannot halt when one is absent. The precondition is not met.

**Attack that reasoning.** Is it correct, or is it an excuse for not doing the hard thing? Can a
prose loader enforce more than credited — and if so, exactly how would you write a trigger that
an agent cannot skip? Or is the true answer that conditional law is never enforceable law, in
which case the other seats' 12,400-token proposal is dangerous and should be rejected outright
rather than deferred?

## Your standing

You are a **guest seat**, metered, invited back because your first pass changed the design. You
owe this shop nothing. Say the thing the house seats will not.

## Rules
- Quote anchors exactly, 8–15 words verbatim.
- Rank findings by what an orchestrator would DO differently.
- If the applied changes are sound, say so plainly and briefly — a manufactured objection is
  worse than none.
- Do not write any file. Report only.

## Output
```
VERDICT (3 sentences)
BREAKS IN WHAT WAS APPLIED   — ranked, with anchors
THE DEFERRED RESTRUCTURE     — correct call, or cowardice? Argue it.
WHAT I GOT WRONG LAST TIME   — audit your own first pass
THE THING NOBODY WILL SAY
CONFIDENCE + what would change your mind
```
