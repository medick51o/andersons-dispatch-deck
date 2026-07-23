<div align="center">

# 🟡 Anderson's Dispatch Deck

### Heavy multi-model agentic orchestration — conducted from a single chat window.

**One conductor. Four AI vendors. Zero terminal-juggling.**

Claude · Codex · Grok · Gemini — dispatched to their strengths, reviewed across vendors,
gated, and reported plainly. The powerhouse, straight-faced.

`•` no persona `•` no theater `•` right-model-right-job `•` honest cross-vendor review `•` cost-aware

</div>

---

## What it is

Most people talk to one AI. **ADD treats models as a toolbox with a foreman.** A single
orchestrator — **Claude by default, because most of us drive the Claude CLI** — runs the conductor role
(it wears **gold** 🟡, above the players; the seat is *model-agnostic* — a Codex-first shop puts Codex in
gold and Claude in support). It reads each job, sends it to the model that's actually best for it, has a
*different* vendor review the result, runs the gates, and reports back. No four
terminals, no guessing, no drift.

It's the straight-faced sibling of *Team Rocket Takes Over*: same engineering spine,
none of the show.

## How a job flows

```mermaid
flowchart TD
    H([👑 Human — the mission]) --> O{{🟡 Orchestrator · Claude by default<br/>plan → fence → route}}
    O -->|deep logic / architecture| C[🟠 Claude]
    O -->|bounded build| X[🔵 Codex]
    O -->|UI / skins / art| G[⚫ Grok]
    O -->|images / cheap / overflow| M[🟢 Gemini]
    C --> R{{Cross-vendor review<br/>never the builder's own vendor}}
    X --> R
    G --> R
    M --> R
    R -->|findings + fixes| O
    R -->|clean| GT[✅ Gates — evidence, not vibes]
    GT --> D([👑 Human rules & merges])
```

## The arsenal

| | Model | Best at | Dispatch it for |
|:--:|---|---|---|
| 🟠 | **Claude** (Anthropic) | deepest reasoning, architecture, honest judgment | design & specs · root-cause · engine-grade logic · reviewing others |
| 🔵 | **Codex** (OpenAI) | precise builds; the sharpest code review (*proves* bugs) | bounded implementation · reviewing Claude/Grok/Gemini code |
| ⚫ | **Grok** (xAI) | fearless one-shot visual design | UI · skins · concept pages · "make it feel like X" |
| 🟢 | **Gemini** (Google / Antigravity) | budget builder · **image gen (Nano Banana)** · overflow capacity | real builds · renders · cheap sweeps · an independent 4th vote |

## The rules that make it trustworthy

1. **A reviewer never wears the builder's own vendor.** Cross-vendor, or it's just a mirror — different training, different blind spots, real catches.
2. **Right model for the job — and cost-aware.** Dispatch weighs the meter, not just capability (heavy Claude work can fail over to a cheaper lane and keep going).
3. **The banner never lies.** When a model wears a borrowed brain, both are shown (`🟠🟢`).
4. **Findings ship fixes.** Every review finding carries a suggested fix; reviews land at checkpoints and never stop the build.
5. **Gates before "done."** Claims capped at evidence — *"gates pass,"* never *"it works."* The human is the final gate and the only one who merges.
6. **No unasked fleets.** Multi-agent dispatch is deliberate and bounded, never a swarm.

## The Council — every vendor, one question

For a call that has to be *right* — a design fork, a decision, a claim that must survive scrutiny — the Deck convenes **the council**: it dispatches the same question to **every reachable vendor at once**, each handed a distinct lens (correctness · cost · *refute-it*), gathers the independent reads, synthesizes best-of-breed with **every disagreement named**, caps the debate at two rounds, and hands you the verdict. Four vendors mean four sets of blind spots — the special move for when one model's read isn't enough. No cast, no theater: just the panel, reported by model name. It's **stakes-gated** — a two-line ask (*"rewrite this email," "did I send the PO"*) is handled by one seat, **never** a council. *(Same engine move as TRM's crew council and TRTO's set-piece — here it's straight-faced.)*

## In this repo

| File | What |
|---|---|
| [`SKILL.md`](SKILL.md) | the `/dispatch` loader — drop it **+ [`SPINE.md`](SPINE.md)** into a Claude CLI and Claude becomes the conductor |
| [`SPINE.md`](SPINE.md) | **the shared engine** — the whole method, brand-neutral; the *same* SPINE that TRM and TRTO run |
| [`SETUP.md`](SETUP.md) | install · auth · gotchas · the reachability probe |
| [`FIELD-NOTES.md`](FIELD-NOTES.md) | proven capabilities a fresh install inherits (so it doesn't re-learn what's already known) |
| [`MODEL-DISPATCH-GUIDE.md`](MODEL-DISPATCH-GUIDE.md) | the deep who-to-send-where playbook |
| [`dispatch-console.html`](dispatch-console.html) | a color-coded visual quick-reference |

## Quick start

1. Install the vendor CLIs you want in the arsenal (see [`SETUP.md`](SETUP.md)) — **all are
   optional; Claude alone is a valid, degraded deck.**
2. Drop [`SKILL.md`](SKILL.md) **and [`SPINE.md`](SPINE.md)** into `~/.claude/skills/dispatch/`.
3. In a Claude CLI, run **`/dispatch`** (or just say *"run the dispatch deck"*). It probes
   what's online, declares the live arsenal, and asks for the job.

## Part of a family — try the other tiers

ADD is the straight-faced tier. Same engine underneath; two siblings add personality — **worth a look:**

| Tier | Repo | What you get |
|---|---|---|
| 🟡 **Anderson's Dispatch Deck** *(you're here)* | this repo | the engine, straight-faced — model names, no cast |
| 🟠 **Team Rocket Method** | **[→ team-rocket-method](https://github.com/medick51o/team-rocket-method)** | SPINE + a permanent crew — named seats, adversarial cross-reviews |
| 🚀 **Team Rocket Takes Over** | **[→ team-rocket-takes-over](https://github.com/medick51o/team-rocket-takes-over)** | SPINE + crew + the full show — the agentic-AI playground, cast & cat |

Promote up the tiers when you want more personality; the discipline underneath is identical.

---

## Lineage

ADD grew from the **Team Rocket Method (TRM)** — the original two-model-shop discipline —
and is the *straight-faced* cut of its playful successor, *Team Rocket Takes Over*. It keeps
the engineering (fenced tickets, cross-vendor review, gates, decision batching) and drops
the persona. Credit to TRM as the trunk this branch grew from. 🫡

---

<div align="center">

*Reserved future rebrand: **Agentic Dispatch Director** (also ADD).*

Built with heavy AI collaboration, and honest about it — that's the house rule.
The value is the **method**: vendor-proof, because the roles are permanent and the models
are just the costumes they wear.

</div>
