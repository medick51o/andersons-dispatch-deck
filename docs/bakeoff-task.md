# BAKEOFF TASK — identical brief for every seat

You are reviewing ONE file: `mcp-seats/wmw_grok_mcp.py` in this repository.

It is an MCP stdio server that wraps the Grok Build CLI so an orchestrator can dispatch to Grok as
a persistent conversational seat. It was hardened by a council on 2026-08-22 and has not been
touched since. Nobody has re-reviewed it after that hardening.

## What to look for

Read the file and report real defects. Areas worth your attention, though you are not limited to
them:

- **Prompt transport.** The prompt is written to a temp file and passed with `--prompt-file`. Is
  the temp file always cleaned up on every path? Can its contents leak? Is the path safe?
- **Subprocess handling.** Argument construction, encoding, timeouts, exit-code interpretation,
  what happens to a child process on timeout.
- **The read-only claim.** With `always_approve` false the wrapper passes explicit `--deny` rules
  for Write/Edit/MultiEdit/NotebookEdit/Bash. Is that actually sufficient to make the call
  read-only? What could still get through?
- **The `_safe_cwd` guard.** It is meant to stop a write-capable session from being pointed at a
  home, system or credential directory. Does it succeed? Consider descendants, symlinks, case
  sensitivity, and drive-relative paths.
- **Session-id validation**, JSON-RPC protocol handling, and error paths that could mislead a
  caller into believing a failed call succeeded.
- **Anything else that is genuinely wrong.**

## Rules

- Report only defects you can point at in the actual code. No speculation presented as fact.
- If you believe something is fine, do not pad the report with it.
- "None found" in a category is a valid and useful answer.

## Deliverable

Numbered findings, most severe first. Each one:

**severity** (CRITICAL / HIGH / MEDIUM / LOW) · location (function or line) · what is wrong ·
why it matters · a concrete fix.

Then a verdict line: **SHIP** / **SHIP-WITH-FIXES** / **REWORK**, one sentence of rationale, signed
with your exact model name.
