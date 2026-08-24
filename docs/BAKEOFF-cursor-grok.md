I'll read the handoff prompt and the required skill first, then follow those instructions exactly.Using the review skill next, then I’ll read the bakeoff task and the target file.The bakeoff brief is the source of truth here. I’ll inspect the Grok MCP wrapper and nearby context next.The wrapper’s safety claims need a check against the real CLI flags and the later Cursor seat, not just this file.Grok’s own permission docs disagree with this wrapper’s deny list. I’ll read those next and confirm the tool names.Checked `_safe_cwd`, the deny-list argv, `grok-reply`, and Grok’s own permission docs (including this machine’s `permission_mode = "always-approve"`). Numbered findings follow, most severe first.

1. **HIGH** · `_safe_cwd` (L155–156) + `_tool_call` (L244, L251–257) + grok schema (L212) · A write-capable session does not require a cwd, and `grok-reply` never runs the guard at all.
   Schema text says cwd is required when `always_approve` is true. The code does the opposite: `_safe_cwd` returns immediately when `cwd is None`, `_safe_argv(None)` is a no-op, and `run_grok` then adds `--always-approve` with no `--cwd`. `grok-reply` has no cwd argument and never calls `_safe_cwd`, so a follow-up can escalate a read-only thread to YOLO in whatever directory the MCP process inherited (often the open workspace, sometimes the profile).
   **Fix:** If `always_approve` is true, refuse a missing cwd (same hard error the later Cursor wrapper added). Run `_safe_cwd` on the reply path too, and add `cwd` to the `grok-reply` schema so a write-capable resume cannot skip the check.

2. **HIGH** · `_safe_cwd` (L157–170) · The path guard is an exact, case-sensitive match on a few roots, then returns the original string rather than the resolved path.
   `real in banned` does not cover descendants, so `C:\Windows\System32`, `C:\Program Files\Git`, and `D:\` (only the current drive’s root is banned via `os.path.abspath(os.sep)`) all pass. Python string compare is case-sensitive, so `c:\users\<you>` vs `C:\Users\<you>`, and `.SSH` vs `.ssh`, bypass the home and secret checks on Windows. Validation uses `os.path.realpath` but `--cwd` still gets the caller’s original path, so a symlink can be checked as one location and executed as another.
   **Fix:** Case-fold (`os.path.normcase`), reject cwd inside system roots (`SystemRoot`, `ProgramFiles`, `ProgramFiles(x86)`, `ProgramData`) with `os.path.commonpath`, keep home as an exact-root ban so projects under the profile still work, compare secret path segments case-insensitively, and return `real` rather than `cwd`.

3. **MEDIUM** · `run_grok` read-only argv (L32, L105–113) · The deny list does not make the default call read-only for anything outside those five names, and it never overrides config YOLO.
   `--deny Write/Edit/NotebookEdit/Bash` matches Grok’s documented rule names, and deny still wins under always-approve. `--deny MultiEdit` does not: Grok skips unrecognized rule names with a warning (`MultiEdit` is a hook alias, not a `--deny` tool class). This box’s `~/.grok/config.toml` has `permission_mode = "always-approve"`; the wrapper never passes `--permission-mode default`, so every undenied tool is auto-approved. Grok’s own docs keep MCP tools available unless denied (`MCPTool(...)`); none of the deny rules mention them. `--tools read_file,grep,list_dir` is the documented read-only recipe; this wrapper does not use it.
   **Fix:** On the read-only path pass `--permission-mode default` (flag beats config), `--deny MCPTool`, drop the no-op `MultiEdit` rule, and prefer an allowlist (`--tools` / `--disallowed-tools` with Grok’s real ids: `read_file`, `grep`, `list_dir`) instead of a Claude-shaped deny list.

4. **MEDIUM** · `run_grok` `subprocess.run` (L116–122) · Timeout kills only the Grok process, not its children.
   `timeout=GROK_TIMEOUT_S` maps to `Popen.kill()` → Windows `TerminateProcess` on that PID. Shell/`run_terminal_command` grandchildren are not in a job object, so they keep running after the wrapper returns `isError` and unlinks the prompt file. A timed-out build ticket can leave compilers, writes, or network jobs going.
   **Fix:** On Windows, assign the child to a Job Object (or `taskkill /F /T /PID`) and kill the tree in the `TimeoutExpired` handler before returning.

5. **MEDIUM** · `run_grok` footer (L150–151) + `grok-reply` (L251–254) · `sessionId` exists only as a forgeable line in model text.
   The MCP result has no structured `sessionId`. Callers have to regex the footer out of `text`. The model can emit a lookalike `[wmw-grok] sessionId:` line; a parser that takes the first match resumes the wrong UUID. `grok-reply` will happily `--resume=` whatever UUID survived validation.
   **Fix:** Put `sessionId` in a structured field (or a second content block the model cannot write). Strip lookalike footer lines from `text` before appending the real one.

6. **LOW** · `TOOLS` `grok-reply` (L220–234) · Reply is as dangerous as `grok` when `always_approve` is true, but it has no `destructiveHint`/`openWorldHint` and its description never says the default is deny-listed or that YOLO is a loaded gun.
   **Fix:** Copy the `grok` annotations and the same always_approve/cwd warning onto `grok-reply`.

**Prompt transport:** none found. `NamedTemporaryFile(..., delete=False)` plus `finally: os.unlink` runs on timeout, `OSError`, and success; argv is a list so the temp path is not shell-parsed.

**Session-id argv injection:** none found. UUID regex plus `--resume={id}` still blocks leading-dash flag smuggling.

**False success:** none found. Nonzero exit, `type == "error"`, missing/empty `sessionId`, and unparseable JSON all return `isError: true`.

**SHIP-WITH-FIXES** — UUID/prompt-file/isError plumbing is sound, but the write-capable cwd guard does not do what the schema and README claim, and the read-only path still inherits config YOLO plus MCP. — Cursor Grok 4.6

---
🟣➤⚫ [wmw-cursor] ♾️ xAI · cursor-grok-4.6-high
   sessionId: 3be6453a-2a0b-410d-8008-c8d6171bcb23 · meter: INCLUDED · 145236 in / 23522 out