# HEAD-TO-HEAD REVIEW TASK

Review ONE file: `mcp-seats/wmw_gemini_mcp.py` in this repository.

It is an MCP stdio server that wraps the Antigravity CLI (`agy`) so an orchestrator can dispatch to
Google's Gemini as a persistent conversational seat. It was hardened by a council on 2026-08-22 and
**has never been re-reviewed since**. Nobody has audited it in its current state.

You have tools. Use them. Do not assume what the `agy` CLI does — verify it against its actual
help output, its documentation, or the machine's own configuration. A finding backed by evidence is
worth ten that are backed by pattern-matching.

## Specifically worth your attention

- **The read-only claim.** With `always_approve` false, what actually restrains this seat? Compare
  against what the CLI genuinely supports. Is "read-only" true, or only true for some tools?
- **Escalation paths.** If this seat can reach other tools or other agents, can it do things its
  own permission mode forbids? Consider MCP servers, sub-agents, shell, and web access.
- **`_safe_cwd`** — meant to stop a write-capable session being pointed at a home, system or
  credential directory. Does it hold up against descendants, symlinks, case differences and
  drive-relative paths?
- **The prompt path.** The prompt is passed as a command-line argument with a 25,000-character cap.
  Is that safe on this platform? What happens with unusual characters?
- **Effective-model reporting.** The footer reports a `brain`. Can it be wrong or spoofed? Why
  would that matter to a shop that decides review independence by vendor?
- **Error handling and the spend/audit path** — can a failed call look like a successful one?
- Anything else genuinely wrong.

## Rules

- Report only defects you can point at in real code or real documented behaviour.
- Say what you VERIFIED and how (name the command or source). Say what you could not verify.
- Do not pad. "None found" is a valid answer for a category.

## Deliverable

Numbered findings, most severe first. Each: **severity** (CRITICAL / HIGH / MEDIUM / LOW) ·
location · what is wrong · why it matters · a concrete fix.

Then: a **VERIFIED** section (what you checked and how) and a verdict line
**SHIP** / **SHIP-WITH-FIXES** / **REWORK**, signed with your exact model name.
