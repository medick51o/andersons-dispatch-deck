# Usage-pool research — as of 2026-08-23

Researched against live vendor pages on 2026-08-23. Where a vendor does **not** publish a number, this document says so. Community / anecdotal figures are labelled **REPORTED** and are not treated as facts.

Confidence labels:

- **OFFICIAL** — stated on a vendor page (x.ai, docs.x.ai, help.x.com, cursor.com, cursor.com/docs, cursor.com/help) on the fetch date.
- **REPORTED** — third-party, forum, Wayback, or staff-on-forum. Not a crawlable plan card.
- **UNKNOWN** — no public number exists.

---

## 1. How xAI actually meters (read this first)

Since June 2026, paid Grok plans no longer use per-product daily caps. Official FAQ:

> Instead of separate daily limits for each product (like Chat, Imagine, Voice, or Build), you get **one shared weekly usage pool** that you can spend however you like across any Grok product.

How it is shown: a **percentage used**, broken down by product (API, Build, Chat, Imagine, Voice). Different products consume different amounts of the pool because they cost different compute. A chat message uses little; a high-quality video or a long coding task uses far more. The reset date is in Settings → Usage.

When the weekly pool is exhausted: paid features pause until reset; free-tier Chat and Voice remain; you can buy Extra Usage Credits (web only, from $5, expire in one year, **higher cost per action than included usage**) or upgrade.

**xAI does not publish the size of that weekly pool in messages, tokens, or dollars for any consumer plan.** Guides that still quote “~100 prompts / 2 hours” or “~100 messages/day” are describing the **pre-June 2026** system, which the FAQ says was retired.

Source: https://docs.x.ai/grok/faq

---

## xAI / Grok plans

