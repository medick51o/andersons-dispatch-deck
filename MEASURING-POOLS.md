# Measuring an unpublished usage pool

*How to find out what a subscription actually gives you, when the vendor will not say.*

This is a method, not a table of numbers. Prices and allowances change; the technique does not.
Everything here was worked out and verified on real accounts in August 2026.

## The problem

Vendors increasingly sell AI subscriptions with **no published allowance**. Two live examples:

- One vendor describes the included pool as *"generous included usage"* — the identical phrase on
  its $20, $60 and $200 plans. Staff confirm on their own forum that the pool scales with tier, then
  decline to say by how much: *"we don't publish a specific multiplier."*
- Another retired message counts entirely and now shows only a **percentage of a weekly pool** whose
  size it never states.

So "how much do I actually get?" has no published answer, and buying the next tier up is a guess.

## Why you cannot just look it up

We searched Reddit, X, GitHub, Hacker News and both vendors' forums with four agents. Nothing.
There is a structural reason, and it is worth understanding before you waste time:

> **Both vendors' billing APIs return only a PERCENTAGE USED. The size of the tank is never
> transmitted to the client at all.**

That is not an oversight anyone can exploit. It means the number cannot be recovered by inspecting
traffic, decompiling a client, or reading a payload — the value simply is not there. Open-source
projects that reverse-engineered both APIs independently hit the same wall.

There is exactly one way to size a tank when the gauge shows only a percentage:

> **Pour in a known amount and measure how far the needle moves.**

## The method

### 1. Find the meter

Both vendors expose a usage endpoint to their own clients, authenticated with credentials already on
your machine. Community projects document them (see *Credits* below). Reading your own usage is
read-only and spends nothing.

The shape you are looking for in the response:
- an overall **percent used** for the current period
- ideally a **per-product breakdown**, so you can isolate the product you actually care about
- the **period start/end**, so you know what window you are measuring

Bank a small script that prints this. You will run it constantly.

### 2. Find the cost of a unit of work

You need a denominator. Two ways, in order of preference:

- **The vendor tells you.** Some CLIs report a per-run cost in their JSON output (look for a
  `total_cost_usd`-style field). This is the vendor's own accounting and is the best number you can get.
- **You price it yourself.** Multiply the run's token counts by the vendor's published per-token
  rates. Less exact — caching discounts make raw token counts overstate real cost — but workable.

### 3. Burn, and read the needle either side

Read the meter. Run a job of known cost. Read the meter again.

```
$ per point   =  cost of the job  ÷  points the meter moved
whole pool    =  $ per point  ×  100
```

**Do this at least twice, with jobs of different sizes.** Percentages are usually reported as
integers, so a job that moves the needle 2 points carries up to ±25% quantization error. Two
independent readings that agree are worth far more than one precise-looking result.

*Real example:* a 23-cent job moved a weekly meter 2 points; a 51-cent job moved it 3. That brackets
one point at 12–17 cents, so the full weekly pool is $12–17 of model time. Both readings agreed, so
the range is trustworthy even though neither reading alone was precise.

### 4. Cross-check against something you did not produce

This is the step people skip and it is the one that makes the result defensible.

Look for an independent measurement of a *different* tier of the same product — a blog post with
dashboard screenshots, a forum user quoting their own numbers. Adjust it for any announced policy
changes since (one vendor doubled its included pool mid-year; any earlier figure must be doubled to
be current). Then price it at published rates and compare against your own derivation.

*Real example:* a stranger's dashboard screenshots of the top tier, doubled for an announced policy
change and priced at published rates, came to ~$7,000/month. An independent derivation from a
different account, by unrelated arithmetic, came to ~$6,900. **Agreement within 1.5%, from two
methods that knew nothing about each other.** That is what turns an estimate into a finding.

## Traps

- **A denylist is not a measurement.** Do not infer a pool's size from what the vendor *says* it
  includes. Measure it.
- **Don't compare across vendors in vendor units.** A weekly percentage and a monthly dollar
  allowance cannot be compared. Convert both to a neutral unit — *dollars of model value per month*
  works well, since every vendor publishes per-token rates even when they hide allowances.
- **Watch for one-way spillover.** On at least one platform, when the included pool empties, work
  silently starts drawing the *paid* credit pool. It never flows back. A measurement taken after
  spillover begins is measuring the wrong tank.
- **Check whether the period reset mid-measurement.** Read the period start/end on both reads.
- **Dashboards lag and sometimes lie.** Both vendors have open bug reports about stuck or
  non-updating usage percentages. Prefer the API over the rendered page, and re-read if a number
  looks impossible.
- **Bonus/subsidy fields are real and variable.** One vendor's payload carries a bonus field showing
  free usage granted on top of what was purchased — in one observed case, several times the plan
  price. It is genuine, and the vendor's own note says it *may vary*. Never model a subsidy as
  permanent.

## What to do with the answer

Convert everything to **value returned per dollar spent**, and the comparison becomes obvious:

| Shape | What it usually means |
|---|---|
| ~2× the sticker price | Fair, sustainable pricing. The vendor is charging near cost. |
| 15×+ the sticker price | A subsidy — the vendor is buying market share. Real, and temporary. |

Both are fine to use. Only one is safe to build on. **Use a subsidized tier hard while it lasts;
do not dismantle anything you would miss the week it ends.**

## Tools in this repo

- `mcp-seats/read-meters.py` — reads both vendors' live usage, read-only
- `mcp-seats/bench-burn.py` — reports what a reserve seat's calls have cost

## Credits

The endpoints this relies on were documented by open-source developers who reverse-engineered the
official clients — `Tendo33/cursor-usage-tracker`, `kenryu42/pi-grok-cli`, and
`JoshuaWang2211/grok-usage-watch` on GitHub. Without their work none of the above would be possible.
The staff statements quoted in the method are public posts on the vendors' own forums.
