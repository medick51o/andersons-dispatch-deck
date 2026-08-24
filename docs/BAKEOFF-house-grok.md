I'll review `mcp-seats/wmw_grok_mcp.py` against the brief: read the actual code first, then report only defects I can point at.The wrapper is in `mcp-seats`. I'll read the current file and the sibling seats so findings rest on the code, not the old council packet.I have the wrapper. Next I’ll verify Grok’s real CLI flags, session-id shape, and whether `_safe_cwd` / deny-rules actually bind the way the comments claim.Grok 0.2.106 is on the box. I’ll probe deny-rule vs disallowed-tools, inspect config, and empirically break `_safe_cwd` and the UUID guard.Review of `mcp-seats/wmw_grok_mcp.py` (v1.3, last hardened 2026-08-22). Findings are from the file plus live checks against Grok 0.2.106 on this box.

---

### 1. **CRITICAL** · `DENY_RULES` (L32) and `run_grok()` (L105–113) · the read-only path is not read-only

**What is wrong.** When `always_approve` is false the wrapper only adds `--deny Write|Edit|MultiEdit|NotebookEdit|Bash`. That is a permission gate on five names, not a tool-set jail.

Grok’s own docs distinguish the two controls: `--deny` leaves tools available and only gates them; `--disallowed-tools` / `--tools` actually remove them. The documented read-only recipe is `--tools read_file,grep,list_dir`. The wrapper uses neither.

Three holes follow from the code that is there:

- **MCP is not denied.** Grok’s built-in table includes `search_tool` / `use_tool` for MCP, and the headless flag table says *“MCP meta-tools remain available unless denied.”* `DENY_RULES` has no `MCPTool`. `grok inspect` in this directory loads `playwright`, `github`, `wmw-grok`, `wmw-cursor`, `wmw-gemini` from `~/.claude.json` (`compat.claude.mcps` defaults on).
- **User YOLO is not overridden.** `~/.grok/config.toml` has `permission_mode = "always-approve"`. Deny rules still win for names they match, but everything *not* denied is auto-approved. The wrapper never passes `--permission-mode default` (the one CLI value Grok says actually overrides config).
- **`--deny MultiEdit` is a no-op.** Grok’s permission tool names are `Bash`, `Read`/`NotebookRead`, `Edit`/`Write`/`NotebookEdit`, `Grep`/`Glob`, `MCPTool`, `WebFetch`, `WebSearch`. Unrecognized names are *“skipped with a warning rather than failing the load.”*

**Why it matters.** A caller that omits `always_approve` is told this is a read-only review seat. On this box that seat can still drive GitHub MCP, Playwright, or a nested `wmw-grok` call with `always_approve: true` — which bypasses this wrapper’s deny list entirely.

**Fix.** On the default path: `--tools read_file,grep,list_dir` (and `web_search,web_fetch` only when `allow_web_search`), plus `--deny MCPTool`, plus `--permission-mode default` so config YOLO cannot auto-approve leftovers. Drop the unrecognized `MultiEdit` deny.

---

### 2. **HIGH** · `_safe_cwd()` (L153–170) · the write-cwd guard does not do what it claims

**What is wrong.** The guard is exact-match on `realpath` plus a basename/substring check for six secret dirnames. Empirically, with `always_approve=true`, these were **ALLOWED** on this box:

| cwd | why it slips |
|---|---|
| `\\?\C:\Users\andre` | `realpath` keeps the `\\?\` prefix; it does not equal `C:\Users\andre` |
| `\\localhost\C$\Users\andre` | UNC home; not in `banned` |
| `C:\Users` | parent of home, not equal to home |
| `C:\WINDOWS\System32`, `C:\Windows\SysWOW64`, `C:\Windows\Temp` | descendants of `SystemRoot`; only `C:\Windows` itself is banned |
| `C:\Program Files\Git`, `C:\Program Files (x86)` | descendants / `ProgramFiles(x86)` is not even in the env list |
| `C:\Users\andre\AppData\Roaming`, `...\AppData\Local` | credential roots; not in the secret list |
| `C:\Users\andre\.gnupg` | missing from `(".ssh", ".aws", ".grok", ".gemini", ".claude", ".config")` |

It also returns the **original** `cwd`, not `real`. A symlink can pass the check pointing at a project and be swapped before Grok starts. The later cursor wrapper already fixed this class of bugs (`_is_within`, `ProgramFiles(x86)`, `.gnupg`/`.kube`, return canonical path). This file did not.

**Why it matters.** The whole point of the function is “a write-capable seat may not be pointed at a home, system or credential directory.” It fails that on the reference OS, including home itself via `\\?\` / UNC.

**Fix.** `normcase(realpath(...))`, then refuse if the path **is or is under** home/profile, drive root, `SystemRoot`/`windir`/`ProgramFiles`/`ProgramFiles(x86)`/`ProgramData`, or any path component in `{.ssh,.aws,.grok,.gemini,.claude,.config,.gnupg,.kube,.azure}`. Return the canonical path, not the caller string. Strip/reject `\\?\` and UNC forms of those same roots.

---

### 3. **HIGH** · `_safe_cwd()` (L155–156), `_tool_call()` (L242–257), schema (L212 vs L217) · write-capable calls skip the guard

**What is wrong.**

```155:156:mcp-seats/wmw_grok_mcp.py
    if not always_approve or cwd is None:
        return cwd
