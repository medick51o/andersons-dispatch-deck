<div align="center">

# ⚫➤ Anderson's Dispatch Deck

### **cursor-v2** — the Cursor edition

Heavy multi-model agentic orchestration — conducted from **one Cursor chat**.

**⚫➤ conducts. 🟣 Composer builds. Everybody else is a specialist.**

`•` no persona `•` no theater `•` right-model-right-job `•` honest review `•` meter-aware

[![branch](https://img.shields.io/badge/branch-cursor--v2-FFD100?style=for-the-badge)](https://github.com/medick51o/andersons-dispatch-deck/tree/cursor-v2)
[![status](https://img.shields.io/badge/status-in_progress-ff6b00?style=for-the-badge)](https://github.com/medick51o/andersons-dispatch-deck/tree/cursor-v2)
[![main](https://img.shields.io/badge/CLI_trunk-main-111111?style=for-the-badge)](https://github.com/medick51o/andersons-dispatch-deck)

</div>

> **You are on the Cursor branch.** The main talker is **⚫➤** — Grok inside Cursor, not Claude in a terminal.
> The original Claude-CLI deck still lives on [`main`](https://github.com/medick51o/andersons-dispatch-deck).
> Same engine ([`SPINE.md`](SPINE.md)). New seats. More landing in the coming days.

---

## What it is

Most people talk to one AI. **ADD treats models as a toolbox with a foreman.**

In Cursor, that foreman is **⚫➤** (this Grok chat). It reads the job, fences the files, sends the work to the model that's actually best for it, gets a *different* line to look at the result, runs the gates, and reports back in plain language.

No four terminals. No "it works." No theater.

It's the straight-faced sibling of *Team Rocket Takes Over*: same engineering spine, none of the show.

---

## How a job flows *(this branch)*

```mermaid
flowchart TD
    H([👑 Human — the mission]) --> O{{⚫➤ Orchestrator · Cursor Grok<br/>plan → fence → route}}
    O -->|bounded build| P[🟣 Composer]
    O -->|architecture / hard judgment| C[🟠 Claude]
    O -->|sharp code review| X[🔵 GPT / Codex]
    O -->|first-class cheap / overflow| M[🟢 Gemini 3.7 Flash]
    P --> R{{Review — never the builder's own vendor}}
    C --> R
    X --> R
    M --> R
    R -->|findings + fixes| O
    R -->|clean| GT[✅ Gates — evidence, not vibes]
    GT --> D([👑 Human rules & merges])
```

---

## The arsenal *(Cursor edition)*

| | Seat | Best at | Dispatch it for |
|:--:|---|---|---|
| ⚫➤ | **Grok** *(this Cursor chat)* | conducting the deck | plan · fence · Gate-0 · the one talking to you. Parallel Grok Tasks wear this same badge and **cannot** review it |
| 🟣 | **Composer 2.5** | fast, bounded builds | tickets the conductor fenced — **never** the main talker, **never** independent review of Grok |
| 🟠 | **Claude** | deepest reasoning | architecture · specs · hard judgment — **not** daily conductor in Cursor |
| 🔵 | **GPT-5.6 Sol / Codex** | precise builds; the review that *proves* bugs | code review of work it did **not** build |
| 🟢 | **Gemini 3.7 Flash** | first-class speed + an independent vote | real work + cheap honest reads — **not a spare tire** |

Two harnesses, one method:

| Harness | When | Who pays |
|---|---|---|
| **Cursor-native** | daily drive inside this IDE | Cursor Models (Grok + Composer) · Other Models only when you *name* them |
| **CLI overflow** | you explicitly want Claude Max / Codex / `agy` / Grok CLI | those subscriptions — not the Cursor meter |

### Reading a run

Seat first, act second. Building is the hammer. Reviewing is a **red dot on the seat**. Reject is a stop — never another red dot.

| You see | It means |
|---|---|
| 🟣🔨 | Composer is building |
| **🔵🔴** | Codex is **reviewing** |
| **🔵🔴→⛔** | Codex reviewed, then **rejected** |
| 🟠🔴 | Claude is reviewing |
| 🟢🔴 | Gemini is reviewing |
| 🟣🔴 | Composer verification (check, not cross-vendor) |
| 👥 | Council in session |
| 🧪 | Gates running |

---

## The rules that make it trustworthy

1. **A reviewer never wears the builder's own vendor.** Grok cannot review Grok. Composer verifying Grok is a **check**, not cross-vendor independence.
2. **Right model for the job — and cost-aware.** The deck reads the plan before it spawns anyone. No surprise Claude on a $20 tank.
3. **The banner never lies.** If the shop is Grok + Composer only, it says **solo-vendor degraded** — it does not print "full cross-vendor."
4. **Findings ship fixes.** Reviews land at checkpoints and never freeze the build.
5. **Gates before "done."** *"Gates pass."* Never *"it works."* The human is the final merge.
6. **No unasked fleets.** A two-line ask is one seat. A council is a special move, and it **asks first**.

---

## Status

This branch is the Cursor reseat. The method is proven; the Cursor wardrobe is being written now.

- [x] Branch cut from the public deck
- [x] Seats named: ⚫➤ conducts · 🟣 Composer · Gemini 3.7 first-class
- [x] Review = red dot on the seat (**🔵🔴**). Reject = **⛔**. Council = **👥** (🟣 is Composer)
- [ ] Skill rewrite (`SKILL.md` + Cursor-native guide)
- [ ] Dual-harness switch (`cursor` · `cli` · `off`) without the wrong-meter oops
- [ ] Console + dispatch guide updated for this wardrobe

Star the repo, switch the branch dropdown to **`cursor-v2`**, and watch it grow.

---

## Quick start *(today)*

**Claude CLI trunk** (stable, on `main`):

1. Install the vendor CLIs you want — see [`SETUP.md`](SETUP.md). All optional; Claude alone is a valid, degraded deck.
2. Drop [`SKILL.md`](SKILL.md) **and** [`SPINE.md`](SPINE.md) into `~/.claude/skills/dispatch/`.
3. Run **`/dispatch`**.

**Cursor edition** (this branch — landing now):

1. Stay in Cursor. This chat is already **⚫➤**.
2. The Cursor skill lives with your user skills (`dispatch on` / `/dispatch`).
3. Don't switch the model picker to "be" Claude. Dispatch Claude as a worker, or don't.

---

## In this repo

| File | What |
|---|---|
| [`SKILL.md`](SKILL.md) | loader — Claude-CLI trunk today; Cursor rewrite coming on this branch |
| [`SPINE.md`](SPINE.md) | **the shared engine** — same one TRM and TRTO run |
| [`SETUP.md`](SETUP.md) | install · auth · gotchas |
| [`FIELD-NOTES.md`](FIELD-NOTES.md) | proven capabilities a fresh install inherits |
| [`MODEL-DISPATCH-GUIDE.md`](MODEL-DISPATCH-GUIDE.md) | who-to-send-where (CLI wardrobe; Cursor guide coming) |
| [`dispatch-console.html`](dispatch-console.html) | color-coded visual quick-reference |

---

## Part of a family

Same engine underneath; the other tiers add personality:

| Tier | Repo | What you get |
|---|---|---|
| ⚫➤ **Anderson's Dispatch Deck** *(you're here)* | this repo · branch **`cursor-v2`** | Cursor Grok conducts · 🟣 Composer builds · straight-faced |
| 🟡 **ADD · CLI trunk** | [`main`](https://github.com/medick51o/andersons-dispatch-deck) | Claude conducts from the terminal |
| 🟠 **Team Rocket Method** | **[→ team-rocket-method](https://github.com/medick51o/team-rocket-method)** | SPINE + a permanent crew |
| 🚀 **Team Rocket Takes Over** | **[→ team-rocket-takes-over](https://github.com/medick51o/team-rocket-takes-over)** | SPINE + crew + the full show |

---

<div align="center">

*Reserved future rebrand: **Agentic Dispatch Director** (also ADD).*

Built with heavy AI collaboration, and honest about it.
The value is the **method**: the roles stay; the models are the costumes.

**Share this branch:** [github.com/medick51o/andersons-dispatch-deck/tree/cursor-v2](https://github.com/medick51o/andersons-dispatch-deck/tree/cursor-v2)

</div>
