I'll read the handoff prompt and the required skills first, then follow those instructions exactly.Using the review skills for a defect-first pass on `wmw_gemini_mcp.py`. Next I’ll load the head-to-head task spec and the file under review.The head-to-head task is a defect-first review of `wmw_gemini_mcp.py`. I’ll read the file, related wrappers, and verify the `agy` CLI rather than assuming how it behaves.I’ll verify `agy` itself—help, config, and docs—and compare this wrapper to the Cursor/Grok seats rather than trusting comments.Web search was blocked, so I’ll probe the live `agy` CLI, its config, and the sibling wrappers next.I found Antigravity’s on-disk CLI under `~/.gemini/antigravity-cli`. Next I’ll read its logs, settings, and JSON shape instead of guessing flags.Review of `mcp-seats/wmw_gemini_mcp.py` (v1.3). Findings are from the current file plus this machine’s Antigravity CLI config, logs, and captured `--output-format json` objects. `agy --help` and the live docs URLs were blocked in this session, so CLI behaviour is taken from on-disk sources, not from a fresh `--help` dump.

---

### 1. **HIGH** · `run_gemini()` (L103–105) · the default path is not a tool jail

**What is wrong.** When `always_approve` is false the wrapper adds **no** hardening flags. It only omits `--dangerously-skip-permissions`. Restraint then comes entirely from Antigravity’s own print-mode policy plus this box’s CLI settings.

Verified on this machine:

