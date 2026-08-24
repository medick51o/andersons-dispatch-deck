I'll treat this as a security verification, not a code-and-ship task: read the wrapper, check the deny names against this CLI, and try to prove whether a read-only call can still write.Next I’ll read the Grok wrapper and the sibling seats so the deny list, flags, and reply path can be checked against how they actually run.I have the wrapper. Next I’ll check Grok’s own permission docs and CLI help so deny names and `--permission-mode` are verified, not assumed.Docs already show a few sharp edges. I’ll confirm them against CLI help and a live deny-name check, then hunt remaining write paths.CLI help confirms the flags exist. I’ll now inspect which MCP servers Grok actually loads and run live deny / permission-mode canaries.There's already a playpen from today's verification. I'll read those canary logs first so we don't re-run work that's already on disk.Prior canaries already show a write under `--permission-mode default`. I’ll extract the exact flags and unrecognized-name warnings from those logs, then re-run the critical tests myself.`--permission-mode default` still auto-allowed a write, and `--no-subagents` may not have blocked spawn. I’ll confirm those flags against the real argv, then rerun the leftover-tool path with the wrapper’s exact command line.Prior canaries didn’t pin the exact argv. I’ll rerun with the wrapper’s real flags: deny-name warnings, `--no-subagents`, and one leftover write tool.The original Codex/MCP write is **dead**. A read-only call is no longer a loaded gun via sibling seats. It is **not** a sealed jail: deny rules do the real work, and several controls the wrapper added do not do what the comments claim.

Verified on Grok Build **0.2.106**, this box, `permission_mode = "always-approve"` in `~/.grok/config.toml`, MCP servers loaded from `~/.claude.json` (including `wmw-codex`, `wmw-grok`, playwright). Canaries run with the wrapper’s exact argv (`--deny Write/Edit/MultiEdit/NotebookEdit/Bash/MCPTool/WebFetch/WebSearch --permission-mode default --no-subagents --no-memory --disable-web-search`).

---

### 1. HIGH · `run_grok()` read-only argv · `--no-subagents` does not block spawn

**What.** `--no-subagents` is passed. `spawn_subagent` was still **allowed** (`permission_resolved … decision=allow, wait_ms=0`). A general-purpose child ran to completion.

**Why it didn’t write.** The child **inherits deny rules**. Its `write` / `search_replace` / `run_terminal_command` / `use_tool` were denied (`deny rule on edit/bash/mcp`). `CANARY_G46_SUBAGENT.txt` was not created.

**Why it still matters.** This is not the jail the comment describes. `Agent` is **not** a `--deny` class (docs: unrecognized names are skipped). The real kill switch is `--disallowed-tools Agent`. Subagents remain a fan-out / spend / “try every leftover tool” path.

**Fix.** On the read-only path add `--disallowed-tools Agent` (and keep the deny list). Do not trust `--no-subagents` alone.

---

### 2. HIGH · `grok-reply` / `_tool_call()` · write-capable reply skips the cwd guard

**What.** `grok-reply` still takes `always_approve`, still does **not** take `cwd`, and never calls `_safe_cwd`.

Legal sequence: `grok(cwd="…\\.ssh")` (read-only; `Read` is not denied) → `grok-reply(always_approve=true)` (YOLO, no path check). Session dirs are already namespaced by cwd.

**Why.** The schema says a write-capable seat must name a project directory. The reply tool does not.

**Fix.** Require `cwd` whenever `always_approve` is true, on **both** tools. Run `_safe_cwd` on that path. Refuse home/system/credential trees by containment (`normcase(realpath)` + `_is_within`), not equality. The cursor sibling already does this.

This is **not** the original MCP bug. It is a remaining write-capable hole the orchestrator can still open.

---

### 3. HIGH · leftover undenied tools · `--permission-mode default` is not a write jail in headless

**What.** `--permission-mode default` **does** override config YOLO: logs show `permission_mode=Some(Default)` and `yolo_mode: false`.

It does **not** stop writes of tools the deny list does not name. Control run **without** `--deny Write`: headless hit `permission_prompt` on `write`, then `permission_resolved decision=allow wait_ms=0`, and wrote `CANARY_PERM_MODE.txt`. Docs say a headless prompt is cancelled; **this CLI auto-allows it**.

So in headless, `default` and YOLO are equivalent for anything not denied. Deny rules are the only gate.

Live leftovers under the wrapper argv:

| Tool | Result |
|---|---|
| `write` / `search_replace` | Denied (`deny rule on edit`) |
| `run_terminal_command` | Denied (`deny rule on bash`) |
| `monitor` | Denied as Bash (`deny rule on bash for tool monitor`) |
| `use_tool` → `wmw-codex__codex`, `wmw-grok__grok` (`always_approve: true`), `playwright__browser_run_code_unsafe` | Denied (`deny rule on mcp for tool use_tool`) |
| `search_tool` | **Allowed** (discovery only) |
| `spawn_subagent` | **Allowed**; child inherit-denied |
| `scheduler_create` | **Allowed**; fired a child that inherit-denied; canary file not created |