```

- Schema text says cwd is *“Required when always_approve is true.”* `required` is still only `["prompt"]`. `cwd is None` + `always_approve=true` is allowed; Grok then inherits the MCP server’s process cwd (often a home or random project).
- `grok-reply` never calls `_safe_cwd`, never accepts `cwd`, and still takes `always_approve`.
- Because the guard is skipped entirely when `always_approve` is false, this sequence is legal: `grok(cwd="C:\\Users\\andre\\.ssh")` (read-only, secrets readable because `Read` is not denied) → `grok-reply(always_approve=true)` (write-capable, no cwd check). Session dirs on disk are already namespaced by cwd (`~/.grok/sessions/<url-encoded-cwd>/<uuid>`).

The cursor sibling requires cwd on YOLO and runs **both** start and reply through `_safe_cwd`. Grok does not.

**Why it matters.** The loaded gun does not have to name a project directory. A reply can escalate a session that was opened on a banned path.

**Fix.** `if always_approve and not cwd: raise ValueError(...)`. Run `_safe_cwd` on every call that has a cwd, including read-only. Give `grok-reply` a `cwd` field and require it (and the guard) whenever `always_approve` is true.

---

### 4. **HIGH** · `run_grok()` timeout handler (L116–122) · timeout reports failure while children keep running

**What is wrong.** `subprocess.run(..., timeout=3600)` on timeout does `process.kill()`. On Windows that is `TerminateProcess` of `grok.exe` only. Grok is an agent that spawns tool processes (`run_terminal_cmd`, MCP servers, etc.). Those grandchildren are not in a job object or process group the wrapper owns. The handler then `return True, "grok timed out..."` and unlinks the prompt file.

**Why it matters.** The caller is told the call failed. Under `always_approve`, a shell/write child can still finish. That is a false-failure with live side effects, up to an hour after dispatch.

**Fix.** On Windows, assign the child to a Job Object with `KILL_ON_JOB_CLOSE` (or `taskkill /T /F /PID` as a fallback). On POSIX, `start_new_session=True` and kill the process group. Do this in the `TimeoutExpired` handler *and* on unexpected wrapper death.

---

### 5. **LOW** · prompt tempfile (L91–95, finally L125–130) · leak on write failure; file is 0o666 for the whole run

**What is wrong.** Cleanup in `finally` does run on timeout and launch failure — that part is fine. Two leftovers:

- `tmp = f.name` is assigned **after** `f.write(prompt)`. If write raises, `tmp` is still `None`, `delete=False` has already created the file, and `finally` will not unlink it.
- Live `NamedTemporaryFile` on this box is mode `0o100666` under `%TEMP%`. The prompt sits there for the entire Grok run (up to 3600s). Same-user processes can read it. (Windows ACLs on `Local\Temp` stop other users; this is not a cross-user leak.)

**Why it matters.** Disk-full / huge-prompt errors leave prompt text in temp. Long-running dispatches leave the full prompt on disk for an hour.

**Fix.** `tmp = f.name` before write; `chmod 0o600` after create; unlink in `finally` as today. Optional: write under a user-only directory instead of the shared temp root.

---

### None found

- **Session-id validation.** `_UUID_RE` + `\A...\Z` rejects trailing newline, spaces, and leading-dash ids. `--resume={id}` equals form binds the value (does not reparse as flags). Live Grok ids like `01a02b88-b508-7c40-8faf-29ac8085ed1d` match.
- **JSON-RPC misleading success.** Nonzero exit, `{"type":"error",...}`, missing/empty `sessionId`, and unparseable stdout all return `isError: true`. `_extract_json` fail-closes if the first object has no `sessionId`.

---

**SHIP-WITH-FIXES** — the stdio/session-id/error-flag plumbing is sound; do not trust the read-only claim or the cwd guard until MCP is actually removed from the toolset and `_safe_cwd` matches descendants, prefixes, and write-capable replies. — Grok 4.6