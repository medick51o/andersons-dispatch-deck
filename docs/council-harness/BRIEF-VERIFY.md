# VERIFY — did the fixes actually land, or do they only look like they did?

Yesterday a blind council reviewed `council.py`, the program dispatching you now. Ten
findings carried. The file below is the version after the fixes. **Your job is to try to
prove the fixes are fake.**

Assume good intentions and bad execution. A fix that reads well in a comment and does
nothing in the code is worse than the original bug, because it closes the ticket.

## What was claimed fixed — check each against the code, not the comment

1. **Carries count LABS, not seats.** Two seats fronting the same lab (`grok` and `cgrok`
   are both xAI) should count as one vote toward a carry.
2. **The synthesiser is anonymised.** It sees S1..Sn, never seat names, so it cannot
   favour its own findings. A free non-voter is preferred when one exists.
3. **Synthesis failure is loud.** Falling back to the dumb string counter must mark the
   run DEGRADED, never silently print numbers in the fixed format.
4. **Turnout is separated from verdict.** Too few labs voting must print INCONCLUSIVE,
   not "nothing carried".
5. **Synthesis is audited.** Findings a seat raised but that landed in no group must be
   reported as a possible drop.
6. **Reply parsing takes the LAST complete object**, and a nonzero exit code is surfaced.
7. **Read-only is NOT claimed as enforced.** Only Grok's transport has real deny-flags;
   the others rest on one vendor mode flag plus a throwaway cwd. `hard_ro` records which
   is which and the run prints the weak ones. *An earlier version of this brief claimed
   the sandbox enforced read-only everywhere. Three councils graded that false assurance,
   correctly. The claim is withdrawn; check that the CODE makes no stronger promise.*
8. **Blindness survives across runs for RELATIVE paths only** — unique run directory,
   per-seat throwaway sandboxes outside the repo and outside the artifact tree. An
   absolute path still defeats it, and that is a documented limit, not a fixed bug.
9. **Prose with no `[FINDING]` anchor is not turnout — but `[CLEAN]` is.** A seat that
   reviewed and found nothing votes clean; only a reply that ignored the format is
   dropped.
10. **The exit code carries the verdict** — a degraded or inconclusive council must not
    exit 0.

## Attack each one

For every item: find the line that implements it, then find the input that defeats it.
Concretely — can you construct a reply, a seat list, a timing, or a filesystem state where
the claimed protection does not hold? Race conditions and absolute paths count.

Also answer: **which of these ten is the weakest**, and is any of them *false assurance* —
a guard that makes an operator believe they are protected when they are not? False
assurance is the most serious defect a safety mechanism can have, worse than its absence.

If a fix is genuinely correct, say so plainly and move on. A review that objects to
everything is as useless as one that objects to nothing.

## Output — this exact anchor format

```
[FINDING] short name, under 60 chars
WHY: one or two sentences, naming the line or construct
FIX: what to change
```

If you reviewed everything above and genuinely found nothing worth raising, say so with a
single `[CLEAN]` line and a sentence on what you checked. That is a real vote and it is
counted. Do not manufacture a finding to look thorough.

Do not write any file. Report only.
