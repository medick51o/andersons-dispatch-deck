
# The Model Dispatch Guide — who to send where

**Purpose (boss-commissioned 2026-07-17):** so the orchestrator (the cat / whatever
Claude is driving) ALREADY KNOWS which model to dispatch for which job on any future
project — no re-discovery. Consult this at project start. Core law it rests on:
**characters are permanent, models are wardrobes** — so this guide is about the MODELS
(the tools); the characters (Jessie/James/Butch/Cassidy/the cat) just wear them.

---

## 🟠 CLAUDE (Anthropic) — the brain + the orchestrator
**Characters:** 😼 the cat (orchestrator, usually Fable) · 🟠 Jessie (builder) · 🔴 Butch (reviewer).
**Strengths:** deepest multi-file reasoning, architecture, spec-writing, root-cause
debugging, tricky/tangled logic, adversarial review, and honest judgment — it FLAGS its
assumptions instead of hiding them ("I bounded this to 2/3 because the engine only means
2/3 — ruling queued"). Best narrator/orchestrator.
**Dispatch for:** the orchestration itself · architecture & design calls · specs · engine
surgery · root-cause hunts · hard multi-file changes · reviewing other vendors' work.
**Watch-out:** the expensive seat — ration it; watch the weekly meter. TIER IT:
- **Fable** = specs, review, orchestration, conversation (heavyweight; the cat's default).
- **Sonnet** = code + research sub-agents (the workhorse for builds).
- **Haiku** = mechanical (gate re-runs, log mining, builds). the boss watches the counter.
**Mechanism:** it's the HOME CLI (Claude Code). Sub-agents via the Agent tool. This is the
one window everything else hangs off.

## 🔵 CODEX (OpenAI / ChatGPT) — the precision builder + sharpest reviewer
**Characters:** 🔵 James (builder) · 🩷 Cassidy (reviewer).
**Strengths:** disciplined, exact implementation of a clear spec (no drift) · the SHARPEST
static/adversarial code review in the shop — it doesn't just claim a bug, it PROVES it
(raw-socket-forges the bad input, shows it break) · validation-matrix / edge-case thinking.
**Dispatch for:** bounded implementation of a clear fenced ticket · cross-vendor code
review (esp. Cassidy reviewing Claude-built work) · security/validation passes.
**Watch-out:** wants ONE clean goal per ticket (refuses messy multi-fix tickets) · runs on
a SEPARATE plan → costs the Claude meter $0 (great default builder for budget) · headless
needs stdin closed.
**Mechanism:** `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`
(the danger-full-access lane is the working one on the Anderson box — its OS-sandbox ACL
bug is upstream; boss blessed a `Bash(codex*)` allow rule). Embed code IN the prompt for
reviews (reviews-by-embed) when file access is flaky.

## ⚫ GROK (xAI) — the fearless artist
**Characters:** cat-driven ⚫ (or a 🫡 Wobbuffet skit); it's a wardrobe, not a permanent character.
**Strengths:** fearless one-shot visual design — hand it a VIBE, get back a world · UI/UX,
skins, concept/vision pages, demo-mode storytelling · fast · leaves a signed lineage trail.
**Dispatch for:** UI face-lifts · concept/vision HTML · skins & art direction · "make it
feel like a starship" · anything with a screen and a mood.
**Watch-out:** UI SURFACE ONLY — "Grok reskins, it does not rewire"; keep it off engine
logic · gate for platform ceilings (e.g. WebKit-16 for the old iPad) · mandatory
GROK-TRAIL.md entry per job for lineage.
**Mechanism:** `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <file> --always-approve < /dev/null`
(NOTE: `grok` is on PATH in a normal shell but NOT in the tool's bash — use the full path).

## 🟢 GEMINI / ANTIGRAVITY (Google) — the value powerhouse (the biggest find)
**Characters:** cat-driven 🟢 for builds/art · 🟠🟢 Jessie fronts when it wears a Claude
brain (Overflow Valve) · 🔵 James fronts its reviews of Claude-built work. Wardrobe, not a
permanent character (yet).
**Strengths (proven 2026-07-17, exceeded expectations):**
- **A real BUILDER, not just a reviewer** — Flash 3.5 one-shot a premium Flydigi Vader 4
  Pro GPV (live gamepad API, trigger bars, tension-ring detail it added unprompted).
  Strong comprehension (inferred "GPV = Game Pad Viewer" from 3 letters).
- **IMAGE GENERATION via Nano Banana** — asked to "use Nano Banana 2," it PIVOTED from
  code to image gen and wrote a real 656KB photoreal JPEG. **Runs on the $4.99 AI Pro SUB
  with the credit card OFF = zero per-image cost.** (The free AI-Studio-KEY path 429s on
  images; the SUB path does NOT. Different doors.) This is the shop's art-generation engine.
- **Cheap Flash tier** for wide sweeps, cold reviews, mechanical passes (its first-ever
  review caught 3 real threading bugs).
- **A different gene pool** — a genuine independent 4th vote when the bench is split.
- **The Overflow Valve** — its wardrobe includes Claude Sonnet 4.6, Claude Opus 4.6, and
  GPT-OSS 120B, all billed to Google. When the Claude weekly meter runs hot, move heavy
  work here — some still wearing a Claude brain — on the $4.99 tab.
**Dispatch for:** real builds (Flash) · IMAGE gen (skins art, mascots, concept renders via
Nano Banana) · cheap cold reviews / sweeps · overflow capacity · a 4th independent opinion.
**Watch-out:** headless `-p` auto-denies external TOOL use (but it CAN write to its own
brain dir + generate images fine) · review-independence only counts when it runs a GEMINI
model (agy-wearing-Claude is NOT a second Claude opinion) · **promo $4.99/mo → $19.99
~mid-Oct 2026** (keep/cancel decision).
**Mechanism:** `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.5 Flash (High)"`
(tiers: Flash Low/Med/High, Gemini 3.1 Pro Low/High, Claude Sonnet/Opus 4.6, GPT-OSS 120B).
Generated images land in `C:\Users\<you>\.gemini\antigravity-cli\brain\<uuid>\*.jpg` — fish
them out from there.

---

## QUICK DECISION TABLE — "I need to ___ → send ___"
- **Architect / spec / hard root-cause** → 🟠 Claude (Fable).
- **Build a clear fenced spec, cheap** → 🔵 Codex (James) — $0 to Claude meter.
- **Build, mixed / when Codex is busy** → 🟢 Gemini Flash (proven builder) or 🟠 Claude Sonnet.
- **Review Claude-built code** → 🔵 Codex or 🟢 Gemini — never Claude reviewing itself.
- **Review Codex-built code** → 🟠 Claude — never Codex reviewing itself.
- **Review Grok/Gemini-built code** → 🔵 Codex (the sharpest code reviewer; catches Grok's
  UI-surface gaps) — or 🟠 Claude for architecture/design. Route the reviewer by the CODE'S
  TYPE + the cross-vendor rule; ANY model can build, Codex is the default code-reviewer
  whenever it didn't build the code, Claude reviews Codex + owns architecture review.
  (In ADD / no-character mode, say it by model+color; in Team Rocket mode, by character.)
- **UI / skins / concept pages / "make it cool"** → ⚫ Grok (cat-driven).
- **Generate an IMAGE (art, mascot, render)** → 🟢 Gemini Nano Banana (cat-driven, free on sub).
- **Wide sweep / log-mine / mechanical** → 🟢 Gemini Flash (cheap) or 🟠 Haiku.
- **Claude meter running hot** → 🟢 Overflow Valve: route Claude-grade work to the GREEN
  seat — either a real Claude brain on Antigravity (🟠🟢, Google's tab) OR Gemini's own top
  tier as a capable-if-lesser Claude stand-in (🟢). Dispatch is COST-AWARE, not just
  capability-aware — the orchestrator weighs the meter, not only the "best" model.
- **A true independent 4th vote** → 🟢 Gemini (real different lineage).

## THE IRON RULES (never break)
1. **A reviewer never wears the builder's own vendor.** Cross-vendor or it's just a mirror.
2. **Right model for the job** — the whole point; this table is the map.
3. **The banner never lies** — always show the real model under a worn wardrobe (🟠🟢 etc.).