- `~\.gemini\antigravity-cli\settings.json` auto-allows `read_file(*)` and a list of shell readers (`command(cat*)`, `command(type*)`, `command(Get-Content*)`, `command(rg*)`, `git log/show/diff/status`, …). Deny is empty.
- Live logs load that allow-list on every print-mode start (`cli_setting_manager.go:92`). A run **without** skip-permissions still logs `Propagating selected model override` and proceeds; `read_file(*)` is live. `list_directory` / `glob` / `search_file_content` grants are ignored as unknown actions, so those three names are noise.
- Print mode **does** auto-deny writes and non-allowlisted commands: `permission check failed for write_file … user denied permission` (`cli-20260819_232650.log`) and the same for `echo`, `dotnet build`, `git ls-files`, `powershell -Command …`. With `--dangerously-skip-permissions`, logs say `auto-approving all tool permissions` and then `Always-proceed: auto-approving … WriteToFile`.
- SPINE’s field note that headless “auto-denies `read_file` etc.” is stale against current settings. The sibling Grok wrapper at least puts `--deny` / `--no-subagents` on argv; this one does not.
- MCP / subagents are empty **today** (`empty component: prompt section "mcp_servers"` / `"subagent_reminder"`; no `~\.gemini\config\mcp_config.json`). The wrapper still never disables them. Antigravity’s own docs say a global `mcp_config.json` is injected into every conversation. `~\.gemini\config\config.json` also grants `command(agy)`.
- Default runs still try to install Playwright and write `webm_encoder.exe` under `~\.gemini\antigravity-cli\bin\` (`cli-20260822_180002.log`). That is a side effect of a “review” call, outside `cwd`.

**Why it matters.** A caller that omits `always_approve` is told this is the research/review seat. On this box that seat can still `read_file(*)` / `Get-Content` any path the process can read (including credential dirs). Writes are blocked unless someone later sets `always_approve` or adds MCP/nested `agy`. “Read-only” is write-blocked, not sandboxed.

**Fix.** Do not advertise the default as read-only. On `always_approve is false`, pass whatever the CLI actually uses to pin a read-only toolset (and override `settings.json`, not inherit it). Refuse to start if user grants include `command(agy)` or a non-empty `mcp_config.json` unless those are explicitly denied. Copy the Cursor/Grok pattern: an allowlist, not “hope headless denies everything.”

---

### 2. **HIGH** · `_safe_cwd()` (L143–160) and `gemini-reply` (L240–245) · the write-cwd guard does not do what it claims

**What is wrong.**

- Guard is skipped when `always_approve` is false **or** `cwd is None` (`L145–146`). Schema `required` is still only `["prompt"]`. `always_approve: true` with no cwd is legal; `subprocess.run(..., cwd=None)` inherits the MCP server’s process directory.
- `gemini-reply` accepts `always_approve`, never takes `cwd`, never calls `_safe_cwd`. Live CLI logs show `--conversation=` resumes the stored thread (`Print mode: resuming conversation 28321cbc-…`) while `workspaceDirs` comes from **process cwd**. A start in a sensitive tree, then `gemini-reply(always_approve=true)`, never re-checks the path.
- Banned set is an exact, case-sensitive `realpath` match on home / drive root / a few env dirs. Descendants are allowed: `C:\Users\<you>\Documents`, `C:\Windows\System32`, `C:\Program Files\…`. `os.path.abspath(os.sep)` is only the **current** drive’s root. `.SSH` vs `.ssh` bypasses the secret substring on Windows.
- After resolving, it **returns the original `cwd`**, not `real`. The Cursor sibling returns the canonical path and uses `_is_within`.
- `~\.gemini\antigravity-cli\settings.json` already lists `C:\\Users\\andre` under `trustedWorkspaces`. The wrapper never reads or overrides that file. `last_conversations.json` already has a conversation keyed at `C:\\Users\\andre`.

**Why it matters.** `--dangerously-skip-permissions` is the loaded gun (logs: auto-approve `WriteToFile`). The guard is supposed to keep that gun off home, system, and credential dirs. It does not, and reply can escalate a read-allowlisted thread to YOLO with no second check.

**Fix.** Match the Cursor wrapper: require an explicit cwd when `always_approve` is true; compare with `normcase` + “is within”, not equality; return `realpath`; run the same guard on `gemini-reply` (add `cwd` to that schema). Refuse if the resolved path is inside a `trustedWorkspaces` root that is home/profile.

---

### 3. **HIGH** · footer brain (L132–140) · independence reporting cannot see the real model

**What is wrong.** The footer reads `data.get("model") or data.get("model_name")`. Captured live JSON does not have those keys. A SUCCESS object is:

`conversation_id`, `status`, `response`, `duration_seconds`, `num_turns`, `usage`

An ERROR object is the same plus `error`. No `model` / `model_name`.

What the CLI actually uses is `~\.gemini\antigravity-cli\settings.json` → `"model": "Gemini 3.6 Flash (High)"`. Print-mode logs with `model=""` (no `--model` flag) still say `Propagating selected model override to backend: label="Gemini 3.6 Flash (High)"`. The wrapper never reads that file. Requested `--model` is only echoed as `UNREPORTED (requested: …)`, which is correctly not treated as observed — and also means a pinned Overflow-Valve Claude brain is indistinguishable from Gemini.

**Why it matters.** This shop decides review independence by vendor. A host that rents Claude/GPT must not count as a Gemini vote. The footer will almost always be `UNREPORTED`, so a conductor either always fails closed (the seat is unusable as a verified independent vote) or ignores the footer and assumes green = Gemini (the Overflow Valve hole). The field is not spoofable from argv, but it is also not observable from the JSON the wrapper parses.

**Fix.** Do not claim the footer reports the effective brain until the CLI JSON actually contains it. Options: a CLI flag that includes model in `--output-format json` (if one exists — not verified here); parse the log line `label="…"` as `brain: UNVERIFIED_LOG …` and still fail closed; or refuse the call unless `--model` was passed **and** the CLI echoes that same string in JSON. Never treat settings.json or the request argument as observed.

---

### 4. **MEDIUM** · `MAX_ARGV_PROMPT` / `-p` (L93–97, L105) · prompt still rides the Windows command line

**What is wrong.** Prompt is an argv value after `-p`. Cap is `len(prompt) > 25000` (Python code points). Windows `CreateProcessW` limits the **entire** command line to 32,767 UTF-16 code units, including quotes. `subprocess` on Windows uses `list2cmdline`: every `"` is escaped and the string is wrapped. A 25k prompt of quotes, or of supplementary-plane characters (2 UTF-16 units each), can still overflow. Newlines in the prompt become embedded in that command line.

There is no `--prompt-file` anywhere under `~\.gemini\antigravity-cli\builtin` (searched). The Grok seat already avoided this with a temp file. The error text tells the caller to put long material in a file and read it **only** `with always_approve: true` — but `read_file(*)` is already on the default allow-list, so that restriction is wrong.

**Why it matters.** Oversized or oddly encoded prompts can still crash or truncate at the OS, not at the clean `isError` path. Unusual characters are the gap the 25k check does not cover.

**Fix.** If the CLI has a file/stdin prompt flag, use it. If not, write the prompt to a temp file under a safe dir and pass a short `-p` that only names that file (works on the default allow-list). Count UTF-16 units of the **serialized** command line, not `len(prompt)`. Stop telling callers they need `always_approve` just to read a file.

---

### 5. **MEDIUM** · error / spend path (L119–127) · ERROR is honest, but spend is invisible and retries are easy

**What is wrong.** Nonzero exit, missing JSON, missing `conversation_id`, or `status != "SUCCESS"` all return `isError: true`. That part is sound.

A real captured object (`docs/council-2026-08-22-persistent-seats/SIGNED-R2-gemini.json`) is `status: "ERROR"` with a full review in `response`, `conversation_id` set, `error: "Find command timed out…"`, and `usage.total_tokens: 138854`. The wrapper will flag this as failure and keep only `text[:1000]`. The work was produced and billed; the orchestrator is told it failed and will likely retry.

