# COUNCIL BRIEF — ROUND 2 (verification pass) — 2026-08-22

You are ONE seat on a four-vendor council. You are blind to the other seats. Round 1 reviewed this
same work and returned: REWORK (Codex), SHIP-WITH-FIXES (Grok, Gemini, Claude). The builder then
applied fixes. **Your job is to verify the FIXED state, not to re-litigate round 1.**

## What was claimed fixed

WRAPPERS (mcp-seats/*.py, now v1.2):
1. Large prompts crashed the Windows command line (32K limit) -> Grok now sends the prompt via
   --prompt-file; Gemini rejects >25K prompts with a clean error instead of crashing.
2. A crafted sessionId could smuggle CLI flags into the resumed session (e.g. sessionId
   "--always-approve"), because the CLI's --resume takes an OPTIONAL value -> ids must now match a
   UUID; no argv value (cwd/model) may start with "-"; resume uses the equals form (--resume=<id>).
3. "Read-only default" was only a doc claim -> when always_approve is false the Grok wrapper now
   passes real argv: --sandbox read-only --disable-web-search --no-subagents --no-memory.
4. PATH was searched before the known install path (substitute-binary risk) -> absolute install
   path is now preferred, PATH is the fallback; stdin is closed (DEVNULL).
5. Errors could look like success -> nonzero exit / error JSON / missing session id now return
   isError; UTF-8 stdio forced; per-request exception boundary so one bad request cannot kill the
   server; JSON extracted with raw_decode instead of first-brace.
6. Gemini's footer now reports the effective brain (UNREPORTED when unknown) so a rented
   non-Gemini brain cannot silently pass as an independent Gemini vote.

DOCTRINE:
7. SPINE existed in three divergent copies, two sharing a version string -> SPINE v2.0 is now the
   single canon, byte-identical in all six locations; it gained THE NOTATION v4.0 (owner of the
   emoji marks) and THE TRANSPORT LAW (persistent seats).
8. The transport laws were unowned and drifting across six files -> SPINE owns them; tier files
   (Deck SKILL, CREW v1.2) now render and cite rather than restate.
9. "Fresh call = blind seat" read as sufficient for independence -> now stated everywhere as
   necessary-but-not-sufficient (a reviewer also needs a different effective-model vendor, or to be
   human-launched).
10. Install was worded as mandatory -> now opt-in per vendor, offer-never-install, with a documented
    one-command removal, a declared Python prereq, and a documented one-request-at-a-time limitation.

## Your job

1. VERIFY each claimed fix against the actual current files. State PASS / FAIL / UNVERIFIED per item
   you check, with the evidence you used.
2. REGRESSION HUNT: did the fixes break anything or introduce new problems? (e.g. does UUID
   validation reject legitimate ids from either CLI? does the read-only argv break normal research
   calls? did the SPINE re-sync drop or contradict any pre-existing law?)
3. Anything still genuinely dangerous on a PUBLIC repo that strangers install from.

## Deliverable

Numbered findings, most severe first: severity (CRITICAL/MAJOR/MINOR/NIT) - file+location - what -
why it matters - concrete fix. Then a verification table of the 10 items. Then a verdict line:
SHIP / SHIP-WITH-FIXES / REWORK, one sentence, signed with your model name. No padding; "none found"
is a valid section.
