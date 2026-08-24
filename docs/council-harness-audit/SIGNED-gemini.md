```
VERDICT (3 sentences)
The harness introduces valuable visibility into CLI spend and prompt transport security, but its security controls contain critical implementation gaps that leave the system open to privilege escalation and unauthorized file modification. Enforcement is deeply inconsistent across seats—with Gemini completely omitting working directory validation on session replies and bypassing path containment checks—while the central concurrency lock suffers from a stale-reclaim race condition under load. Ultimately, because the harness only governs a small fraction of total account activity while cloud, IDE, and subagent execution bypass it entirely, it provides false assurance in its current state.

Q1 THE THREE FIXES
  1. injection      HOLDS
                    The Cursor prompt transport fix in `wmw_cursor_mcp.py` (lines 461-477) spills prompt text to a file in the playpen and passes an ASCII-only pointer (`pointer.isascii()`), while validating model IDs against `_MODEL_RE` (`r"\A[a-z0-9][a-z0-9._-]{0,63}\Z"`, line 125) and session IDs against `_UUID_RE` (line 126). Cwd is passed via the OS working directory (`subprocess.run(cwd=workdir)`), preventing shell metacharacters from reaching the `cursor-agent.cmd` Windows shim argv.

  2. read-only      BROKEN — `wmw_cursor_mcp.py:489` and `wmw_gemini_mcp.py:249-254`
                    In `wmw_cursor_mcp.py` line 489, `--approve-mcps` is passed unconditionally even when `always_approve=False` (`--mode ask`). This auto-approves all MCP tools defined in `~/.cursor/mcp.json`, allowing a read-only Cursor call to execute write/edit/shell actions via external or sibling MCP servers. Furthermore, in `wmw_gemini_mcp.py` lines 249-254, `gemini-reply` fails to extract or pass `cwd`, executing `agy --mode plan` in an unconstrained directory.

  3. escalation     BROKEN — `wmw_cursor_mcp.py:489` and `wmw_gemini_mcp.py:108-113`
                    While `wmw_grok_mcp.py` (lines 123-132) denies `MCPTool` and passes `--disallowed-tools Agent`, `wmw_cursor_mcp.py` line 489 unconditionally passes `--approve-mcps`, enabling a read-only Cursor seat to call sibling `wmw-*` seats registered in `~/.cursor/mcp.json`. `wmw_gemini_mcp.py` does not restrict subagents or tool invocation in `--mode plan`, allowing Gemini to escalate actions through child processes or sibling seats.

Q2 NEW FINDINGS
  1. HIGH / `wmw_gemini_mcp.py:249-254` (`_tool_call` for `gemini-reply`)
     ATTACK: `gemini-reply` does not extract `cwd` from arguments nor call `_safe_cwd`. When `always_approve=True` is passed to continue a conversation, `run_gemini` executes `agy --dangerously-skip-permissions` in the process's default directory without any path restrictions, allowing file writes in sensitive user or system directories.
     FIX: Extract `cwd` in `gemini-reply` and pass `cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve)` to `run_gemini`.

  2. HIGH / `wmw_gemini_mcp.py:152-169` (`_safe_cwd`)
     ATTACK: `_safe_cwd` checks exact string equality (`real in banned`). Banning `%USERPROFILE%` or `C:\Windows` does not prevent pointing `cwd` at `C:\Windows\System32` or `%USERPROFILE%\AppData`. Furthermore, line 169 returns uncanonicalized `cwd` instead of `real`, creating a TOCTOU symlink bypass.
     FIX: Implement path containment checks (`_is_within(real, banned_dir)`) like `wmw_grok_mcp.py` line 203, and return `real`.

  3. HIGH / `wmw_gemini_mcp.py:101-114` (`run_gemini`)
     ATTACK: Prompt text is passed directly on the command line (`cmd += ["-p", prompt]`). If `find_agy()` resolves to a Windows batch shim (`agy.cmd`), `subprocess.run` invokes `cmd.exe`, causing unescaped shell metacharacters (`&`, `|`, `%`, `^`, `<`, `>`) in `prompt` to execute host commands.
     FIX: Spill prompts to a temporary handoff file (or pass via stdin) and supply a sanitized file pointer on argv.

  4. HIGH / `dispatch-guard.py:64-87` (`Lock.__enter__`)
     ATTACK: If a process holds `LOCK` for longer than `LOCK_STALE_S` (30 seconds), a competing process calls `os.unlink(LOCK)` and acquires the lock (lines 74-76). When the first process completes, its `__exit__` unlinks the new lock, destroying mutual exclusion and allowing concurrent dispatches to exceed concurrency (`MAX_CONCURRENT`) and percentage caps.
     FIX: Store PID in `LOCK`, verify ownership before unlinking, or use OS-native atomic file locking (`msvcrt.locking` / `fcntl.flock`).

  5. MEDIUM / `wmw_grok_mcp.py` & `wmw_gemini_mcp.py` (Missing Guard Integration)
     ATTACK: Neither Grok nor Gemini wrappers load or execute `dispatch-guard.py` (`preflight` or `reserve`). Dispatches to Grok or Gemini bypass repository sanity checks and consume unlimited unreserved model usage.
     FIX: Wire `preflight()` and `reserve()` into `run_grok()` and `run_gemini()` identically to `wmw_cursor_mcp.py` (lines 433-453).

  6. MEDIUM / `wmw_grok_mcp.py:45-46` (`DENY_RULES`) & line 133
     ATTACK: `DENY_RULES` relies on exact tool name strings (`Write`, `Edit`, `Bash`). Unlisted tool names or new tools introduced in Grok CLI updates fall through to auto-approval under `--permission-mode default`.
     FIX: Pin permission mode to deny-all by default for any unrecognised tool names.

  7. LOW / `wmw_cursor_mcp.py:228-253` (`_recent_billable`)
     ATTACK: `_recent_billable` returns `0` if `SPEND_LEDGER` (`bench-spend.jsonl`) is missing or unparseable. An agent operating inside `PLAYPEN` can delete or corrupt `bench-spend.jsonl` to reset `_recent_billable` to 0, completely bypassing `COUNCIL_LOCK`.
     FIX: Move spend ledger storage to a protected directory outside `PLAYPEN` and treat file missing/corruption as failing closed.

Q3 CANARY AUDIT
  - REAL CHECKS:
    - Cursor tool registration and argument validation (`spend_credits` refusal, `auto`/`UNKNOWN` refusal, metacharacter model ID refusal, non-allowlisted YOLO model refusal).
    - Preflight refusal for write dispatches on empty git repositories (`_armcheck_emptyrepo`).
    - Grok session ID flag-smuggling prevention and reply escalation `cwd` check.
  - THEATRE / FLAWED CHECKS:
    - `write-capable in System32 refused` (`armcheck.py:41-42`): Only tests Cursor seat; Gemini seat completely lacks System32 containment checks and would fail this test if executed against `wmw_gemini_mcp.py`.
    - `no lease left behind` (`armcheck.py:54-55`): Evaluates `not {}` to `True` if `RESV` file does not exist, passing trivially without validating lease cleanup.
    - `meters readable` (`armcheck.py:66-76`): Fails whenever an access token in `~/.grok/auth.json` expires, measuring token freshness rather than harness code validity.
  - UNCOVERED:
    - Zero security coverage for Gemini (`wmw_gemini_mcp.py`): no prompt injection checks, no `gemini-reply` `cwd` checks, no `_safe_cwd` containment tests.
    - Zero coverage for inter-seat privilege escalation via `--approve-mcps`.
    - Zero coverage for concurrent locking races in `dispatch-guard.py`.
  - CAN THE ARM TEST PASS WHILE RIG IS UNSAFE?
    - YES. `armcheck.py` reports `ALL ARMED` despite `wmw_gemini_mcp.py` allowing unconstrained `gemini-reply` write sessions, command injection via prompt argv in Gemini, inter-seat escalation in Cursor via `--approve-mcps`, and mutex breakdown in `dispatch-guard.py`.

Q4 IS IT WORTH IT
  The harness in its current state provides FALSE ASSURANCE. 
  While the architectural intent (atomic reservations, prompt spilling, allowance tracking) is sound, the implementation is fragmented and incomplete. Critical controls present in one seat (such as `dispatch-guard.py` integration or `_safe_cwd` containment) are omitted in others. More importantly, as acknowledged in `dispatch-guard.py` lines 24-28, these stdio wrappers govern only dispatches that pass directly through them. IDE agent modes, Cloud Agents, web dashboards, and CI runners execute on vendor infrastructure and completely bypass this entire codebase. Because those ungoverned lanes account for the vast majority of real spend and risk, maintaining ~2,500 lines of complex Python wrappers that fail open in multiple internal edge cases creates high maintenance overhead without guaranteeing security or cost bounds.

WHAT IS WELL BUILT
  - Prompt Spilling & Pointer Indirection (`wmw_cursor_mcp.py:461-477`): Excellent defense against Windows `.cmd` / PowerShell command injection by isolating caller prompt text in temporary files and passing ASCII-only pointers.
  - Atomic Reservation Architecture (`dispatch-guard.py:184-225`): Correctly identifies that post-hoc meter reading cannot stop concurrent spend spikes, implementing a proactive headroom reservation model.
  - Lineage & Spend Ledger Logging (`wmw_cursor_mcp.py:165-182`): Clean, structured JSONL tracking with detailed model lineage classification and explicit YOLO allowlisting.
  - Grok Read-Only Hardening (`wmw_grok_mcp.py:123-133`): Strong defense-in-depth against Grok CLI defaults by disabling `Agent` subagents and pinning permission modes.

CONFIDENCE + WHAT WOULD CHANGE YOUR MIND
  - CONFIDENCE: HIGH (CONFIRMED). All findings are directly anchored to line numbers and code paths in `pkt-gemini.md`.
  - WHAT WOULD CHANGE MY MIND:
    1. Empirical proof that `cursor-agent` in `--mode ask` suppresses all MCP tool calls regardless of `--approve-mcps`.
    2. Empirical proof that `agy` (`Antigravity CLI`) enforces strict read-only execution in `--mode plan` when `--dangerously-skip-permissions` is supplied without a `cwd`.
    3. Proof that vendor CLI shims on Windows handle raw command-line string arguments without invoking `cmd.exe` or PowerShell parsing.
```
