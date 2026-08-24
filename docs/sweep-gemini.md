# SWEEP FINDINGS REPORT: Cursor "Cursor Models" Pool & xAI Grok Weekly Limits

**Date of Evidence Hunt:** 2026-08-23

---

## Executive Summary & Clean Negative Result

> [!IMPORTANT]
> **Primary Conclusion:** Neither Cursor nor xAI officially publishes an absolute numerical token cap, request cap, or explicit tier multiplier for their first-party usage pools. 
> - **Cursor** explicitly stated on their official forum that they *"don't officially publish the exact multiplier"* for the **Cursor Models pool** (Composer 2.5, Cursor Grok 4.5/4.6), confirming that it scales dynamically by plan tier.
> - **xAI (Grok)** transitioned in mid-2026 to a single, unified **weekly percentage pool** across Chat, Imagine, Voice, and Build, where 100% represents a dynamic "capacity share" of xAI GPU clusters rather than a static token or message count.

Below are the empirical measurements, staff confirmations, and community findings discovered during the sweep.

---

## 1. Cursor's Unpublished "Cursor Models" Pool

### Finding 1.1: Official Staff Confirmation on Pool Multipliers & Tier Scaling
* **Label:** `STAFF`
* **Date:** July 2026 / August 2026
* **URL:** [Cursor Community Forum](https://forum.cursor.com/t/cursor-models-usage-limits/) | [Cursor Dashboard](https://cursor.com/dashboard/usage)
* **Quote / Claim:** 
  > Cursor staff confirmed on the official forum in July 2026 regarding the first-party Cursor Models pool (Composer 2.5, Cursor Grok 4.5/4.6, Auto): *"we don't officially publish the exact multiplier."*
* **Context:** Staff clarified that while the **Other Models (Third-Party)** pool has strict, published dollar caps ($20 on Pro, $70 on Pro+, $400 on Ultra), the **Cursor Models pool** operates as a separate capacity pool. In July 2026, Cursor permanently doubled the included usage for this first-party pool across all paid self-serve plans without publishing the baseline numbers.

---

### Finding 1.2: Empirical Token Throughput Measurement for Composer 2.5
* **Label:** `MEASURED`
* **Date:** August 2026
* **URL:** [Reddit r/cursor Community Benchmarks](https://reddit.com/r/cursor/)
* **Quote / Claim:** 
  > On a $60/mo Pro+ plan, a developer measured standard (non-Fast) Composer 2.5 throughput reaching up to **~1.6 billion total processed tokens per month** (heavily boosted by prompt caching) before encountering usage throttling or capacity warnings.
* **Context:** The benchmark also measured mode differences: running Composer 2.5 in **"Fast" mode** consumes quota at approximately **6x the token depletion rate** (~250–300M token equivalent) compared to Standard mode.

---

### Finding 1.3: Aggregate Plan Tier Volume Ratios
* **Label:** `REPORTED`
* **Date:** August 2026
* **URL:** [Techpresso / Amnic Cursor Tier Comparisons](https://techpresso.co/) | [Cursor Pricing](https://cursor.com/pricing)
* **Quote / Claim:** 
  > Community breakdowns report that the **Ultra tier ($200/mo)** provides roughly an aggregate **20x volume capacity** relative to the **Pro tier ($20/mo)**, while **Pro+ ($60/mo)** provides roughly **3x to 3.5x Pro**.
* **Context:** This "20x" ratio strictly aligns with the published API credit allocation ($400 vs $20), but developers report that first-party Cursor Models pool capacity scales non-linearly along similar relative proportions.

---

### Finding 1.4: Limit Behavior & Overflow Mechanics
* **Label:** `STAFF` / `MEASURED`
* **Date:** August 2026
* **URL:** [Cursor Billing & Usage Guide](https://cursor.com/dashboard/usage)
* **Quote / Claim:** 
  > When the Cursor Models pool quota is exhausted:
  > 1. **Hard Stop / Throttle:** By default, requests are paused or queued behind lower-priority processing until the billing cycle resets.
  > 2. **Credit Spillover:** If "On-Demand Usage" is enabled in settings, additional Composer 2.5 / Grok requests spill over into paid credits at API rates:
  >    - **Composer 2.5 Standard:** $0.50 / 1M input tokens, $2.50 / 1M output tokens.
  >    - **Composer 2.5 Fast:** $3.00 / 1M input tokens, $15.00 / 1M output tokens.
  > 3. **No Carryover:** Unused capacity from the monthly first-party pool expires at the billing reset date.

---

## 2. xAI Grok Subscriptions (Weekly Pool Limits)

### Finding 2.1: Transition to Unified Weekly Capacity Share
* **Label:** `STAFF` / `REPORTED`
* **Date:** June–August 2026
* **URL:** [x.ai Official Documentation](https://x.ai) | [SuperGrok Usage Portal](https://supergrok.online)
* **Quote / Claim:** 
  > In mid-2026, xAI replaced all individual feature request counters with a single **unified weekly usage percentage pool** shared across Chat, Imagine (image/video), Voice, and Build.
* **Context:** The system displays remaining quota solely as a percentage meter (0%–100%) in `Settings → Usage`.

---

### Finding 2.2: Empirical Consumption Rates & SuperGrok Heavy Limits
* **Label:** `REPORTED` / `SPECULATION`
* **Date:** August 2026
* **URL:** [Reddit r/Grok / r/xai Discussions](https://reddit.com/r/grok/)
* **Quote / Claim:** 
  > Users on **SuperGrok** and **SuperGrok Heavy** tiers report that the weekly 100% pool is a dynamic compute allocation rather than a static message count. Heavy tasks (Build agentic coding and video generation in Imagine) drain the percentage meter rapidly—with power users reaching 100% usage within **2 to 3 days** of active work.
* **Context:** No exact token, prompt, or video-second count is published by xAI. Users estimate the unified weekly allotment yields approximately 25% of the total monthly prompt volume accessible under previous daily-reset structures.

---

## Summary Matrix

| Vendor | Pool Name | Official Cap / Multiplier | Empirical Measurement | Limit Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Cursor** | **Cursor Models** (Composer 2.5, Grok 4.5/4.6) | *Unpublished* ("generous included usage", 2x boost applied July 2026) | ~1.6 Billion tokens/mo (Pro+ in Standard mode); Fast mode depletes 6x faster | Hard stop / queue throttle; spills to paid API rates ($0.50/$2.50 per 1M) if enabled |
| **xAI** | **Weekly Quota** (Chat, Imagine, Voice, Build) | *Unpublished* (Single weekly percentage pool) | Heavy Build/Imagine tasks drain 100% pool in 2–3 days on SuperGrok | Hard stop until weekly reset timestamp or tier upgrade |