There is no spend/audit log (the Cursor seat has `_log_spend`). `usage` is sitting in the JSON and is discarded. `subprocess.run(timeout=PROC_TIMEOUT_S)` uses `TerminateProcess` on the direct child only. Logs show agy spawning a separate language-server process (`Starting language server process with pid …`). On Windows that tree is not a Job Object; a timeout can leave a skip-permissions grandchild running after the MCP call has already returned an error.

**Why it matters.** A failed call does **not** look successful (good). It can still have spent a six-figure token count, dropped a usable answer, and — under `always_approve` — left writes in flight. That is a false-failure with live cost and possible side effects, up to `PRINT_TIMEOUT` (60m) / `PROC_TIMEOUT_S` (3900s).

**Fix.** If `status == "ERROR"` but `response` and `usage` are present, return `isError: true` **and** the full text plus a spend line (`usage` tokens, `error` string, `conversationId`). Log every attempt. On Windows, run `agy` inside a Job Object (or `taskkill /T`) so timeout kills the language server too.

---

### 6. **LOW** · `TOOLS` `gemini-reply` (L210–225) and `find_agy()` (L45–57)

**What is wrong.** Reply is as dangerous as `gemini` when `always_approve` is true, but it has no `destructiveHint` / `openWorldHint` and never says YOLO is a loaded gun. `find_agy()` prefers `%LOCALAPPDATA%\agy\bin\agy.exe`; that directory is empty on this box (0 files). The known-path substitute-binary defence does not fire; resolution is `shutil.which("agy")`. The tree that actually holds CLI state is `~\.gemini\antigravity-cli\`, which is not in the candidate list.

**Fix.** Copy the `gemini` annotations and always_approve warning onto `gemini-reply`. Add the real install paths (`~\.gemini\antigravity-cli\…` if the exe lives there; PATH last).

---

## VERIFIED

- Read `mcp-seats/wmw_gemini_mcp.py` v1.3 in full; compared `_safe_cwd` / default argv / brain footer to `wmw_grok_mcp.py` and `wmw_cursor_mcp.py`.
- `~\.gemini\antigravity-cli\settings.json` — default model, allow-list, `trustedWorkspaces` includes home.
- `~\.gemini\config\config.json` — `command(agy)` grant.
- CLI logs under `~\.gemini\antigravity-cli\log\` — skip-permissions vs auto-deny `write_file`; workspaceDirs from process cwd; resume via `--conversation=`; model label from settings, not JSON; empty `mcp_servers` / `terminal_sandbox` prompt sections; Playwright/webm_encoder side effects.
- `~\.gemini\antigravity-cli\cache\last_conversations.json` — conversations keyed by cwd, including `C:\Users\<you>`.
- Captured JSON: `docs/council-2026-08-23-cursor-bench/SIGNED-gemini.json` (SUCCESS, no model key, has `usage`) and `docs/council-2026-08-22-persistent-seats/SIGNED-R2-gemini.json` (ERROR + full response + 138k tokens).
- On-disk CLI docs: `~\.gemini\antigravity-cli\builtin\skills\antigravity_guide\references\cli.md`, `agy-customizations/docs/mcp_servers.md`. No `--prompt-file` in that tree.
- `%LOCALAPPDATA%\agy` empty. UUID / `--conversation=` equals-form / stdin `DEVNULL` / `status != SUCCESS` → `isError` still match the 2026-08-22 hardening.

## Could not verify

- Live `agy --help` / `agy --version` (shell blocked in this Ask session).
- Official pages `https://antigravity.google/docs/cli/reference` and Context7 (fetch rejected).
- Whether a JSON flag exists that would emit `model`.
- Empirically exploding `list2cmdline` at 25k; reasoned from the documented 32,767 WCHAR `CreateProcess` cap.
- What `trustedWorkspaces` changes at runtime (present in settings; no matching log line).
- Whether `command(agy)` from `config.json` is merged into the printed Allow list (applyUserSe<you><you>ttings logs `allow=1`, then a different Allow snapshot).

**None found:** flag-smuggling on `conversationId` (UUID + `--conversation=` still binds); a SUCCESS footer on `status: "ERROR"`; fresh `-p` calls silently resuming a prior thread when `conversationID=""`.

---

**SHIP-WITH-FIXES** — UUID / equals-form / `isError` on non-SUCCESS are sound; do not trust the read-only claim, the cwd guard, or the `brain:` footer until they match this CLI’s real settings, JSON, and process-cwd resume behaviour. — Cursor Grok 4.6

---
🟣➤⚫ [wmw-cursor] ♾️ xAI · cursor-grok-4.6-high
   sessionId: ad7ffe71-ec17-4467-8f60-fdd4c6b28742 · meter: INCLUDED · 167839 in / 22820 out