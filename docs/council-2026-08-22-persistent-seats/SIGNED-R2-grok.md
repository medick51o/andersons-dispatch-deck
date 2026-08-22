I'll start by reading the full council brief and the current files so I can verify the claimed fixes against the code, not re-litigate round 1.The packet is truncated. I'll pull the rest of the brief plus the on-disk wrappers and SPINE copies so the verification is against current files, not the excerpt.Next I’ll hash the SPINE copies, read the live wrappers, and check Grok/Gemini session-id shapes so the UUID and flag-injection claims can be attacked rather than trusted.Wrappers match the packet. I’ll hash every SPINE copy, probe real CLI id formats, and try to break the UUID / dash guards plus the new argv.SPINE hashes already diverge in a couple of places. Next I’ll confirm the six claimed copies, then probe real CLI id formats and whether the new read-only flags break resume.UUID injection looks dead. I’ll check whether `--sandbox read-only` actually binds on this box, what CREW still restates, and how Gemini IDs look.The sandbox probe is still running; I’ll wait on it and independently locate the six claimed SPINE copies.Live CLI checks are in: flag-injection is dead; `--sandbox read-only` is recorded but does not look enforced on Windows. Writing the verification verdict.## Findings

1. **MAJOR** — `mcp-seats/wmw_grok_mcp.py` `run_grok()` (the `not always_approve` argv) + this box’s `~/.grok/config.toml`
   **What:** Claim 3’s flags are on the argv. They do not make the seat read-only on the reference OS. Grok’s own docs list sandbox enforcement as Landlock (Linux) / Seatbelt (macOS) only; unsupported platforms “log a warning and continue without enforcement.” Windows is not in that table. Live: `grok --sandbox not-a-real-profile -p x --max-turns 1` **ran and billed** (`sessionId` `01a02ba2-2ed5-7582-a47c-e945c52ad9c5`, summary `sandbox_profile=not-a-real-profile`). No `~/.grok/sandbox-events.jsonl`. This user’s config still has `permission_mode = "always-approve"`; the wrapper never passes `--permission-mode`.
   **Why it matters:** Round 1’s bug was “read-only is a comment.” On Windows it still is, plus config YOLO. `--disable-web-search` / `--no-subagents` do bind. FS/shell do not.
   **Fix:** On `always_approve is false`, pass `--permission-mode dontAsk` (and/or `--deny` write/shell). Do not advertise `--sandbox read-only` as the Windows control. Optionally refuse to start if `grok inspect` reports `sandbox_profile` off after a sandbox was requested.

2. **MAJOR** — `mcp-seats/wmw_gemini_mcp.py` `run_gemini()` brain line
   **What:** `brain = data.get("model") or data.get("model_name") or (model if model else "UNREPORTED")`. A caller-supplied `--model` is treated as the observed brain when JSON is silent.
   **Why it matters:** Overflow Valve is exactly “agy wearing a non-Gemini brain.” A conductor that pins `model: "Gemini …"` and gets no JSON confirmation will still print `brain: Gemini …` and can count a Claude/GPT vote as an independent Gemini vote. That is the hole claim 6 said it closed.
   **Fix:** Footer brain comes only from CLI JSON. Missing/unknown → `UNREPORTED`. Never copy the request argument.

