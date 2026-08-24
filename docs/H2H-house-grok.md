I'll start from the source and the real `agy` CLI, not from assumptions — locating the seat file, its helpers, and how the CLI actually behaves.The previous council is context, not evidence. Next I’ll read the current wrapper and check `agy` itself.The wrapper is in hand. Next I’ll pull `agy` help, its config, and the sibling Grok seat so the read-only and reporting claims can be checked against real behavior.`agy` help is only a start. I’ll pull the rest of the flags, this box’s config, and whether `-p` actually denies tools.The CLI ships its own docs on this box. I’ll read those and then run live probes so the read-only, JSON, and cwd claims are evidence, not guesses.Official docs say workspace writes are auto-allowed. I’ll prove that on this box, and check JSON, `_safe_cwd`, and the argv cap with live probes.I have the JSON schema from a prior live run (no `model` key). Next I’ll empirically test writes, `_safe_cwd`, slash-commands, and the argv cap.Cleanup is done. The live canaries are enough: trusted-workspace writes go through on the default path; `--mode plan` does not stop them.

# Review of `mcp-seats/wmw_gemini_mcp.py` (v1.3, agy 1.1.19)

## Findings

### 1. **CRITICAL** · `run_gemini()` L103–105; tool schema L194–205 · default path is not read-only

**What is wrong.** `always_approve: false` only *omits* `--dangerously-skip-permissions`. No `--mode`, no deny list (agy has none), no `--sandbox`. The 57-tool agent still loads, including `write_to_file`, `replace_file_content`, `run_command`, `invoke_subagent`, `call_mcp_tool`, `search_web`, and the browser stack (live `stream-json` `init.tools`).

What actually restrains a default call is Antigravity’s workspace-trust policy, not this wrapper:

| Probe (no `--dangerously-skip-permissions`) | Result |
|---|---|
| `write_to_file` under this repo (`C:\Sync\Projects\andersons-dispatch-deck\…`) | `status: ERROR`, “user denied permission”, file absent |
| `write_to_file` under `C:\Users\andre\AppData\Local\Temp` | **`status: SUCCESS`, file written with the exact token**, then deleted |
| Same trusted write with `--mode plan` | **still SUCCESS, file written** |
| `run_command echo …` | `status: CANCELED`, stderr: tool auto-denied |
| `git status --short` | `status: ERROR`, “user denied permission” |

This box’s `~\.gemini\antigravity-cli\settings.json` lists `trustedWorkspaces`: `C:\Users\andre` (the whole profile) and `C:\Sync\Projects\madman-kontroller`. Official headless docs say workspace file writes are auto-allowed; shell/MCP/web default to Ask. `--mode plan` only prepends a `/plan` instruction; it does not structurally block writes (live proof). GitHub issue #548’s “`--mode plan` blocks mutation” workaround is **false on 1.1.19**.

SKILL.md (“omit always_approve = read-only”), mcp-seats README (“default call passes deny rules”), and the tool text (“set always_approve when Gemini must edit files”) are therefore wrong for any cwd inside a trusted workspace. A “review” pointed at home, Temp, Documents, or madman-kontroller **will write**.

**Why it matters.** Review tickets are dispatched on this path. The seat can mutate the tree it is supposed to be reading, and the call still returns `isError: false`.

**Fix.** Stop claiming read-only. On `always_approve is false`: never pass the target repo as cwd; pin an **untrusted** playpen (on this box `C:\Sync\Playpen\gemini` is outside the trust list — our untrusted write was denied). Parse `settings.json` `trustedWorkspaces` and refuse a default-path cwd that sits inside one. `--mode plan` is **not** the fix. For build tickets keep `--dangerously-skip-permissions` behind `always_approve`, with finding 2’s cwd guard. Optional: mtime/canary the playpen and fail if it changed.

---

### 2. **HIGH** · `_safe_cwd()` L143–160; `_tool_call` L232–245 · write-capable cwd guard does not do what it says

**What is wrong.** Guard runs only when `always_approve` **and** `cwd is not None`. It exact-matches `realpath` against home / drive root / `SystemRoot` / `ProgramFiles` / `USERPROFILE`, plus a basename substring for six secret dirnames. Empirically, with `always_approve=true`, **ALLOWED**:

- `C:\Users\andre\Documents`, `C:\Users\andre\AppData\Roaming`, `C:\Users\andre\AppData\Local\Temp` (we wrote a canary there)
- `C:\Windows\System32`
- `C:\Program Files\Git`
- `cwd=None` (inherits the MCP process cwd)
- drive-relative `C:System32` when the process’s C: directory is `\Windows` (returns the original string, not the canonical path)

