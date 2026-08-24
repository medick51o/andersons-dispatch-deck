# COUNCIL SYNTHESIS — is subscription arbitrage the right architecture?

**Convened 2026-08-24 by boss order. Cap set in advance: 5 seats, 5 distinct lineages.**
Reported: ⚫ Grok (xAI) · 🎼 Composer (Cursor) · 🌙 Kimi K3 (Moonshot) · 🟢 Gemini (Google).
🔵 Codex (OpenAI) reported last; its amendment is section 7, and it REFUTED the headline fix.

Each seat read the same brief with a different lens, blind to the others.

---

## 1. UNANIMOUS — the leak is NOT fixed

All five seats, independently and without hedging. **Knowledge is not a control plane.** Nothing
enforceable has changed since the incident; the next cloud-agent launch repeats it.

They also converged on *why no file can ever fix it*, stated most cleanly by Kimi:

> *"Anything that executes on the vendor's infrastructure is governed by the vendor's settings,
> not yours. A guard that the guarded system cannot see is decoration."*

### CORRECTION — the first proposed fix does not work

Grok's spend-fuse recommendation was published below and then **refuted by Codex**, whose
objection the operator's own dashboard confirms:

> **"A vendor-side hard overage limit protects cash but does not protect the prepaid monthly
> allowance; an agent can still destroy the included pool without charging another dollar.
> The required control is a usage/concurrency cap or feature disablement, not merely $0
> overage."** — Codex

**The incident proves him right.** The billing page for the burn window reads
`On-Demand Usage (Aug 21 - Aug 24): $0.00`. Thirteen cloud agents consumed 51.9M tokens and
two-thirds of the month **entirely inside the included pool, with on-demand at zero the whole
time.** Setting on-demand to $0 would not have prevented a single one of them. Grok's premise
that "Cloud Agents require on-demand to launch" is contradicted by this shop's own data.

**Ruling: the $0 fuse is a CASH backstop, not an allowance guard.** Set it anyway, it is free
and caps the tail risk of an uncapped overage bill, but do not mistake it for the fix.

**The actual control is to disable the cloud-agent lane, or gate it behind a remote policy that
caps concurrency and forbids the expensive modes.** Codex: *"a checklist, local hook, or
dashboard alert is not a guard."*

### The fix that was proposed first, and why it looked right

⚫ Grok found the one control that sits on the lane the money actually travels:

> **Cursor dashboard → Spending. Set on-demand OFF, or on with a $0 (or ~$10 fuse) limit.**
> Cursor's own docs: when the limit is hit, AI features stop until the next cycle.
> **Cloud Agents require on-demand to launch.** It is the only control they cannot ignore,
> because it lives on *Cursor's* billing plane.
> — cursor.com/help/account-and-billing/spend-limits

Everything else proposed is secondary: a pre-flight that refuses to launch against an empty
write-set, a cap on concurrent agents, and never stacking `maxMode` + `effort:xhigh` +
`speed:fast`.

### Other lanes that bypass local guards the same way (pooled, deduped)

Cursor IDE agent mode · the web dashboard launcher · the mobile app · Bugbot on PRs ·
scheduled/background agents · ChatGPT scheduled tasks and Codex cloud · Claude in the browser
(as distinct from the local CLI) · Grok Build / Grok Bot cloud · Gemini's 24/7 cloud agent ·
direct vendor CLI calls made outside MCP · team seats, where a non-admin can lift the cap if
"only admins can edit usage settings" is off.

### Two failure modes nobody had named

- **On-demand auto-continue** (Grok): once the included pool empties, a single earlier "yes"
  silently turns the next agent swarm into an uncapped metered bill.
- **Long-context re-billing** (Grok): on Grok and Gemini, crossing 200k tokens reprices the
  **entire request** at roughly 2x. This will manufacture a fake "volume crisis" if mix is
  not watched.
- **The vendor draws the needle** (Kimi): every usage figure in the rig is vendor-reported.
  `bonusSpend` can be halved silently and the meter would calmly report the worse reality as
  normal. There is no independent meter anywhere.

---

## 2. THE BIG QUESTION — subs vs API vs rented GPU vs owned iron

**3 of 4 say KEEP THE SUBSCRIPTIONS. 4 of 4 say NO GPU.**

Gemini dissented toward "move background agents to API now," but see §4 — its pricing was
stale, and the one seat with live web access reached the opposite conclusion on better data.

### Live pricing (⚫ Grok, official pages, fetched 24 Aug 2026)

Blended at a 70/30 input/output split, on this shop's estimated model mix:

