I'll read the handoff prompt and the required skills first, then follow those instructions exactly.Using the review-agent skill for a defect-first review. Next I’ll load the head-to-head task and the Gemini MCP seat file.The task needs live CLI proof, not just a code read. I’ll check `agy` help, sibling seats, and `_safe_cwd` before running canary probes.Grok’s wrapper denies write/edit/shell on the default path; Gemini’s does not. I’ll pull the rest of `agy` help and run live canaries to see what that actually allows.Prior H2H notes disagree on whether print-mode writes are denied. I’ll read this box’s Antigravity settings and run live canaries in a scratch directory.Official docs say workspace file writes are auto-allowed in headless mode. I’ll prove that with live canaries and test `_safe_cwd` in Python.Scratch dirs and junctions are in place. Next I’ll fire live `agy` write and shell canaries, including one through the wrapper’s default argv.The agent wrote into Antigravity’s own scratch tree, not process cwd. I’ll confirm those files, then retry with absolute paths so the permission check is unambiguous.Trusted-home writes went through on the default path; the untrusted playpen write was denied. I’ll pin the remaining gaps: git-root auto-allow, shell without YOLO, `--mode plan`, and model reporting.`--mode plan` still wrote under `.gemini`, so it is not a read-only fix. Cleaning up canaries next, then I’ll write the review.Review of `mcp-seats/wmw_gemini_mcp.py` (v1.3) against live `agy` 1.1.19 on this box.

---

### 1. **CRITICAL** · `run_gemini()` L103–105; tool schema L189–205 · default path is not read-only

**What is wrong.** `always_approve: false` only *omits* `--dangerously-skip-permissions`. The wrapper adds no `--mode`, no `--sandbox`, no deny list (agy has none), and no `--disable-slash-commands`. Headless still loads a 57-tool agent, including `write_to_file`, `replace_file_content`, `run_command`, `invoke_subagent`, `call_mcp_tool`, `search_web`, and the browser stack (`stream-json` `init.tools`). `permission_mode` is `request-review`.

