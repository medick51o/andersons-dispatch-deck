# BASELINE — Cursor Pro ($20), captured before any upgrade

**Read 2026-08-24 08:44, from the account's own billing page. Cycle Aug 21 → Sep 21, 2026.**

This is the "before" reading. Once the plan changes, the $20 tier becomes unmeasurable
forever, so this file is the only thing that will make a $60 comparison provable rather
than anecdotal.

## Raw, as displayed

| Item | Tokens | Usage |
|---|---:|---:|
| **Cursor Models** | **79.8M** | **29.6%** |
| cursor-grok-4.6-xhigh-fast | 51.9M | 21.8% |
| composer-2.5-fast | 15.5M | 4.3% |
| cursor-grok-4.6-medium | 6.7M | 1.6% |
| cursor-grok-4.6-high | 3.2M | 1.2% |
| cursor-grok-4.6-high-fast | 1.1M | 0.6% |
| composer-2.5 | 1.3M | 0.1% |
| auto | 165.5K | 0.0% |
| **Other Models** | **939.1K** | **2.6%** |
| kimi-k3-max | 381.7K | 1.3% |
| kimi-k3-high | 218.5K | 0.6% |
| gpt-5.3-codex | 256.7K | 0.6% |
| glm-5.2-high | 82.1K | 0.1% |

**On-Demand Usage (Aug 21 – Aug 24): $0.00.** No overage. Nothing has touched a card.
**Invoice Aug 21: $20.00, Paid.** **Auto-renews Sep 21, 2026.**
API `totalSpend` at the same moment: **$89.98** = $20.00 paid + $69.98 bonus.

## Derived — the pool size, finally defensible

Earlier estimates ($345, then $304) came from dividing spend by ONE of the two percentages,
which is why they disagreed. The dashboard shows both halves, and they sum:

```
29.6% (Cursor Models) + 2.6% (Other Models) = 32.2% of the allowance consumed
$89.98 of model value consumed at that same moment
$89.98 / 0.322  =  ~$279 per month of included model value
```

**~$279/month of model value on a $20 plan — about 14x sticker.**

*Assumption stated plainly:* that both percentages are shares of ONE allowance. The single
"Included Usage" panel and single date range say they are, and the arithmetic corroborates
— pricing each half separately at the implied rate reproduces the reported $89.98 to within
0.2%. The decisive test is still a burn: spend a known amount and watch the needle
(`bench-burn.py`).

14x is subsidy shape, not sustainable-pricing shape. Use it hard; do not build a
load-bearing lane on it (SPINE, THE METER LAW 4 — boss ruling 2026-08-24).

## Derived — what things actually cost

Dividing each row's %-used by its token count gives a price list the vendor never publishes:

| Model | Cost (% of pool per 1M tokens) | vs cheapest |
|---|---:|---:|
| **composer-2.5** | **0.077** | **1.0x** |
| cursor-grok-4.6-medium | 0.239 | 3.1x |
| composer-2.5-fast | 0.277 | 3.6x |
| cursor-grok-4.6-high | 0.375 | 4.9x |
| cursor-grok-4.6-xhigh-fast | 0.420 | 5.5x |
| cursor-grok-4.6-high-fast | 0.545 | 7.1x |
| glm-5.2-high | 1.218 | 15.8x |
| gpt-5.3-codex | 2.337 | 30.4x |
| kimi-k3-high | 2.746 | 35.7x |
| kimi-k3-max | 3.406 | 44.2x |

**Two findings that change how the rig should be driven:**

1. **The FAST tiers carry a real surcharge, now measured rather than assumed.**
   `composer-2.5-fast` costs **3.6x** what plain `composer-2.5` costs for the same tokens.
   The seat's `DEFAULT_MODEL = "composer-2.5"` (non-fast) was a guess when it was written;
   this is the receipt that it was right.

2. **One model is eating the account.** `cursor-grok-4.6-xhigh-fast` alone is **21.8% of
   32.2% used — roughly two-thirds of everything consumed this cycle**, and it is 5.5x the
   price of composer-2.5. It is not coming from the MCP seat (which defaults to non-fast and
   refuses `auto`); the `auto` row and the fast-tier volume point at IDE-side usage.

