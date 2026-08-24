I'll read the handoff prompt and follow its instructions exactly.I'll load the bakeoff task and the Grok MCP wrapper, then verify the safety claims against current Grok CLI docs.Next I’ll pull Grok CLI docs and the wrapper’s deny/sandbox claims so the review is based on documented behavior, not assumptions.Web search was blocked, so I’ll pull Grok CLI docs from Context7 and local files, then check the deny-rule and sandbox behavior against those sources.Found Grok’s local user-guide docs. I’ll read permissions, sandbox, headless, and config next so the deny-rule review matches what the CLI actually documents.Checking a few remaining protocol and timeout details against the docs so findings stay evidence-based.Review of `mcp-seats/wmw_grok_mcp.py` (v1.3). Findings are from the file plus Grok’s on-disk user guide (`~/.grok/docs/user-guide/`) and this machine’s `~/.grok/config.toml`.

---

### 1. **CRITICAL** · `DENY_RULES` (L32) and `run_grok()` (L105–113) · the default path is not read-only

**What is wrong.** When `always_approve` is false the wrapper only adds `--deny Write|Edit|MultiEdit|NotebookEdit|Bash`. That is a permission gate on five names, not a tool-set jail.

Grok’s own docs distinguish the two controls: `--deny` leaves tools available and only gates them; `--tools` / `--disallowed-tools` actually remove them. The documented read-only recipe is `--tools "read_file,grep,list_dir"`. The wrapper uses neither.

What still gets through, from the docs and this box:

- **MCP is not denied.** `--tools` “retains requested tools plus always-on MCP meta-tools” unless they are denied. Recognized deny names include `MCPTool`; the wrapper never passes it. GitHub, Playwright, filesystem, or a nested write-capable seat remain callable.
- **User YOLO is not overridden.** `~/.grok/config.toml` has `permission_mode = "always-approve"`. Deny still wins for names it matches; everything else is auto-approved. The wrapper never passes `--permission-mode default` (the one CLI value Grok says actually overrides config). Passing `dontAsk` on the flag is accepted but **does not** enable that policy.
- **`--deny MultiEdit` is a no-op.** Permission tool names are `Bash`, `Read`/`NotebookRead`, `Edit`/`Write`/`NotebookEdit`, `Grep`/`Glob`, `MCPTool`, `WebFetch`, `WebSearch`. Unrecognized names are “skipped with a warning rather than failing the load.” `MultiEdit` is a hook alias for `search_replace`, not a `--deny` class.
- **`--no-subagents` / `--no-memory` / `--disable-web-search` do bind** (those flags exist). They do not close MCP or config YOLO.

The comment at L106–108 is right that `--sandbox` fails open on Windows (Landlock/Seatbelt only; unsupported platforms “log a warning and continue without enforcement”). Switching to `--deny` does not make the call read-only.

**Why it matters.** A caller that omits `always_approve` is told this is a deny-listed review seat. On this box that seat can still drive MCP — including a nested `wmw-grok` call with `always_approve: true` — which bypasses this wrapper’s deny list entirely.

**Fix.** On the default path: `--tools read_file,grep,list_dir` (and `web_search,web_fetch` only when `allow_web_search`), plus `--deny MCPTool`, plus `--permission-mode default` so config YOLO cannot auto-approve leftovers. Drop the unrecognized `MultiEdit` deny. Do not use `--permission-mode dontAsk`; the docs say that flag value does not enable the policy.

---

### 2. **HIGH** · `_safe_cwd()` (L153–170) and `grok-reply` (L251–257) · the write-capable cwd guard does not do what the schema claims

**What is wrong.** The guard is exact-match on `realpath` plus a basename/substring check for six secret dirnames. It does not succeed against descendants, missing cwd, or the reply path.

- **Descendants of banned roots are allowed.** `real in banned` is equality, not containment. `C:\Windows\System32`, `C:\Program Files\Git`, and `C:\Users\<you>\Documents` are not in the set. There is no `commonpath` / `_is_within` check (the later Cursor wrapper added one). `ProgramFiles(x86)` and `ProgramData` are not even in the env list.
- **`cwd is None` skips the guard.** `if not always_approve or cwd is None: return cwd`. Schema text says cwd is required when `always_approve` is true; `required` is still only `["prompt"]`. Grok then inherits the MCP server’s process cwd.
- **`grok-reply` never calls `_safe_cwd`, never accepts `cwd`, and still takes `always_approve`.** Because the guard is skipped entirely when `always_approve` is false, this sequence is legal: `grok(cwd="C:\\Users\\andre\\.ssh")` (read-only; `Read` is not denied) → `grok-reply(always_approve=true)` (write-capable, no cwd check). Sessions on disk are already namespaced by cwd (`~/.grok/sessions/<url-encoded-cwd>/<uuid>`).
- **The function returns the original `cwd`, not `real`.** Validation uses the resolved path; Grok is launched with the unresolved one.

**Why it matters.** The schema and README say a write-capable seat cannot be pointed at home, system, or credential directories. The code allows exactly that via a descendant, a missing cwd, or a reply-path escalate.

**Fix.** `if always_approve and not cwd: raise ValueError(...)`. Refuse when the resolved path is *inside* a banned root, not only equal to it; `os.path.normcase` the comparison on Windows. Run `_safe_cwd` on every call that has a cwd, including read-only. Give `grok-reply` a `cwd` field and require it (and the guard) whenever `always_approve` is true. Pass the canonical path to `--cwd`.

---

### 3. **MEDIUM** · `run_grok()` timeout (L116–122) · the child tree is not reaped

**What is wrong.** `subprocess.run(..., timeout=GROK_TIMEOUT_S)` does kill `grok.exe` on expiry (Python waits for that PID). The except path then returns `isError`. It does not use a Windows job object or `taskkill /T`. Grok’s own docs say file modifications by tools are not rolled back on SIGTERM, and child bash/MCP processes are separate PIDs.

**Why it matters.** The caller is told the call failed. Under `always_approve`, a shell/write grandchild can still finish. That is a false-failure with live side effects, up to an hour after dispatch.

**Fix.** On `TimeoutExpired`, kill the whole process tree (job object or `taskkill /F /T /PID`), then wait, then return the error.

---

### 4. **LOW** · `TOOLS` `grok-reply` (L220–234) · reply is as dangerous as `grok` and does not say so

**What is wrong.** `grok` sets `destructiveHint` / `openWorldHint` and warns that `always_approve` is the loaded gun. `grok-reply` accepts the same flag, has no those annotations, and never says the default is deny-listed.

**Why it matters.** An orchestrator that only reads the reply schema will YOLO a follow-up without the warning the start tool carries.

**Fix.** Copy the `grok` annotations and the same `always_approve` / cwd warning onto `grok-reply`.

---

**SHIP-WITH-FIXES** — UUID / `--prompt-file` / `isError` plumbing is sound, but the default seat is not read-only against Grok’s actual tool and permission model, and the write-capable cwd guard does not do what the schema claims. — Cursor Grok 4.6

---
🟣➤⚫ [wmw-cursor] ♾️ xAI · cursor-grok-4.6-high
   sessionId: 8ff73272-e5e6-4ccf-8d02-f2995b880899 · meter: INCLUDED · 113836 in / 18997 out