Official headless docs: *“Reading and writing files inside your active workspace is auto-allowed.”* On this box the agent’s real workspace is not the wrapper `cwd`. With process cwd at the untrusted playpen, `write_to_file` to `C:\Users\<you>\.gemini\antigravity-cli\scratch\` **succeeded** without YOLO:

| Probe (no `--dangerously-skip-permissions`) | Result |
|---|---|
| Write `CANARY_NOSKIP_HOME.txt` / `CANARY_NOSKIP_PLAYPEN.txt` into CLI scratch | **Wrote.** Tokens `H2H-XVAQEF5Q-NOSKIP-HOME` / `…-PLAYPEN` on disk. One run even returned `status: SUCCESS`. |
| Abs write to untrusted playpen `C:\Sync\_playpen\…\CANARY_ABS_NOSKIP.txt` | **Denied** (`user denied permission for write_file`). `status: ERROR`, exit 1. |
| Abs write to `C:\Users\<you>\_h2h_xvaqef5q\CANARY_ABS_HOME2.txt` (under `trustedWorkspaces` home) | **Denied** (same user-denied). Home-as-trusted-root ≠ every child is writable. |
| `echo H2H-XVAQEF5Q-SHELL-NOSKIP` | **Denied** (`user denied permission to run command`). |
| `--mode plan` “create CANARY_PLAN.txt” | Did **not** create the canary, but **did** write `implementation_plan.md` under `~\.gemini\antigravity-cli\brain\<cid>\` and returned `status: SUCCESS`. Plan is not read-only. |

`--dangerously-skip-permissions` (the wrapper’s `always_approve: true`) then wrote the playpen file and ran shell (`pwsh Get-Location` → CLI scratch; `bash -c echo …>` wrote `CANARY_SHELL_SKIP.txt`).

The tool text (“set `always_approve` when Gemini must edit files”), SKILL/README “omit = read-only / deny rules” copy, and the Grok sibling’s real `--deny` argv are therefore false for this seat. A “review” call can persist files in `~\.gemini\antigravity-cli\scratch\` (and under `--mode plan`, in `brain\`).

**Fix.** Stop claiming read-only. On `always_approve is false`, pin an untrusted playpen the CLI will not auto-write (on this box, `C:\Sync\_playpen\…` *outside* the CLI scratch was denied), and fail the call if `write_to_file` / `run_command` actually ran (parse `stream-json` tool steps, or mtime the playpen). `--mode plan` is not the fix. Keep YOLO behind `always_approve` with finding 2’s cwd/project guard.

---

### 2. **HIGH** · `_safe_cwd()` L143–160; `gemini-reply` L240–245 · the cwd guard watches the wrong tree, and YOLO can skip it

**What is wrong.** `_safe_cwd` only runs when `always_approve` **and** `cwd` is set. It refuses the exact home/system roots and basename/path fragments `.ssh` / `.aws` / `.grok` / `.gemini` / `.claude` / `.config`. Live Python probes:

- `always_approve=True, cwd=None` → **ALLOW** (guard skipped). `subprocess.run(..., cwd=None)` inherits the MCP server’s cwd.
- `Documents`, `AppData`, `.cursor`, `.antigravity`, `ProgramFiles(x86)` → **ALLOW**.
- Exact home, `SystemRoot`, `ProgramFiles`, drive root, `.ssh`, `.gemini` → **REFUSE**.
- Junction `…\junc-home` → home: **REFUSE** (`realpath` works). Junction `…\junc-docs` → Documents: **ALLOW**.
- Mixed-case `USERPROFILE`: `realpath` canonicalized; not a bypass on this NTFS.

`gemini-reply` never takes `cwd` and never calls `_safe_cwd`, so `always_approve: true` on a follow-up is YOLO with no path check.

Worse: the agent’s shell cwd is **not** the wrapper cwd. YOLO `Get-Location` returned `C:\Users\<you>\.gemini\antigravity-cli\scratch` while `init.cwd` was the playpen. Wrapper `cwd` is only `subprocess.run`’s process cwd. agy has `--project`, `--new-project`, `--add-dir`; the wrapper passes none. `--add-dir <playpen>` still denied a playpen write, so “pass cwd through” is not a one-flag fix — the seat is pinned to the CLI’s default project (scratch under `.gemini`, a directory `_safe_cwd` would refuse if it ever saw it).

**Why it matters.** The loaded gun (`--dangerously-skip-permissions`) is supposed to be aimed at a project directory. It is aimed at `~\.gemini\antigravity-cli\scratch`, and reply can flip a thread to YOLO with no second check. Descendants of an already-trusted `C:\Users\<you>` (`trustedWorkspaces` in `~\.gemini\antigravity-cli\settings.json`) are wide open for YOLO.

**Fix.** Require an explicit project for YOLO (`--new-project` / `--project` / documented workspace root), run `_safe_cwd` on the *resolved* workspace (CLI scratch counts as `.gemini` — refuse it), require `cwd` on `gemini-reply` when `always_approve` is true, and ban home descendants unless they are a named project outside the secret list. Include `ProgramFiles(x86)`.

---

### 3. **HIGH** · footer L136–140 · `brain:` cannot be observed on the JSON path the wrapper uses

**What is wrong.** Footer does `data.get("model") or data.get("model_name")`, else `UNREPORTED` / `UNREPORTED (requested: …)`. Official JSON envelope fields are `conversation_id`, `status`, `response`, `error`, `duration_seconds`, `num_turns`, `usage` — **no `model`**. Live `--output-format json` with `--model gemini-3.6-flash-low` still had those keys only. `stream-json` `init.model` appears **only when `--model` is passed**; the `result` event still has no model.

Default settings model is `"Gemini 3.6 Flash (High)"`. `agy models` also lists `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `gpt-oss-120b-medium` (Overflow Valve). The wrapper never reads `settings.json` and never switches to `stream-json`.

**Why it matters.** This shop counts independent review by **vendor of the effective model**. A silent Claude/GPT default on the Gemini host is a Claude vote wearing a green badge if the conductor treats the seat name as lineage, and a hard fail-closed if they treat `UNREPORTED` as unknown. Either way the footer cannot settle it.

