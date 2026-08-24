# THE BENCH LEDGER — 🟣➤ the Cursor reserve

*Wiring, not law. **SPINE v2.1 owns the rules** (THE NOTATION v4.1 · reserve-seat doctrine); this
file records what the reserve can reach, what it costs, and what it has actually proven. Roster
verified live 2026-08-23 against `cursor-agent models` (204 ids). Meter classes verified the same day
against Cursor's published pricing. Re-probe before any summon: this file claims "was available on
the verified date," never "is available."*

## THE FIRST FACT — two pools, not one

Cursor Pro is **not** one bucket of models. It is two, and confusing them is how a flat-rate shop
starts paying per token:

| Pool | Mark | What's in it | Cost |
|---|---|---|---|
| **Cursor Models** | ♾️ | `composer-*` · `cursor-grok-*` — Cursor's OWN models | **Included.** "Generous included usage." The pool people vibe-code with all day. |
| **Other Models** | 💸 | `claude-*` · `gpt-*` · `gemini-*` · `kimi-*` · `glm-*` | **Charged at the model's API price.** ~$20/month included, then pay-as-you-go. |
| *(unrecognised / `auto`)* | ⚠️ | anything else | **Fails closed** — never summoned. |

**"Fast" is a surcharge, not a speed-up.** Composer 2.5 goes **$0.5/$2.5 → $3/$15** per million on
Fast (6× the output rate); Cursor Grok 4.6 doubles ($2/$6 → $4/$12). Fast variants get their own
louder mark so they can never be picked up by accident.

**Enforced in code, not prose:** `wmw-cursor` refuses any 💸 or ⚠️ model unless the call passes
`spend_credits: true`. The free door is always open; the paid door needs a deliberate hand.

## A · ♾️ THE FREE BENCH — summon at will

**Exactly 16 of the 204 ids are free** (8 standard + 8 fast-surcharged). Everything else is metered.
The complete free list, verified 2026-08-23 — there is nothing else:

```
composer-2.5                    <- the default door
cursor-grok-4.6-low / -medium / -high / -xhigh
cursor-grok-4.5-low / -medium / -high
   ...plus a -fast twin of each (♾️💸 surcharged: 2-6x, deliberate use only)
```

Full generated classification of all 204: `docs/cursor-pool-classified.md`.

| Model | Mark | Lineage | Good for | Verified | Track record |
|---|---|---|---|---|---|
| `composer-2.5` **(default)** | 🟣➤🎼 ♾️ | Cursor | Bounded mechanical sweeps, scratch builds, fast bounded tickets; **seated on the council** (free + a bloodline the house lacks) | 2026-08-23 live | 6 dispatches — 4.7s cold / 2.1s resumed; correctly refused a write under `--mode ask`; executed a scoped build ticket to spec and verified before inventing a flag; answered a plan-economics question candidly against its own vendor's interest |
| `cursor-grok-4.6-high` | 🟣➤⚫ ♾️ | xAI | Hands-on coding agent; multi-file implementation | 2026-08-23 live | 4 dispatches — matched the house Grok CLI's CRITICAL finding on a real security review when given equal permissions, in 2.4x less time. *(Correction 2026-08-23: its "jointly trained by Cursor and SpaceXAI" self-description was logged here as a false claim; it is Cursor's own documented wording. The model was right, the ledger was wrong.)* |
| `cursor-grok-4.5-*` | 🟣➤⚫ ♾️ | xAI | Older tier; no reason to prefer it over 4.6 | 2026-08-23 live | *(none)* |
| `composer-2.5-fast` · `cursor-grok-*-fast` | 🟣➤ ♾️💸 | Cursor / xAI | **Only** when latency is the actual requirement | 2026-08-23 live | *(none)* — 2–6× surcharge, choose deliberately |

⚠️ **Lineage note:** `cursor-grok-*` is **xAI blood** — the same vendor as your house ⚫ Grok seat.
It can never independently review Grok-built work.

## B · 💸 THE CREDIT BENCH — asked, never assumed

Billed at API prices against the third-party pool. Each of these needs `spend_credits: true`.

| Family | Mark | Lineage | NEW blood? | Good for | Track record |
|---|---|---|---|---|---|
| `kimi-k3` (low·high·max) | 🟣➤🌙 💸 | Moonshot | **YES** | Long independent reviews; scoped build/fix/verify; retros and doc sweeps | 2 dispatches — self-assessed with unusual honesty, refused to invent a version number, named its own weaknesses unprompted |
| `kimi-k2.7-code` | 🟣➤🌙 💸 | Moonshot | **YES** | Code-shaped work on the same foreign blood | *(none)* |
| `glm-5.2` (high·max) | 🟣➤🔷 💸 | Zhipu | **YES** | A genuinely foreign tie-break when a house council splits | 1 dispatch — terse, accepted terms, offered no argument |
| `claude-*` (88 ids, incl. **1M** tiers) | 🟣➤🟠 💸 | Anthropic | no — **mirror** | A 1M-context ceiling the house genuinely lacks. **Capacity routing only, never an independent read of Claude work** | *(none)* |
| `gpt-*` (83 ids, incl. **1M** Sol/Luna/Terra) | 🟣➤🔵 💸 | OpenAI | no — **mirror** | Same: context ceiling or window relief vs 🔵 Codex | *(none)* |
| `gemini-*` (10 ids) | 🟣➤🟢 💸 | Google | no — **mirror** | Window relief vs 🟢 Gemini | *(none)* |
| `auto` | ⚠️ | **UNKNOWN** | — | **Never.** May route anywhere; unknown lineage fails closed | — |

**Only three families in 204 ids are blood the house doesn't already own: Kimi, GLM, and Composer.**
Everything else is your own bloodlines wearing a meter. That is the whole honest case for the bench.

## C · How to read this ledger

- **`lineage` is the only column that decides independence.** No row → no cast. A mirror may never
  review its own vendor's work; the 🟣➤🟠 banner makes that visible at a glance.
- **Track-record cells stay empty until a real dispatch fills them.** No dispatch, no reputation —
  "good for" is a hypothesis until receipts say otherwise. Never run a dispatch just to fill a row.
- **Staleness:** any row unverified >60 days is ADVISORY and must be re-probed before a summon.
- **Refresh events, and only these three:** the weekly lineage review · after a real bench dispatch ·
  when a summon's live probe disagrees with this file. Never a sweep to "keep it fresh."
- Raw roster: `docs/cursor-pool-raw.txt` (204 ids, 2026-08-23).

## D · The orchestrator's foreknowledge card

At a decision point, offer ONE line. Free options may simply be used; paid options must be asked.

| Situation | Reach for | Cost |
|---|---|---|
| Bounded mechanical sweep, scratch build, quick bounded ticket | `composer-2.5` | ♾️ free — just use it |
| A coding agent to grind a multi-file implementation | `cursor-grok-4.6-high` | ♾️ free — but xAI blood, can't review Grok's work |
| A long review, or a genuinely foreign lens | `kimi-k3-high` | 💸 **ask first** |
| House council split, want a foreign tie-break | `glm-5.2-high` or `kimi-k3-max` | 💸 **ask first** |
| A packet no house seat can hold in one context | a 1M tier (`claude-opus-5-thinking-high`, `gpt-5.6-sol-high`) | 💸 **ask first** — capacity only, NOT an independent read |
| Anything else | **the house seat** | ♾️ already paid, already clears the bar |