| | blended $/M tokens |
|---|---:|
| Claude Opus 5 | $11.00 |
| GPT-5.6 Sol (promo, ends ~21 Nov) | $8.80 |
| Grok 4.6 | $3.20 |
| DeepSeek V4-Flash | $0.18 |
| **Estimated shop mix** | **$7.04** (+5.5% via OpenRouter = $7.42) |

### Crossover against the ~$205/mo subscription stack

| Monthly volume | API at shop mix | Opus-only | Grok-only | Subscriptions |
|---|---:|---:|---:|---|
| 100M | **$704** | $1,100 | $320 | $205 |
| 500M | **$3,518** | $5,500 | $1,600 | *cannot deliver* |
| 1B | **$7,035** | $11,000 | $3,200 | *cannot deliver* |

Break-even is **~29M tokens/month**. This shop is far past it — which is exactly why the
subscription stack wins on price and loses on *capacity*. Grok's framing: **the cap, not the
sticker, is the binding constraint.**

### GPUs — the answer to a different question

> *"You cannot rent 'Opus 5' as a GPU."* — ⚫ Grok

- Frontier open weights (DeepSeek V3.2, 671B FP8) need ~700 GB → **8× H200**; an 8×H100 node
  does not even fit it. 24/7 on Vast: **~$21,197/mo**.
- A single H100 running a 70B at 4 h/day is ~$239/mo — *if you remember to stop the pod.*
- Owned RTX 5090 (~$3,000 all-in, 575W) vs renting: **~81-month break-even** against a card
  with an 18–24 month useful life. **It never buys itself back.**
- Quality gap: best open API scores Intelligence Index 52 vs Opus 5 at 63, Grok 4.6 at 61.
- Self-hosting DeepSeek-class only beats DeepSeek's own API at ~831–933M tokens **per day**.

**Verdict: the "rent GPUs from a datacenter" instinct answers a real question — serving open
weights at high utilization. That is not this shop's job.** This shop directs frontier *closed*
models, burstily, with one human. GPUs cannot run them at any price.

---

## 3. THE DEEPEST FINDING — 🌙 Kimi

Assigned to argue *against* the current architecture, Kimi could not do it honestly on the
math — and then found something better:

> **"The rig optimizes the vendor's metric, not the shop's.** Every guard measures spend
> against an allowance the vendor defines and reports. Nothing measures cost per accepted line
> of shipped product. So the shop can be perfectly 'efficient' — 13x subsidy captured! — while
> producing 586 lines a month. A business that meters its inputs and not its outputs will
> optimize its way into buying very cheap nothing."

The Aug 21–22 incident is precisely that: the failure was caught by the needle, never by the
output. 🎼 Composer reached the same place from the engineering side:

> *"~1,400 lines of seat code protect orchestrator dispatch; $0 of code protects cloud-agent
> launch. Guards are ~95% theater against last week's actual threat."*

**The missing instrument is cost-per-accepted-change.** It would have caught the incident in
hours instead of days, and no vendor will ever build it.

---

## 4. WHERE THE SEATS DISAGREED, AND HOW IT RESOLVED

🟢 **Gemini** alone recommended moving background agents to pay-per-token immediately, calling
the stack *"a fragile temporary hack on ToS loopholes."*

Its reasoning on ToS was sound and is retained below. **Its pricing was not.** It quoted
"Claude 3.5 Sonnet at $3/$15", "DeepSeek R1", and a "Mac Studio M2 Ultra" — all superseded —
while presenting them with source URLs as if freshly fetched. Composer and Kimi both stated
plainly that they could not reach the web and labeled every figure ESTIMATE. Gemini did not.

**Ruling: on price, Grok's live-fetched figures govern. Gemini's strategic risk analysis
stands; its numbers do not.** The disagreement dissolves once the real prices are used —
at $7.04/M blended, moving background agents to API costs more, not less.

*This is itself a finding about the rig: a seat that cannot search will answer from memory and
may not tell you. Web-capability must be verified per seat before a research council, not
assumed.*

---

## 5. THE RISK EVERY SEAT NAMED — Terms of Service

Three of four independently put ToS at the top, and Grok supplied the precedent:

> **Anthropic cut Pro/Max off from third-party agent harnesses (OpenClaw-class) on 4 Apr 2026**
> — a single OpenClaw day was costing them $1k–$5k of API value. An MCP stdio wrapper around a
> consumer CLI is the same pattern.

Kimi's addition: an enforcement action is **correlated** — four consumer seats wrapped the same
way can die on the same afternoon, with no SLA and no appeal queue a one-person shop can wait in.

**This is the actual reason to keep a warm API lane** — not price. Price says stay.

---

## 6. WHAT THE COUNCIL SAYS TO DO, IN ORDER

