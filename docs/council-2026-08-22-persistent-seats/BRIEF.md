# COUNCIL BRIEF — comprehensive review of the 2026-08-22 "Persistent Seats" update

You are ONE seat on a four-vendor review council. You are blind to the other seats: you have not
seen their findings and must not guess at them. Review the material on its own merits. Be
adversarial where your lens calls for it — a real finding with a fix is worth more than praise.

## What shipped (the work under review)

Commit `0cbaccf` on the PUBLIC repo github.com/medick51o/andersons-dispatch-deck (branch main),
plus companion edits to the private local method skills:

1. `mcp-seats/wmw_grok_mcp.py` — stdlib Python MCP stdio server wrapping the Grok Build CLI
   (tools: grok / grok-reply, session resume via --resume).
2. `mcp-seats/wmw_gemini_mcp.py` — same pattern wrapping the Antigravity CLI (`agy`)
   (tools: gemini / gemini-reply, resume via --conversation; bakes in a 60-min --print-timeout
   and a --dangerously-skip-permissions switch behind `always_approve`).
3. `mcp-seats/README.md` — portable install guide for strangers (register with
   `claude mcp add`, codeword acceptance test, transport doctrine).
4. `SETUP.md` §4 — persistent seats as a standing install step of the method.
5. `SKILL.md` — new PERSISTENT SEATS doctrine section + LEGEND v4.0 (conductor wears ➤; reviewing
   = 🔴 suffix on the seat; reject/blocked = ⛔; council = 🌈👥👥; no meter wrap on this trunk).
6. (Local, not pushed) `CREW.md` shared by TRM/TRTO: a persistent-seats block + the conductor-arrow
   law.

Purpose of the update: the method's vendor seats (Codex/Grok/Gemini) used to be amnesia one-shot
CLI dispatches; they are now persistent MCP conversations inside Claude Code. Two doctrine laws
ride the transport: a FRESH call is a blind seat (required for reviews); a REPLY-CHAINED session
stays in its owning-seat lineage forever (never reviews work its thread touched).

## Deliverable (exact format)

1. Numbered findings, most severe first. Each: **severity** (CRITICAL / MAJOR / MINOR / NIT) ·
   file + location · what is wrong · why it matters · a concrete suggested fix.
2. If you verified something works, say what you checked. If you could not verify, say so.
3. End with a verdict line: **SHIP** / **SHIP-WITH-FIXES** / **REWORK**, one sentence of rationale,
   and sign with your model name.

Do not pad. No findings in a category = say "none found."
