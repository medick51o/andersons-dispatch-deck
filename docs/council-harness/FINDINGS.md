# The council harness reviewing itself — three rounds, 2026-08-25

`mcp-seats/sdk/council.py` runs this shop's standing pattern: the same question sent blind
to several models from different labs, tallied against a rule fixed before anyone reports.

It was pointed at itself. Five seats, blind, reviewing the program that dispatched them.
This is the record of what they found and what was done about it — not the transcripts,
which are provenance for one shop rather than method anyone else needs to load.

## Round 1 — ten carried

| Finding | Fixed by |
|---|---|
| The synthesiser is one of the voting seats | prefer a non-voting seat; when none exists, anonymise |
| The voting round is blind; the output directory is not | unique run dir; seat sandboxes moved out of the artifact tree |
| Synthesis failure silently restores the original tally bug | fallback marks the run DEGRADED and says why |
| Too few seats reports as "nothing carried" | INCONCLUSIVE is its own verdict |
| Synthesis output is trusted with no verification | every finding gets an ID; placement is audited by identity |
| The first JSON object can become the vote | last top-level object with content wins |
| Read-only is enforced on one transport only | see **Known limits** — the honest answer is not a code fix |
| Prose replies pass as successful turnout | a finding needs an anchor AND a WHY line |
| The process exits 0 despite seat failures | verdict tiers carried in the exit code |
| Blind dispatch, meter honesty, pre-committed rule | *declared sound — no change* |

**The headline came from a seat auditing its own redundancy.** `cgrok` observed that the
default bench held xAI **twice** — itself and `grok` — so a carry could be one lab agreeing
with itself, violating the shop's own "a pool is not a vendor" law inside the tool that
enforces it. **Carries now count LABS, not seats.**

That finding got **one vote**. Under the counting rule of the day it would have been
discarded. Vote count measures agreement, not importance; the tally is a noise filter, and
it is not a ranking of what matters.

## Round 2 — the council refused the fixes

Three seats independently graded the containment fix **FALSE ASSURANCE**: it set a working
directory, called that "read-only enforced for every transport," and closed the ticket.

> *"Containment is exactly where it was before the fix, plus a cosmetic cwd. That is worse
> than no fix, because it closed the ticket."*

They also caught a hard blocker introduced BY the fix: a relative `--cwd` made one seat
exit 1 on every dispatch, so a four-seat council silently ran as three.

Fixed in round 2: nested JSON objects shadowing the real reply · same-second run
collisions · an audit that netted a dropped finding against a spurious one to zero · the
brief's own template line counting as a vote · nonzero-exit seats voting at full strength
in silence.

## Round 3 — five more; three fixed

Fixed: the `S1..Sn` index was assigned off a sorted seat list, so the label number itself
told a synthesiser which findings were its own · the ungrouped fallback printed the same
`** CARRIED **` marker as a clean tally · the synthesiser pool skipped failed seats, which
are genuine non-voters, and an explicit `--synth` ended the retry chain after one attempt.

## Known limits — documented, not fixed

**A seat with file tools and an absolute path can read anything the operator can read.**
Per-seat sandboxes are throwaway directories outside the repo and outside the artifact
tree, which stops a well-behaved relative write and keeps council answers out of reach of
a relative path. That is all they do. During review one seat demonstrated the limit by
reading a config file well outside its sandbox.

Real containment is an OS-level job — a container, an AppContainer, or dispatching seats
as a separate low-privilege user. Until that exists, `SEATS[*]["hard_ro"]` records which
transports have real vendor deny-flags, and every run prints the ones that do not. **The
harness does not claim containment it does not have.**

## Why this stopped at three rounds

Round 1 found ten. Round 2 refused the fixes and found more. Round 3 found five more. A
council pointed at any artifact will always find another layer — that is what adversarial
review *is*, not a defect in the artifact.

The harness's own law says a fan-out must be **BOUNDED — declared before the run, never
"as many as it takes."** That was applied to the seats and not to the rounds. Bound the
rounds too, or the loop never closes.

## Gate

`python mcp-seats/sdk/council_selftest.py` — 33 checks, offline, no model dispatched, one
named test per ruling above. A fix with no test is a fix that quietly reverts.
