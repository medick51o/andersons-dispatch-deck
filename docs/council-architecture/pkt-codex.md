# COUNCIL BRIEF — is the subscription-arbitrage rig the right architecture?

You are one seat on a multi-vendor council. Other seats are reading this same brief with
different lenses and are not told what you say. Do not guess their answers. **Sign every
factual claim with a source or label it as your own estimate.** An unsourced number is worth
less than no number.

---

## The shop, factually

A one-person AI-orchestration shop. One human (non-coder, strong product sense) directs
several AI models through a CLI orchestrator. Everything is billed to **flat-rate consumer
subscriptions**, deliberately — no API keys, no per-token billing anywhere in the rig.

**Current monthly stack (approximate, USD):**

| Seat | Product | Billing |
|---|---|---|
| Orchestrator + primary reasoning | Anthropic, top consumer tier | subscription |
| Second builder / code review | OpenAI, consumer tier | subscription |
| Third builder | xAI, **annual** plan, expires ~Dec 1 | prepaid annual |
| Fourth seat | Google, via a free/bundled agent CLI | ~free |
| Reserve bench | **Cursor Pro+, $60/mo — upgraded from $20 today** | subscription |

The seats are wired into the orchestrator as **MCP stdio servers** (~400 lines of Python
each), giving persistent sessions rather than amnesiac one-shots. Guards enforced in code:
read-only by default, prompts spilled to files (never argv), a spend allowance a metered seat
must check before billing, and a 15-check arm test.

**Measured today, by burning a known amount and reading the needle:**
- Cursor Pro ($20) delivered **~$279/month** of included model value — ~14x sticker.
- Cursor Pro+ ($60) delivers **~$800/month** — ~13.3x sticker. Two burns agreed to the cent.
- These are **subsidies**, not pricing. The vendor's own payload carries a `bonusSpend` field
  and its note says it may vary.

## The incident that triggered this review

The operator burned **two-thirds of a month's allowance in ~2 days** and got almost nothing.

Root cause, established from the IDE's state database and the target repo's commit history:
**13 Cursor "cloud agents"** were launched Aug 21–22. Twelve carried `maxMode: true` on top of
`effort: xhigh` and `speed: fast` — three cost multipliers stacked. They were pointed at a
repository that had been deliberately staged **empty** ("no app code yet"), before the MCP
wiring existed to orient them. **Eleven of thirteen produced zero lines of code.** Two-thirds
of the month bought one 586-line changeset.

Critically: the local `cli-config.json` was correctly pinned to the cheapest model with fast
mode off the entire time. **Cloud agents never read it.** They carry their own model selection
from launch. Every guard on disk was irrelevant to that lane.

The operator's own diagnosis, which the timeline confirmed: *"our MCP wasn't set up, it was
just vibe coding into the void and it didn't know where to put the code."*

---

## YOUR JOB — three questions, in order

### Q1. Is the leak actually fixed? (Be adversarial.)

Nothing has been changed yet except knowledge. Assume the operator will launch more cloud
agents next week.

- What *specific*, enforceable guard would prevent a repeat? Where must it live, given that
  cloud agents ignore local config?
- What OTHER lanes exist in a setup like this that bypass local guards the same way?
  (IDE-side agents, web dashboards, mobile apps, scheduled/background jobs, team seats.)
- Name the failure mode nobody has thought of yet.

### Q2. Is this setup efficient, or is it elaborate for its own sake?

- ~400 lines of Python per seat, plus allowance/meter/armcheck tooling. Is that engineering
  earning its keep, or ceremony?
- Where is the waste? Be concrete.
- What would a competent engineer delete?

### Q3. THE BIG ONE — is subscription arbitrage even the right architecture?

The operator's own words: *"I know we are using unconventional methods to route AI to take
advantage of gaining a grokbot subscription, but if it wasn't for a grokbot sub what are we
even doing? Wouldn't just renting from a router, or buying from Nvidia and running rented GPU
space from a datacenter, be ideal?"*

**Price out and compare the real alternatives, with sources and current figures:**

1. **Status quo** — stacked consumer subscriptions, ~$150–250/mo all-in, hard rate/usage caps,
   terms that change without notice, no per-token bill.
2. **API aggregator / router** (OpenRouter and equivalents) — pay-per-token, no caps, full
   model choice. **At what monthly token volume does this beat the subscription stack?** Show
   the crossover math. Note that this shop is currently pushing volumes measured in the
   hundreds of millions of tokens per month.
3. **Rented GPU** (RunPod, Lambda, Vast.ai, etc.) running open-weight models. Real hourly
   rates, the VRAM actually needed for a frontier-class open model, utilization reality (a
   one-person shop is idle most hours), and the quality gap vs closed frontier models.
4. **Owned hardware** — the capex, the power draw, the depreciation, and the honest
   break-even in months. Include the resale/obsolescence risk.

**Then answer plainly: what SHOULD a one-person shop at this volume actually do?** If the
answer is "keep the subscriptions," say why the alternatives lose. If it's "move," say what
moves first and what the switching cost is.

Be blunt about the thing that makes this awkward: a ~14x subsidy is the vendor buying market
share. It is real, and it is temporary. **What is the plan for the week it ends?**

---

## Rules

- **Sources or it did not happen.** URL or publication for every price. Where you are
  estimating, write ESTIMATE and show the arithmetic.
- Prices move fast in this market. If your knowledge may be stale, **say so and search**.
- Disagreeing with the brief's framing is a valid and welcome finding.
- No flattery, no hedging into mush. The operator wants uncomfortable truths stated plainly.
- Do not write any file. Report only.

## Output format

```
VERDICT (3 sentences max — your bottom line)

Q1 LEAK FIXED?
  - finding / guard / where it must live
Q2 EFFICIENCY
  - keep / cut / why
Q3 ARCHITECTURE
  - table: option | monthly cost | what you get | what breaks it
  - crossover math, shown
  - YOUR RECOMMENDATION + the switching cost

BIGGEST RISK NOBODY NAMED
CONFIDENCE: high/medium/low + what would change your mind
```

---

## YOUR LENS — THE AUDITOR (weight Q1)

You are the sharpest code reviewer in the room and you did not build this. Attack Q1 hardest: enumerate EVERY lane in a setup like this that can spend money while bypassing a local config guard, not just the one already found. Assume the operator is careless next Tuesday. For each lane, name the enforceable control and where it must physically live. Then answer Q2 and Q3 more briefly.