| Plan | Price | What the pool actually is (vendor units) | Source | Confidence |
|---|---|---|---|---|
| **X Premium+** (annual) | **$40/mo or $395/yr** on US web. Regional annual prices differ (e.g. UK £313/yr, many EUR countries €377/yr). | X’s own unit: “**higher limits on Grok**” than X Premium, which itself has “increased usage limits on Grok.” **No message/token/weekly-percentage number is published.** Premium+ also includes Grok **on grok.com** (X Help, for org/affiliate copy, calls this “access to SuperGrok, xAI’s Premium subscription for the Grok web and mobile app”). Grok Build is available to Premium+ (xAI launch post). Paid Grok usage, once on grok.com, is the **same weekly-percentage pool mechanism** as SuperGrok — **pool size vs SuperGrok $30 is not published.** These are **different billing products** (X vs xAI), not one shared bank account. | https://help.x.com/en/using-x/x-premium · https://help.x.com/en/using-x/x-premium-faq · https://x.ai/news/grok-build-cli · https://docs.x.ai/grok/faq | Price: **OFFICIAL**. Grok access: **OFFICIAL**. Pool size vs SuperGrok: **UNKNOWN**. Old 2-hour prompt counts: **REPORTED / stale**. |
| **SuperGrok** | **$30/month** (annual ~$300 / ~$25/mo is widely listed; x.ai/pricing card shows **$30/month**) | Official: “higher rate limits” + Grok 4.6, Expert, Imagine image/video, connectors. Usage = **one weekly compute-weighted pool**, shown as a **percentage**, shared across Chat / Imagine / Voice / **Build**. **No published count of messages, tokens, or percent-of-what.** Plus is described as having “significantly higher usage” than this tier, so this is the baseline paid pool. | https://x.ai/pricing · https://docs.x.ai/grok/faq | Price and metering model: **OFFICIAL**. Absolute pool size: **UNKNOWN**. |
| **SuperGrok Plus** | **$100/month** | Official card: everything in SuperGrok, plus **Grok Bot access**, 1080p video, “**significantly higher usage across Chat, Imagine, Voice & Build**,” faster replies, peak priority, early features. **No multiplier** (not “3x”, not a token budget). Same weekly-percentage pool, larger allowance. 720p video still has a **tier-specific cap** (FAQ: 720p falls back to 480p once you hit the cap; the cap number is unpublished). | https://x.ai/pricing · https://x.ai/bot · https://docs.x.ai/grok/faq | Feature list and “significantly higher”: **OFFICIAL**. How much higher in units: **UNKNOWN**. |
| **SuperGrok Heavy** | **$300/month** is the established list price (xAI launch coverage July 2025; still the figure used on grok.com checkout and aggregators). The 2026-08-23 crawl of x.ai/pricing **prints $30 and $100 on Individual cards** and lists Heavy in the compare grid **without a dollar figure in that HTML**. FAQ independently confirms Heavy exists and can be billed **yearly**. | Official compare/bot copy: highest usage, fastest speed, “solve extremely hard problems,” most powerful intelligence, dedicated support, early access, **Grok Bot**. Same weekly-percentage pool, maximum published wording. **No message/token number.** | https://x.ai/pricing · https://x.ai/bot · https://docs.x.ai/grok/faq · launch: https://www.teslarati.com/xai-launches-grok-4-supergrok-heavy-subscription-details/ | Plan existence + Bot + “highest usage”: **OFFICIAL**. $300 list: **REPORTED** against live card HTML (historically official at launch; still the market price). Pool size: **UNKNOWN**. |
| **Grok Build CLI** | Included on SuperGrok and X Premium+ (launch). Also on Plus/Heavy via “everything in SuperGrok.” | **Same weekly pool as grok.com Chat.** FAQ: one pool across “any Grok product”; Usage tab breakdown explicitly includes **Build**. Warp’s docs (integrating SuperGrok OAuth) describe the same: chat, Build, and subscription-routed API share the pool; Warp traffic shows under the **API** product label in grok.com Usage. Separate **prepaid API credits** on console.x.ai are a different product (non-refundable). | https://docs.x.ai/grok/faq · https://x.ai/news/grok-build-cli · https://docs.warp.dev/agents/inference/grok-subscription/ | Same pool as chat: **OFFICIAL**. Prepaid API credits ≠ subscription pool: **OFFICIAL**. |
| **Grok Bot** | No standalone Bot SKU. Included with **SuperGrok Plus, SuperGrok Heavy, Cursor Pro+, Cursor Ultra, Cursor Teams** (Standard and Premium seats). **Not** on basic SuperGrok $30. **Not** on Cursor Pro $20. SuperGrok Team/Enterprise **cannot** link. | Official: **weekly** included usage, then on-demand on the **Cursor** account. Metered **on Cursor, not on grok.com**. SuperGrok link is a **usage grant** onto a Cursor account. Qualifiers: Ultra / Heavy = “highest weekly usage”; Pro+ / Plus = “generous weekly usage, below Ultra/Heavy.” **No token, step, or dollar figure published.** Trial is a usage credit (agent steps + tokens), not a day count, with a 7-day window. | https://x.ai/bot · https://docs.x.ai/grok-bot/teams-and-enterprises · https://cursor.com/help/grok-bot/plans · https://cursor.com/help/grok-bot/supergrok-heavy | Who gets it: **OFFICIAL**. Weekly, Cursor-metered: **OFFICIAL**. Absolute allowance: **UNKNOWN**. |

### X Premium+ vs SuperGrok $30 — same pool or not?

**Not the same billing pool.** One is an X subscription; one is an xAI subscription. Linking an X account at grok.com Settings → Account lets xAI “retrieve your X subscription status and grant relevant benefits.”

**Feature access overlap (official):** both get Grok on grok.com/apps and Grok Build. X org help literally calls Premium+ “access to SuperGrok.”

**Pool size overlap (official):** unpublished. Anyone claiming “they are identical” or “SuperGrok is 3× Premium+” is using **anecdotal / pre-June** measurements, not a vendor table. Treat size comparison as **UNKNOWN**.

Stale REPORTED figures (do not use as current entitlements): Premium+ ~100 prompts / 2 hours; SuperGrok ~300+ / 2 hours; or SuperGrok ~100 messages/day. Those describe the old per-window caps.

---

## Cursor plans

Cursor uses **two monthly pools**, resetting with the billing cycle. Unused does not roll over.