1. **Set the Cursor spend fuse today.** On-demand off, or limit $0/$10. The only guard the
   cloud lane traverses. *(Grok, echoed by Kimi and Composer.)*
2. **Open a metered API account with a $50 hard cap and leave it cold.** Do not route
   production through it. It is the overflow valve for the week the subsidy ends, and the
   thing that makes an enforcement action survivable rather than fatal. *(3 of 4 seats.)*
3. **Build cost-per-accepted-change.** The one instrument the rig lacks, and the only one that
   measures the shop's own metric instead of the vendor's. *(Kimi, Composer.)*
4. **Renew the xAI annual monthly, not annually**, until the ToS and subsidy picture stabilizes.
   *(Grok.)*
5. **Do not buy or rent GPUs.** Unanimous.
6. **Watch `bonusSpend` weekly.** The subsidy will *creep* — 13x → 8x → 4x — not cliff. Composer:
   *"the bankruptcy is slow and looks like 'Cursor got worse,' not 'architecture failed.'"*
   Pre-commit the API lane before the ratio hits 3x.

## What would change the answer

- Claude Code itself being pulled from Max the way OpenClaw was.
- `bonusSpend` reaching 1x — at which point Pro+ is $70 of included value for $60, still
  rational, but the arbitrage is over and Pro at $20 plus metered overflow may beat it.
- 30 days of audited logs showing >80% uncached frontier tokens, which would push the API
  column toward $11/M and make the stack even more cap-bound.

---

## 7. AMENDMENT — the fifth seat, Codex (OpenAI)

Codex arrived last and changed two things materially.

**It refuted the headline fix** (see the correction in section 1). That refutation is the single
most valuable output of this council: without it the operator would have set a $0 overage limit,
believed the leak sealed, and been wrong.

**It expanded the bypass inventory from ~10 lanes to ~15**, adding the ones a one-person shop
would never think of:

- **WSL, containers, remote workstations, SSH hosts, VMs** — each a separate enforcement domain
  that can hold copied credentials and none of the local guards.
- **Plugins, MCP tools, nested agents, tool-spawned subprocesses** — a permitted agent can
  recursively open another metered lane. This shop already proved that class of escalation on
  2026-08-23, when a read-only Grok seat wrote a file *through* the Codex seat.
- **OAuth tokens, copied browser sessions, old devices** — revoking a local config revokes
  nothing that already exists elsewhere.
- **Automatic model fallback / Max escalation / vendor-side retries** — a cheap launch can
  silently become expensive if routing changes or the chosen model is unavailable.
- **Crash recovery, duplicate delivery, auto-resume** — a job can run twice on one click.

**Its "biggest risk nobody named" is a real race, and it explains the incident's shape better
than anything else offered:**

> **Concurrent allowance oversubscription — a time-of-check/time-of-use race.** Thirteen
> launches can each read the same apparently-available balance before delayed vendor telemetry
> records any of them. Every launch passes its check; their combined commitment exceeds the
> month. *"A meter that merely rereads bonusSpend cannot prevent this race."*

Thirteen agents were launched. Thirteen is the number in the incident. The fix is an **atomic
reservation before dispatch** — worst-case cost reserved per job, one active lease, no child
launch without a sub-reservation, reconciliation afterward.

**It also demoted this shop's allowance tool honestly:** `allowance.py` cannot be called
enforcement unless every credential and all outbound traffic pass through it. It is
**telemetry**. Keep it for reconciliation and alerts; drop any claim that it prevents overspend.

Codex's own pricing was blocked by its sandbox — it said so plainly and labeled everything
ESTIMATE. Its Sonnet-class blended figure of **$5.70/M including OpenRouter's 5.5% fee**, with
crossover at **26-44M tokens/month**, lands close to Grok's live-fetched **$7.04/M and 29M**:
two seats, different sources, same conclusion. On owned hardware it was blunter than anyone —
**$42,260 of capex is a 211-month break-even against a $200/month stack, and you still would
not have Claude.**

### Final tally across five seats

| | Leak fixed? | Subs vs API | GPU? |
|---|---|---|---|
| Grok | NO | keep subs | no |
| Composer | NO | keep subs | no |
| Kimi | NO | keep subs, as a bridge | no |
| Gemini | NO | move background agents *(stale prices)* | no |
| Codex | NO | keep subs, restrict to attended work | no |

**5/5 the leak is not fixed. 5/5 no GPU. 4/5 keep the subscriptions**, and the lone dissent
rests on superseded pricing that live data contradicts.

Codex's framing is the one to keep:

> *"The ~14x subsidy is the vendor buying adoption. Refusing it would be economically
> irrational, while designing the business to require it would be operationally reckless."*