**Held:** junction to home refused (realpath resolves); existing-path case folds via realpath; exact home / `C:\Windows` / `C:\` refused.

`gemini-reply` accepts `always_approve` and never calls `_safe_cwd`, never takes `cwd`. Schema does not require cwd when YOLO is on (Cursor’s wrapper does).

**Why it matters.** YOLO can be aimed at System32 or anywhere under the already-trusted user profile. Reply can flip a thread to `--dangerously-skip-permissions` with no cwd check. Finding 1 already writes in those trees *without* YOLO; this is the shell/MCP unlock on top.

**Fix.** `if always_approve and not cwd: raise`. Compare with `os.path.normcase` + `_is_within` (see `wmw_cursor_mcp.py`). Ban descendants of `SystemRoot` / `ProgramFiles` / `ProgramFiles(x86)` / `ProgramData` / home, not just the roots. Ban secret path parts case-insensitively. Return and pass the canonical path. Give `gemini-reply` a `cwd` field and run the same guard whenever `always_approve` is true.

---

### 3. **HIGH** · `run_gemini()` L132–140 · `brain:` cannot report the effective model from `--output-format json`

**What is wrong.** Footer does `data.get("model") or data.get("model_name")`, else `UNREPORTED` / `UNREPORTED (requested: …)`. Official JSON envelope fields are `conversation_id`, `status`, `response`, `error`, `duration_seconds`, `num_turns`, `usage` — **no `model`**. Live envelopes on 1.1.19 match that (PING and canary runs). `stream-json` `init.model` appears **only when `--model` is passed**; the `result` event still has no model.

So every default call (the Overflow Valve path: whatever `settings.json` `"model"` is, currently `Gemini 3.6 Flash (High)`, persistable via `/model`) footers `brain: UNREPORTED`. Passing Claude yields `UNREPORTED (requested: …)` at best, never a CLI-confirmed effective brain.

**Why it matters.** This shop counts independent review by **vendor of the effective model**. A silent Claude/GPT default on the Gemini host is a Claude vote wearing a green badge if the conductor treats the seat name as lineage, and a hard fail-closed if they treat `UNREPORTED` as unknown. Either way the footer cannot settle it.

**Fix.** Always pass an explicit `--model` (headless does not silently remap unknown slugs — it errors). Switch to `--output-format stream-json` and take `init.model`. If `init.model` is missing, keep `UNREPORTED` and do not copy the request argument into a confirmed slot. Do not invent Gemini from the server name.

---

### 4. **HIGH** · `run_gemini()` L99–100, L123–127 · missing `--conversation` id starts a **new** SUCCESS session

**What is wrong.** Live:

```
agy --conversation=00000000-0000-0000-0000-000000000000 -p "Reply with exactly PING" --output-format json
```

stderr: `warning: conversation "00000000-…" not found`  
stdout: `status: SUCCESS` with a **new** `conversation_id` (`3469bc7e-…`). Same for space form.

The wrapper never compares requested id to returned id. Success path ignores stderr. Footer reports the new id as if resume worked.

UUID / equals-form injection is dead (`_safe_id` + `--conversation=` live-bound the value). Persistence is not.

**Why it matters.** `gemini-reply` with a stale/typo’d UUID looks like a continued seat, bills a fresh turn, and drops the thread. The codeword acceptance test can “fail” as amnesia while `isError` is false.

**Fix.** If `conversation_id` was sent and `cid != conversation_id`, return `isError`. Surface the stderr warning. Do not treat “not found → new chat” as resume.

---

### 5. **MEDIUM** · `MAX_ARGV_PROMPT` L35, L93–97 · 25k Python chars is the wrong unit; no prompt-file path

**What is wrong.** Prompt is `-p` argv. Windows `CreateProcessW` cap is 32,767 **UTF-16 code units for the whole line**. Measured with `subprocess.list2cmdline`:

- 25,000 ASCII → 25,089 units (under)
- 25,000 `"` → **50,089 units** (over)
- 20,000 💩 → **40,089 units** (over)

`agy --help` has **no** `--prompt-file`. `--input-format stream-json` reads prompts from stdin (wrapper sets `stdin=DEVNULL`). Oversized lines become `OSError` (WinError 206) at L114–115 — clean `isError`, ugly message — not a crash. `agy.exe` is a real PE, not a `.cmd` shim, so this is not the Cursor PowerShell-injection bug.

**Why it matters.** A legal-looking prompt still blows the cap; the error text tells the caller to YOLO and have Gemini read a file.

**Fix.** Reject when `len(subprocess.list2cmdline(cmd).encode("utf-16le"))//2 >= 32767`. For large prompts, use `--input-format stream-json` / `--output-format stream-json` and send a `user` event on stdin.

