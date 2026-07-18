# Field Notes — proven capabilities (treat as KNOWN, don't re-discover)

**For the orchestrator reading this on a fresh install:** these are things the shop has
*proven with evidence*, not guesses. Trust them. You don't need the human to re-teach you
that Gemini can generate images or that Codex catches bugs — it's established. Act on it.
(This file is how the method carries its learnings forward: when something new is proven,
it gets committed here, and every future pull inherits the wisdom. The repo is the shared
brain; git is the "phone home.")

---

## Gemini / Antigravity — a first-class model, not a sidekick
- **It BUILDS.** Gemini 3.5 Flash one-shot a full, premium Flydigi Vader 4 Pro gamepad
  viewer (live Gamepad API, analog triggers, tension-ring detail it added unprompted) —
  strong comprehension (inferred "GPV = Game Pad Viewer" from three letters). Dispatch it
  for real builds, not just grunt work.
- **It generates IMAGES.** Asked to "use Nano Banana," it pivoted from code to image gen
  and produced a photoreal render — running on the Antigravity **subscription** (no billed
  API key needed; the free AI-Studio *key* path 429s on images, the *sub* path does not).
  Output lands in `~/.gemini/antigravity-cli/brain/<uuid>/*.jpg`. This is the shop's art
  engine — skins, mascots, concept renders.
- **It REVIEWS.** Its first cold review caught three real thread-lifecycle bugs. A genuine
  independent perspective (different gene pool) — a real 4th vote.
- **The Overflow Valve is real.** Its wardrobe includes Claude Sonnet/Opus and GPT-OSS, so
  it can carry Claude-grade work on Google's tab when the primary meter is hot.
- **Bottom line:** treat Gemini/Antigravity as a legitimate build/review/image model. It
  earned it.

## Codex (OpenAI) — the sharpest code reviewer
- Proves bugs instead of claiming them (opens a raw socket, forges the bad input, shows it
  break). Default code-reviewer whenever it didn't build the code. Precise, bounded builder.
  One clean goal per ticket.

## Grok (xAI) — fearless one-shot visual design
- Hand it a vibe, get a world. UI/skins/concept pages, fast. Surface only — it reskins,
  it doesn't rewire; route its code to Codex for correctness review.

## Claude (Anthropic) — the reasoner + the conductor
- Deepest multi-file reasoning, architecture, honest judgment (flags its own assumptions).
  The orchestrator role. Expensive — tier it (Fable / Sonnet / Haiku), watch the meter.

## Hard-won gotchas (so you don't relearn them)
- **Grok CLI** isn't on the automation-shell PATH even when it's on your normal PATH — use
  the full binary path when dispatching.
- **Codex + Store/MSIX PowerShell** = broken shell (err 5); needs real PowerShell (GitHub
  MSI). Use the `--sandbox danger-full-access` lane; close stdin (`< /dev/null`).
- **Antigravity headless `-p`** auto-denies external tool use, but writes to its own brain
  dir and generates images fine; embed code in the prompt for reviews.
- **The banner never lies** — if a model wears another's brain, show both (🟠🟢).
- **Reviewer never shares the builder's vendor.** Non-negotiable.

---

*Add to this file whenever the shop proves something new. That's the whole idea — the
method gets smarter every time someone teaches it, and everyone downstream inherits it.*