`image_gen` / `image_edit` / video tools were not invoked (model skipped: they cannot write that exact token file). They are **not** in the deny class list. Given the perm-mode canary, an undenied image tool would auto-allow and write under `images/`.

**Fix.** On the read-only path use the CLI’s actual jail, not a longer deny list:

```
--tools read_file,grep,list_dir
--deny MCPTool
--disallowed-tools Agent
```

Add `web_search,web_fetch` only when `allow_web_search` is true. Drop the hope that `default` will catch leftovers.

---

### 4. MEDIUM · `DENY_RULES` · `MultiEdit` is still a no-op

Recognized permission names (CLI docs, 22-permissions-and-safety.md): `Bash`, `Read`/`NotebookRead`, `Edit`/`Write`/`NotebookEdit`, `Grep`/`Glob`, `MCPTool`, `WebFetch`, `WebSearch`. Unrecognized names are skipped with a warning.

Live: `--deny Write` matched `search_replace` / `write`. `--deny Bash` matched `run_terminal_command` and `monitor`. `--deny MCPTool` matched `use_tool` and `mcp:wmw-codex__codex` / `mcp:wmw-grok__grok`.

`MultiEdit` is a **hook alias** for `search_replace`, not a permission class. A MultiEdit-only deny still wrote `CANARY_MULTIEDIT.txt`. The file’s own comment already admits this; the name is still in the tuple.

**Fix.** Delete `MultiEdit` from `DENY_RULES`. It does not fail the load; it just pretends.

---

### 5. MEDIUM · `allow_web_search` is dead

When `always_approve` is false, `DENY_RULES` **always** includes `WebFetch` and `WebSearch`. `allow_web_search: true` only skips `--disable-web-search`. Deny still wins, so research tickets cannot fetch.

**Fix.** Omit `WebFetch`/`WebSearch` from the deny loop (and omit `--disable-web-search`) when `allow_web_search` is true.

---

### 6. LOW · version / docs drift · `_safe_cwd` still exact-match

- Module docstring says v1.3, comments say v1.4, `serverInfo.version` is `"1.3.0"`.
- `_safe_cwd` still equality-matches home/`SystemRoot` and misses `\\?\`, UNC, descendants (`C:\Windows\Temp`, `Program Files (x86)`, `.gnupg`). Write-capable only; cursor sibling already fixed this class.
- Read-only may still `cwd` into `.ssh` and **read** secrets (`Read` is not denied).

---

## Answers to the four questions

**1. Is the escalation closed?**  
**The Codex/MCP write is closed.** A read-only call cannot have another MCP seat write. Verified:

- Policy text: `Denied by permission policy: deny rule on mcp for tool use_tool`
- Same deny on `mcp:wmw-grok__grok` with `always_approve: true` and on `mcp:playwright__browser_run_code_unsafe`
- `CANARY_MCP_CODEX.txt` and `CANARY_G46_LEFTOVER.txt` do not exist

`grok-reply` **does** apply the same deny list when `always_approve` is false (both tools call `run_grok()`). It does **not** apply `_safe_cwd` when the caller sets `always_approve` true.

Skills: invocation is auto-approved; the tools a skill then requests still hit deny. Slash `/always-approve` cannot beat deny (“enforced before YOLO”). Hooks in this run were not a write path. Subagents and scheduler still **run**, but inherit the deny list.

**2. Are the deny names correct?**  
**Yes, except `MultiEdit`.** `Write`, `Edit`, `NotebookEdit`, `Bash`, `MCPTool`, `WebFetch`, `WebSearch` matched live. `MCPTool` is the name this CLI documents (`mcp__server__tool` never matches). `Agent` is a `--disallowed-tools` entry, not a `--deny` class.

**3. Does `--permission-mode default` override `always-approve`?**  
**It turns YOLO off. It does not make undenied tools fail closed in headless.** `yolo_mode: false` + `write` still auto-allowed and wrote a file. Claude `~/.claude/settings.json` also has `"defaultMode": "auto"`, and the log says `auto permission mode seeded from Claude defaultMode`. Deny rules still win over YOLO. Do not treat this flag as the read-only control.

**4. Anything else?**  
`--tools` allowlist still missing (the documented read-only recipe). `allow_web_search` contradicted by the deny list. `grok-reply` YOLO with no cwd guard. `_safe_cwd` still a surface check. `--no-subagents` is theater; `--disallowed-tools Agent` is the real one.

---

## Verdict

**SHIP-WITH-FIXES — Grok 4.6**

The bug you reproduced (read-only Grok → Codex MCP → file write) is **actually closed**. I would not ship this as “read-only is airtight.” Minimum patch: `--tools read_file,grep,list_dir`, `--disallowed-tools Agent`, drop `MultiEdit`, make `allow_web_search` actually allow web, require `cwd` + `_safe_cwd` on every `always_approve` call including `grok-reply`.

**Verified how:** read `mcp-seats/wmw_grok_mcp.py`; checked Grok 0.2.106 `--help` and `~/.grok/docs/user-guide/{14,16,22}-*.md`; `grok inspect --json`; live canaries in `C:\Sync\_playpen\grok-verify-mcp-20260823` with session events (`permission_resolved`, `deny rule matched`) rather than model claims.