# REVIEW TASK — wmw_cursor_mcp.py v1.6

Review the file `mcp-seats/wmw_cursor_mcp.py` in this repo. It is an MCP stdio server that wraps
the Cursor Agent CLI so an orchestrator can dispatch to Cursor-pool models as a persistent seat.

Four changes landed in v1.6 that you should focus on, though you may report anything you find:

1. **Argv-unsafe prompt transport.** The Cursor CLI has no prompt-file flag and no documented stdin
   prompt path, and the Windows `.cmd` shim corrupts long or non-ASCII command lines. So when a
   prompt is over 2000 chars or contains non-ASCII text, `run_cursor()` now writes it to an
   ASCII-named UTF-8 temp file inside `cwd` and sends only a short ASCII pointer prompt telling the
   model to read that file. The spill file is removed in a `finally` block.
2. **`_safe_cwd()` now raises when `always_approve` is true and `cwd` is None** — previously a
   write-capable `--yolo` run with no cwd would inherit the server process's own working directory,
   which could be a home or system directory.
3. **Spend-ledger completeness.** `_log_spend()` is now also called on timeout, on unparseable
   output, on a reported agent error, and on a nonzero exit — so a call that may already have burned
   metered tokens still leaves an audit row, not just successful calls.
4. **Stale metadata** — the model-note string said the default was `composer-2.5-fast`; the actual
   default is `composer-2.5`.

## What to assess

- **Correctness of the spill-file transport.** Is the cleanup actually guaranteed on every path,
  including the early `return` inside the `except OSError` branch? Can the pointer prompt be
  confused by an existing file? Is writing into `cwd` safe on a read-only (`--mode ask`) call?
- **Whether fix 2 closes the hole completely**, or whether a write-capable path still exists that
  skips validation.
- **Whether the ledger is now genuinely complete**, or whether a billable path still escapes logging.
- **Any regression** in the meter guard (INCLUDED / CREDITS / UNKNOWN and the `spend_credits`
  refusal), the UUID session-id validation, the `--mode ask` read-only default, or the footer.
- Anything else that is actually wrong.

## Deliverable

Numbered findings, most severe first. Each: **severity** (CRITICAL / HIGH / MEDIUM / LOW) ·
file + location · what is wrong · why it matters · a concrete fix. Then a verdict line:
**SHIP** / **SHIP-WITH-FIXES** / **REWORK**, one sentence of rationale, signed with your model name.

Be concrete and skeptical. No padding. "None found" is a valid section.