**Fix.** Always pass explicit `--model`. Switch to `--output-format stream-json` and take `init.model`. If `init.model` is missing, keep `UNREPORTED` and do not copy the request argument into a confirmed slot. Do not invent Gemini from the server name.

---

### 4. **MEDIUM** · L98–105; missing `--disable-slash-commands` · escalation tools stay loaded; YOLO is the shell/MCP unlock

**What is wrong.** Default `init` advertises `invoke_subagent`, `define_subagent`, `call_mcp_tool`, `search_web`, `read_url_content`, full `browser_*`, `generate_image`. Docs: subagents may get write/MCP/shell. Wrapper cannot pass `--no-subagents` (flag does not exist). `--disable-slash-commands` exists (“Disable slash command and skill expansion in print mode”) and is **not** passed; docs say `agy -p /model` persists the default model.

Shell/MCP/web on the default path **are** mostly gated: `echo` came back `user denied permission` in 2s; wrapper treats non-`SUCCESS` as `isError`. `git status --short` (on this box’s `permissions.allow`) was *invoked* and marked DONE with no captured output, then the run `CANCELED` — I could not prove the command’s stdout. `~\.gemini\config\mcp_config.json` exists but is empty; `agy mcp list` = none.

Escalation that **does** bite today: trusted/default-workspace **file** tools (finding 1) and YOLO `run_command` (finding 1). This box also allow-lists `read_file(*)` and `Get-Content*` in settings — the wrapper does not override that.

**Fix.** Pass `--disable-slash-commands` on every print invocation. Document that agy has no `--no-subagents` / `--deny`. Refuse to start (or YOLO) if `mcp_config.json` is non-empty unless the caller opts in. Do not inherit global `permissions.allow` for a review seat — pin a deny/ask policy or an untrusted playpen.

---

### 5. **MEDIUM** · `MAX_ARGV_PROMPT` L35, L93–97 · 25k Python chars is the wrong unit; no prompt-file path

**What is wrong.** Prompt is `cmd += ["-p", prompt]`. `agy --help` has **no** `--prompt-file`. `--input-format stream-json` reads prompts from stdin (wrapper sets `stdin=DEVNULL`). A 25 000-char prompt produces `list2cmdline` length **25089** (CreateProcessW cap 32767; headroom 7678) — the 25k cap is conservative in *this* flag set, but it is a character count of the prompt, not of the full UTF-16 command line (model id + conversation equals-form + flags eat the remainder). `agy.exe` is a real PE (`MZ`), not a `.cmd` shim. A prompt `hello" & echo H2H-ARGV-INJECT>…` did **not** create a file (killed after 2s; inject target absent). Embedded NUL raises `ValueError` inside `run_gemini`; `_tool_call` maps that to `invalid arguments` — clean `isError`, not a crash.

**Why it matters.** Oversized / odd prompts fail closed. The remaining issue is capability: long review briefs cannot be passed except by asking Gemini to read a file, which the error text says requires `always_approve: true`, while `view_file` of CLI-scratch files already worked on the default path.

**Fix.** Keep the cap (maybe budget against `list2cmdline` of the *full* argv). For long material, use `--input-format stream-json` with a wrapper-owned stdin (today stdin is `DEVNULL`) or a file the default path can already read. Do not tell callers they need YOLO just to read a prompt file.

---

### 6. **LOW** · L119–127 · a failed tool can still leave a successful-looking mutation, and a successful mutation can look like a failure

**What is wrong.** Non-`SUCCESS` / missing `conversation_id` / no JSON → `isError: true`. That part is honest. Live:

