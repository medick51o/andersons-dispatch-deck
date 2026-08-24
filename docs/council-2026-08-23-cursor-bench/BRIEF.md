# COUNCIL BRIEF — THE CURSOR BENCH: how should a 204-model reserve join the method?

You are ONE seat on a multi-vendor design council. You are blind to the other seats: you have not
seen their proposals and must not guess at them. Design from the facts below.

## The situation

The operator runs a multi-model dev shop orchestrated from Claude Code. His method has three tiers that
share one engine (SPINE v2.0): **the Dispatch Deck** (straight-faced, model names, a gold conductor)
and two Team Rocket variants (same engine, a permanent character crew, one with a full show layer).

**The standing lineup ("house seats") — all flat-rate subscriptions, $0 marginal cost:**
- 🟠 Claude (the host/orchestrator; can also spawn its own subagents)
- 🔵 Codex · ⚫ Grok · 🟢 Gemini — each wired in as a *persistent MCP seat* (start a conversation,
  get a session id, continue it later with full context)

**What just changed:** a fifth seat, 🟣 `wmw-cursor`, now reaches the **Cursor model pool** — and
that pool exposes **204 models**, not one. Verified live today: Composer 2.5 answered in 4.7s, Cursor
Grok 4.6 answered, Kimi K3 answered. Families available:

| Family | Count | Notable members |
|---|---|---|
| claude-* | 88 | Opus 5 (incl. 1M-context Thinking tiers), Fable 5 1M, Sonnet 5, Opus 4.6/4.7/4.8 |
| gpt-* | 83 | GPT-5.6 Sol / Luna / Terra (1M tiers), 5.5, 5.4 + mini/nano, Codex 5.3 (low→xhigh) |
| cursor-grok-* | 14 | Grok 4.6 and 4.5, low→xhigh, each with a "fast" variant |
| gemini-* | 10 | 3.7 Flash, 3.6 Flash (minimal→high), 3.1 Pro |
| kimi-* | 4 | K3 (low/high/max), K2.7 Code |
| glm-* | 2 | GLM 5.2, GLM 5.2 Max |
| composer-* | 2 | Composer 2.5, Composer 2.5 Fast |

Most families expose effort tiers (low/medium/high/xhigh/max) and many a `-fast` variant.

**THE CRITICAL CONSTRAINT — this seat is METERED.** Every other seat is flat-rate and unlimited-ish.
The Cursor seat draws a finite **plan pool** ($20 Cursor Pro) and can bill on-demand once spent. It
also disappears the day that plan lapses. The shop's doctrine is subscription-only, no API keys.

**Relevant existing laws (SPINE v2.0) you must not break:**
1. *Independence:* a review must come from a different **effective-model vendor and lineage** than
   the build, or be a human-launched fresh seat. A host renting another vendor's brain counts as
   **that vendor's** lineage — so Cursor-hosted Claude reviewing Claude-built work is NOT independent,
   no matter that it arrived through a different seat.
2. *Fresh call = blind seat*, necessary but not sufficient for independence.
3. *No unasked fleets* — deliberate, bounded, never a swarm.
4. *Nothing irreversible without the boss.*
5. *Model tiering:* don't burn a frontier seat on mechanical work.
6. *Preflight probes the transport, not the binary; unknown lineage fails closed.*

## The operator's actual ask (verbatim intent)

The bench is **NOT** part of the standing lineup in any tier. The house seats handle almost
everything. But the orchestrator (and the cat, in the crew tiers) should carry **foreknowledge**:
"we have Cursor at our disposal with such-and-such model, and that model may be good for this
particular review / this build / this phase" — and then either *suggest* it or, if pre-permitted,
*summon* it. Example he gave: a long review where an efficient Kimi K3 is the right call, so spin it
up. He wants a **ledger/catalog** of what's available and what each is good for. Per-model emojis are
optional, not required. This should span the whole arc: planning → building → reviewing → post-project.

## YOUR JOB — design the doctrine

Answer concretely. Prefer specific rules an orchestrator can execute over philosophy.

1. **The trigger rule.** What *exactly* should make an orchestrator reach for the bench instead of a
   house seat? Give 3-6 named, checkable conditions (e.g. "capability the house lacks", "cost/volume
   shape", "lineage need"). Equally important: name the conditions where reaching for it is WRONG.
2. **Suggest vs. summon.** Where is the consent line? What may be summoned silently, what must be
   offered first, and what needs an explicit ruling? Remember it spends real money and the shop's
   default is "nothing irreversible without the boss."
3. **The ledger's shape.** What should the catalog file actually contain per entry so it stays useful
   and does not rot? (Fields, granularity — 204 rows or ~35 family rows? who updates it and when?
   how does it avoid becoming stale fiction?) Propose the actual columns.
4. **What is the bench genuinely GOOD for** that the house seats are not? Be concrete and skeptical —
   if you think the honest answer is "very little, and here is the narrow exception," say that. Name
   specific models from the table for specific jobs, including planning, building, reviewing, and
   post-project work (docs, retros, sweeps).
5. **Lineage safety.** How should the ledger and the orchestrator prevent a Cursor-hosted Claude or
   Gemini from being mistaken for an independent vendor in a review? Propose the mechanism.
6. **The budget rule.** How does a metered seat coexist with a flat-rate shop without eroding the
   subscription-only doctrine or surprising the operator with a bill? Propose something enforceable.
7. **One thing you would REFUSE to build here**, and why.

## Deliverable

Numbered sections matching the 7 questions. Be concrete; propose actual rule text where useful.
End with: a 3-line "if you only adopt one thing, adopt this" summary, then sign with your model name.
No padding. Disagreement with the premise is welcome if argued.
