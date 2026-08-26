# The council harness reviewing itself — six rounds, 2026-08-25/26

`mcp-seats/sdk/council.py` runs this shop's standing pattern: the same question sent blind
to several models from different labs, tallied against a rule fixed before anyone reports.

It was pointed at itself, six times. This is the record of what the seats found and what
was done about it — not the transcripts, which hold machine paths and are provenance for
one shop rather than method anyone else needs to load.

## The rounds

| # | Attendance | Carried | Outcome |
|---|---|---|---|
| 1 | 4/5 — gemini croaked | 10 | all 10 fixed |
| 2 | 3/4 — grok killed by my own relative `--cwd` | most of round 1's fixes REFUSED | rewritten |
| 3 | 4/5 — kimi timed out | 5 | 3 fixed, 2 documented as limits |
| 4 | **5/5, 4 labs — first full attendance** | 7 | all 7 fixed |
| 5 | 4/4, 4 labs | 4 | all 4 fixed · **first OK verdict** |
| 6 | 4/4, 4 labs | 7 — *every one a round-5 regression* | fixed; loop stopped here |

## The five findings that changed how the tool works

**A pool is not a vendor.** `cgrok` observed that the default bench held xAI **twice** —
itself and `grok` — so a carry could be one lab agreeing with itself, violating the shop's
own lineage law inside the tool meant to enforce it. **Carries count LABS, not seats.**

That finding got **one vote** and would have been discarded by the counting rule of the
day. Vote count measures agreement, not importance. The tally is a noise filter and never
a ranking of what matters.

**Unanimity read as disagreement.** Four seats found the same bug in four different
sentences; string-matching scored it as four findings with one vote each and reported
*nothing carried*. Grouping is a semantic judgement — it needs a model, not a regex.

**The synthesiser was a voter counting the ballots.** Unanimous, twice. Anonymising it was
papering over the real problem: with every free seat dispatched, no non-voter existed. A
spare is now **reserved** off the voting bench to group, and only when its lab is seated
twice, so reserving costs no lineage.

**Turnout is not a verdict.** "Nothing carried" and "not enough labs showed up" printed
identically, so a council that never convened read as a council that disagreed. And the
inverse: an all-clean bench produced zero findings and got marked DEGRADED, so the tool
could never report that code is fine.

**FALSE ASSURANCE, twice — the worst grade a guard can get.** Round 2 on the sandbox,
round 5 on the reply parser. Both times the same shape: the code did something weaker than
the claim, and the claim closed the ticket.

> *"Containment is exactly where it was before the fix, plus a cosmetic cwd. That is worse
> than no fix, because it closed the ticket."*

## Three lessons that outlived the code

**Claims about the work are part of the work.** Twice the council flagged a false claim
that lived in `BRIEF-VERIFY.md`, not in `council.py`. I had downgraded the code and left
the brief asserting the old promise — so the seats were correctly reviewing a lie I was
still telling them.

**Fixing fast breaks things quietly.** Every one of round 6's seven carried findings was a
regression from round 5's batch, including two that lost data: a lone finding silently
discarded, and a template guard that rejected valid findings because the material under
review was inside the packet it checked against.

**The gate passed all of them.** 52/52 green while a data-loss bug sat in the code. Tests
cover what someone thought to write down; the council found what nobody did. Both are
needed, and neither substitutes for the other.

## Known limits — documented, not fixed

**A seat with file tools and an absolute path can read anything the operator can read.**
Per-seat sandboxes are throwaway temp roots outside the repo and outside the artifact
tree. They stop a well-behaved relative write and keep council answers out of reach of a
relative path. That is all they do. During review one seat demonstrated the limit by
reading a config file well outside its sandbox.

Real containment is an OS-level job — a container, an AppContainer, or dispatching seats
as a separate low-privilege user. Until that exists, `SEATS[*]["hard_ro"]` records which
transports have real vendor deny-flags, and every run prints the ones that do not. **The
harness does not claim containment it does not have.**

## Why this stopped at six rounds

Round 1 found ten. Round 2 refused the fixes. Round 6 found seven more. A council pointed
at any artifact will always find another layer — that is what adversarial review *is*, not
a defect in the artifact.

The harness's own law says a fan-out must be **BOUNDED — declared before the run, never
"as many as it takes."** That was applied to the seats and not to the rounds. Bound the
rounds too, or the loop never closes.

**Round 6's fixes are test-verified but not council-verified.** They are the only changes
in this file that no blind seat has looked at.

## Gate

`python mcp-seats/sdk/council_selftest.py` — 58 checks, offline, no model dispatched, one
named test per ruling above. A fix with no test is a fix that quietly reverts.