| Plan | Price | Cursor Models pool (Composer, Cursor Grok) | Other Models pool | Grok Bot | Source | Confidence |
|---|---|---|---|---|---|---|
| **Pro** | **$20/mo** | **Not unlimited.** Official language: “**generous included usage**” / “generous First-party models pool” / marketing: “Generous limits for Grok.” Covers **Cursor Grok 4.6, Grok 4.5, and Composer 2.5** (standard + Fast variants). **No published token, request, or dollar cap** for this pool. It **can be exhausted**; then on-demand or wait for reset. Tab completions on paid plans are unlimited and outside this. | **$20 / month** of third-party models at each model’s API price. After that, on-demand at the same rates if enabled. Pricing page also says “Extended limits on Agent.” | **Not included.** | https://cursor.com/docs/models-and-pricing · https://cursor.com/help/models-and-usage/usage-limits · https://cursor.com/help/account-and-billing/pricing · https://cursor.com/pricing · https://cursor.com/help/grok-bot/plans | Dollar Other Models: **OFFICIAL**. Cursor Models = generous, finite, unpublished size: **OFFICIAL**. Grok Bot absent: **OFFICIAL**. |
| **Pro+** | **$60/mo** | Same official wording as Pro: “generous” Cursor Models / “Generous limits for Grok.” Docs **do not publish a larger Cursor Models number** for Pro+ vs Pro. Marketing “3x Pro limits on Agent” refers to the **Agent / Other Models** ladder, not a published Grok multiplier. | **$70 / month** (docs). Pricing page: “3x Pro limits on Agent.” $70 vs $20 is 3.5×; the “3x” is marketing rounding. | **Included.** “Generous weekly usage, below Ultra.” No token number. | same as above | Other Models $70: **OFFICIAL**. Cursor Models size vs Pro: **UNKNOWN** (same adjective). Bot: **OFFICIAL**. |
| **Ultra** | **$200/mo** | Again “generous” / “Generous limits for Grok” — **same phrase as Pro and Pro+.** No published extra Cursor-Grok allotment for Ultra. | **$400 / month.** Pricing page: “20x Pro limits on Agent.” $400 vs $20 is exactly 20×. | **Included.** “Highest weekly usage.” No token number. | same as above | Other Models $400: **OFFICIAL**. Cursor Models size vs Pro: **UNKNOWN**. Bot: **OFFICIAL**. |

### Cursor Grok vs Composer — same pool, different burn rate

**Same pool.** Official: “The Cursor Models pool includes Cursor Grok 4.6, Grok 4.5, and Composer 2.5.”

**Not the same consumption.** Cursor Start docs (the only place Cursor publishes a ratio): Grok 4.6 and 4.5 “draw from the same monthly pool as Composer 2.5, but consume usage faster. **Grok 4.5 consumes usage about 3× faster than Composer 2.5.**” That sentence is on the Start plan page; token list prices on the main pricing doc are consistent with Grok being several times more expensive per token than Composer:

| Model (Cursor Models) | Input / cache-read / output per 1M tokens |
|---|---|
| Composer 2.5 | $0.50 / $0.20 / $2.50 |
| Composer 2.5 Fast | $3 / $0.50 / $15 |
| Grok 4.6 / 4.5 | $2 / $0.50 / $6 |
| Grok 4.6 Fast | $4 / $1 / $12 |
| Grok 4.5 Fast | $4 / $1 / $18 |

**Fast is not a separate entitlement.** It is the same Cursor Models pool at a higher listed rate.

**Spillover (staff on forum, 2026-08-21):** Cursor Models is used first; when it is exhausted, Cursor Grok/Composer **continue from remaining Other Models dollars**. Named third-party models never draw Cursor Models. This spillover is **REPORTED** (Cursor staff on the forum), not written on the pricing page.

Sources: https://cursor.com/docs/models-and-pricing · https://cursor.com/help/account-and-billing/cursor-start · https://forum.cursor.com/t/possible-bug-in-cursor-token-statistics-other-models-disabled-after-grok-quota-exhausted/169032

### Grok Bot on Cursor

| Cursor plan | Grok Bot? | Official usage wording |
|---|---|---|
| Hobby / Pro | No | Upgrade or link SuperGrok Plus/Heavy |
| Pro+ | Yes | Generous weekly, below Ultra |
| Ultra | Yes | Highest weekly |
| Teams Standard / Premium | Yes, every seat | Follows the Teams seat allowance |
| Enterprise | Rolling out; AE enables | Admin-managed |

Linking SuperGrok Plus/Heavy grants **Grok Bot usage on the Cursor account**. It is **not** a Cursor plan change.

Source: https://cursor.com/help/grok-bot/plans · https://cursor.com/help/grok-bot/supergrok-heavy · https://docs.x.ai/grok-bot/teams-and-enterprises

---

## The cross-deal (question 10)

### What was real

**Direction: SuperGrok Heavy → Cursor Ultra at $0. Not the reverse.**

