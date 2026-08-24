# TICKET CLD-CUR-001 — argv-unsafe prompt transport

**Seat:** Composer (free bench, write-capable this ticket)
**Repo:** `C:\Sync\Projects\andersons-dispatch-deck`

## The bug (real, reproduced 4x today)

`mcp-seats/wmw_cursor_mcp.py` passes the user's prompt to the Cursor CLI as a command-line argument
(`-p <prompt>`). On Windows the CLI is reached through a `.cmd` shim. When a long prompt contains
emoji or unusual unicode, the shim mangles it: the CLI then emits plain text instead of the
requested JSON, the wrapper cannot parse a reply, and the receiving model reports it never got the
prompt body at all.

Reproduced today at ~2KB and ~7KB with emoji. A 5KB pure-ASCII prompt worked fine, and a short
prompt containing markdown pipes worked fine — so the trigger is non-ASCII content, not size alone.

## The fix — scoped, do exactly this

1. In `run_cursor()`, detect an **argv-unsafe prompt**: longer than 2000 characters OR containing
   any non-ASCII character.
2. For an argv-unsafe prompt, deliver it to the CLI WITHOUT putting it on the command line.
   **Verify first, do not guess:** check `cursor-agent --help` yourself for a prompt-from-file flag
   or a documented stdin path. If a supported non-argv path exists, use it (write a UTF-8 temp file
   or pipe via stdin as appropriate). **If NO supported non-argv path exists, do not invent a flag** —
   instead make the function fail fast with a clear, actionable error explaining the limit and
   telling the caller to shorten the prompt or move bulk into a file the model can read.
3. Clean up any temp file in a `finally` block.

## Must NOT change

The meter guard (INCLUDED / CREDITS / UNKNOWN classes and the `spend_credits` refusal), the
`--mode ask` read-only path, the UUID session-id validation, the `_safe_cwd` guard, the spend
ledger, and the footer must all keep behaving exactly as they do now.

## Write set

`mcp-seats/wmw_cursor_mcp.py` — this file ONLY.

## Must not

Do not commit. Do not push. Do not run any git command that changes state.

## Verify (run these, quote the output)

```
python -c "import ast,io; ast.parse(io.open('mcp-seats/wmw_cursor_mcp.py',encoding='utf-8').read()); print('AST OK')"
python -c "import sys; sys.path.insert(0,'mcp-seats'); import wmw_cursor_mcp as w; print(w.meter_class('kimi-k3-high'), w.meter_class('composer-2.5'), w.meter_class('auto'))"
```

The second must print `CREDITS INCLUDED UNKNOWN` — that proves the meter guard survived your edit.

## Report back

What you changed, what you VERIFIED (name the exact command and quote what it printed), and anything
you were unsure about. Claims are capped at evidence here: say "verified X by running Y", never
"it works".
