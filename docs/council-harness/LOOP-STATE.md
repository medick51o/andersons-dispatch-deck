# OVERNIGHT AUTOLOOP — council reviews itself, I fix, repeat

Started 2026-08-26 ~00:55. Andrew went to bed and asked for it in automode.
**This file is the resume point if context compacts. Read it first.**

## The reading I'm building on (headless — stated loud, per house rule 2)

"Loop it, summon the council, review, loop it again, fix it, all in automode" =
run more rounds of *the harness reviewing itself*, applying what carries, without waking
him. Same loop as rounds 1–3, now unattended.

## BOUNDS — declared before the run, because that is the harness's own law

I told him hours ago that this loop does not converge and that BOUNDED must apply to
rounds, not just seats. So:

- **3 rounds maximum: 4, 5, 6.** Then stop regardless of what is still open.
- **Stop early** if a round carries nothing, or carries only the two documented
  architecture limits (absolute-path reads / no real containment).
- **No push.** Local commits only. The repo is PUBLIC and pushing is outward-facing.
- **No deletes, no sends, no config changes** outside this repo.
- **The gate is `council_selftest.py`.** It must be green before every commit. If a fix
  turns it red and I cannot repair it in one attempt, revert that fix and carry on.
- **Metered spend:** kimi is ON (~cents/round). He said "spend what you got to spend to
  get it done" during this campaign and asked tonight why seats were missing rounds.
  glm and claude stay off.

## Bench

`grok composer cgrok gemini kimi` — 4 labs (xAI, Cursor, Google, Moonshot).
Rule 2 labs. kimi timeout 1500s (it timed out at 700s in round 3 and lost the round).
gemini votes again this round: the agy shell-command auto-deny that killed it in rounds
1–2 now has a prompt-level guard, and `_run_seat` retries once on a croak.

## Round log

| Round | Carried | Fixed | Verdict |
|---|---|---|---|
| 1 (22:53) | 10 | 10 | 4/5 seats — gemini croaked |
| 2 (23:17) | ~10 refusals of round 1's fixes | all | 3/4 — grok killed by my relative `--cwd` |
| 3 (23:39) | 5 | 3 (+2 documented as limits) | PARTIAL — kimi timed out |
| 4 (00:58) | 7 | 7 (2 of them by withdrawing a false claim in the BRIEF) | DEGRADED — **5/5 seats, 4 labs, first full attendance** |
| 5 | *in flight* | | |

**Round 4's lesson:** three seats unanimously flagged "fix #7 claimed read-only
enforcement" — and the false claim was in `BRIEF-VERIFY.md`, not the code. I had
downgraded the code and left the brief asserting the old promise, so the council was
correctly reviewing a lie I was still telling it. Briefs are part of the artifact.

Round 4 fixes: reserved synthesiser (a same-lab spare is pulled off the voting bench, so
no voter groups and no lineage is lost) · opaque flat shuffled finding ids, which no
longer leak authorship or per-seat counts · `[CLEAN]` is now a real vote, so a unanimous
"nothing wrong" cannot report INCONCLUSIVE · longest-content JSON parsing, so a trailing
status object cannot overwrite a finished review · invented ids reported instead of
silently filtered · tighter template-echo rejection.

## Standing facts a resumed session needs

- Committed at `6917e62` (local, unpushed, on `main`).
- Since that commit, uncommitted: one-retry-on-croak, the agy no-shell guard, and the
  selftest fix for a FLAKY test (hardcoded `S1-1` ids vs the randomised label map).
- Raw seat transcripts are gitignored — they hold machine paths and the repo is public.
- Known limits, NOT bugs to re-fix: absolute-path reads defeat the sandbox; real
  containment is an OS-level job. If a round re-raises these, log and move on.
- `seat_core.truncate_reply` still returns 135 chars for `limit=100` — found by the very
  first council, never fixed, lives in shared code both seat families use. Fair game.

## Morning report should say

Rounds run, what carried, what I fixed, what I refused to fix and why, gate status, and
the exact commits — plus anything I chose not to touch because he was asleep.
