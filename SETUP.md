# ADD — Setup: bring the arsenal online

Anderson's Dispatch Deck runs from **Claude Code** (the home CLI). The other three
vendors are separate CLIs you install and log into once; then Claude dispatches to them
headlessly. This is the install + auth + gotcha guide, plus a reachability probe so the
orchestrator knows what's actually online.

> Platform note: paths/commands below are Windows (the reference rig). Adapt for macOS/Linux.

---

## 0. Claude Code (the conductor) — already your home base
This is the CLI you're reading this in. It's the orchestrator; everything else hangs off
it. Nothing to install for ADD itself beyond dropping the `/dispatch` skill in
`~/.claude/skills/dispatch/`.

## 1. Codex (OpenAI) — the precise builder + sharpest reviewer
- **Install:** the OpenAI Codex CLI (npm or the official installer).
- **Auth:** log in with a ChatGPT/OpenAI plan (separate plan → its usage does NOT touch
  your Claude/Anthropic meter).
- **Dispatch pattern:** `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`
- **GOTCHAS (learned the hard way):**
  - **Store/MSIX PowerShell kills it.** If your PowerShell is the Microsoft-Store (MSIX)
    build, Codex can't spawn a shell (CreateProcessAsUserW err 5). Fix: install real
    PowerShell from the **GitHub MSI** (not winget — winget reinstalls the MSIX), via
    elevated msiexec.
  - **OS-sandbox ACL bug** on some boxes → use the `--sandbox danger-full-access` lane
    (the working one). Add a `Bash(codex*)` allow-rule for hands-free dispatch.
  - **Always close stdin** headless (`< /dev/null`), or it hangs.
  - One clean goal per ticket — it refuses messy multi-fix tickets.

## 2. Grok (xAI) — the artist
- **Install:** the Grok CLI (lands at e.g. `C:\Users\<you>\.grok\bin\grok.exe`).
- **Auth:** log in with a **Super Grok / X Premium+** subscription (OIDC, no API key;
  token in `~/.grok/auth.json`).
- **Dispatch pattern:** `"<full path>\grok.exe" --prompt-file <file> --always-approve < /dev/null`
  (or `-p "<prompt>"`).
- **GOTCHAS:**
  - **Not on the tool-shell PATH** even when it's on your normal PATH — always use the
    FULL path when dispatching from an automation shell.
  - UI/art surface only ("reskins, doesn't rewire"). Require a trail-log entry per job.
  - Allow-rule for hands-free: `Bash("C:\Users\<you>\.grok\bin\grok.exe"*)`.

## 3. Gemini / Antigravity (Google) — the value powerhouse + image gen
- **Install:** `irm https://antigravity.google/cli/install.ps1 | iex` → `agy` at
  `C:\Users\<you>\AppData\Local\agy\bin\agy.exe`.
- **Auth:** log in with a **Google AI Pro** subscription. Do NOT chase the free "Login
  with Google" individuals OAuth — Google retired it (IneligibleTierError); Antigravity is
  the living path. *(Pricing/promos change over time — that's a current detail, not a
  requirement of the method. ADD treats every vendor as optional; use what you have.)*
- **Dispatch pattern:** `"<...>\agy.exe" -p "<prompt>" --model "Gemini 3.5 Flash (High)"`
  - Models under the sub: Gemini 3.5 Flash (Low/Med/High) · Gemini 3.1 Pro (Low/High) ·
    Claude Sonnet 4.6 · Claude Opus 4.6 · GPT-OSS 120B.
  - **Image gen (Nano Banana):** ask it to generate an image — runs on the SUB (no card
    needed); output lands in `~/.gemini/antigravity-cli/brain/<uuid>/*.jpg`.
- **GOTCHAS:**
  - Headless `-p` auto-denies external TOOL use (but writes to its brain dir + makes
    images fine). For code review, embed the code in the prompt.
  - The free AI-Studio KEY path 429s on images (no billing) — the SUB path does not.
  - ExecutionPolicy can block npm `.ps1` shims → `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## 4. Persistent seats (MCP) — wire the crew so it REMEMBERS

One-shot dispatches gave every seat amnesia: each call started from zero. The method now rigs
each vendor CLI into Claude Code as a **persistent MCP seat** — the orchestrator starts a
conversation with a seat, gets a session id back, and continues that exact conversation later
with full context. Same subscriptions, no API keys. **Opt-in, per vendor:** wire only the seats
you actually have and want — vendors are suggestions, and a missing one just isn't in the pool
(the method degrades loud, never demands a purchase). The orchestrator should OFFER this wiring
when it spots a CLI ("you have Gemini — want it persistent instead of amnesia one-shots?"), not
install it unasked. Registration is user-scope only, touches nothing else in your setup, and one
`claude mcp remove <name>` undoes it. Once a seat is wired, persistent is its default transport.

Full instructions, the wrapper scripts, the acceptance test, and the transport doctrine live in
**[`mcp-seats/README.md`](mcp-seats/README.md)**. The short version:

```bash
# Codex — MCP server mode is built in (Windows: codex.cmd if plain codex isn't found)
claude mcp add --scope user codex -- codex mcp-server
# Grok — bundled stdlib wrapper
claude mcp add --scope user grok -- python <repo>\mcp-seats\wmw_grok_mcp.py
# Gemini / Antigravity — bundled stdlib wrapper
claude mcp add --scope user gemini -- python <repo>\mcp-seats\wmw_gemini_mcp.py
```

Restart Claude Code (new MCP tools only appear in fresh sessions), confirm `claude mcp list`
shows each seat `✔ Connected`, then run the codeword acceptance test from the README per seat.
The wrappers also fix the two classic headless croaks: a 60-minute timeout (Antigravity's
default was 5) and an `always_approve` switch for build tickets (headless runs can't click
permission prompts). Two laws ride the transport: **reviewers are ALWAYS fresh calls** (a fresh
call is blind — exactly what independent review requires), and **a reply-chained session stays
in its owning-seat lineage forever** (it can never review work its thread touched).

---

## The reachability probe — what's online right now?
The orchestrator runs this (or its equivalent) at the start of a session and declares the
LIVE arsenal. Only dispatch to what actually answers. **Probe the default transport first:**
`claude mcp list` must show each wired seat Connected (and its tools present in THIS session —
they only appear in sessions started after registration); the CLI `--version` checks below prove
only the fallback lane. The arsenal declaration names which transport each seat answered on
(SPINE v2.0, transport law #4).

```bash
# Codex
codex --version 2>/dev/null && echo "CODEX: online" || echo "CODEX: missing (see §1)"
# Grok (use the real path)
"$HOME/.grok/bin/grok.exe" --version 2>/dev/null && echo "GROK: online" || echo "GROK: missing (see §2)"
# Gemini / Antigravity
"$LOCALAPPDATA/agy/bin/agy.exe" --version 2>/dev/null && echo "GEMINI: online" || echo "GEMINI: missing (see §3)"
# Claude is the host — always online (it's running this).
```

The orchestrator then states, plainly: *"Arsenal online: 🟠 Claude · 🔵 Codex · ⚫ Grok ·
🟢 Gemini. Ready."* — or names what's missing and points at the section above. A model
that isn't installed simply isn't in the dispatch pool for that session; the method
degrades gracefully (fewer weapons, same discipline). If NO cross-vendor reviewer is
reachable, say so — unreviewed work is never reported as done.
