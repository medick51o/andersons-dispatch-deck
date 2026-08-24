I’ll read the review instructions first, then inspect `mcp-seats/wmw_cursor_mcp.py` and return the review in exactly the requested format.I’ve loaded the review spec and target file; next I’m double-checking against the required skill guidance and then I’ll deliver findings ordered by severity.1. **HIGH** · `mcp-seats/wmw_cursor_mcp.py` (`_safe_cwd`, around `L174-L183`) · Write-capable path validation only bans exact directory matches for home/system roots, not descendants, and uses case-sensitive string comparison on Windows paths.  
   Why it matters: `always_approve: true` can still target dangerous locations like `C:\Windows\System32` (descendant of `windir`) or bypass an exact-match ban via case variation, leaving a write-capable `--yolo` path that the fix was meant to close.  
   Concrete fix: Normalize with `os.path.normcase(os.path.realpath(...))` and reject when `real == banned` **or** `real.startswith(banned + os.sep)` for each banned root.

2. **MEDIUM** · `mcp-seats/wmw_cursor_mcp.py` (argv-unsafe spill block, around `L248-L254` and cleanup `L283-L290`) · Spill-file cleanup is not guaranteed if `mkstemp` succeeds but `os.fdopen(...).write(...)` fails; the `except OSError` returns before reaching the outer `finally` cleanup.  
   Why it matters: Failed handoffs can leave orphan `wmw_cursor_prompt_*.md` files in project directories, creating residue and possible prompt-data leakage.  
   Concrete fix: Move spill creation/write into a nested `try/finally` that unlinks on any write failure, or avoid early return in that branch and let a unified `finally` always run when `spill_path` is set.

3. **MEDIUM** · `mcp-seats/wmw_cursor_mcp.py` (argv-unsafe transport design, around `L234-L260`) · Read-only calls (`--mode ask`) still perform a real filesystem write in `cwd` for long/non-ASCII prompts.  
   Why it matters: This breaks the practical expectation of “read-only means no writes,” can trip file watchers, and fails on truly read-only directories even when the agent call itself should be non-destructive.  
   Concrete fix: Write spill files outside the user workspace (e.g., system temp dir) and pass an absolute ASCII path in the pointer prompt, or gate this behavior behind explicit opt-in when `cwd` is immutable.

4. **LOW** · `mcp-seats/wmw_cursor_mcp.py` (no-JSON trust branch, `L297-L300`) · Spend ledger is skipped on the “Workspace Trust Required” early return path.  
   Why it matters: Your v1.6 claim is “failed calls that may have burned tokens leave an audit row”; this branch is still an executed failure path without a ledger row.  
   Concrete fix: Add `_log_spend(..., ok=False, ...)` before returning from the trust-required branch (with `usage=None`, `sid=None`).

None found: meter guard behavior (`INCLUDED/CREDITS/UNKNOWN` + `spend_credits` refusal), UUID session-id validation, default `--mode ask` path, and default-model metadata note all appear consistent with the stated v1.6 intent.

**VERDICT: SHIP-WITH-FIXES** — core hardening is directionally correct, but the write-capable cwd guard and spill-file lifecycle still leave meaningful safety/audit gaps that should be closed before calling this robust. — *Codex 5.3*

---
🟣➤🔵 [wmw-cursor] 💸 OpenAI · gpt-5.3-codex
   sessionId: 786d2e4c-1971-42cb-a7d1-e845688a7eab · meter: CREDITS · 32767 in / 4040 out
🟣➤ 💸 —— THIS CALL SPENT MONEY —— 💸 🟣➤
   third-party CREDIT pool — billed at API prices