3. **MAJOR** — both wrappers’ `always_approve` + `cwd`; user-scope `claude mcp add`
   **What:** `always_approve: true` is still an LLM-controlled boolean mapping to Grok `--always-approve` / Gemini `--dangerously-skip-permissions`. `cwd` is any existing directory (no home/profile/root allowlist). Registration is `--scope user`, so the tools exist in every later project.
   **Why it matters:** Flag-injection is dead (finding 0 below). The confused-deputy remains: a hostile public repo’s instructions only have to set the boolean. Default-false is not a sandbox on Windows (finding 1). Gemini’s false path still sends no hardening flags at all (relies on agy headless auto-deny).
   **Fix:** Require an allowlisted `cwd` when `always_approve` is true; refuse `$HOME`, profile, `C:\`, `.ssh`, `.aws`, `.grok`. Mark tools `destructiveHint`/`openWorldHint`. README: user-scope + YOLO is a loaded gun.

4. **MINOR** — `SETUP.md` §4 (~L92–94); `trm/CREW.md` and `team-rocket-takes-over/CREW.md` ~L138–140; `trm/SKILL.md` and `team-rocket-takes-over/SKILL.md` PERSISTENT SEATS block
   **What:** Claim 9 is not “everywhere.” SETUP still says a fresh call is “exactly what independent review requires.” CREW restates “Reviewers are ALWAYS fresh calls… that blindness is exactly what Butch and Cassidy require” with no necessary-not-sufficient qualifier. Both launcher SKILLs say “doctrine … live in CREW.md (the one owner)” — SPINE owns THE TRANSPORT LAW.
   **Why it matters:** A conductor loading SETUP or CREW in isolation re-learns the round-1 independence bug. Claim 8 (“cite, don’t restate”) is not met in CREW.
   **Fix:** Point at SPINE law #2; delete the sufficient wording. Launchers: owner is SPINE, CREW renders.

5. **MINOR** — `SKILL.md` L88; `mcp-seats/README.md` L76–77
   **What:** Deck SKILL still hardcodes `C:\Sync\Projects\andersons-dispatch-deck\mcp-seats\`. README still says a stalled permission prompt waits until the timeout **executes** it (Gemini header correctly says kills).
   **Why it matters:** Public-repo layout leak; “executes” can be read as auto-run-on-timeout.
   **Fix:** Relative `mcp-seats/`; “kills.”

6. **MINOR** — Grok default argv `--disable-web-search` bundled with “research/review omit always_approve”
   **What:** SKILL/README tell research tickets to take the read-only default. That default now disables web search. The `grok` tool description still sells web search. Getting search back means `always_approve: true` (finding 3).
   **Why it matters:** Research/council seats go blind, or they YOLO. `--no-memory` is only cross-session memory (CLI help); it does not break `--resume`. UUID shape matches on-disk Grok ids (`01a02b9e-…` etc.) and agy brain ids.
   **Fix:** Three modes, not a boolean: read-only+search / read-only+no-net / YOLO+cwd.

7. **NIT** — both wrapper module docs still open “v1.1” while `serverInfo.version` is `1.2.0`. `legacy/cursor-native/SPINE.md` in this public repo is still v1.2 (62147 bytes, different hash) — not one of the six, but strangers can open it.

**Flag-injection (round 1 CRITICAL) — dead, not a finding.** Attacked `_UUID_RE` + `_safe_argv` + `--resume=` / `--conversation=`. Rejected: `--always-approve`, leading dash, trailing space/newline, NULs, `;`/`{` wrappers, UUID glued to a flag. `\Z` does not match a trailing newline (Python `$` would). Live: `grok --resume=00000000-0000-0000-0000-000000000000 …` → `Error: Session does not exist` (value bound, not reparsed as flags). Equals form is the real kill; UUID is defense-in-depth. Grok session dirs are 8-4-4-4-12 hex (version nibble 7); regex accepts them. Gemini brain dirs are v4 UUIDs; same.

## Verification table

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1 | Large prompts: Grok `--prompt-file`; Gemini >25K clean error | **PASS** | Grok: `NamedTemporaryFile` + `--prompt-file` (CLI flag exists, “Single-turn prompt from a file”). Gemini: `MAX_ARGV_PROMPT = 25000` returns `isError` before `subprocess.run`. |
| 2 | UUID ids + no-leading-dash argv + `--resume=` | **PASS** | `_safe_id` / `_safe_argv`; `--resume={session_id}` / `--conversation={conversation_id}`; attack table + live equals-form parse above. |
| 3 | Read-only default is real argv | **FAIL** | Argv is present (`--sandbox read-only --disable-web-search --no-subagents --no-memory`). On Windows it does not enforce FS (finding 1). Config `permission_mode=always-approve` never overridden. |
| 4 | Known install path first; stdin DEVNULL | **PASS** | `find_grok`/`find_agy` known path then `shutil.which`; `stdin=subprocess.DEVNULL`. Residual: PATH fallback still exists if the known binary is missing (Unix agy has no known path). |
| 5 | Errors → isError; UTF-8; request boundary; `raw_decode` | **PASS** | Nonzero / `type==error` / missing sid (Grok); nonzero / `status!=SUCCESS` / missing cid (Gemini); `_utf8_stdio`; `except Exception` in `main`; `_extract_json` uses `JSONDecoder.raw_decode`. |
| 6 | Gemini footer brain / UNREPORTED | **FAIL** | `UNREPORTED` exists, but requested `model` is used as a stand-in (finding 2). |
| 7 | SPINE v2.0 byte-identical in six locations + NOTATION v4.0 + TRANSPORT LAW | **PASS** | SHA256 `6D749ADA…` / 65310 bytes on: ADD, `team-rocket-method-public`, `team-rocket-takes-over`, `~/.claude/skills/{dispatch,team-rocket-takes-over,trm}`. Version `spine v2.0 (2026-08-22)`; laws at L731 and L764. (Out of the six: `legacy/cursor-native` and SecondBrain copies still diverge.) |
| 8 | SPINE owns transport; tiers cite, don’t restate | **FAIL** | Deck SKILL cites SPINE. CREW v1.2 still restates the two laws (and drops the qualifier). Launcher SKILLs name CREW as “the one owner.” |
| 9 | Fresh call necessary-not-sufficient everywhere | **FAIL** | Present in SPINE L741, Deck SKILL, mcp-seats README. Absent/contradicted in SETUP.md and CREW (finding 4). |
| 10 | Opt-in, offer-never-install, one-command remove, Python 3.10+, one-request-at-a-time | **PASS** | README Install/Opt-in/Known limitation; SPINE transport law #1; wrapper docstrings. SETUP remove line omits `--scope user` (nit). |

## Verdict

**SHIP-WITH-FIXES** — sessionId flag-injection is actually dead (UUID + equals-form verified live); do not ship the Windows “read-only” story or the Gemini brain fallback until `--permission-mode dontAsk` is on the default path and `UNREPORTED` cannot be replaced by the request’s `model`. — Grok 4.6