## Burn rate — the actual argument for upgrading

```
32.2% consumed in 3 days (Aug 21 → Aug 24)  =  10.7% per day
Pool empties on day 9.3 of a 31-day cycle   ≈  Aug 30
Days of the cycle left with an empty tank   ≈  22
```

At the current rate this plan runs dry in the first third of every month. That — not the
raw pool size — is the case for a bigger tier. **But check finding 2 first:** if most of
that burn is one surcharged fast model being driven from the IDE, changing the default may
buy back more headroom than $40/month does.

## What to re-read after any upgrade

Same page, same fields, so the comparison is apples to apples:
`Included Usage` percentages for both halves · token counts per model · `On-Demand` subtotal ·
API `totalSpend` / `bonusSpend` · cycle start and end. Then re-run the per-model cost table
and compare against this file.

---

# PREDICTION, recorded BEFORE the upgrade (2026-08-24 08:57)

Written down first so it can be scored honestly instead of retrofitted afterward.

## What the research said (last night, sourced)

**Cursor staff, [forum.cursor.com/t/166360](https://forum.cursor.com/t/question-about-first-party-models-pool-limits-between-pro-pro-plus-an):**
> "Pro+ includes more than Pro, and Ultra includes more than Pro+."
> "A higher tier means a higher limit for first-party models, **but we don't officially publish
> the exact multiplier.** That's why the plans page uses the same wording for all plans, Generous
> included usage."
> **"Upgrading increases BOTH pools."**

**Billing behavior — staff-confirmed across three forum threads:** the checkout charges the **full
$60 immediately** and a **prorated refund lands days later**; the old Pro plan **auto-cancels the
moment you upgrade**. Not a double charge. But one billing reply (Aug 21) contradicts the
calendar-day explanation given elsewhere: *"Upgrade refunds are based on usage. If Pro monthly
usage was already consumed, no refund."* Included allowance here is fully consumed, so **assume no
refund**; treat any credit as a bonus. Several users also reported credits never arriving and had
to chase them with an invoice ID.

## The projection vs the measurement — last night's model, tested by today's dashboard

An independently published Ultra measurement (~7.0B tokens/mo after the July doubling) was used to
project the lower tiers. Today's dashboard measures the Pro pool directly for the first time:

| | tokens/mo | note |
|---|---:|---|
| Projected Pro (assumed Ultra:Pro = 20:1) | 350M | last night |
| **MEASURED Pro (first-party)** | **270M** | 79.8M ÷ 29.6%, today |
| Error | **23% high** | same order; the assumed ratio was optimistic |
| Implied real ratio Ultra:Pro | **26:1** | replaces the assumed 20:1 |

## The prediction

Applying the $70:$400 price ratio (1:5.7) to the same Ultra anchor:

- **Pro+ first-party pool ≈ 1,230M tokens/month — about 4.6x the measured Pro pool.**
- At the current burn (26.6M tok/day) that is **~46 days of runway**, against the **825M** a
  31-day cycle needs at this rate. Pro should therefore go from running dry on **day ~10** to
  covering a full cycle with roughly a third to spare.
- **Both pools rise**, not just the first-party one (staff, above).
- **The billing cycle restarts** on upgrade, since Pro auto-cancels. If so, before/after
  percentages are NOT comparable and the comparison must be made on **burn rate**, not on %-used.

**Confidence, stated honestly:** the Pro number is now MEASURED. The Pro+ number is a
*projection from a price ratio*, and the same method just came in 23% high on Pro — so treat
~1,230M as an optimistic ceiling and expect somewhere in the 800M–1,300M band. Anything below
~825M means Pro+ still will not cover a full cycle at the current burn rate.

## How to score it

After the upgrade, read the dashboard again and divide: `tokens ÷ (percent/100)` = pool.
Also record the new cycle start/end (tests the reset prediction) and whether the Other Models
percentage moved (tests "both pools rise"). Compare against this file.
