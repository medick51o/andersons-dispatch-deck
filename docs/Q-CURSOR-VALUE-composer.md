Reading the handoff file and following its instructions.


Searching the codebase and docs for Cursor pricing, pool limits, and Grok model details.


## Q1 — Pro+ vs Pro on the Cursor Models pool

**Your reading matches Cursor’s public docs.** On [models-and-pricing](https://cursor.com/docs/models-and-pricing), Pro, Pro Plus, and Ultra all list **“Generous included usage”** for Cursor Models. The only numeric tier ladder in that table is **Other Models**: **$20 / $70 / $400**.

The “3× / 20× Agent limits” marketing tracks that **Other Models** ladder, not a published bigger Composer/Grok tank.

**What $40 more actually buys (official):**
- Other Models: $20 → $70
- Grok Bot ([help](https://cursor.com/help/grok-bot/plans)) — not on Pro $20
- Same Cursor Models wording on every paid individual tier

I have **no internal knowledge** that Pro+ secretly enlarges the included Composer/Grok pool. If it does, Cursor hasn’t published it. **UNKNOWN**, not refuted.

---

## Q2 — Knowing you’re near the included-pool limit

**Where to look (official):** [cursor.com/dashboard/usage](https://cursor.com/dashboard/usage) and **editor Settings** — docs say **both pools** are visible there.

**What you won’t get:** a grok.com-style **weekly % bar with a published size**. Cursor never publishes a token/$ cap for Cursor Models.

**At the limit (official):** exceed included usage → **on-demand at listed API rates** or **upgrade**. Docs say requests are **not** downgraded in quality/speed.

**REPORTED (forum staff, not pricing page):** exhausted Cursor Models may **spill into remaining Other Models dollars** before a hard stop.

**Inferring:** you’ll see pool consumption on the dashboard, but not “47% of a known tank” like grok.com.

---

## Q3 — Dropping SuperGrok $30 for Cursor Pro $20

**You lose (SuperGrok side):**
- **grok.com chat** — separate **weekly % pool** on the xAI account
- **Grok Imagine** (image/video)
- **Grok Voice**
- **Expert / reasoning modes** on grok.com’s product surface
- **Grok Build CLI** — draws the **SuperGrok weekly pool**, not Cursor’s pools
- **Grok Bot** — SuperGrok $30 doesn’t include it (Plus $100+ or Cursor Pro+)

**`cursor-grok-4.6` vs grok.com Grok 4.6:** **not the same SKU.** Official: **“Jointly trained by Cursor and SpaceXAI.”** It’s a **Cursor-hosted** agent model with Cursor agent tooling, effort tiers (`low`–`xhigh`), and **Cursor billing**. Same lineage family; different product, meter, and likely different behavior/context.

**Cursor Pro gives that SuperGrok doesn’t:**
- **Composer 2.5** on the included pool
- **cursor-grok-4.6** via `cursor-agent` CLI on Cursor’s meter
- **$20/month Other Models** for Claude/GPT/Gemini/Kimi in the agent
- **Not** grok.com chat, Imagine, Voice, or Grok Build on the SuperGrok meter

---

## Q4 — CLI-only, never opening the IDE

**Honest case:** you’re **not** only buying an editor. `cursor-agent` is a real subscription surface — you’re using it headlessly today. Pro is the entry tier for that agent + pools.

**But** you **are** paying for bundled IDE features (tab completions, editor integrations) you may never touch. That’s real dead weight.

**Sensible if:** you want **Composer + Cursor Grok** as a metered reserve from the terminal, with optional third-party models on the $20 Other Models allowance.

**Poor fit if:** your work is **Grok-only code review/build from terminal** — **SuperGrok + Grok Build CLI** is the direct product. Dropping SuperGrok for Cursor Pro trades a clear weekly meter and grok.com features for an **unpublished** Cursor Models tank and a **joint-trained** Grok variant.

**Inferring for your shop:** Cursor Pro works as a **cheap bench seat**, but heavy headless dispatch is exactly what drains an unpublished pool — and you already have flat-rate house seats for most lanes.

---

**Bottom line:** Pro+ mainly scales **Other Models + Grok Bot**, not a documented bigger Composer/Grok tank. SuperGrok and Cursor Pro are **different billers and different products** — not a clean $30→$20 swap for terminal Grok work.

---
🟣➤🎼 [wmw-cursor] ♾️ Cursor · composer-2.5
   sessionId: ed05a4da-f76f-4705-aaae-544aa34e2230 · meter: INCLUDED · 45525 in / 3575 out