# COUNCIL REVIEW — ROUND 2 (Verification Pass)

**Lens:** Gemini — The Outsider Installer + Docs Truth  
**Target Repository:** `C:\Sync\Projects\andersons-dispatch-deck`  

---

## Numbered Findings

### 1. MAJOR — `SETUP.md` (L83, L85, L109, L111), `mcp-seats/README.md` (L653, L660), `mcp-seats/wmw_gemini_mcp.py` (L382–388) — Cross-platform failure on macOS/Linux stranger installs and reachability probes
- **What:** 
  1. The registration examples in `mcp-seats/README.md` and `SETUP.md` use Windows backslashes and invoke `python` directly: `claude mcp add --scope user grok -- python <path-to-this-folder>\wmw_grok_mcp.py`. On macOS and Linux, `python` is frequently absent (systems ship `python3` only) and backslashes `\` cause shell path resolution errors in bash/zsh.
  2. The reachability probe script in `SETUP.md` explicitly invokes `"$HOME/.grok/bin/grok.exe"` and `"$LOCALAPPDATA/agy/bin/agy.exe"`. On macOS/Linux, `$LOCALAPPDATA` is empty, and neither binary carries the `.exe` extension. The probe will report both Grok and Gemini as `missing` on non-Windows systems even when installed and functional.
  3. In `wmw_gemini_mcp.py`, `find_agy()` only checks `cand = os.path.join(local, "agy", "bin", "agy.exe")` where `local` defaults to `~\AppData\Local`. On macOS/Linux, `agy` installs to `~/.antigravity/bin/agy` or `~/.local/bin/agy`. Because non-Windows install paths are missing from candidate lookups, `find_agy()` bypasses the preferred absolute-path check on Unix and falls back directly to `shutil.which("agy")`, violating the substitute-binary defense on macOS/Linux.
- **Why it matters:** A stranger attempting to install or run reachability probes on macOS or Linux will encounter immediate script failures, and `wmw_gemini_mcp.py` loses its primary binary substitution defense on Unix.
- **Concrete Fix:** 
  1. Update `mcp-seats/README.md` and `SETUP.md` registration commands to use forward slashes `/` (which work on Windows PowerShell, cmd, bash, and zsh) and note `python3` for Unix environments.
  2. Update `find_agy()` in `wmw_gemini_mcp.py` to include Unix install candidates (`os.path.expanduser("~/.antigravity/bin/agy")`, `os.path.expanduser("~/.local/bin/agy")`).
  3. Update `SETUP.md`'s reachability script to inspect non-`.exe` binary names on POSIX platforms.

### 2. MINOR — `SETUP.md` (L92–93) — Legacy phrasing on "Fresh Call" independence
- **What:** `SETUP.md` states: *"reviewers are ALWAYS fresh calls (a fresh call is blind — exactly what independent review requires)"*. This omits the *"necessary, not sufficient"* qualifier established in claim 9 and present in `SPINE.md` (L742), `SKILL.md` (L939), and `mcp-seats/README.md` (L701).
- **Why it matters:** A reader consulting `SETUP.md` in isolation might conclude a fresh call to the *same* vendor is sufficient for an independent review, contradicting SPINE v2.0 doctrine.
- **Concrete Fix:** Update `SETUP.md` L92–93 to align with `SPINE.md`: *"reviewers are ALWAYS fresh calls (a fresh call is blind — necessary, but not sufficient: independent review also requires a different effective-model vendor or a boss-launched fresh seat)"*.

### 3. NIT — `mcp-seats/wmw_grok_mcp.py` (L96–97) — Raw backslashes in `os.path.expanduser`
- **What:** `os.path.expanduser(r"~\.grok\bin\grok.exe")` contains hardcoded backslashes inside `expanduser`. On macOS/Linux, `~` expands to the user's home directory, but backslashes are treated as literal path characters (`/home/user/\.grok\bin\grok.exe`), causing a redundant `os.path.isfile` failure before reaching line 98 `~/.grok/bin/grok`.
- **Why it matters:** Minor path-handling hygiene on Unix platforms.
- **Concrete Fix:** Use `os.path.join(os.path.expanduser("~"), ".grok", "bin", "grok.exe")` or `os.path.normpath`.

---

## Verification Table

| # | Claimed Fix | Verification Status | Evidence / Notes |
|---|---|---|---|
| 1 | Large prompts crash command line (32K limit) | **PASS** | `wmw_grok_mcp.py` writes prompt to temporary `.md` file and passes `--prompt-file <path>`. `wmw_gemini_mcp.py` checks `len(prompt) > 25000` (`MAX_ARGV_PROMPT = 25000`) and returns a clean `isError = True` diagnostic message. |
| 2 | Session ID flag smuggling via `--resume` | **PASS** | `_UUID_RE` enforces strict UUID format on `session_id` / `conversation_id`. `_safe_argv` rejects leading `-` on optional string arguments (`cwd`, `model`). Subprocess invocations use equals form (`--resume=<id>` and `--conversation=<id>`). |
| 3 | Read-only default enforced in argv | **PASS** | `wmw_grok_mcp.py` (L153–155) explicitly appends `["--sandbox", "read-only", "--disable-web-search", "--no-subagents", "--no-memory"]` when `always_approve` is `False`. Verified all 4 options against `grok --help`. |
| 4 | Known install path preferred over PATH | **PASS** *(with Unix caveat)* | `find_grok()` and `find_agy()` check known absolute executable paths with `os.path.isfile` before calling `shutil.which`. Subprocess calls pass `stdin=subprocess.DEVNULL`. *(Note: `find_agy()` needs Unix candidate paths added; see Finding 1).* |
| 5 | Honest error detection & exception boundary | **PASS** | Nonzero exit codes, unparseable output, missing session IDs, or error JSON return `isError = True`. `_utf8_stdio()` enforces UTF-8 stdio, `json.JSONDecoder().raw_decode` handles noisy stdout, and `main()` wraps `handle(msg)` in a per-request `try/except` boundary. |
| 6 | Gemini footer reports effective brain | **PASS** | `wmw_gemini_mcp.py` (L463–465) reports `brain: <model>` or `UNREPORTED` when unknown. Verified against live `agy` CLI JSON output (which omits model key by default without explicit flags), ensuring preflights fail closed. |
| 7 | SPINE healed to single canon v2.0 byte-identical in 6 locations | **PASS** | Calculated SHA256 hashes of all 6 active canonical locations (`andersons-dispatch-deck/SPINE.md`, `team-rocket-method-public/SPINE.md`, `team-rocket-takes-over/SPINE.md`, `~/.claude/skills/dispatch/SPINE.md`, `~/.claude/skills/team-rocket-takes-over/SPINE.md`, `~/.claude/skills/trm/SPINE.md`). All 6 files are 65,310 bytes with SHA256 `6D749ADAF62080C70699E077F0F4629A867D01A3A7835E296FAF850537061230`. Version line is `spine v2.0 (2026-08-22)`, carrying THE NOTATION v4.0 and THE TRANSPORT LAW. |
| 8 | Transport laws owned in SPINE and cited elsewhere | **PASS** | `SPINE.md` L731–755 defines `THE TRANSPORT LAW — persistent seats (owner: SPINE; added v2.0, 2026-08-22)`. `SKILL.md` (L938) and `mcp-seats/README.md` (L699) cite SPINE as owner and render without restating. |
| 9 | "Fresh call = blind seat" stated as necessary-but-not-sufficient | **PASS** *(with minor doc note)* | `SPINE.md` (L742), `SKILL.md` (L939), and `mcp-seats/README.md` (L701) explicitly state "necessary, not sufficient". *(Note: `SETUP.md` L92 retains legacy phrasing; see Finding 2).* |
| 10 | Install opt-in, removal, Python prereq & single-request cap documented | **PASS** | Consent-first flow, `claude mcp remove --scope user <name>` removal command, Python 3.10+ requirement, and single-threaded limitation documented in `mcp-seats/README.md` and `SETUP.md`. |

---

## Verdict

SHIP-WITH-FIXES: The wrapper security hardening, prompt caps, error boundaries, and SPINE v2.0 byte-identical re-sync pass verification cleanly, but cross-platform install instructions, Unix reachability probes, and Unix binary lookup paths require minor fixes for macOS/Linux strangers. — Gemini 3.6 Flash (High)