---

### 6. **MEDIUM** · `run_gemini()` L103–105; `TOOLS` `gemini-reply` L210–224 · YOLO reply + full toolset are escalation hatches

**What is wrong.** Default `init` advertises `invoke_subagent`, `define_subagent`, `call_mcp_tool`, `search_web`, `read_url_content`, full `browser_*`, `generate_image`. Docs: subagents may get write/MCP/shell. Wrapper cannot pass `--no-subagents` (flag does not exist). `--disable-slash-commands` exists (“Disable slash command and skill expansion in print mode”) and is **not** passed; `agy -p /model` is a documented print invocation that persists the default model. `gemini-reply(always_approve: true)` adds `--dangerously-skip-permissions` with no cwd guard (finding 2).

Shell/MCP/web on the default path **are** gated: `run_command` came back `CANCELED` in 2s with an auto-deny notice; wrapper treats non-`SUCCESS` as `isError`. I could **not** get an allow-listed command (`git status --short`) to run in `-p`. Escalation that *does* bite today: trusted-workspace **file** tools (finding 1) and YOLO on reply.

**Fix.** Pass `--disable-slash-commands` on every call. Copy `destructiveHint` / the YOLO warning onto `gemini-reply`. Require cwd + `_safe_cwd` when reply sets `always_approve`. Do not advertise a review seat that still carries `invoke_subagent` / `write_to_file` unless finding 1 is closed.

---

### 7. **LOW** · success path L116–141 · `usage` dropped; tool text lies about stalling

**What is wrong.** JSON `usage` (input/output/thinking/cache tokens) is discarded; no spend ledger (unlike `wmw_cursor_mcp.py`). ERROR/CANCELED **are** flagged (`isError: true`) — verified. The hole is SUCCESS-with-writes (finding 1), not failed-as-success.

Tool description: “headless permission prompts otherwise stall the run.” Live denies in ~2s (`ERROR`/`CANCELED`), no stall. Issue #548 hangs look fixed on 1.1.19 for these tools.

**Fix.** Append `usage` to the footer. Say “denied”, not “stall”. Keep `--print-timeout 60m` for long generation, not for permission prompts.

---

## VERIFIED

| Check | How |
|---|---|
| agy 1.1.19 flags | `agy.exe --help` — no `--cwd`, `--deny`, `--prompt-file`, `--no-subagents`; has `--dangerously-skip-permissions`, `--mode accept-edits\|plan`, `--sandbox`, `--disable-slash-commands`, `--conversation`, `--output-format json\|stream-json` |
| `--cwd` | `flags provided but not defined: -cwd` — wrapper’s `subprocess cwd=` is the right knob; `init.cwd` followed it |
| JSON envelope | Official headless docs + live PING/canary objects; no `model` |
| `init.model` | `stream-json` + `--model gemini-3.6-flash-high` → init had the slug; result still no model |
| Trusted vs untrusted writes | Python `subprocess.run` matching the wrapper (`stdin=DEVNULL`, `-p`, `--output-format json`); Temp write SUCCESS; repo probe ERROR |
| `--mode plan` | Trusted write still SUCCESS |
| Shell default | `echo` → `CANCELED` + jetski stderr; `git status --short` → `ERROR` user denied |
| Missing conversation | Fake UUID → warning + new SUCCESS id |
| `_safe_cwd` | Imported the module; junction/case/descendants/drive-relative as above |
| Argv budget | `list2cmdline` + UTF-16 unit counts |
| Config | `~\.gemini\antigravity-cli\settings.json` (trust list, allow rules, default model); `agy mcp list` → none; `mcp_config.json` empty |
| Docs | `https://antigravity.google/docs/cli/{headless,permissions,modes,sandbox,reference,features}` |

## Could not verify

- Whether `permissions.allow` is honored in `-p` (issue #548 says no; `git status --short` may also have been a pattern miss).
- `read_file(*)` / web / browser / subagent / MCP in a live default call (MCP servers empty on this box).
- Whether `--sandbox` AppContainer would contain `run_command` on Windows (irrelevant to `write_to_file`).
- Orphaned grandchildren after `PROC_TIMEOUT_S` (Python `TerminateProcess` on the parent; subagents are documented as separate processes).
- `/model` via `-p` actually mutating `settings.json` (not run; would persist).

## Verdict

**SHIP-WITH-FIXES** — stdio, UUID, equals-form, stdin close, and ERROR/CANCELED handling are sound. Do not send review tickets through this seat until finding 1 is closed; `--mode plan` is not a write block on agy 1.1.19.

— Grok 4.6