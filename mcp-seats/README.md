# mcp-seats — persistent vendor seats for the method

*The method's models are crew, not vending machines. This folder rigs every vendor CLI into
Claude Code as a **persistent MCP seat**: the orchestrator starts a conversation with a seat,
gets a session id back, and can continue that exact conversation later with full context. No
more amnesia one-shots where the seat forgets everything between dispatches. Everything rides
the subscriptions you already pay — no API keys, no per-token bills.*

## What you get

| Seat | Server name | Start tool | Continue tool |
|---|---|---|---|
| Codex (OpenAI) | `codex` | `codex` | `codex-reply` + conversationId |
| Grok (xAI) | `grok` | `grok` | `grok-reply` + sessionId |
| Gemini (Google, via Antigravity) | `gemini` | `gemini` | `gemini-reply` + conversationId |

Server names are yours to choose at registration — this shop prefixes them with its machine name
(`wmw-grok`), you don't have to.

## Install

**Prereqs:** each vendor's CLI installed and logged in to your subscription. Verify before wiring:
`codex --version` · `grok --version` · `agy --version` (Antigravity). Wire only the seats you have —
the method degrades loud, not silent, when a vendor is missing.

**1 · Codex — one command** (its MCP server mode is built in):

```
claude mcp add --scope user codex -- codex mcp-server
```

(Windows: use `codex.cmd` if plain `codex` isn't found.)

**2 · Grok** — uses the bundled wrapper `wmw_grok_mcp.py` (stdlib-only Python, no dependencies):

```
claude mcp add --scope user grok -- python <path-to-this-folder>\wmw_grok_mcp.py
```

**3 · Gemini / Antigravity** — bundled wrapper `wmw_gemini_mcp.py`:

```
claude mcp add --scope user gemini -- python <path-to-this-folder>\wmw_gemini_mcp.py
```

**4 · Restart Claude Code.** New MCP tools only appear in fresh sessions. Then check
`claude mcp list` shows every seat `✔ Connected`.

## Acceptance test (run it before trusting a seat)

The codeword test, per seat: call the start tool with *"My codeword is REDHAWK. Reply with exactly:
STORED"*, take the session id from the reply footer, call the continue tool asking *"What is my
codeword?"* **PASS = the codeword comes back.** That proves real persistence, not a fresh session
wearing the same name.

## Why the wrappers exist (and what they quietly fix)

Codex ships an MCP server; Grok Build and Antigravity don't — but both have headless modes and
session resume, so a ~150-line stdlib wrapper closes the gap. The wrappers also bake in two fixes
for the classic "the seat croaked mid-task" failures of headless dispatching:

- **60-minute timeout** — Antigravity's headless default is 5 minutes; any longer task died mid-thought.
- **`always_approve` switch** — a headless run can never click a tool-permission prompt; without
  this flag a build task stalls on an unanswerable prompt until the timeout executes it. Pass
  `always_approve: true` on build tickets (with `cwd` pointed at the repo); omit it for read-only
  research and review work.

Adapting a wrapper to a NEW vendor CLI: only three parts change — the exe finder, the command-line
flags (headless flag, resume flag, JSON output flag), and the output parsing. The MCP plumbing at
the bottom never changes.

## Transport doctrine (the method's laws, applied to these tools)

- **Fresh call = blind seat.** A new start-tool call remembers nothing from any other session —
  exactly what council and review seats require. Reviewers are ALWAYS fresh calls; never brief a
  reviewer through a session that saw the build.
- **Reply-chain = the same seat continuing.** Use the continue tool for follow-ups inside one
  seat's owned lane. A reply-chained session stays in its owning-seat lineage forever — it can
  never become the independent reviewer of work its thread touched.
- Raw one-shots (`grok -p`, `codex exec`, `agy -p`) remain legal fallback transport; the
  persistent seats are the default.