Cursor’s own help page, archived 2026-08-16:

> Qualifying customers receive **free Cursor Ultra created at $0**, which includes Grok Bot access. The subscription remains active at no charge so long as the SuperGrok Heavy plan is active on renewal.

Wayback: https://web.archive.org/web/20260816025546/https://cursor.com/help/grok-bot/supergrok-heavy

Cursor staff (deanrie) on 2026-08-15: the banner was the live offer; Ultra stayed active for as long as Heavy stayed active; the old “one month” help text was outdated. https://forum.cursor.com/t/free-cursor-ultra-with-grok/168286

Already-on-Ultra users got **nothing extra** (no stacked Ultra). Team accounts were ineligible. Reverse deal **never existed**: Cursor Ultra does **not** include a SuperGrok consumer subscription. Ultra includes **Grok Bot**, which is a different product.

### What is current (2026-08-23)

**The Ultra-at-$0 promo has ended for new links.**

- 2026-08-21: Cursor staff **Colin** posted that “the promotion including Cursor Ultra with SuperGrok Heavy has ended.” Existing Heavy users who **already claimed** Ultra keep it. Grok Bot remains available. https://forum.cursor.com/t/free-cursor-ultra-with-grok/168286?page=2
- Live docs now: linking is a **usage grant, not a Cursor plan**. “If you had no Cursor plan before linking, you still don’t.” “Linking SuperGrok does not swap you to Ultra.” https://cursor.com/help/grok-bot/supergrok-heavy · https://cursor.com/help/grok-bot/plans
- Cursor Billing, quoted by a customer on 2026-08-22: no published cutoff date/time/announcement; a **new** Heavy link adds Grok Bot only and **does not create Ultra**. https://forum.cursor.com/t/did-i-miss-an-announcement-on-supergrok-heavy-and-cursor-ultra/169128

**Grandfathering:** Colin said existing claimants keep Ultra. Some users report the $0 Ultra was later cancelled or never provisioned; that is account-level dispute, not a published rule.

**Honest status:** the Heavy→Ultra bundle **was** official, **is not** the current published offer, and there is **no** Ultra→SuperGrok reverse bundle.

---

## What is genuinely comparable, and what is not

Vendors do not publish in the same units. A cell-by-cell “who has more Grok” table would be invented precision.

**Comparable (same vendor, same unit):**

- Cursor **Other Models**: $20 / $70 / $400 per month at API rates. This is the only fully numeric, official individual allowance.
- Cursor Agent marketing multipliers: Pro 1×, Pro+ 3×, Ultra 20× — these track Other Models, not Cursor Grok.
- xAI **relative** wording: SuperGrok < Plus (“significantly higher”) < Heavy (“highest”). Plus and Heavy include Grok Bot; $30 SuperGrok does not.
- Grok Bot **relative** wording: Pro+ / Plus = generous weekly; Ultra / Heavy = highest weekly. Same product, two billers, Cursor does the metering.

**Not comparable without guessing:**

- SuperGrok weekly **percentage** vs Cursor monthly **dollars**. One is compute-weighted and unpublished; the other is API-priced and published only for third-party models.
- Cursor **Cursor Models** (“generous”) vs xAI SuperGrok weekly pool. Both are finite; **neither publishes a number**. Cursor Grok in the IDE is **not** SuperGrok chat quota.
- X Premium+ vs SuperGrok $30 **quantity**. Access overlap is official; size is unpublished.
- “Messages,” “requests,” and “prompts / 2 hours” across vendors. xAI retired that unit in June 2026. Cursor retired request-count pricing in 2025.
- Grok Bot weekly usage vs grok.com weekly usage. Officially **different meters** (Cursor account vs xAI weekly pool).
- Grok Build CLI vs Cursor Agent. Build draws SuperGrok’s weekly pool. Cursor Agent draws Cursor Models / Other Models. Linking SuperGrok does **not** pour the SuperGrok weekly pool into the IDE.

**If you only remember one thing:** the number you can take to the bank is Cursor’s **Other Models** dollar pool. Everything Grok-branded on both sides is “a larger unpublished weekly/monthly compute pool than the tier below,” plus named feature gates (Bot, 1080p, Heavy models). Anyone selling you “Heavy is N× Plus in tokens” or “Premium+ = SuperGrok 1:1 in messages” is filling in a blank the vendors left blank.
