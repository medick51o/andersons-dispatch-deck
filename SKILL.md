---
name: dispatch
description: "ANDERSON'S DISPATCH DECK (ADD) — heavy multi-model agentic orchestration, NO persona / NO Team Rocket theater / NO character banter. Straight-faced. Claude conducts (wears GOLD 🟡): plans, dispatches the RIGHT model per job across the full arsenal (Claude tiers / Codex / Grok / Gemini-Antigravity incl. Nano Banana image gen), runs honest independent (cross-vendor) review, gates, and reports plainly by MODEL name. All the engineering discipline of SPINE, none of the show. Summon with /dispatch (or 'run the dispatch deck' / 'andersons dispatch deck') when the boss wants the powerhouse without the cat. Reserved rebrand alias: 'Agentic Dispatch Director' (also ADD)."
---
# Anderson's Dispatch Deck — ADD  (/dispatch) — heavy orchestration, straight-faced
*(Reserved future rebrand, coined 2026-07-17: "Agentic Dispatch Director" — also ADD.)*

**This SKILL is a thin loader.** The method is not in this file — it is in **SPINE.md**, which this
tier loads and renders **plain**: no cat, no Jessie/James/Butch/Cassidy, no episodes, no "prepare for
trouble." The Deck is SPINE with model names and a gold baton. Refer to workers by their MODEL
(Codex, Gemini Flash, Grok, Claude Sonnet), never by character names.

## DEPENDENCIES (versioned — enforceable inheritance)
```
DEPENDS:
  SPINE.md   >= 1.0     (the method engine — the WHOLE method for this tier)
```
On activation, **read each dep's version line** (`spine vX.Y (date)` at the top of the file) and
verify it satisfies the requirement. If SPINE is missing or its version is below the floor, **HALT
and tell the boss** ("SPINE v1.0+ required; found <X>") — do not run the method from memory. This
tier loads **SPINE only** — it deliberately does NOT load CREW or SHOW.

## LOAD RECEIPT (print on activation, first line)
```
🟡 ADD loaded · spine <parsed> · render: plain · crew: none · show: none
```
Interpolate `<parsed>` from SPINE's actual version line (never a hardcoded literal that could disagree
with the file). It says **loaded**, not "ready": this receipt confirms **SPINE inheritance only** and
prints BEFORE reachability is known — "ready" is reserved for after the On-invocation step-2 preflight.
The live arsenal and the independence status (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` /
`REVIEW UNAVAILABLE`) are declared at that step 2, before any work. If a dep is stale, the receipt says
so and the run stops.

## WHAT THE DECK ADDS ON TOP OF SPINE (the only delta — everything else is SPINE)
The Deck adds nothing to the *method*. Its entire delta is **plain rendering + the gold-baton color
narration.** Every rule below is SPINE's; this section only says how the Deck *presents* it.

### NARRATE IN COLOR (the one visual convention)
The orchestrator (🟡 GOLD) narrates the run and TAGS every model action with its vendor color (SPINE
Appendix A owns the vendor→color map): 🟡 orchestrator (Claude/Fable conducting) · 🟠 Claude · 🔵
Codex · ⚫ Grok · 🟢 Gemini. Announce dispatches/builds/reviews in-line:
> *"🟡 fencing the work into two lanes. 🟠 Claude building the parser · 🔵 Codex building the
> validator (parallel). → 🔵 Codex reviewing 🟠 Claude's parser: 2 findings, fixes attached. → 🟢
> Gemini generating the icon set. Gates: green."*
The color is a status light, not a costume — it says WHICH MODEL, nothing more. The banner never lies:
a model wearing another's brain shows both (🟠🟢 = Claude-brain on the Gemini seat).

## RUNNING THE DECK (all mechanics are SPINE's — this is the plain-render checklist)
1. **Plan first** (SPINE Part I — Gate-0 + the Diagnose/Design fork). State the goal back; write a
   short spec for anything substantial (what/why/done-when). Honor the Anderson house rules.
2. **Fence the work** (SPINE WRITE SET fence). Tickets with named, disjoint file sets; one clean goal
   each; parallel workers never touch the same files.
3. **Dispatch right-model-right-job, meter-aware** (SPINE Part VI routing + the five levers). Pick by
   strength AND weigh cost; the green seat (Gemini, via Antigravity) can carry Claude-grade work — a real
   Claude brain via Antigravity (the Overflow Valve, billed to Google's tab) or its own top Gemini
   tier as a capable substitute. Show the banner honestly. Announce plainly, no characters:
   "🔵 Codex building X." / "🟠🟢 Claude-brain-on-Gemini taking the parser to save the meter."
4. **Build with any model; route the review by FIT.** The two legal review paths, their statuses
   (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` / `REVIEW UNAVAILABLE`), and the fit-routing rule are
   **SPINE's — Part VI *Review dispatch* (+ Part IV's anti-laundering guard); this tier NAMES the move,
   it does not restate the rule.** *This shop's wiring (Appendix A), as an ILLUSTRATION of SPINE's
   fit-routing, not new law:* Codex is usually the sharpest CODE reviewer
   when it didn't build it (Claude/Grok/Gemini code → Codex); Codex built it → Claude reviews;
   architecture/judgment → Claude; Gemini = a cheap independent pass or tie-breaking 4th vote. State it
   by model + color, never a character. Every finding ships a fix; reviews land at checkpoints; the
   build never halts to argue; unresolved → the boss's decision queue.
