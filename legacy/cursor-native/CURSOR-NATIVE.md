# ADD — Cursor-native arsenal (frugal)

Built-in models only. No `claude.exe`, `agy.exe`, `grok.exe`, or Codex plugin unless the boss names a CLI.

**Current plan file:** `C:\Users\<you>\.cursor\cursor-plan`  
**Live posture (2026-08-21):** `pro-20` — Cursor **Pro $20**. Other Models included = **$20**. Soak **Cursor Models** (Grok + Composer). Do not "practice ADD" by lighting Claude/GPT.

## Plan ladder (the boss's, not a recommendation to spend)

| Step | Plan | Other Models included | What this deck may spend without asking |
|---|---|---|---|
| **Now** | Pro $20 | **$20** | ⚫➤ this chat · 🟣 Composer. Other Models **parked**. |
| Next | Pro Plus $60 | **$70** | Same default. Named Claude/GPT/Gemini OK for a *single* review when he asks. Still no councils. |
| If he likes it | Ultra $200 | **$400** | Meter-aware ADD: Composer/Grok build; Claude/GPT for architecture + independent review. Council still ask-first. |
| After Ultra | BYOK / provider APIs | bills Anthropic/OpenAI/Google directly | Overflow only. He sets keys; this agent does not cancel subs or paste keys. |

Watch both pools: https://cursor.com/dashboard/usage

| Pool | What burns it | Wrap |
|---|---|---|
| **Cursor Models** | This Grok chat, Grok subagents, Composer 2.5 | **♾️ … ♾️** |
| **Other Models** | Claude, GPT, Gemini at API rates inside Cursor | **💸 … 💸** |
| **Vendor API / empty tank** | Anthropic invoice, ChatGPT recharge, BYOK — **only when known** | **🚨💳 … 🚨💳** |
| **CLI sub** | `claude.exe` / `codex` / `agy` / `grok.exe` already paid | **♾️ … ♾️** |

## Task slugs this harness may actually send

Do not invent slugs. If a requested model is not in this table, skip it and say so.

| Color | Seat | Slug | Pool | Independent of this Grok conductor? |
|---|---|---|---|---|
| ⚫➤ | Orchestrator | this chat (`inherit`) | Cursor Models | — |
| ⚫➤ | Grok overflow | `cursor-grok-4.6-xhigh-fast` or `cursor-grok-4.5-high-fast` | Cursor Models | **No** — same badge, same vendor |
| 🟣 | Composer | `composer-2.5-fast` | Cursor Models | Cursor first-party, not xAI. Weak independence vs Grok. On `pro-20` this is the only extra builder. |
| 🟠 | Claude | `claude-opus-5-thinking-high` | Other Models | Yes. **Ask first** on Pro / Pro Plus. |
| 🔵 | GPT (Codex-shaped) | `gpt-5.6-sol-medium` | Other Models | Yes. Banner: **GPT-5.6 Sol**. **Ask first** on Pro / Pro Plus. |
| 🟢 | Gemini 3.7 Flash | `gemini-3.7-flash-high` | Other Models | Yes. First-class seat (not a spare tire). Still **ask first** on `pro-20`. |
| 🟢 | Gemini heavier | `gemini-3.1-pro` | Other Models | Yes. Ask first. |

## Fit by posture

**`pro-20` / `pro-plus` default (SHOESTRING):** build in ⚫➤ or 🟣. Independent review = **declare degraded** (🟣 reviewing ⚫➤ is not cross-vendor) unless he names an Other Models seat. Never a council.

**`ultra` default (CRUISE):** architecture 🟠 · bounded build 🟣 · code review 🔵 if it did not build · extra vote 🟢 · UI ⚫➤. Council: propose cost, wait.

## Dispatch ledger (one line per spawn)

`YYYY-MM-DD HH:MM · color · slug · pool · wrap · job · files`

Narrate as: `🔵🔴 💸 reviewing parser 💸` — badges, then wrap, words, same wrap.

No spawn, no line. Guessing dollars is forbidden — dashboard only. Never use **🚨💳** unless the vendor bill is known.