- Scratch write + later denied write to `~\.gemini\antigravity-cli\` (hardcoded protection boundary) → **file stayed**, envelope `status: ERROR`. Orchestrator sees failure; disk changed.
- YOLO write + shell succeeded, then a later `view_file` error → files on disk, envelope `ERROR`.
- Soft-deny of playpen/`echo` → `ERROR` + nonzero exit (stricter than the docs’ “soft-deny, exit 0, SUCCESS”). Good for the audit path.
- No spend/audit ledger (unlike `wmw_cursor_mcp.py`). `usage` is in the JSON and is dropped.

**Fix.** If any `write_to_file` / `run_command` step is `DONE`, treat the call as write-capable even when terminal `status` is `ERROR`. Optionally log `usage` like the Cursor seat.

---

## VERIFIED

| What | How |
|---|---|
| agy 1.1.19 flags | `agy.exe --help` — no `--cwd`, `--deny`, `--prompt-file`, `--no-subagents`; has `--dangerously-skip-permissions`, `--mode accept-edits\|plan`, `--sandbox`, `--disable-slash-commands`, `--conversation`, `--output-format json\|stream-json`, `--add-dir`, `--project` |
| Models / Overflow Valve | `agy models` — Gemini 3.7/3.6/3.5/3.1 plus `claude-sonnet-4-6`, `claude-opus-4-6-thinking`, `gpt-oss-120b-medium` |
| MCP | `agy mcp list` → none; `~\.gemini\config\mcp_config.json` exists and is empty |
| Docs | https://antigravity.google/docs/cli/{headless,permissions,sandbox,features,reference}; on-disk `~\.gemini\antigravity-cli\builtin\skills\…` |
| This box’s policy | `~\.gemini\antigravity-cli\settings.json` — model `Gemini 3.6 Flash (High)`; `read_file(*)`, `Get-Content*`, `git status*`, …; `trustedWorkspaces`: `C:\Users\<you>`, `C:\Sync\Projects\madman-kontroller`; no `enableTerminalSandbox` |
| Default-path scratch writes | `agy -p … --output-format stream-json --print-timeout 2m` (no skip). Files appeared in `~\.gemini\antigravity-cli\scratch\` |
| Untrusted playpen write | Abs path `C:\Sync\_playpen\gemini-h2h-xvaqef5q\playpen\CANARY_ABS_NOSKIP.txt` → `user denied permission` |
| YOLO write + shell | `--dangerously-skip-permissions` wrote `CANARY_ABS_SKIP.txt` and `CANARY_SHELL_SKIP.txt` in the playpen; `pwsh Get-Location` → CLI scratch |
| `--mode plan` | Wrote `implementation_plan.md` under `brain\<cid>\`; `status: SUCCESS` |
| `--add-dir` playpen | Still denied playpen `write_to_file` |
| JSON brain | `agy -p PING --output-format json --model gemini-3.6-flash-low` → no `model` key. Same prompt `stream-json` → `init.model = gemini-3.6-flash-low`, `result` still has no model |
| `_safe_cwd` | Imported `wmw_gemini_mcp._safe_cwd`; junctions via `mklink /J` |
| Argv cap / PE / injection | `find_agy()` → `…\agy.exe`; magic `MZ`; `list2cmdline` 25089 for 25k prompt; cmd-metachar prompt did not create a file; `run_gemini("x"*25001)` → `isError` |
| Cleanup | Junctions `rmdir`’d first (not `rm -rf` through them). Removed playpen tree, `~\ _h2h_xvaqef5q`, my `CANARY_*XVAQEF5Q*` scratch files, and the plan artifact. Left pre-existing `CANARY_READONLY.txt`. Home/Documents intact. |

**Could not verify:** whether a *populated* `mcp_config.json` would execute `call_mcp_tool` without YOLO; whether `invoke_subagent` can write/shell in headless; web/browser on the default path; whether `--sandbox` AppContainer contains `run_command` on Windows (wrapper never passes it; `enableTerminalSandbox` is unset); whether allow-listed `git status --short` actually produced output (DONE, no `output`, then `CANCELED`); hitting WinError 206 at the 32767 wchar ceiling.

---

**REWORK** — UUID / equals-form / `isError` on non-SUCCESS / 25k cap are sound; do not ship this as a read-only Gemini review seat until the default path cannot write CLI scratch, YOLO is pinned to a real project (not `~\.gemini\…\scratch`), and `brain:` is taken from `stream-json` `init.model`. — Cursor Grok 4.6

---
🟣➤⚫ [wmw-cursor] ♾️ xAI · cursor-grok-4.6-high
   sessionId: 82a6849c-897d-497d-a815-9416a68a47dd · meter: INCLUDED · 474572 in / 36550 out