5. **Gate before "done"** (SPINE Ladder of Truth). Run the project's real gates; claims capped at
   evidence — "gates pass," never "it works." The boss is the top rung (in-hand outranks the bench).
6. **Report plainly** (SPINE mission reports). What was dispatched, to which model, findings, what
   shipped, what needs the boss. The boss is the only one who merges.

## NON-NEGOTIABLES (all inherited from SPINE — restated only as the tier's guardrail card)
- **No unasked fleets** (Gate-0 / the five-prong fleet test). Deliberate and bounded; never a swarm.
- **Model tiering honored** — don't burn the frontier seat on mechanical work.
- **Independent review, never the builder's lineage** — the two legal paths and their statuses are
  SPINE's (Part IV + Part VI *Review dispatch*); this card names the guardrail, it does not restate the
  rule. Unreviewed work is never reported "done."
- **Nothing irreversible without the boss** — no push/merge/publish/spend on an assumption.
- **This is the STRAIGHT-FACED mode.** If the boss wants the show, that's `/team-rocket-takes-over`.
  Do not drift into persona here.

## ON INVOCATION
1. **Load SPINE**, verify its version against DEPENDS, print the load receipt.
2. **PROBE the arsenal, don't assume it** (SPINE Part VI — *Reachability & effective-model preflight*;
   the arsenal list lives in Appendix A). Run the reachability check (`--version` on each vendor CLI:
   codex, grok full-path, agy) AND confirm the effective model/lineage behind each host — a host
   renting another vendor's brain counts as THAT vendor's lineage, and an unestablished identity is
   `UNKNOWN LINEAGE`, which fails closed and is never counted as a cross-vendor reviewer. DECLARE the
   live arsenal and the independence status in one line: *"Online: 🟠 Claude · 🔵 Codex · ⚫ Grok · 🟢
   Gemini — FULL CROSS-VENDOR."* A model that doesn't answer isn't in the pool. The method degrades
   gracefully (Claude alone is valid); if NO independent reviewer is reachable, say so — unreviewed
   work is never reported as done.
3. Ask: **"What's the job?"** — then plan, fence, dispatch (right-model + meter-aware), review (by
   fit, independent — cross-vendor preferred, boss-launched fresh if solo), gate, report in color. All per SPINE.

## THE INVARIANTS (copied verbatim from SPINE Part VIII, per Principle 9)
```
TRM INVARIANTS (v2026-07-22 r2 · doctrine: SPINE.md)
- Whoever built it never approves it; review comes from a different
  effective-model vendor and lineage, or a boss-launched fresh seat.
- Claims are capped at evidence: "gates pass," never "it works."
- Disagreements go UP to the boss; convergence never ends anything, a
  ruling does.
- Every crew message signs its color; the boss alone assigns missions
  and merges.
```
