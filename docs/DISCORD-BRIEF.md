# Discord brief — pasteable

Five posts. Each is under Discord's 2000-character limit, so paste them one at a time in
order. Nothing here names anyone or links to a private project.

---
---

## POST 1 of 5

🧵 **We put the Cursor CLI inside Claude Code as a permanent seat. Here's the setup and what it actually costs.**

Short version: Claude Code can call other AI CLIs as tools over MCP. Most people wire those up as one-shot calls, so the other model wakes up with amnesia every single time. We wired them as **persistent seats** instead — the first call returns a session id, and a `-reply` tool continues that same session with its full context intact.

Four seats are standing right now: Codex 🔵, Grok ⚫, Gemini 🟢, and Cursor 🟣.

The Cursor one is the interesting one, because Cursor's CLI is a doorway to **200+ models** on one $20 subscription — and two of them cost nothing extra to use.

No API keys anywhere in this. Every seat bills against a subscription that was already being paid for.

---
---

## POST 2 of 5

🔌 **The wiring**

```
            YOU
             │
      ┌──────▼──────┐
      │ CLAUDE CODE │  ← conductor: plans, dispatches, reviews, gates
      └──────┬──────┘
             │  MCP (stdio, JSON-RPC)
   ┌─────────┼─────────┬──────────┐
   ▼         ▼         ▼          ▼
 CODEX     GROK     GEMINI     CURSOR
  🔵        ⚫         🟢          🟣
                                  │
                        ┌─────────┴─────────┐
                        ▼                   ▼
                  FREE IN POOL         COSTS CREDITS
                  composer-2.5         claude-* gpt-*
                  cursor-grok-4.6      gemini-* kimi-* glm-*
                        │                   │
                    use freely        gated behind a
                                     recorded allowance
```

Each seat is a small Python program that speaks MCP on stdin/stdout and shells out to that vendor's CLI. About 400 lines each. The conductor sees them as ordinary tools.

The split at the bottom is the whole trick 👇

---
---

## POST 3 of 5

💰 **What you actually get for $20**

Cursor's pool has two halves, and they are not the same thing:

🟢 **Included** — `composer-2.5` and `cursor-grok-4.6`. These draw on the plan, not on credits. This is where all the routine work goes.
🔴 **Credits** — Claude, GPT, Gemini, Kimi, GLM. Real money at API rates.

Our seat **defaults to the free half** and refuses the paid half unless there's a recorded allowance — a bound (N calls per window) that expires on its own. No allowance, no spend. That was deliberate: the failure mode we were designing against is a tool quietly running up a bill.

📊 **Measured today (3 days into a fresh cycle):**
> **$89.98 of model value consumed. $20.00 paid. The other $69.98 is a bonus the vendor's own API reports.**

That's not our estimate — it's Cursor's own accounting field, read straight off the billing endpoint. Roughly **4.5x the sticker price, in three days.**

That shape means one thing: **it's subsidized.** Which is fine. Use it hard. Just don't build anything you'd miss the week it ends.

---
---

## POST 4 of 5

🥊 **Does the cheap seat actually work?**

We ran the Cursor-hosted Grok head to head against the standalone Grok CLI on the same task, twice.

First run, the Cursor one looked clearly worse. Easy conclusion: cheaper model, worse results.

**That conclusion was wrong.** The gap was the harness, not the model — the Cursor seat had been given fewer tool permissions. Once both sides got equal footing, they matched.

Worth saying plainly because it's the mistake everyone makes when benchmarking a budget tier: **you are usually measuring your own setup, not the model.**

🔒 **Three real security holes we found and closed while building this:**
1. A Windows `.cmd` shim forwarded arguments straight to PowerShell — a crafted prompt could run host commands. Fixed by writing prompts to a file and passing only a plain pointer.
2. A "read-only" seat wrote an 11KB file. The flag we trusted meant *authorize*, not *restrict*. Different flag now.
3. A read-only seat escalated by calling **another** seat and having it do the writing. Cross-seat calls are blocked now.

If you wire this up yourself, assume all three apply to you too.

---
---

## POST 5 of 5

🔍 **How to check any of this yourself**

Neither vendor publishes how big your pool is. They only show a percentage. So you measure it: burn a known amount of work, read the needle before and after, and convert to *dollars of model value per month* — every vendor publishes per-token rates even when they hide allowances.

Then cross-check against someone else's numbers you had no hand in producing. We priced a stranger's published dashboard screenshots of a higher tier and got ~$7,000/month; an independent derivation from a different account by unrelated arithmetic came to ~$6,900. **Agreement within 1.5%** — that's what turns a guess into a finding.

⚠️ **Two honest caveats:**

**Dashboards lie.** While writing this, Cursor's own API told us *"You've hit your usage limit"* — at 29.6% used. We sent a test call anyway. It answered in 3.5 seconds. **Verify with a call, not a banner.**

**Subsidies are temporary by definition.** The vendor's own note says the bonus may vary. Treat this as a window, not a foundation.

📌 Method + measurement writeup is public if anyone wants it — the how-to-measure-a-hidden-pool part generalizes to any vendor, not just this one.

*(Numbers read 2026-08-24. They're a floor at a moment in time, not a constant.)*
