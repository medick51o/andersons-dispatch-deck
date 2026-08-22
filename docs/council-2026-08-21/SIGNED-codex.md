Reading additional input from stdin...
OpenAI Codex v0.145.0
--------
workdir: C:\Sync\Projects\andersons-dispatch-deck
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 01a026ad-21da-7da2-9b5b-e2c6f79586ad
--------
user
YOUR LENS (≡ƒö╡ Codex CLI): CORRECTNESS of a Cursor skill that must actually dispatch. Task-tool slugs, two credit pools (Cursor Models vs Other Models), Pro $20 vs CLI overflow, builder-never-approves. Propose a seat table a file can enforce. You may read SKILL.md / SPINE.md in this repo. Do not edit files.

You are Codex CLI (OpenAI), NOT Cursor GPT. Do not edit files.


# COUNCIL BRIEF ΓÇö Cursor branch of Anderson's Dispatch Deck
*2026-08-21 ┬╖ convened by Cursor Grok ≡ƒƒí ┬╖ CLI + Composer ┬╖ do not edit files ┬╖ signed opinion only*

## The question (verbatim from the boss)

He wants a **new branch** of the **Cursor version** of Anderson's Dispatch Deck. The original skill was written when **Claude Fable on a $200 Max plan was the orchestrator**. A lot has changed. Cursor Grok is now gold in this IDE. Gemini 3.7 Flash (High) is, in his words, "hot shit" and an excellent tool ΓÇö not a spare tire. He wants the council to **reevaluate seats by current strengths**, not 2026-07 wardrobe folklore.

He is **frugal**: Cursor **Pro $20** now (Other Models = $20 ΓÇö treat as radioactive). Likely **Pro Plus $60** next to try Grokbot. Ultra + provider APIs as overflow only if he likes the work. **Wean off living in CLIs** for daily build, but **today's panel is CLI + Composer** so we do not burn Cursor Other Models.

## What already exists

1. **Trunk ADD** (this git repo, Claude-as-gold): Claude conducts; Codex builds/reviews; Grok = UI; Gemini = cheap extra vote / builder / Nano Banana / overflow valve (agy can wear Claude brains ΓÇö that is Google bill, Claude lineage).
2. **Cursor-native draft** at `C:\Users\andre\.cursor\skills\dispatch\` (NOT committed here): Grok conducts; Composer = Cursor-pool builder; Claude Task = architect/judge (Other Models); GPT-5.6 Sol Task = Codex-shaped (Other Models); Gemini Task = extra vote; Grok worker cannot review Grok conductor. On Pro $20 those Other Models seats are **parked**.
3. **CLI seats still alive on this box** (billed to those subs, not Cursor): `claude.exe` Max ┬╖ `codex` 0.145.0 ┬╖ `agy.exe` with **Gemini 3.7 Flash (High)** on the roster ┬╖ `grok.exe` Super Grok.

## Numbered points EVERY seat must answer

1. **Gold:** Who should conduct inside Cursor day-to-day (Grok vs Claude vs Composer vs human-switches-the-picker), and why?
2. **Reseat the table:** For each of Claude, Codex/GPT, Gemini 3.7 Flash, Gemini Pro, Grok (Cursor vs CLI), Composer 2.5 ΓÇö what jobs should they **own**, what should they **never** do, given 2026-08 strengths not 2026-07 memory?
3. **Gemini:** The old skill treats Gemini as cheap extra / 4th vote / overflow. The boss says 3.7 Flash is first-class. Propose a **concrete new seat**, not a pep talk.
4. **Two harnesses:** Daily Cursor-native (Task tool, Cursor credits) vs CLI overflow (Max / Codex / Google / Super Grok). How should one SKILL.md describe both without the orchestrator "oops" into the wrong bill?
5. **Pro $20:** What is legal independent review when Other Models are parked? Do not fake cross-vendor.
6. **What to delete** from the original ADD skill (Fable-as-gold, Gemini-as-spare, Grok-UI-only) vs **what is load-bearing** (SPINE, fences, builder-never-approves, council ask-first).
7. **File shape:** What files belong on the `cursor-v2` branch (SKILL.md, CURSOR-NATIVE.md, SPINE pointer vs copy, MODEL-DISPATCH-GUIDE rewrite, etc.).

## Your unique lens (do not repeat the others)

See the wrapper prompt that launched you.

## Output format (mandatory)

Sign the first line: `SIGNED: <vendor> <model> ┬╖ <color> ┬╖ CLI|Composer`
Then: Gold recommendation ┬╖ Seat table (markdown) ┬╖ Gemini 3.7 seat in one sentence ┬╖ Pro $20 review honesty ┬╖ Delete vs keep ┬╖ Files ┬╖ Disagreements you expect ┬╖ Confidence (high/med/low) and what you did not verify.
Do not edit files. Do not invent that you read SPINE if you did not. Keep it under ~800 words.

codex
IΓÇÖll inspect the repoΓÇÖs `SKILL.md` and `SPINE.md`, plus any dispatch guide, then give a signed correctness opinion focused on enforceable routing and billing boundaries. No files will be changed.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'rg --files -g "SKILL.md" -g "SPINE.md" -g "*DISPATCH*" -g "AGENTS.md"' in C:\Sync\Projects\andersons-dispatch-deck
 succeeded in 2259ms:
SPINE.md
SKILL.md
MODEL-DISPATCH-GUIDE.md

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw -LiteralPath 'MODEL-DISPATCH-GUIDE.md'" in C:\Sync\Projects\andersons-dispatch-deck
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw -LiteralPath 'SKILL.md'" in C:\Sync\Projects\andersons-dispatch-deck
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw -LiteralPath 'SPINE.md'" in C:\Sync\Projects\andersons-dispatch-deck
 succeeded in 524ms:

# The Model Dispatch Guide ΓÇö who to send where

**Purpose (boss-commissioned 2026-07-17):** so the orchestrator (the cat / whatever
Claude is driving) ALREADY KNOWS which model to dispatch for which job on any future
project ΓÇö no re-discovery. Consult this at project start. Core law it rests on:
**characters are permanent, models are wardrobes** ΓÇö so this guide is about the MODELS
(the tools); the characters (Jessie/James/Butch/Cassidy/the cat) just wear them.

---

## ≡ƒƒá CLAUDE (Anthropic) ΓÇö the brain + the orchestrator
**Characters:** ≡ƒÿ╝ the cat (orchestrator, usually Fable) ┬╖ ≡ƒƒá Jessie (builder) ┬╖ ≡ƒö┤ Butch (reviewer).
**Strengths:** deepest multi-file reasoning, architecture, spec-writing, root-cause
debugging, tricky/tangled logic, adversarial review, and honest judgment ΓÇö it FLAGS its
assumptions instead of hiding them ("I bounded this to 2/3 because the engine only means
2/3 ΓÇö ruling queued"). Best narrator/orchestrator.
**Dispatch for:** the orchestration itself ┬╖ architecture & design calls ┬╖ specs ┬╖ engine
surgery ┬╖ root-cause hunts ┬╖ hard multi-file changes ┬╖ reviewing other vendors' work.
**Watch-out:** the expensive seat ΓÇö ration it; watch the weekly meter. TIER IT:
- **Fable** = specs, review, orchestration, conversation (heavyweight; the cat's default).
- **Sonnet** = code + research sub-agents (the workhorse for builds).
- **Haiku** = mechanical (gate re-runs, log mining, builds). the boss watches the counter.
**Mechanism:** it's the HOME CLI (Claude Code). Sub-agents via the Agent tool. This is the
one window everything else hangs off.

## ≡ƒö╡ CODEX (OpenAI / ChatGPT) ΓÇö the precision builder + sharpest reviewer
**Characters:** ≡ƒö╡ James (builder) ┬╖ ≡ƒ⌐╖ Cassidy (reviewer).
**Strengths:** disciplined, exact implementation of a clear spec (no drift) ┬╖ the SHARPEST
static/adversarial code review in the shop ΓÇö it doesn't just claim a bug, it PROVES it
(raw-socket-forges the bad input, shows it break) ┬╖ validation-matrix / edge-case thinking.
**Dispatch for:** bounded implementation of a clear fenced ticket ┬╖ cross-vendor code
review (esp. Cassidy reviewing Claude-built work) ┬╖ security/validation passes.
**Watch-out:** wants ONE clean goal per ticket (refuses messy multi-fix tickets) ┬╖ runs on
a SEPARATE plan ΓåÆ costs the Claude meter $0 (great default builder for budget) ┬╖ headless
needs stdin closed.
**Mechanism:** `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`
(the danger-full-access lane is the working one on the Anderson box ΓÇö its OS-sandbox ACL
bug is upstream; boss blessed a `Bash(codex*)` allow rule). Embed code IN the prompt for
reviews (reviews-by-embed) when file access is flaky.

## ΓÜ½ GROK (xAI) ΓÇö the fearless artist
**Characters:** cat-driven ΓÜ½ (or a ≡ƒ½í Wobbuffet skit); it's a wardrobe, not a permanent character.
**Strengths:** fearless one-shot visual design ΓÇö hand it a VIBE, get back a world ┬╖ UI/UX,
skins, concept/vision pages, demo-mode storytelling ┬╖ fast ┬╖ leaves a signed lineage trail.
**Dispatch for:** UI face-lifts ┬╖ concept/vision HTML ┬╖ skins & art direction ┬╖ "make it
feel like a starship" ┬╖ anything with a screen and a mood.
**Watch-out:** UI SURFACE ONLY ΓÇö "Grok reskins, it does not rewire"; keep it off engine
logic ┬╖ gate for platform ceilings (e.g. WebKit-16 for the old iPad) ┬╖ mandatory
GROK-TRAIL.md entry per job for lineage.
**Mechanism:** `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <file> --always-approve < /dev/null`
(NOTE: `grok` is on PATH in a normal shell but NOT in the tool's bash ΓÇö use the full path).

## ≡ƒƒó GEMINI / ANTIGRAVITY (Google) ΓÇö the value powerhouse (the biggest find)
**Characters:** cat-driven ≡ƒƒó for builds/art ┬╖ ≡ƒƒá≡ƒƒó Jessie fronts when it wears a Claude
brain (Overflow Valve) ┬╖ ≡ƒö╡ James fronts its reviews of Claude-built work. Wardrobe, not a
permanent character (yet).
**Strengths (proven 2026-07-17, exceeded expectations):**
- **A real BUILDER, not just a reviewer** ΓÇö Flash 3.5 one-shot a premium Flydigi Vader 4
  Pro GPV (live gamepad API, trigger bars, tension-ring detail it added unprompted).
  Strong comprehension (inferred "GPV = Game Pad Viewer" from 3 letters).
- **IMAGE GENERATION via Nano Banana** ΓÇö asked to "use Nano Banana 2," it PIVOTED from
  code to image gen and wrote a real 656KB photoreal JPEG. **Runs on the $4.99 AI Pro SUB
  with the credit card OFF = zero per-image cost.** (The free AI-Studio-KEY path 429s on
  images; the SUB path does NOT. Different doors.) This is the shop's art-generation engine.
- **Cheap Flash tier** for wide sweeps, cold reviews, mechanical passes (its first-ever
  review caught 3 real threading bugs).
- **A different gene pool** ΓÇö a genuine independent 4th vote when the bench is split.
- **The Overflow Valve** ΓÇö its wardrobe includes Claude Sonnet 4.6, Claude Opus 4.6, and
  GPT-OSS 120B, all billed to Google. When the Claude weekly meter runs hot, move heavy
  work here ΓÇö some still wearing a Claude brain ΓÇö on the $4.99 tab.
**Dispatch for:** real builds (Flash) ┬╖ IMAGE gen (skins art, mascots, concept renders via
Nano Banana) ┬╖ cheap cold reviews / sweeps ┬╖ overflow capacity ┬╖ a 4th independent opinion.
**Watch-out:** headless `-p` auto-denies external TOOL use (but it CAN write to its own
brain dir + generate images fine) ┬╖ review-independence only counts when it runs a GEMINI
model (agy-wearing-Claude is NOT a second Claude opinion) ┬╖ **promo $4.99/mo ΓåÆ $19.99
~mid-Oct 2026** (keep/cancel decision).
**Mechanism:** `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.5 Flash (High)"`
(tiers: Flash Low/Med/High, Gemini 3.1 Pro Low/High, Claude Sonnet/Opus 4.6, GPT-OSS 120B).
Generated images land in `C:\Users\<you>\.gemini\antigravity-cli\brain\<uuid>\*.jpg` ΓÇö fish
them out from there.

---

## QUICK DECISION TABLE ΓÇö "I need to ___ ΓåÆ send ___"
- **Architect / spec / hard root-cause** ΓåÆ ≡ƒƒá Claude (Fable).
- **Build a clear fenced spec, cheap** ΓåÆ ≡ƒö╡ Codex (James) ΓÇö $0 to Claude meter.
- **Build, mixed / when Codex is busy** ΓåÆ ≡ƒƒó Gemini Flash (proven builder) or ≡ƒƒá Claude Sonnet.
- **Review Claude-built code** ΓåÆ ≡ƒö╡ Codex or ≡ƒƒó Gemini ΓÇö never Claude reviewing itself.
- **Review Codex-built code** ΓåÆ ≡ƒƒá Claude ΓÇö never Codex reviewing itself.
- **Review Grok/Gemini-built code** ΓåÆ ≡ƒö╡ Codex (the sharpest code reviewer; catches Grok's
  UI-surface gaps) ΓÇö or ≡ƒƒá Claude for architecture/design. Route the reviewer by the CODE'S
  TYPE + the cross-vendor rule; ANY model can build, Codex is the default code-reviewer
  whenever it didn't build the code, Claude reviews Codex + owns architecture review.
  (In ADD / no-character mode, say it by model+color; in Team Rocket mode, by character.)
- **UI / skins / concept pages / "make it cool"** ΓåÆ ΓÜ½ Grok (cat-driven).
- **Generate an IMAGE (art, mascot, render)** ΓåÆ ≡ƒƒó Gemini Nano Banana (cat-driven, free on sub).
- **Wide sweep / log-mine / mechanical** ΓåÆ ≡ƒƒó Gemini Flash (cheap) or ≡ƒƒá Haiku.
- **Claude meter running hot** ΓåÆ ≡ƒƒó Overflow Valve: route Claude-grade work to the GREEN
  seat ΓÇö either a real Claude brain on Antigravity (≡ƒƒá≡ƒƒó, Google's tab) OR Gemini's own top
  tier as a capable-if-lesser Claude stand-in (≡ƒƒó). Dispatch is COST-AWARE, not just
  capability-aware ΓÇö the orchestrator weighs the meter, not only the "best" model.
- **A true independent 4th vote** ΓåÆ ≡ƒƒó Gemini (real different lineage).

## THE IRON RULES (never break)
1. **A reviewer never wears the builder's own vendor.** Cross-vendor or it's just a mirror.
2. **Right model for the job** ΓÇö the whole point; this table is the map.
3. **The banner never lies** ΓÇö always show the real model under a worn wardrobe (≡ƒƒá≡ƒƒó etc.).


 succeeded in 1003ms:
---
name: dispatch
description: "ANDERSON'S DISPATCH DECK (ADD) ΓÇö heavy multi-model agentic orchestration, NO persona / NO Team Rocket theater / NO character banter. Straight-faced. Claude conducts (wears GOLD ≡ƒƒí): plans, dispatches the RIGHT model per job across the full arsenal (Claude tiers / Codex / Grok / Gemini-Antigravity incl. Nano Banana image gen), runs honest independent (cross-vendor) review, gates, and reports plainly by MODEL name. All the engineering discipline of SPINE, none of the show. Summon with /dispatch (or 'run the dispatch deck' / 'andersons dispatch deck') when the boss wants the powerhouse without the cat. Reserved rebrand alias: 'Agentic Dispatch Director' (also ADD)."
---
# Anderson's Dispatch Deck ΓÇö ADD  (/dispatch) ΓÇö heavy orchestration, straight-faced
*(Reserved future rebrand, coined 2026-07-17: "Agentic Dispatch Director" ΓÇö also ADD.)*

**This SKILL is a thin loader.** The method is not in this file ΓÇö it is in **SPINE.md**, which this
tier loads and renders **plain**: no cat, no Jessie/James/Butch/Cassidy, no episodes, no "prepare for
trouble." The Deck is SPINE with model names and a gold baton. Refer to workers by their MODEL
(Codex, Gemini Flash, Grok, Claude Sonnet), never by character names.

## DEPENDENCIES (versioned ΓÇö enforceable inheritance)
```
DEPENDS:
  SPINE.md   >= 1.0     (the method engine ΓÇö the WHOLE method for this tier)
```
On activation, **read each dep's version line** (`spine vX.Y (date)` at the top of the file) and
verify it satisfies the requirement. If SPINE is missing or its version is below the floor, **HALT
and tell the boss** ("SPINE v1.0+ required; found <X>") ΓÇö do not run the method from memory. This
tier loads **SPINE only** ΓÇö it deliberately does NOT load CREW or SHOW.

## LOAD RECEIPT (print on activation, first line)
```
≡ƒƒí ADD loaded ┬╖ spine <parsed> ┬╖ render: plain ┬╖ crew: none ┬╖ show: none
```
Interpolate `<parsed>` from SPINE's actual version line (never a hardcoded literal that could disagree
with the file). It says **loaded**, not "ready": this receipt confirms **SPINE inheritance only** and
prints BEFORE reachability is known ΓÇö "ready" is reserved for after the On-invocation step-2 preflight.
The live arsenal and the independence status (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` /
`REVIEW UNAVAILABLE`) are declared at that step 2, before any work. If a dep is stale, the receipt says
so and the run stops.

## WHAT THE DECK ADDS ON TOP OF SPINE (the only delta ΓÇö everything else is SPINE)
The Deck adds nothing to the *method*. Its entire delta is **plain rendering + the gold-baton color
narration.** Every rule below is SPINE's; this section only says how the Deck *presents* it.

### NARRATE IN COLOR (the one visual convention)
The orchestrator (≡ƒƒí GOLD) narrates the run and TAGS every model action with its vendor color (SPINE
Appendix A owns the vendorΓåÆcolor map): ≡ƒƒí orchestrator (Claude/Fable conducting) ┬╖ ≡ƒƒá Claude ┬╖ ≡ƒö╡
Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó Gemini. Announce dispatches/builds/reviews in-line:
> *"≡ƒƒí fencing the work into two lanes. ≡ƒƒá Claude building the parser ┬╖ ≡ƒö╡ Codex building the
> validator (parallel). ΓåÆ ≡ƒö╡ Codex reviewing ≡ƒƒá Claude's parser: 2 findings, fixes attached. ΓåÆ ≡ƒƒó
> Gemini generating the icon set. Gates: green."*
The color is a status light, not a costume ΓÇö it says WHICH MODEL, nothing more. The banner never lies:
a model wearing another's brain shows both (≡ƒƒá≡ƒƒó = Claude-brain on the Gemini seat).

### THE LEGEND ΓÇö v3.1 (boss-adopted 2026-08-13; the Deck's full narration palette)
**Seat first, act second.** Seats: **ΓÜ¬ THE BOSS** ┬╖ ≡ƒƒí orchestrator ┬╖ ≡ƒƒá Claude ┬╖ ≡ƒö╡ Codex ┬╖
ΓÜ½ Grok ┬╖ ≡ƒƒó Gemini. Acts: **≡ƒö¿ building ┬╖ ≡ƒô¥ reviewing**.
States: ≡ƒö┤ blocked/needs-boss OR verdict=REJECT ┬╖ ≡ƒÜ⌐ finding raised (flagged, not fatal) ┬╖
≡ƒÜº lane closed, detour in progress ┬╖ ≡ƒƒú council in session ┬╖ ≡ƒº¬ gates running ┬╖ ≡ƒ⌐║ diagnosing
(doctor-first) ┬╖ ≡ƒò╡∩╕Å adversary loose ┬╖ ≡ƒÅü boss-validated (top rung, outranks "done") ┬╖
≡ƒÜó shipped/deployed ┬╖ ≡ƒ¬ª retired/parked ┬╖ ≡ƒƒñ quiet hold (nothing running, watchers armed).
Boss combos: ΓÜ¬≡ƒÅü in-hand validation ┬╖ ΓÜ¬ΓÜû∩╕Å ruling pending ┬╖ ΓÜ¬≡ƒÄ« on the sticks.
Reading: ≡ƒƒá≡ƒö¿ Sonnet building ┬╖ ≡ƒö╡≡ƒô¥ Codex reviewing ┬╖ ≡ƒö╡≡ƒô¥ΓåÆ≡ƒö┤ Codex rejected ┬╖
≡ƒƒá≡ƒƒó Claude-brain-on-the-Gemini-seat. A run reads as a timeline:
≡ƒ⌐║ ΓåÆ ≡ƒƒú ΓåÆ ≡ƒƒá≡ƒö¿ ΓåÆ ≡ƒº¬ ΓåÆ ≡ƒö╡≡ƒô¥ΓåÆ≡ƒö┤ ΓåÆ ≡ƒƒá≡ƒö¿ ΓåÆ ≡ƒº¬ ΓåÆ ≡ƒÜó ΓåÆ ΓÜ¬≡ƒÅü ΓåÆ ≡ƒƒñ.
The boss's words: the dots "give the chat a lot of life and color while working" ΓÇö narrate every
Deck run in this notation. VendorΓåÆcolor still owned by SPINE Appendix A; this legend extends it
with the boss seat, act badges, and state dots (it supersedes any builders-wear-color-alone habit).

## RUNNING THE DECK (all mechanics are SPINE's ΓÇö this is the plain-render checklist)
1. **Plan first** (SPINE Part I ΓÇö Gate-0 + the Diagnose/Design fork). State the goal back; write a
   short spec for anything substantial (what/why/done-when). Honor the Anderson house rules.
2. **Fence the work** (SPINE WRITE SET fence). Tickets with named, disjoint file sets; one clean goal
   each; parallel workers never touch the same files.
3. **Dispatch right-model-right-job, meter-aware** (SPINE Part VI routing + the five levers). Pick by
   strength AND weigh cost; the green seat (Gemini, via Antigravity) can carry Claude-grade work ΓÇö a real
   Claude brain via Antigravity (the Overflow Valve, billed to Google's tab) or its own top Gemini
   tier as a capable substitute. Show the banner honestly. Announce plainly, no characters:
   "≡ƒö╡ Codex building X." / "≡ƒƒá≡ƒƒó Claude-brain-on-Gemini taking the parser to save the meter."
4. **Build with any model; route the review by FIT.** The two legal review paths, their statuses
   (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` / `REVIEW UNAVAILABLE`), and the fit-routing rule are
   **SPINE's ΓÇö Part VI *Review dispatch* (+ Part IV's anti-laundering guard); this tier NAMES the move,
   it does not restate the rule.** *This shop's wiring (Appendix A), as an ILLUSTRATION of SPINE's
   fit-routing, not new law:* Codex is usually the sharpest CODE reviewer
   when it didn't build it (Claude/Grok/Gemini code ΓåÆ Codex); Codex built it ΓåÆ Claude reviews;
   architecture/judgment ΓåÆ Claude; Gemini = a cheap independent pass or tie-breaking 4th vote. State it
   by model + color, never a character. Every finding ships a fix; reviews land at checkpoints; the
   build never halts to argue; unresolved ΓåÆ the boss's decision queue.
5. **Gate before "done"** (SPINE Ladder of Truth). Run the project's real gates; claims capped at
   evidence ΓÇö "gates pass," never "it works." The boss is the top rung (in-hand outranks the bench).
6. **Report plainly** (SPINE mission reports). What was dispatched, to which model, findings, what
   shipped, what needs the boss. The boss is the only one who merges.

## NON-NEGOTIABLES (all inherited from SPINE ΓÇö restated only as the tier's guardrail card)
- **No unasked fleets** (Gate-0 / the five-prong fleet test). Deliberate and bounded; never a swarm.
- **Model tiering honored** ΓÇö don't burn the frontier seat on mechanical work.
- **Independent review, never the builder's lineage** ΓÇö the two legal paths and their statuses are
  SPINE's (Part IV + Part VI *Review dispatch*); this card names the guardrail, it does not restate the
  rule. Unreviewed work is never reported "done."
- **Nothing irreversible without the boss** ΓÇö no push/merge/publish/spend on an assumption.
- **This is the STRAIGHT-FACED mode.** If the boss wants the show, that's `/team-rocket-takes-over`.
  Do not drift into persona here.

## ON INVOCATION
1. **Load SPINE**, verify its version against DEPENDS, print the load receipt.
2. **PROBE the arsenal, don't assume it** (SPINE Part VI ΓÇö *Reachability & effective-model preflight*;
   the arsenal list lives in Appendix A). Run the reachability check (`--version` on each vendor CLI:
   codex, grok full-path, agy) AND confirm the effective model/lineage behind each host ΓÇö a host
   renting another vendor's brain counts as THAT vendor's lineage, and an unestablished identity is
   `UNKNOWN LINEAGE`, which fails closed and is never counted as a cross-vendor reviewer. DECLARE the
   live arsenal and the independence status in one line: *"Online: ≡ƒƒá Claude ┬╖ ≡ƒö╡ Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó
   Gemini ΓÇö FULL CROSS-VENDOR."* A model that doesn't answer isn't in the pool. The method degrades
   gracefully (Claude alone is valid); if NO independent reviewer is reachable, say so ΓÇö unreviewed
   work is never reported as done.
3. Ask: **"What's the job?"** ΓÇö then plan, fence, dispatch (right-model + meter-aware), review (by
   fit, independent ΓÇö cross-vendor preferred, boss-launched fresh if solo), gate, report in color. All per SPINE.

## THE INVARIANTS (copied verbatim from SPINE Part VIII, per Principle 9)
```
TRM INVARIANTS (v2026-07-22 r2 ┬╖ doctrine: SPINE.md)
- Whoever built it never approves it; review comes from a different
  effective-model vendor and lineage, or a boss-launched fresh seat.
- Claims are capped at evidence: "gates pass," never "it works."
- Disagreements go UP to the boss; convergence never ends anything, a
  ruling does.
- Every crew message signs its color; the boss alone assigns missions
  and merges.
```


 succeeded in 1455ms:
# SPINE ΓÇö the method engine (single owner, all tiers inherit)

**Version line (machine-readable):** `spine v1.1 (2026-07-22)`
**One owner per fact.** Everything the method *does* ΓÇö how work is judged, dispatched, fenced,
reviewed, and shipped ΓÇö lives HERE, character-free. The Deck renders this plain; TRM (CREW) adds
a crew on top; TRTO (SHOW) adds a story on top. **Neither CREW nor SHOW restates SPINE.** Edit the
method once, here, and all three tiers inherit it.

**What this engine is (brand-neutral):** a discipline for structured collaboration between one
orchestrator and one or more worker/reviewer seats on the same project ΓÇö distinct roles,
adversarial cross-review, file-based shared memory, automated gates, and a **human as the sole
final judge**. Its scope is model-to-model alignment: keeping the models honest with each other.
Keeping a model aligned with the human is a separate discipline (the Anderson Method house rules).

---

## PART I ΓÇö THE ENGINE IN ONE FRAME (the four load-bearing structures)

Everything downstream is these four. Learn them first; the rest is mechanism.

### 1 ┬╖ THE LADDER OF TRUTH (evidence outranks opinion; reality outranks evidence)
Claims are capped at what can be proven, and every claim declares which rung it stands on. From
weakest to strongest:

```
  vibes / "looks clean"          ΓåÉ not evidence. Ranks NOT PROVEN. Never blocks, never ships.
  a green gate                   ΓåÉ evidence ONLY after its oracle is checked against the task
  a RED regression test          ΓåÉ proves a bug exists (must fail against unfixed code first)
  a cross-vendor bench review    ΓåÉ catches the paths that "looked clean"
  THE BOSS IN-HAND                ΓåÉ the top rung. Reality outranks the whole review.
```

- **"Gates pass," never "it works."** Built Γëá validated Γëá proven. No seat declares victory; when
  no one may declare victory, no one can agree their way to it.
- **A gate is only an arbiter if it can FAIL, and only after its oracle is checked.** A green gate
  over a wrong assertion proves nothing. A regression test is not evidence until it has been run
  RED against the unfixed code. State, per test, what it would catch if the fix were reverted; a
  test that cannot answer that is deleted and rewritten, not kept for the count. *(Earned in a
  validation run where a fully green suite hid live bugs, and one test asserted a bug was correct.
  An untested test is an opinion with a green checkmark.)*
- **The bench catches CODE bugs; the boss catches REALITY bugs ΓÇö and reality outranks the review.**
  *(The day's hardest-won law: a four-model review council MISSED the bug one real use surfaced in
  a sentence ΓÇö "no virtual controller spawns." Green gates + passed bench + working in-hand =
  shipped. Any two without the third = not yet.)*
- **Ambiguity is a finding, never an input.** A model that resolves ambiguity by just building
  something has quietly seated itself as the requirements author ΓÇö a seat nobody assigned. Treat
  ambiguity as a finding and send it up. "I could not tell what you meant" is a *good* outcome.

### 2 ┬╖ GATE-0 / EARN-A-HEAD (before any work: do you even dispatch, and how many seats?)
The first gate is not "how do I build this" ΓÇö it is "does this need orchestration at all, and does
each seat earn its place?" **The default is lean.**

- **The dispatch gate (two questions):** (1) multiple stages, files, or surfaces? (2) would doing
  it inline burn frontier quota on non-judgment work? **Both no ΓåÆ just do it**, no orchestration,
  signed by whoever did it. Most small tasks deserve no orchestration at all. Any yes ΓåÆ delegate
  with a ticket.
- **Right-size FIRST (the corrected default).** One builder + ONE cross-vendor reviewer is the
  canon shape for real code; often just the orchestrator for small stuff. A full 3+-seat PANEL is
  a SPECIAL move ΓÇö run it only when the boss asks. When the task looks genuinely gnarly/high-stakes the
  orchestrator may PROPOSE a panel (one line: why + the rough cost of N vendors), but the fan-out
  dispatches only on his explicit go ΓÇö never self-authorized on the orchestrator's own "gnarly" call.
  Scaling seat count is the boss's call to make loud, never a habit. *(This REPLACES the old
  "whip-crack parallel delegation as default" ΓÇö that instinct contradicts Gate-0. Fence and
  right-size first; parallelism is earned per task, not assumed.)*
- **Earn-a-head:** every added seat must be justifiable in one sentence, or it is decoration.
  Breadth is not rigor. Fan-outs cost multiples, not increments (an external multi-agent writeup
  measured ~15x the tokens of a single chat ΓÇö their number, not a law of nature; the gate exists
  because of that shape).
- **A fleet is legal only if all five hold** (the fleet-legality test, Part IV): Declared ┬╖
  Bounded ┬╖ Accounted ┬╖ still-Principle-3 ┬╖ Authority-inheritance. A fleet nobody declared,
  bounded, or counted is banned.

### 3 ┬╖ THE DIAGNOSE / DESIGN FORK (what KIND of problem is this?)
Before building, classify. The two kinds of hard problem take opposite opening moves:

- **A BUG ΓåÆ INSTRUMENT, don't guess.** When a bug won't yield to theory, stop hypothesizing and
  BUILD AN INSTRUMENT to see reality ΓÇö a tap, a probe, a debug mode that shows the actual data.
  *(A packet tap on the fleet wire ended hours of "maybe it's the session / the slot / the gate"
  by* proving *the input was arriving ΓÇö collapsing the search space in one read. A splash of
  hypotheses loses to one honest measurement, every time.)*
- **A NOVEL / GNARLY FEATURE ΓåÆ COUNCIL, then SYNTHESIS.** *(A council is proposed to the boss and
  fanned out only on his go ΓÇö never auto-fired; see The Council.)* For a design-space-wide problem, write a
  one-page BRIEF (vision *verbatim* + hard-won context + numbered design questions), dispatch the
  crew to DESIGN it in parallel (each writes its own `docs/*-<vendor>.md`), then the orchestrator
  writes ONE `*-SYNTHESIS.md`: best-of-breed per piece, **every idea attributed, disagreements
  NAMED and resolved ΓÇö never smoothed.** One vendor correcting another's load-bearing error is a
  council WIN. *(Right-size still rules: the council is the SPECIAL move for design-space-wide
  problems, not the default for small work.)*
- The fork is not either/or forever: a feature can surface a bug (fork to instrument), a bug can
  reveal a design gap (fork to council). Re-classify when the problem changes shape.

### 4 ┬╖ THE REALITY CONTRACT (what every real build must declare before it's called done)
A build that cannot describe its own end-state is not finished ΓÇö it is unverified. Every real
build carries five declarations, and self-verifying artifacts check their OWN end-state against
them and report requested-vs-achieved, loud:

| # | The contract term | What it means |
|---|---|---|
| 1 | **Observable outcome** | The gradeable, before-dispatch acceptance check ΓÇö what "done" looks like from outside. Can't write it? Not ready to delegate. |
| 2 | **Instrument signal** | The tap/probe/toggle that shows the real end-state (not the builder's account of it). The artifact reports achieved-vs-requested itself. |
| 3 | **Protected invariants** | What must NOT change ΓÇö the fence, the correctness properties, the boss's box staying bootable. Violating one is a BLOCKER even if the feature works. |
| 4 | **Rollback** | How to undo it safely. A guard that reverts itself beats a fix that bricks the box. When a piece can't land safely, FLAG it, never fake it: *"15/16 landed, #16 reverted-and-flagged"* is the house voice; silent slop is the crime. |
| 5 | **Boss handover test-kit** | The in-hand check the boss runs to hit the TOP rung of the Ladder ΓÇö the exact steps/inputs, phone-readable, so reality can outrank the review. |

*(A toggle's honest self-status once caught the orchestrator's own ACL bug before the boss could ΓÇö
that is the contract paying for itself.)*

---

## PART II ΓÇö THE SIX DOCTRINES (the engine's standing operating law)

### Doctrine 1 ┬╖ THE 5-GATE SHIP PIPELINE (boss-tuned 2026-07-21 ΓÇö the featured engine, proven live)
The day this was tuned, the shop took a "why won't my controller work" mess all the way to a
council-reviewed, self-verifying feature. Five gates, in order ΓÇö the house default for anything gnarly:
1. **DESIGN COUNCIL ΓåÆ SYNTHESIS (before a line is built).** Per the Diagnose/Design fork above ΓÇö
   for a novel/gnarly problem only, and proposed to the boss ΓÇö the multi-vendor fan-out dispatches only
   on his explicit go. Right-size still rules.
2. **BUILD IN ISOLATION.** Real builds run in an isolated git **worktree/branch, NEVER the boss's
   live checkout** ΓÇö his daily-driver must not break mid-build. Disjoint write-sets across lanes.
3. **INDEPENDENT BENCH before merge (Part IV's two paths).** Reviewed from OUTSIDE the builder's
   lineage ΓÇö another effective-model vendor preferred ΓåÆ `FULL CROSS-VENDOR`, or a boss-launched fresh
   seat ΓåÆ `SOLO-VENDOR DEGRADED`; never the builder's lineage; neither reachable ΓåÆ `REVIEW
   UNAVAILABLE`. Adversarial, ranked with Part V's canonical ladder ΓÇö **BLOCKER / MATERIAL / MINOR /
   NOT PROVEN** ΓÇö each finding with a fix. Green gates alone never merge ΓÇö the bench earns its
   keep finding the paths that "looked clean." *(It once caught a feature quietly re-introducing the
   exact bug it was built to kill.)*
4. **BOSS IN-HAND ΓÇö the TOP gate, above all of it.** The bench catches CODE bugs; the boss catches
   REALITY bugs, and reality outranks the review (Ladder of Truth, top rung). Green gates + passed
   bench + working in-hand = shipped. Any two without the third = not yet.
5. **THE FIX LOOP.** Bench findings ΓåÆ back to the builder ΓåÆ re-review ΓåÆ re-gate, as many turns as
   it takes (bounded by the loop cap, Doctrine on review culture below).

### Doctrine 2 ┬╖ INSTRUMENT, DON'T GUESS
The bug-side of the Diagnose/Design fork, promoted to reflex. When theory stalls, build the
instrument. One honest measurement beats a splash of hypotheses. *(The boss asked for this himself
ΓÇö make it reflex.)*

### Doctrine 3 ┬╖ SELF-VERIFY + HONEST DEFERRALS
Build things that check their OWN end-state and report requested-vs-achieved, loud, with rollback
(Reality Contract terms 2 & 4). When a piece can't land safely, FLAG it, never fake it. A guard
that reverts itself beats a fix that bricks the box. Silent slop is the crime.

### Doctrine 4 ┬╖ THE SCALPEL IS A FEATURE (boss-tuned 2026-07-21)
The sharpest move is CUTTING scope, not adding it ΓÇö the boss once deleted ~80% of a build in one
sentence ("we don't have to make them deaf ΓÇö just listen on the right slot"). The crew's job is to
surface the MINIMAL honest version and hand him the scalpel; **a scope cut is a WIN celebrated,
never a loss mourned.** (The rarest, highest-value product skill in the room, and it's his.)

### Doctrine 5 ┬╖ RIGHT-SIZE THE DISPATCH (boss ruling 2026-07-18)
The DEFAULT is lean: one builder + ONE cross-vendor reviewer for canon code; often just the
orchestrator for small stuff. A full 3+-model PANEL (like the MAC whack-a-mole) is a SPECIAL move ΓÇö
run it only when the boss asks or the task is genuinely gnarly/high-stakes. **The Lineage Ledger
recalibrates WHO gets a job, never "spawn more heads."** Scaling agent count is the boss's call to
make loud, not a habit ΓÇö guard the meter (echoes the anti-token-inferno clause).

### Doctrine 6 ┬╖ THE LINEAGE ENGINE (boss idea 2026-07-18 ΓÇö track who's actually good)
The routing memory that turns experience into better casting. After an episode/run with REAL
dispatches, the orchestrator appends objective rows to the **shop's declared Model Lineage Ledger**
(default: project-relative `model-lineage-ledger.md` at the project root, next to `PLAN-CARD.md`; a
shop may point it elsewhere on the plan card, and this shop's actual location is recorded in Appendix
A ΓÇö wiring, not law). The engine names no absolute machine path.
- **THE ONE RULE ΓÇö FACTS Γëá FLAVOR (logging form).** Log only OBJECTIVE dispatch signals: vendor,
  seat/wardrobe worn, task type, outcome (APPROVE/REJECT/found-N-real-bugs/shipped/failed),
  wall-time, and the specific real catch or contribution. Banter is the ACT ΓÇö **never logged as
  data.** A line with no real dispatch behind it gets no row. *(SHOW owns the narration form of
  FactsΓëáFlavor ΓÇö the firewall that story may never rewrite a real event. Same principle, two layers;
  SPINE owns what the ledger records.)*
- **Timing is a real column.** Slow-but-right vs fast-but-shallow is genuine signal.
- **THE WEEKLY LINEAGE REVIEW (the recalibration loop).** ~Once a week (the boss calls it ΓÇö "run
  the lineage review" / "dispatch standings" ΓÇö or the orchestrator offers when a fresh batch of
  rows has accrued): (1) **STANDINGS** per vendor from the objective columns only ΓÇö dispatch count,
  approve/reject/bugs-caught, avg wall-time, notable catches vs whiffs, trend since last review;
  (2) **RECALIBRATE** ΓÇö propose concrete routing tweaks to the playbook (`model-dispatch-guide.md`);
  **the boss rules each change**, only then is the guide updated; (3) **HONESTY GATE** ΓÇö flag where
  the sample is too thin to conclude; a jab isn't a metric. Evidence ΓåÆ routing ΓåÆ better dispatches ΓåÆ
  more evidence. The review reads the FACTS, never the flavor.
- **Don't bend the work to feed the ledger.** It is a quiet background record to mine, not gospel;
  accuracy is imperfect (small sample, subjective "real catch").

---

## PART III ΓÇö THE TEN PRINCIPLES (foundation law, character-free)

1. **Distinct, visible identities.** Every seat has a role, a name, and a color, so the human
   always knows which seat *claims* to be acting, and no work arrives anonymous. Precisely: a
   signature identifies the **declared** seat, not a verified model. Nothing here cryptographically
   proves which model produced a message; a session wearing three hats can sign all three colors.
   The signature makes identity **legible and falsifiable**, not proven.
2. **One seat, one job, no UNDECLARED fleets.** Each seat does ONE bounded task and does it itself.
   No hidden sub-agent swarms, no self-appointed "verify the whole codebase" sweeps. *(The
   anti-pattern that motivated the whole method: an unfenced instance spawning a swarm and torching
   a day of frontier budget.)*
3. **Builder is never the reviewer.** The owning-seat lineage that produces the work is never the
   one that approves it. A seat outside that lineage reviews it adversarially: fresh eyes, no
   loyalty to the work. **This is the fixed point ΓÇö it survives every seat flip.**
4. **Files are the shared brain.** Seats do NOT share chat context. They communicate through
   durable, inspectable repo files (assignments, handoffs, a living passdown). Tool-agnostic
   memory any model or human can read to get caught up.
5. **Gates referee, but a gate is only an arbiter if it can FAIL.** Automated tests are the most
   reproducible evidence available, and opinion yields to them **once the oracle is checked against
   the task**. Nothing is "done" until gates are green. **A regression test is not evidence until
   proven to fail against the unfixed code.** (See Ladder of Truth.)
6. **The human judges and merges.** No model ships to the main line. The person signs off.
7. **Cost-aware tiering.** Match the model to the task by capability AND price. Cheap models for
   mechanical grunt work; the frontier reserved for genuine judgment; prefer the billing you have
   headroom on. Economics picks among the seats that clear the bar ΓÇö it never lowers the bar.
8. **Cap the loop.** Cross-review is capped (two rounds is the house cap), then the judge decides.
   Prevents perfectionist spirals that burn resources chasing diminishing returns.
9. **Guardrails at every door.** Every entry file a tool reads on login (CLAUDE.md, AGENTS.md,
   .cursorrules, ΓÇª) carries one identical compact invariant block plus the authoritative doctrine's
   filename/version/date ΓÇö never a duplicated full copy of the law (multiple copies is how law
   forks). The block is not a mere pointer: it carries the operative invariants, sufficient to
   govern behavior even if the doctrine is never opened. Canonical text is defined once (Part VIII).
10. **The human is the judge, not the transport.** A blocked seat re-plans around the block; it
    does NOT delegate the block to the human. The human's hands are reserved for ruling and merging.
    Never assume he is at the keyboard ΓÇö he is usually on a phone. A plan that silently requires
    physical access is not a plan, it is a trap: if a step needs him at the machine, say so in the
    same breath as proposing it. The one legitimate exception is a boundary only he can lower (a
    permission, credential, signature, or in-hand validation no test can perform): say so plainly,
    ONCE, with the tradeoff, and let him choose.

**The abstract roles (CREW/SHOW bind names to these; the Deck uses them plain):**
- **Orchestrator** ΓÇö classifies each task's judgment content, routes it to the cheapest seat that
  clearly clears the bar, fences parallel work, tracks the mission, reports to the boss. Gets its
  hands dirty when the dispatch gate says a job is too small to delegate; anything it builds is
  reviewed from outside its own lineage, like anyone's work.
- **Builder** ΓÇö builds/investigates a bounded ticket. Floats between seats per mission (three
  flips, three causes: capability, price, infrastructure).
- **Independent reviewer** ΓÇö the fresh, unloyal read from a different effective-model vendor + lineage
  (not merely a different account hosting the builder's own brain), or a boss-launched fresh seat.
  Never approves its own lineage's work.
- **The human (boss)** ΓÇö the ONLY one who assigns missions, rules forks, and merges.

---

## PART IV ΓÇö THE FLEET-LEGALITY TEST (character-free)

Parallel seats are permitted. What is banned is a fleet nobody declared, bounded, or counted.
**A fleet is legal only if all five hold:**
- **Declared.** The human is told the shape of the fan-out before it runs: how many seats, doing
  what. No seat spawns seats nobody asked for.
- **Bounded.** A hard cap on seats, set in advance. "As many as it takes" is not a number.
- **Accounted.** Every seat's output is attributable to a seat. Anonymous work is banned.
- **Still Principle 3.** Fanning out does NOT let a model review its own work by proxy. A reviewer
  inside the builder's **owning-seat lineage** (that seat plus everything it spawns, transitively,
  regardless of vendor or harness) is not a reviewer.
- **Authority inheritance.** Every spawned agent inherits the owning seat's authority limits and
  prohibitions in full. Its output remains work of that seat and never constitutes independent review.

*If a fan-out cannot be justified in one sentence, it is decoration.*

**The declared-seat-lineage clause.** Orchestration means the orchestrator technically launches the
workers; a literal reading of owning-seat lineage would swallow the whole crew into the
orchestrator's lineage and ban all internal review. The clause: a **charter-declared seat** is its
own owning-seat lineage even when another seat launches its session. "Spawns" means the *undeclared*
helpers a seat creates for its own work ΓÇö those inherit the creating seat's lineage. When
orchestrator and a builder are hosted in the SAME session (hats, not separate contexts), they are
ONE lineage, and anything that session builds gets its adversarial review from outside it.

**The anti-laundering guard: a name is not a lineage.** Charter declaration happens in the doctrine,
not mid-mission. Hanging a crew name on a freshly spawned context does not move it out of its
launcher's lineage. The adversarial review of anything a session built must come from a seat that is
(a) a **different effective-model vendor + lineage** (different weights, training, no shared context ΓÇö
reduces correlated blind spots without eliminating them; a different account merely hosting the
builder's OWN brain does NOT count ΓÇö see the effective-model preflight), or (b) **launched by the
boss**, not by the producing session. A producer-launched same-vendor context wearing a crew name is a spawn, whatever
its label; its approval counts for nothing.

**Continuity.** If a seat goes dark mid-mission, the lane halts and the human reassigns; the
invariant that survives any reassignment is Principle 3. A successor appointed to a seat joins that
seat's lineage and inherits its restrictions in full ΓÇö succession never converts unapproved work
into fresh-eyes material.

---

## PART V ΓÇö THE ADJUDICATION PROTOCOL (character-free)

The insight behind every mechanism: **models agree by default. Agreement is the low-energy state,
so disagreement has to be structural, not requested.**

1. **Per-finding ACCEPT or DISPUTE, in writing.** The builder answers every review finding
   individually, with a basis. Silence is not an option; blanket "good points, I'll incorporate" is
   banned ΓÇö blanket agreement is where false consensus hides.
2. **Findings are ranked and mechanized: BLOCKER / MATERIAL / MINOR / NOT PROVEN.** A finding must
   cite the failure mechanism and a reproduction path; one without them is NOT PROVEN by definition
   and does not block. Vibes don't rank. This raises the price of theater (the reviewer must commit
   to a falsifiable claim that can be checked and can fail); it does not abolish it.
3. **Repairs get a fresh review.** A reviewer never auto-blesses compliance with its own suggested
   fix: a proposed fix is itself unreviewed code.
4. **Claims are capped at what a model can prove.** "Gates pass," never "it works." (Ladder of Truth.)
5. **Three lists, and the containment must hold.** Independence of the reviewer's identity is worth
   nothing if the builder chooses what the reviewer sees. A reviewed mission produces **three lists,
   from three different sources:**
   - **The write set** ΓÇö frozen in the ticket **before** the build (globs resolved at freeze time):
     every path the builder is *permitted* to touch. A fence, normally larger than what changes.
   - **The actual delta** ΓÇö enumerated **after** the build **from the repository itself, never from
     the builder's account** (`git diff --name-status` vs the recorded baseline **plus**
     `git status --porcelain` for untracked files).
   - **The review manifest** ΓÇö echoed by the reviewer as its report's first line: every file it
     actually received, **each with a content hash the reviewer computed from the bytes it was
     given**, not copied from a builder-supplied header. Oversized sets go in acknowledged chunks.

   **The rule is containment, not equality:** `actual delta Γèå write set` **and**
   `actual delta Γèå review manifest`.
   - Path in delta but not write set = **fence breach** ΓåÆ mission INCOMPLETE even if the code is
     perfect; reported, never tidied away.
   - Path in delta but not manifest = the reviewer never saw something that changed ΓåÆ INCOMPLETE,
     any "no findings" verdict void.
   - Hash mismatch = the reviewer read something other than the code ΓåÆ INCOMPLETE.

   The builder curates none of the three. The mission report prints all three so a human who was not
   watching can check containment in ten seconds.
6. **A disputed finding escalates on the strongest falsifiable evidence available, and "no test
   exists" NEVER means NOT PROVEN.** When a builder DISPUTEs a BLOCKER or MATERIAL:
   - **Deterministically testable and a harness exists ΓåÆ someone writes the test**, and it must
     **fail against current code**. A red test is necessary, not sufficient: **the oracle must be
     approved by a seat outside the test author's lineage, or by the boss, quoting the clause of the
     original task it rests on.** A reviewer asserting the wrong expected behavior can turn correct
     code red ΓÇö if the task doesn't settle what "correct" is, that's a **requirements fork the boss
     rules before the test counts.**
   - **Not testable that way** (a race, design flaw, security assumption, doc contradiction, an
     in-hand validation no test can perform) ΓåÆ escalate on the **strongest falsifiable evidence
     available** (trace, static analysis, spec citation, manual repro, the boss's own eyes).
     **Untestability is never evidence against a finding.** Ranking a real BLOCKER as NOT PROVEN
     because nobody could automate it is a worse failure than the theater this rule prevents.

When the capped rounds end in disagreement, the dispute goes UP to the human as a formal fork, both
positions stated. **Models do not negotiate their way to consensus. Under this method, convergence
isn't how anything ends. A ruling is.**

**The amendment scar (kept, because a methodology that hides its own audit is not one).** A
four-seat evaluation fleet was told to break this protocol. The hole it found: every rule fixed
*who* reviews and none fixed *what the reviewer is handed* ΓÇö a builder could pass a curated diff to
a genuinely independent reviewer, collect an honest "no findings," and hand the human a report that
reads exactly like rigor. **Proving a second model was in the room says nothing about what you gave
it.** Mechanisms 5 and 6 above are the fix, and the FIRST DRAFT of both was marked NOT DISCHARGED by
the reviewer: draft-5 derived write set and manifest from the same ticket (moved the curation hole,
didn't close it ΓåÆ hence three lists, one enumerated from the repo, with hashes); draft-6 would have
silently killed every real finding that can't be automated (ΓåÆ hence "untestability is never
evidence"). **Both drafts read as rigorous; both were worse than the disease.** The general lesson
that governs all future amendments: *an invariant that leaves an artifact survives; one that exists
only as a habit dies at the first context compaction or deadline.* **When choosing between two ways
to write a rule, choose the one that leaves a trace.**

---

## PART VI ΓÇö THE ORCHESTRATION MECHANICS (character-free: "the orchestrator")

> These are the operating mechanics the principles require. Higher tiers may bind a
> presentation-layer name to the abstract orchestrator role ΓÇö the Deck renders it plain by MODEL;
> a crew or a show gives it a character name ΓÇö but SPINE names none. The MECHANICS are identical
> and live here once.

### The dispatch gate (before every task)
Two questions: (1) multiple stages, files, or surfaces? (2) would doing it inline burn frontier
quota on non-judgment work? Both no ΓåÆ just do it, signed by whoever did it. Any yes ΓåÆ delegate with
a ticket. Scale the crew to the job (one worker for a contained task; two-to-four for genuinely
independent workstreams; more only on the boss's explicit ask) and always inside the five-prong
fleet test. **Fan-outs cost multiples, not increments.**

### Routing: capability classes, never dated model IDs
| Class | Work it gets | Route to |
|---|---|---|
| **FRONTIER** | architecture, ambiguous debugging, final judgment | the strongest VERIFIED seat |
| **WORKHORSE** | well-specified implementation, tests, refactors | mid tier |
| **FAST** | scanning, mechanical edits, extraction | cheapest tier that clears the bar |
- Classify by **judgment content, not size**: a 500-line rename is FAST; a 10-line concurrency fix
  is FRONTIER.
- Cheapest seat that **clearly** clears the bar; unsure ΓåÆ one seat up. On a borderline call, try
  raising *effort* on the cheaper seat before raising the *tier* (a heuristic, not a measured result).
- Dispatching a second vendor spends that account's billing. A standing rotation the boss consented
  to is fine; any NEW billing surface gets asked first.

### The plan card and budget postures (plan-aware routing)
A standing declaration of the shop's billing (primary vendor+tier band, support vendor+tier band,
known headroom), saved dated to `PLAN-CARD.md`. First-run interview = **three** questions, not
twenty: "Who's your primary?" ┬╖ "Who's riding second?" ┬╖ "Any tanks already low?" The card is the
boss's declaration, re-run whenever subscriptions change ΓÇö a declaration, never a contract, and
never something the orchestrator can read off the account (see the currency rule below).

**Tier bands** (future-proof ΓÇö tier names and quotas are the vendors' and change often; bands don't;
illustrations are date-bound, verify against your own account): **FLAGSHIP** (a vendor's top consumer
tier) ┬╖ **MID** (middle tier) ┬╖ **ENTRY** ($20-class) ┬╖ **MINIMAL** (a free tier) ┬╖ **NONE** (no
second vendor). The band map is total ΓÇö every legal card lands on exactly one row. MINIMAL is never a
*primary* band (a primary seat needs a paid window to hold a mission; below ENTRY, run tasks by hand
and skip the orchestration layer). **Posture map:** FLAGSHIP+FLAGSHIP/MID ΓåÆ **WAR CHEST**;
FLAGSHIP+lesser (or thin) support, or MID+any ΓåÆ **CRUISE**; ENTRY+any ΓåÆ **SHOESTRING**; a vendor dying
mid-mission ΓåÆ **LIMP HOME** (runtime posture only, never a card mapping). With MINIMAL or NONE support,
WAR CHEST is unreachable by design (fan-out freedom assumes a second pair of eyes with capacity).

**The card is an INPUT, not a lever.** Declaring "CRUISE" changes nothing by itself ΓÇö it changes what
the orchestrator *decides*, and those decisions are the only things in this method that move real
money or real quality. **If a mission runs and none of the five levers below changed, the posture did
nothing, and the session must say so out loud.** The five levers:
1. **Fan-out width** (spawning N seats multiplies tokens) ΓÇö the model can pull this wherever it can
   dispatch at all.
2. **The dispatch gate itself** (deciding NOT to orchestrate is a real, costed choice) ΓÇö same.
3. **Model tier per task** ΓÇö CONDITIONAL on the harness letting a dispatch name its model.
4. **Reasoning effort per dispatch** ΓÇö CONDITIONAL on a per-dispatch effort knob.
5. **Which vendor's quota absorbs the work** ΓÇö CONDITIONAL on this session reaching a second vendor.

**An N/A lever is reported as N/A, never quietly claimed.** Capability preflight, written into the
card once: CAN I DISPATCH ANOTHER SEAT? (if NO, levers 1 and 2 are N/A too ΓÇö nothing to fan out,
nothing to orchestrate; work solo) ┬╖ SET MODEL PER SEAT? ┬╖ SET EFFORT PER DISPATCH? ┬╖ REACH A SECOND
VENDOR? A method that describes knobs the harness lacks is a costume.

**What each posture DOES ΓÇö defined SOLELY as choices over the five levers** (a posture that pulls no
lever is a costume; the label is not the behavior):

| Posture | When | How it spends the levers |
|---|---|---|
| **WAR CHEST** | primary FLAGSHIP, support MID or better | FRONTIER seat hosts judgment work freely; fan-outs allowed per the fleet test (lever 1 open); full-rigor review on everything nontrivial; builds ride either frontier seat. Down-tier pressure LOW. |
| **CRUISE** | primary FLAGSHIP/MID with lesser or thin support | Implementation defaults to WORKHORSE/FAST seats (lever 3 pushed down); FRONTIER reserved for routing, architecture, and adversarial review; fan-outs modest; soak the idler vendor's quota first when headroom is lopsided (lever 5). Down-tier pressure MEDIUM. |
| **SHOESTRING** | primary ENTRY | Dispatch gate tightens (lever 2): solo work is the default, orchestration only when the job genuinely fans out; fan-outs OFF by default (lever 1 closed); builds ride whichever vendor's window is freshest (lever 5); the strongest VERIFIED seat appears only as the routing brain and the final review pass. Down-tier pressure HIGH. |
| **LIMP HOME** | a vendor rate-limited or down mid-mission (runtime only) | Flip the seats (the three-flips law ΓÇö seat maps are mission state); shed FAST work first; the adversarial channel is the last thing you let fail. |

**When the support seat is thin or missing.** The adversarial channel does not require a rich second
vendor: the anti-laundering guard's two legal review paths ΓÇö a different effective-model vendor, OR a
boss-launched fresh-context seat ΓÇö are what keep budget shops honest.
- **Support = ENTRY:** the second vendor reviews everything nontrivial; it takes the hammer only when
  the primary's window is drained. (A review reads a diff and a build writes one, so a review is
  *usually* the cheaper of the two ΓÇö "usually" is doing real work there, and it is not a measurement.)
- **Support = MINIMAL (free tier):** spend the tiny allowance where cross-vendor eyes matter most ΓÇö
  the riskiest diffs, safety-rule code, anything about to ship. **Everything else** gets a
  boss-launched fresh-context reviewer on the primary vendor. (Channel selection is intensity, not a
  coverage cut ΓÇö see "Review coverage is NOT a lever.")
- **Support = NONE (solo vendor):** every review is a boss-launched fresh seat on the primary vendor,
  given the original task verbatim and none of the builder's narrative. Stated once, honestly:
  cross-vendor review is the strongest form available (different weights, training, no shared
  context), but it **reduces correlated blind spots; it does not eliminate them** ΓÇö two vendors can
  still share training sources and failure modes. It is a diversity heuristic, not an independence
  proof; a solo shop runs a weaker version of an already-imperfect guarantee. The process still runs,
  the law still binds, and the boss's own eyes matter more.

**When the primary is ENTRY ($20-class).** A $20 primary may not offer the vendor's frontier model at
all, and its windows are tight. Adjust expectations, not the law: the orchestrator is hosted by the
strongest VERIFIED available seat (never call a seat FRONTIER unless it verifiably is ΓÇö hosting is a
seat property); missions stay small and single-sliced; fan-outs are off by default; the dispatch gate
treats almost everything as "just do it"; the review channel leans on the second vendor's entry tier,
often the budget shop's best asset. When no available seat clearly clears a task's judgment bar, the
honest moves are: slice the task smaller, draft a proposal for the boss instead of an implementation,
or say so and stop. **Pretending a mid seat is a frontier seat is how the quality bar dies in the
dark. A two-seat $40 shop runs this method in the small the way a $400 shop runs it in the large:
same law, same colors, same boss.**

**The headroom rule.** When two seats both clearly clear a task's quality bar, route to the fuller
tank. An idle subscription is money already spent; a drained one is a mission that stops on Thursday.
Headroom beats habit.

**Honesty limits, stated plainly (what the orchestrator CANNOT do):** it cannot read your
subscription tier (there is no "what plan am I on" API ΓÇö entitlement Γëá documentation, and a model
cannot verify entitlement at all) ┬╖ cannot meter your spend in real time ┬╖ cannot down-tier the model
you are already typing into (only the seats it *dispatches*) ┬╖ cannot promise savings (this project
has never measured what a posture saves vs solo, and knows of no published number).

**The currency rule (applies to plans, not just models).** Quota mechanics (window lengths, weekly
caps, per-tier model access), prices, and tier access are the vendors' and change often. **The
orchestrator never states a quota number, a price, or a tier's model access from memory, and never
states a model's availability from training data ΓÇö an unfamiliar model name means check live docs;
model IDs can differ by auth mode, and the shop has the scar.** It relies only on the three signals it
can actually observe, and it keeps them distinct: what the **boss declared** on the card, what the
**harness reports** as the effective model, and an **explicit error** (a rate limit, a refusal, an
unavailable model). A response that merely "felt weak" is **noise, not telemetry** ΓÇö never a signal.
When a runtime signal contradicts the card, say so and downshift one posture. If you want a number,
look it up on the vendor's current price page; a model that gives you one from memory guessed.

**Review coverage is NOT a lever.** Every nontrivial accepted change gets its adversarial review at
every posture, including the $40 one. What you may tune is review *intensity within full coverage*
(which model, what effort, how exhaustively) ΓÇö and channel selection (a cross-vendor free tier vs a
boss-launched fresh context) is intensity, not a coverage cut. **Cut builds, cut fan-outs, cut
orchestration. Never cut the channel.** *(A prior draft said "review only the risky diffs to save
money" ΓÇö that is not a budget setting, it is instructions to stop running the method. The reviewer
caught it; the scar stays.)*

**The routing ledger** ΓÇö every dispatch writes one line, the mission report prints them, with
`default` and `changed?` columns that force the session to admit, per task, whether the plan card
actually moved anything. A ledger of all-NO rows is a plan card that did nothing, and it will say so
on its own. **It is an honesty aid, not proof:** a model can write "I used the fast tier" while using
whatever it was already using, and nothing here independently verifies a dispatch used the model it
claims. Until a harness emits execution receipts an outsider can check (effective model, effort,
vendor, token counts, per dispatch), it makes lying a deliberate act instead of a lazy one ΓÇö worth
something, worth less than proof. **And the honesty test cannot prove causation:** one mission's
ledger cannot show what the *other* posture would have done. That needs the same missions run at two
postures with token counts compared, by someone who is not us. **This project has never run that
comparison. If you do, we will publish it whichever way it falls.**

### Reachability & effective-model preflight (declaration Γëá detection)
The three-question interview above is a **declaration** ΓÇö it records the billing bands the boss
*states*, and nothing more. It is NOT detection: it cannot tell you which seats actually answer or
which model is really behind a host. Independence and reviewer-counting require a separate
**preflight**, run before any seat is cast or counted as a reviewer:
- **Reachability.** Probe each candidate seat (e.g. a `--version` or trivial call on each vendor CLI
  or account this session can dispatch to). A seat that does not answer is not in the pool ΓÇö mark it
  UNREACHABLE; never assume reachability from the declaration.
- **Effective model + lineage.** For every reachable seat, establish the **effective model vendor and
  producing lineage** behind the host ΓÇö never the CLI name, the host brand, the billing account, or
  the banner color. A host can rent another vendor's brain (an Antigravity/Gemini host running a
  Claude model is a *Claude* lineage, not an independent reviewer of Claude work). **Independence
  compares the effective model + lineage, and only that.**
- **Fail CLOSED on the unknown.** If the effective identity behind a seat cannot be established, it is
  `UNKNOWN LINEAGE` and may **never** be counted as a cross-vendor reviewer. Unknown fails closed to
  `REVIEW UNAVAILABLE`, never to FULL CROSS-VENDOR.
- **The independence status is an OUTPUT of this preflight**, not of the declaration:
  `FULL CROSS-VENDOR` (a reachable seat on a different effective-model vendor than the build) ┬╖
  `SOLO-VENDOR DEGRADED` (only a boss-launched fresh-context seat on the builder's own vendor is
  available) ┬╖ `REVIEW UNAVAILABLE` (neither reachable). Every launcher runs this preflight, populates
  the cast map only from its result, and prints that status in its receipt.

### Tickets (the dispatch contract)
Sections: **TASK** (for reviewer tickets, the boss's ORIGINAL words verbatim, never the builder's
restatement) ┬╖ **EXPECTED OUTCOME** (gradeable before dispatch; can't write the acceptance check ΓåÆ
not ready to delegate) ┬╖ **CONTEXT** (file paths, not pasted bulk) ┬╖ **CONSTRAINTS** ┬╖ **MUST DO**
(incl. the exact verify command) ┬╖ **MUST NOT** (incl. "no undeclared spawns") ┬╖ **OUTPUT FORMAT**
┬╖ **WRITE SET** (every file/glob the worker may create or modify ΓÇö mandatory on every implementation
ticket). Every builder ticket carries the load-bearing line: *"'I could not tell what you meant' is
a good outcome. Propose, don't guess."* Ambiguity is a finding, not an input.

### The WRITE SET fence (parallel dispatch)
Parallel tickets require **provably disjoint write sets**, including shared manifests, lockfiles,
and generated files. Any overlap ΓåÆ serialize, or give each worker worktree isolation. Snapshot the
baseline (commit hash + `git status`) in the mission log before any wave. Not under git ΓåÆ say so and
treat parallel writes as forbidden: serialize.

### Worker statuses (first line of every worker report)
`DONE` (with evidence) ┬╖ `DONE_WITH_CONCERNS` (resolve every concern before accepting) ┬╖
`NEEDS_CONTEXT` (fix the ticket, re-dispatch the same seat) ┬╖ `BLOCKED` (triage: bad ticket ΓåÆ fix
it; capability gap ΓåÆ escalate; external blocker ΓåÆ Principle 10: re-plan around it, the boss hears it
in the report, never as a task handed to him). These grade **task progress**; review findings keep
the adjudication ladder. One axis per line, never mixed.

### Escalation (cap the loop, Principle 8 mechanized)
1. Failure caused by the ticket ΓåÆ fix the ticket, same seat (doesn't count against it).
2. First real failure at a seat ΓåÆ retry the same seat with something changed (corrected ticket,
   added context, raised effort).
3. Second real failure ΓåÆ one seat up, **or** the orchestrator takes over (its build reviewed from
   outside its lineage).
4. Top seat failed, or round cap hit ΓåÆ the boss rules, with the evidence.
Never a third identical retry. Never re-try a cheaper seat on a task that proved it needs a bigger one.

### Review dispatch
**Who may review** (the two legal paths, from Part IV's anti-laundering guard): a **different
effective-model vendor + lineage** (preferred ΓÇö different weights/training/context; a different
account merely hosting the builder's own brain does NOT count, see the effective-model preflight),
OR a **boss-launched fresh
seat** (legal, weaker, flagged) ΓÇö never the builder's own producing lineage. **Route by FIT within
those paths:** send each review to the strongest-fit independent seat for the work TYPE ΓÇö the
sharpest bug-proving seat for code, the frontier seat for architecture/judgment, a cheap independent
seat for a scan or a tie-breaking extra vote ΓÇö always outside the builder's lineage. Which concrete
model that is, is the shop's wiring (Appendix A), not the engine's law.

**The reviewer ticket carries exactly four things:**
1. The **ORIGINAL task, verbatim** (never the builder's restatement).
2. The **review set: every file the ticket's write set permitted**, whole, uncurated. The builder
   does not choose what the reviewer sees.
3. The **diff over that set**, plus acceptance criteria.
4. The **verify command and its output**, so the reviewer can re-run rather than trust.
**Never the builder's reasoning** ΓÇö anchoring a reviewer on the builder's narrative converts an
adversarial read into a confirmatory one. (Then the three lists + disputed-findings mechanisms of
Part V apply.) Broken tooling does not stop the channel: hand the reviewer the code itself via
stdin. **The adversarial channel is the last thing you let fail.**

### THE COUNCIL ΓÇö the multi-vendor panel (the orchestrator's special move)
The council is the fan-out turned to full width: instead of one builder + one reviewer, the
orchestrator convenes **every reachable vendor at once** ΓÇö one per seat, each a genuinely different
effective-model lineage ΓÇö for independent reads on a single high-stakes question. It is the SPECIAL
move (Doctrine 5's right-size still rules ΓÇö never the default for small work); reach for it when the
stakes justify the multiples: a design-space-wide fork, a decision that must be right, a bug or claim
that has to survive real scrutiny.

**Consent gates the convening ΓÇö offered, never auto-fired.** Even when work looks council-worthy, the
orchestrator *proposes* the panel (one line: why + the rough cost of N vendors running at once) and
dispatches only on the boss's explicit go. A "gnarly" call is licence to *ask*, never to self-authorize
the most expensive move in the method ΓÇö that is what makes "opt-in" literally true, in the engine and
not just the brochure.

**When NOT to convene ΓÇö the guardrail, not the fine print.** A trivial ask ΓÇö *"rewrite this email,"
"did I send the PO out," a quick fix, a plain question* ΓÇö is handled by the orchestrator alone (or a
single seat), **NEVER a council.** The orchestrator does not *oops* into a token-eating dream team for
a two-line task. Gate-0 and Doctrine 5 bind absolutely here: no genuine need for N independent
perspectives ΓåÆ no council. Breadth is not rigor; fan-outs cost multiples, not increments. The default
for small work is one seat doing it, quietly.

**The procedure the orchestrator runs ΓÇö a defined path, not an improvisation:**
1. **Brief.** One page: the question/vision *verbatim*, the hard-won context, the numbered points each
   seat must answer. Never a blank page.
2. **Convene + assign lenses.** Dispatch to every reachable vendor, each handed a DISTINCT angle
   (correctness ┬╖ cost ┬╖ security ┬╖ "try to *refute* this") so no two reads are redundant. Diverse
   vendors + diverse lenses = maximum coverage. Independence is the point: no seat sees another's
   answer first.
3. **Gather.** Each returns a SIGNED read (`docs/*-<vendor>.md` for design; a ranked verdict on Part
   V's ladder for review). Real outputs from real, *different* models ΓÇö never invented.
4. **Synthesize.** The orchestrator writes ONE synthesis: best-of-breed per piece, **every idea
   attributed, every disagreement NAMED and resolved, never smoothed.** One vendor catching another's
   load-bearing error is a council WIN.
5. **Two-round cap** (Principle 8): one exchange per dispute, then the bell; unresolved splits go to
   the boss's ruling queue. No looping, no token-inferno.
6. **The boss rules.** The council advises; the human decides and merges ΓÇö always (the Ladder's top rung).

This is adversarial verification at full width ΓÇö the one cross-lineage-review law (a review comes
from a different effective-model vendor than the build ΓÇö a same-vendor read is a labeled degraded
self-check, never disguised as cross-vendor), scaled to N independent perspectives. Each tier dresses it
differently ΓÇö a plain **panel** (report by model name), a signed **crew council**, or a puppeteered
**set-piece** ΓÇö but the engine underneath is this single procedure. *(A four-model council once MISSED
a bug that one real use surfaced instantly ΓÇö Part I ┬º1. The council widens coverage; it does not
replace in-hand validation.)*

### Mission reports (to the boss)
Phone-readable (Principle 10): outcome first; per-seat one-liners (name, color, status); rulings
needed as concrete options to react to, never a blank page; a cost note whenever a fan-out ran.
Claims capped: "gates pass," "review adjudicated," "in-hand validation pending" ΓÇö never "it works."

### The three flips (why seat assignment is mission state, not method state)
The builder seat has flipped for three causes: **capability** (the vendor with local file/shell/git
access got the hammer), **price** (one vendor's budget ran dry, the other had headroom),
**infrastructure** (a sandbox broke; the seat that could still write files built). In each flip the
cold reviewer surfaced defects the builder missed ΓÇö including guard tests that would pass even with
their callback deleted, and a reviewer's own overclaims discarded under the NOT PROVEN rule. **The
seat map is mission state, never method state. The only fixed point is that the lineage which produced
the work does not approve it.**
Practical scars: when the reviewer can't read the repo, HAND IT THE CODE via stdin ┬╖ let the builder
write files and the reviewer/orchestrator run git after the gate passes (the builder does not commit
its own work) ┬╖ a seat given an underspecified task wrote a proposal instead of guessing ΓÇö that
instruction is load-bearing, keep it in every builder ticket.

---

## PART VII ΓÇö REVIEW-CULTURE MECHANICS (character-free; CREW adds the rivalry, SHOW adds the drama)

The engine-level rules that keep review from becoming a debate club. *(Born from a true cautionary
tale: a two-agent shop where every review spawned a six-minute all-hands argument about whether a
color was red or pink, and no work ever shipped.)*
- **Reviews never stop the line.** Builders build to the end of their lane; reviews land at the
  CHECKPOINT (lane/episode end), not mid-swing.
- **Circle-backs are scheduled, not ambushed.** Non-blocking findings collect for the scheduled
  circle-back at the checkpoint; a reviewer never ambushes a builder mid-lane with them.
- **Severity ladder, enforced (the canonical four ΓÇö Part V's `BLOCKER / MATERIAL / MINOR / NOT
  PROVEN`).** A **BLOCKER** (breaks correctness, loses data, bricks the boss's box) may surface
  immediately ΓÇö WITH a suggested fix. **MATERIAL** (load-bearing but not a blocker ΓÇö the old "Major")
  and **MINOR** wait for the scheduled circle-back as one-line notes. **NOT PROVEN** (no failure
  mechanism or repro) never blocks and never ships. Never a meeting.
- **Every finding ships with a suggested fix.** "This is wrong, stop everything" is banned dialect.
  "This breaks X under Y ΓÇö here's the patch shape" is how this house speaks.
- **No debate clubs.** Builder and reviewer get ONE exchange. Still split ΓåÆ it goes silently into
  the boss's ruling queue and WORK CONTINUES (extends the two-round cap to tone).
- **Nits don't multiply.** A handful of taste notes per review, max. A pile of style opinions is a
  style-guide proposal, and those go to the boss.
- **Grade the work, not the worker.** A catch is a team win; a gotcha hunt is a crime.
- **THE EMERGENCY BRAKE (real, rare, quiet).** If the bench finds something GENUINELY damning
  (correctness rot, data loss, security holes), YES: write ONE clear report (what breaks, evidence,
  proposed fix), halt the AFFECTED lane only, pivot the crew to unaffected work. It does NOT mean a
  standing argument. The meeting that matters waits for the boss ΓÇö not for consensus theater.

**AUTONOMOUS-HOURS TOKEN DISCIPLINE (the anti-token-inferno core; CREW carries the crew-flavored
telling).** When the shop runs unattended these are ABSOLUTE ΓÇö born from a true horror story (four
agents argued for hours, tokens torched, each restart burning more):
- **Debates are allowed ΓÇö with a BELL.** Hash it out unattended, but every debate has a HARD CUTOFF:
  two rounds each, then the bell. Resolved ΓåÆ proceed. Unresolved ΓåÆ the dispute goes to the DECISION
  QUEUE (a written list the boss rules in batch) and everyone goes BACK TO WORK. **The banned thing
  is the loop: re-litigating past the bell is the cardinal token sin.**
- **A stoppage is a pivot, not an idle.** Blocked lane ΓåÆ reassign to unblocked work. The line stays
  warm; restarts are expensive.
- **DECISION BATCHING.** Taste/design questions are collected and resolved as a SET (when the color
  comes up, the stripes and dots come up in the same pass). Never re-stop the line serially.
- If in doubt: build the safest honest version, note the assumption, keep moving. The boss must
  never come home to a burnt token pile and a transcript of four characters litigating paint.

---

## PART VIII ΓÇö THE SIGNATURE MECHANIC & THE CANONICAL INVARIANT BLOCK

**Signature mechanic (Principle 1 made literal).** Every message from a seat ends with its color.
The colorΓåÆidentity binding is a tier concern: the Deck tags by MODEL (≡ƒƒí orchestrator ┬╖ ≡ƒƒá Claude ┬╖
≡ƒö╡ Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó Gemini); CREW binds those colors to CHARACTERS. SPINE owns only the rule
*that every seat signs* and the vendorΓåÆcolor map (Appendix A).

**The canonical invariant block is defined HERE and nowhere else** (Principle 9). Entry files and
every tier's launcher skill copy it VERBATIM; everything else in them is a pointer:

```
TRM INVARIANTS (v2026-07-22 r2 ┬╖ doctrine: SPINE.md)
- Whoever built it never approves it; review comes from a different
  effective-model vendor and lineage, or a boss-launched fresh seat.
- Claims are capped at evidence: "gates pass," never "it works."
- Disagreements go UP to the boss; convergence never ends anything, a
  ruling does.
- Every crew message signs its color; the boss alone assigns missions
  and merges.
```

*Note on the block id: the `v2026-07-22 r2` inside the block is the invariant block's own identity
and is intended CONTINUITY ΓÇö it tracks the invariant text itself, independent of SPINE's minor
version (SPINE may be v1.0, v1.1, ΓÇª while the block stays at its revision until its wording changes ΓÇö
bumped r1 ΓåÆ r2 on 2026-07-22, when "another vendor's account" was tightened to "a different
effective-model vendor and lineage"). The block is
verified byte-identical across SPINE and all three launchers; do not change it to match a spine
version.*

---

## APPENDIX A ΓÇö THE ARSENAL / WIRING (current wiring, NOT law ΓÇö verify; pricing/promos are details)

The model banner colors (vendor ΓåÆ color; the ONLY color fact SPINE owns): **claude = orange ≡ƒƒá ┬╖
codex = blue ≡ƒö╡ ┬╖ grok = black ΓÜ½ ┬╖ gemini = green ≡ƒƒó** ┬╖ the orchestrator conducting
plain = **gold ≡ƒƒí**. A worn wardrobe shows both (≡ƒƒá≡ƒƒó = a Claude brain on the Gemini seat).

- **Codex (OpenAI)** ΓÇö bounded implementation of a clear spec; the sharpest code reviewer (proves
  bugs, cites sources). `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`.
- **Grok (xAI)** ΓÇö fearless UI/skins/concept pages; surface only, never engine.
  `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <f> --always-approve < /dev/null`. Mandatory trail entry.
- **Gemini / Antigravity (Google)** ΓÇö proven builder (Flash), IMAGE GEN via Nano Banana (on the sub,
  no card), cheap reviews/sweeps, independent 4th vote, and **the Overflow Valve** (rents Claude/GPT
  brains on Google's tab when the Claude meter runs hot ΓÇö count agy as the GOOGLE bloodline only when
  wearing a Gemini model; agy-running-Claude is not an independent reviewer of Claude work).
  `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.6 Flash (High)"`.
  agy `--model` strings are exact-match; Claude tiers need the `(Thinking)` suffix.
- Dispatch ritual for any wardrobe: ticket file ΓåÆ headless dispatch ΓåÆ the orchestrator gates
  independently (render/probe/screenshot) ΓåÆ re-ticket ΓåÆ loop. Trails mandatory where the fence is
  wider than one file.
- **The arsenal is OPTIONAL.** The method works with whatever vendors are reachable (Claude alone is
  a valid, degraded arsenal). No specific vendor, plan, or price is part of the method.
- **This shop's Lineage Ledger location (wiring, NOT law):**
  `<your-brain>\_claude-brain\memory\model-lineage-ledger.md`. The engine (Doctrine 6) names
  no absolute path ΓÇö downloaders default to a project-relative `model-lineage-ledger.md`; this is
  merely where THIS box keeps its shared fleet-wide store.

## APPENDIX B ΓÇö FIELD NOTES (append-only; proven capabilities & gotchas, inherited by all tiers)
*(When a run PROVES something new, it goes here so future installs inherit it.)*
- **agy `--model` strings are exact-match**: Claude tiers require the `(Thinking)` suffix ΓÇö
  `"Claude Sonnet 4.6 (Thinking)"`, `"Claude Opus 4.6 (Thinking)"`. A bad string exits 1 and prints
  the full valid-model list (useful as a probe).
- **Gemini 3.1 Pro (High) handled a heavy adversarial review fine** (~600-word verdict table, physics
  attacks) ΓÇö confirms the Flash review-ceiling workaround: route heavy reviews to Pro, not Flash.
- **Two `codex exec` instances run in parallel** without issue (separate processes, same box).
- **Codex cites sources when reviewing factual claims** (web-searches vendor manuals unprompted) ΓÇö
  doubles as a doc-checker for claim-verification tickets.
- **Cross-vendor consensus worked as designed**: Codex and Gemini independently killed the same two
  pieces of draft advice (mill-first/burn-second; interpolate-from-3-probes) for the same physical
  reasons. Two-vendor agreement = treat as settled.
- Claude-tier doc-verification subagent (Sonnet + web) is slow (~10 min) but resolves which claims
  rest on conflicting sources ΓÇö its "don't publish this number" flags are the payoff.
- **Gemini 3.6 Flash (High) is live and handled a real analysis ticket clean** (2026-07-22,
  token-ticker EP10): agy's valid-model roster now carries the 3.6 Flash family (High/Medium/Low).
  The bad-string probe still works ΓÇö an invalid `--model` exits 1 and prints the current roster.
- **agy HEADLESS auto-denies tool permissions** (`read_file` etc. ΓÇö the run dies with a "jetski"
  permission error and empty output). Headless dispatches must EMBED the evidence in the prompt
  (reviews-by-embed); probe auth cheaply first with a one-word `-p` ping.
- **Secret-gated verification pattern (proven 2026-07-22):** when a reviewer's sandbox denies it a
  secret the proof needs (e.g. an HMAC key), the reviewer AUTHORS the exact verifier script; a
  key-holding seat EXECUTES it unmodified (trivial repairs applied openly and logged); the verdict
  binds to the output. Keeps builder-never-approves intact when secrets gate the evidence ΓÇö the
  reviewer's NOT-PROVEN-until-run discipline is the correct half of the handshake.

---
*SPINE owns the engine. It names no characters and tells no story ΓÇö those are CREW's and SHOW's to
add, never to restate. Provenance of the Team Rocket Method (authorship, credits, status) lives in
CREW, because it is that brand's identity, not the brand-neutral engine's.*


codex
The trunk confirms the key doctrine but also embeds stale wiring: Claude/Fable gold, Grok ΓÇ£surface only,ΓÇ¥ Gemini 3.6/3.1, and CLI commands inside the methodΓÇÖs appendix. IΓÇÖm checking the exact review/lineage language and current official Cursor billing/tool semantics before recommending a table that fails closed.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'rg -n -C 5 "Review dispatch|fresh seat|same-vendor|effective-model|Reachability|fleet|approval|builder|lineage|Appendix A|CLI|Task" SPINE.md SKILL.md MODEL-DISPATCH-GUIDE.md' in C:\Sync\Projects\andersons-dispatch-deck
 succeeded in 816ms:
SKILL.md-35-The Deck adds nothing to the *method*. Its entire delta is **plain rendering + the gold-baton color
SKILL.md-36-narration.** Every rule below is SPINE's; this section only says how the Deck *presents* it.
SKILL.md-37-
SKILL.md-38-### NARRATE IN COLOR (the one visual convention)
SKILL.md-39-The orchestrator (≡ƒƒí GOLD) narrates the run and TAGS every model action with its vendor color (SPINE
SKILL.md:40:Appendix A owns the vendorΓåÆcolor map): ≡ƒƒí orchestrator (Claude/Fable conducting) ┬╖ ≡ƒƒá Claude ┬╖ ≡ƒö╡
SKILL.md-41-Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó Gemini. Announce dispatches/builds/reviews in-line:
SKILL.md-42-> *"≡ƒƒí fencing the work into two lanes. ≡ƒƒá Claude building the parser ┬╖ ≡ƒö╡ Codex building the
SKILL.md-43-> validator (parallel). ΓåÆ ≡ƒö╡ Codex reviewing ≡ƒƒá Claude's parser: 2 findings, fixes attached. ΓåÆ ≡ƒƒó
SKILL.md-44-> Gemini generating the icon set. Gates: green."*
SKILL.md-45-The color is a status light, not a costume ΓÇö it says WHICH MODEL, nothing more. The banner never lies:
--
SKILL.md-55-Boss combos: ΓÜ¬≡ƒÅü in-hand validation ┬╖ ΓÜ¬ΓÜû∩╕Å ruling pending ┬╖ ΓÜ¬≡ƒÄ« on the sticks.
SKILL.md-56-Reading: ≡ƒƒá≡ƒö¿ Sonnet building ┬╖ ≡ƒö╡≡ƒô¥ Codex reviewing ┬╖ ≡ƒö╡≡ƒô¥ΓåÆ≡ƒö┤ Codex rejected ┬╖
SKILL.md-57-≡ƒƒá≡ƒƒó Claude-brain-on-the-Gemini-seat. A run reads as a timeline:
SKILL.md-58-≡ƒ⌐║ ΓåÆ ≡ƒƒú ΓåÆ ≡ƒƒá≡ƒö¿ ΓåÆ ≡ƒº¬ ΓåÆ ≡ƒö╡≡ƒô¥ΓåÆ≡ƒö┤ ΓåÆ ≡ƒƒá≡ƒö¿ ΓåÆ ≡ƒº¬ ΓåÆ ≡ƒÜó ΓåÆ ΓÜ¬≡ƒÅü ΓåÆ ≡ƒƒñ.
SKILL.md-59-The boss's words: the dots "give the chat a lot of life and color while working" ΓÇö narrate every
SKILL.md:60:Deck run in this notation. VendorΓåÆcolor still owned by SPINE Appendix A; this legend extends it
SKILL.md:61:with the boss seat, act badges, and state dots (it supersedes any builders-wear-color-alone habit).
SKILL.md-62-
SKILL.md-63-## RUNNING THE DECK (all mechanics are SPINE's ΓÇö this is the plain-render checklist)
SKILL.md-64-1. **Plan first** (SPINE Part I ΓÇö Gate-0 + the Diagnose/Design fork). State the goal back; write a
SKILL.md-65-   short spec for anything substantial (what/why/done-when). Honor the Anderson house rules.
SKILL.md-66-2. **Fence the work** (SPINE WRITE SET fence). Tickets with named, disjoint file sets; one clean goal
--
SKILL.md-70-   Claude brain via Antigravity (the Overflow Valve, billed to Google's tab) or its own top Gemini
SKILL.md-71-   tier as a capable substitute. Show the banner honestly. Announce plainly, no characters:
SKILL.md-72-   "≡ƒö╡ Codex building X." / "≡ƒƒá≡ƒƒó Claude-brain-on-Gemini taking the parser to save the meter."
SKILL.md-73-4. **Build with any model; route the review by FIT.** The two legal review paths, their statuses
SKILL.md-74-   (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` / `REVIEW UNAVAILABLE`), and the fit-routing rule are
SKILL.md:75:   **SPINE's ΓÇö Part VI *Review dispatch* (+ Part IV's anti-laundering guard); this tier NAMES the move,
SKILL.md:76:   it does not restate the rule.** *This shop's wiring (Appendix A), as an ILLUSTRATION of SPINE's
SKILL.md-77-   fit-routing, not new law:* Codex is usually the sharpest CODE reviewer
SKILL.md-78-   when it didn't build it (Claude/Grok/Gemini code ΓåÆ Codex); Codex built it ΓåÆ Claude reviews;
SKILL.md-79-   architecture/judgment ΓåÆ Claude; Gemini = a cheap independent pass or tie-breaking 4th vote. State it
SKILL.md-80-   by model + color, never a character. Every finding ships a fix; reviews land at checkpoints; the
SKILL.md-81-   build never halts to argue; unresolved ΓåÆ the boss's decision queue.
--
SKILL.md-83-   evidence ΓÇö "gates pass," never "it works." The boss is the top rung (in-hand outranks the bench).
SKILL.md-84-6. **Report plainly** (SPINE mission reports). What was dispatched, to which model, findings, what
SKILL.md-85-   shipped, what needs the boss. The boss is the only one who merges.
SKILL.md-86-
SKILL.md-87-## NON-NEGOTIABLES (all inherited from SPINE ΓÇö restated only as the tier's guardrail card)
SKILL.md:88:- **No unasked fleets** (Gate-0 / the five-prong fleet test). Deliberate and bounded; never a swarm.
SKILL.md-89-- **Model tiering honored** ΓÇö don't burn the frontier seat on mechanical work.
SKILL.md:90:- **Independent review, never the builder's lineage** ΓÇö the two legal paths and their statuses are
SKILL.md:91:  SPINE's (Part IV + Part VI *Review dispatch*); this card names the guardrail, it does not restate the
SKILL.md-92-  rule. Unreviewed work is never reported "done."
SKILL.md-93-- **Nothing irreversible without the boss** ΓÇö no push/merge/publish/spend on an assumption.
SKILL.md-94-- **This is the STRAIGHT-FACED mode.** If the boss wants the show, that's `/team-rocket-takes-over`.
SKILL.md-95-  Do not drift into persona here.
SKILL.md-96-
SKILL.md-97-## ON INVOCATION
SKILL.md-98-1. **Load SPINE**, verify its version against DEPENDS, print the load receipt.
SKILL.md:99:2. **PROBE the arsenal, don't assume it** (SPINE Part VI ΓÇö *Reachability & effective-model preflight*;
SKILL.md:100:   the arsenal list lives in Appendix A). Run the reachability check (`--version` on each vendor CLI:
SKILL.md:101:   codex, grok full-path, agy) AND confirm the effective model/lineage behind each host ΓÇö a host
SKILL.md:102:   renting another vendor's brain counts as THAT vendor's lineage, and an unestablished identity is
SKILL.md-103-   `UNKNOWN LINEAGE`, which fails closed and is never counted as a cross-vendor reviewer. DECLARE the
SKILL.md-104-   live arsenal and the independence status in one line: *"Online: ≡ƒƒá Claude ┬╖ ≡ƒö╡ Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó
SKILL.md-105-   Gemini ΓÇö FULL CROSS-VENDOR."* A model that doesn't answer isn't in the pool. The method degrades
SKILL.md-106-   gracefully (Claude alone is valid); if NO independent reviewer is reachable, say so ΓÇö unreviewed
SKILL.md-107-   work is never reported as done.
--
SKILL.md-110-
SKILL.md-111-## THE INVARIANTS (copied verbatim from SPINE Part VIII, per Principle 9)
SKILL.md-112-```
SKILL.md-113-TRM INVARIANTS (v2026-07-22 r2 ┬╖ doctrine: SPINE.md)
SKILL.md-114-- Whoever built it never approves it; review comes from a different
SKILL.md:115:  effective-model vendor and lineage, or a boss-launched fresh seat.
SKILL.md-116-- Claims are capped at evidence: "gates pass," never "it works."
SKILL.md-117-- Disagreements go UP to the boss; convergence never ends anything, a
SKILL.md-118-  ruling does.
SKILL.md-119-- Every crew message signs its color; the boss alone assigns missions
SKILL.md-120-  and merges.
--
MODEL-DISPATCH-GUIDE.md-8-(the tools); the characters (Jessie/James/Butch/Cassidy/the cat) just wear them.
MODEL-DISPATCH-GUIDE.md-9-
MODEL-DISPATCH-GUIDE.md-10----
MODEL-DISPATCH-GUIDE.md-11-
MODEL-DISPATCH-GUIDE.md-12-## ≡ƒƒá CLAUDE (Anthropic) ΓÇö the brain + the orchestrator
MODEL-DISPATCH-GUIDE.md:13:**Characters:** ≡ƒÿ╝ the cat (orchestrator, usually Fable) ┬╖ ≡ƒƒá Jessie (builder) ┬╖ ≡ƒö┤ Butch (reviewer).
MODEL-DISPATCH-GUIDE.md-14-**Strengths:** deepest multi-file reasoning, architecture, spec-writing, root-cause
MODEL-DISPATCH-GUIDE.md-15-debugging, tricky/tangled logic, adversarial review, and honest judgment ΓÇö it FLAGS its
MODEL-DISPATCH-GUIDE.md-16-assumptions instead of hiding them ("I bounded this to 2/3 because the engine only means
MODEL-DISPATCH-GUIDE.md-17-2/3 ΓÇö ruling queued"). Best narrator/orchestrator.
MODEL-DISPATCH-GUIDE.md-18-**Dispatch for:** the orchestration itself ┬╖ architecture & design calls ┬╖ specs ┬╖ engine
MODEL-DISPATCH-GUIDE.md-19-surgery ┬╖ root-cause hunts ┬╖ hard multi-file changes ┬╖ reviewing other vendors' work.
MODEL-DISPATCH-GUIDE.md-20-**Watch-out:** the expensive seat ΓÇö ration it; watch the weekly meter. TIER IT:
MODEL-DISPATCH-GUIDE.md-21-- **Fable** = specs, review, orchestration, conversation (heavyweight; the cat's default).
MODEL-DISPATCH-GUIDE.md-22-- **Sonnet** = code + research sub-agents (the workhorse for builds).
MODEL-DISPATCH-GUIDE.md-23-- **Haiku** = mechanical (gate re-runs, log mining, builds). the boss watches the counter.
MODEL-DISPATCH-GUIDE.md:24:**Mechanism:** it's the HOME CLI (Claude Code). Sub-agents via the Agent tool. This is the
MODEL-DISPATCH-GUIDE.md-25-one window everything else hangs off.
MODEL-DISPATCH-GUIDE.md-26-
MODEL-DISPATCH-GUIDE.md:27:## ≡ƒö╡ CODEX (OpenAI / ChatGPT) ΓÇö the precision builder + sharpest reviewer
MODEL-DISPATCH-GUIDE.md:28:**Characters:** ≡ƒö╡ James (builder) ┬╖ ≡ƒ⌐╖ Cassidy (reviewer).
MODEL-DISPATCH-GUIDE.md-29-**Strengths:** disciplined, exact implementation of a clear spec (no drift) ┬╖ the SHARPEST
MODEL-DISPATCH-GUIDE.md-30-static/adversarial code review in the shop ΓÇö it doesn't just claim a bug, it PROVES it
MODEL-DISPATCH-GUIDE.md-31-(raw-socket-forges the bad input, shows it break) ┬╖ validation-matrix / edge-case thinking.
MODEL-DISPATCH-GUIDE.md-32-**Dispatch for:** bounded implementation of a clear fenced ticket ┬╖ cross-vendor code
MODEL-DISPATCH-GUIDE.md-33-review (esp. Cassidy reviewing Claude-built work) ┬╖ security/validation passes.
MODEL-DISPATCH-GUIDE.md-34-**Watch-out:** wants ONE clean goal per ticket (refuses messy multi-fix tickets) ┬╖ runs on
MODEL-DISPATCH-GUIDE.md:35:a SEPARATE plan ΓåÆ costs the Claude meter $0 (great default builder for budget) ┬╖ headless
MODEL-DISPATCH-GUIDE.md-36-needs stdin closed.
MODEL-DISPATCH-GUIDE.md-37-**Mechanism:** `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`
MODEL-DISPATCH-GUIDE.md-38-(the danger-full-access lane is the working one on the Anderson box ΓÇö its OS-sandbox ACL
MODEL-DISPATCH-GUIDE.md-39-bug is upstream; boss blessed a `Bash(codex*)` allow rule). Embed code IN the prompt for
MODEL-DISPATCH-GUIDE.md-40-reviews (reviews-by-embed) when file access is flaky.
MODEL-DISPATCH-GUIDE.md-41-
MODEL-DISPATCH-GUIDE.md-42-## ΓÜ½ GROK (xAI) ΓÇö the fearless artist
MODEL-DISPATCH-GUIDE.md-43-**Characters:** cat-driven ΓÜ½ (or a ≡ƒ½í Wobbuffet skit); it's a wardrobe, not a permanent character.
MODEL-DISPATCH-GUIDE.md-44-**Strengths:** fearless one-shot visual design ΓÇö hand it a VIBE, get back a world ┬╖ UI/UX,
MODEL-DISPATCH-GUIDE.md:45:skins, concept/vision pages, demo-mode storytelling ┬╖ fast ┬╖ leaves a signed lineage trail.
MODEL-DISPATCH-GUIDE.md-46-**Dispatch for:** UI face-lifts ┬╖ concept/vision HTML ┬╖ skins & art direction ┬╖ "make it
MODEL-DISPATCH-GUIDE.md-47-feel like a starship" ┬╖ anything with a screen and a mood.
MODEL-DISPATCH-GUIDE.md-48-**Watch-out:** UI SURFACE ONLY ΓÇö "Grok reskins, it does not rewire"; keep it off engine
MODEL-DISPATCH-GUIDE.md-49-logic ┬╖ gate for platform ceilings (e.g. WebKit-16 for the old iPad) ┬╖ mandatory
MODEL-DISPATCH-GUIDE.md:50:GROK-TRAIL.md entry per job for lineage.
MODEL-DISPATCH-GUIDE.md-51-**Mechanism:** `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <file> --always-approve < /dev/null`
MODEL-DISPATCH-GUIDE.md-52-(NOTE: `grok` is on PATH in a normal shell but NOT in the tool's bash ΓÇö use the full path).
MODEL-DISPATCH-GUIDE.md-53-
MODEL-DISPATCH-GUIDE.md-54-## ≡ƒƒó GEMINI / ANTIGRAVITY (Google) ΓÇö the value powerhouse (the biggest find)
MODEL-DISPATCH-GUIDE.md-55-**Characters:** cat-driven ≡ƒƒó for builds/art ┬╖ ≡ƒƒá≡ƒƒó Jessie fronts when it wears a Claude
--
MODEL-DISPATCH-GUIDE.md-83----
MODEL-DISPATCH-GUIDE.md-84-
MODEL-DISPATCH-GUIDE.md-85-## QUICK DECISION TABLE ΓÇö "I need to ___ ΓåÆ send ___"
MODEL-DISPATCH-GUIDE.md-86-- **Architect / spec / hard root-cause** ΓåÆ ≡ƒƒá Claude (Fable).
MODEL-DISPATCH-GUIDE.md-87-- **Build a clear fenced spec, cheap** ΓåÆ ≡ƒö╡ Codex (James) ΓÇö $0 to Claude meter.
MODEL-DISPATCH-GUIDE.md:88:- **Build, mixed / when Codex is busy** ΓåÆ ≡ƒƒó Gemini Flash (proven builder) or ≡ƒƒá Claude Sonnet.
MODEL-DISPATCH-GUIDE.md-89-- **Review Claude-built code** ΓåÆ ≡ƒö╡ Codex or ≡ƒƒó Gemini ΓÇö never Claude reviewing itself.
MODEL-DISPATCH-GUIDE.md-90-- **Review Codex-built code** ΓåÆ ≡ƒƒá Claude ΓÇö never Codex reviewing itself.
MODEL-DISPATCH-GUIDE.md-91-- **Review Grok/Gemini-built code** ΓåÆ ≡ƒö╡ Codex (the sharpest code reviewer; catches Grok's
MODEL-DISPATCH-GUIDE.md-92-  UI-surface gaps) ΓÇö or ≡ƒƒá Claude for architecture/design. Route the reviewer by the CODE'S
MODEL-DISPATCH-GUIDE.md-93-  TYPE + the cross-vendor rule; ANY model can build, Codex is the default code-reviewer
--
MODEL-DISPATCH-GUIDE.md-98-- **Wide sweep / log-mine / mechanical** ΓåÆ ≡ƒƒó Gemini Flash (cheap) or ≡ƒƒá Haiku.
MODEL-DISPATCH-GUIDE.md-99-- **Claude meter running hot** ΓåÆ ≡ƒƒó Overflow Valve: route Claude-grade work to the GREEN
MODEL-DISPATCH-GUIDE.md-100-  seat ΓÇö either a real Claude brain on Antigravity (≡ƒƒá≡ƒƒó, Google's tab) OR Gemini's own top
MODEL-DISPATCH-GUIDE.md-101-  tier as a capable-if-lesser Claude stand-in (≡ƒƒó). Dispatch is COST-AWARE, not just
MODEL-DISPATCH-GUIDE.md-102-  capability-aware ΓÇö the orchestrator weighs the meter, not only the "best" model.
MODEL-DISPATCH-GUIDE.md:103:- **A true independent 4th vote** ΓåÆ ≡ƒƒó Gemini (real different lineage).
MODEL-DISPATCH-GUIDE.md-104-
MODEL-DISPATCH-GUIDE.md-105-## THE IRON RULES (never break)
MODEL-DISPATCH-GUIDE.md:106:1. **A reviewer never wears the builder's own vendor.** Cross-vendor or it's just a mirror.
MODEL-DISPATCH-GUIDE.md-107-2. **Right model for the job** ΓÇö the whole point; this table is the map.
MODEL-DISPATCH-GUIDE.md-108-3. **The banner never lies** ΓÇö always show the real model under a worn wardrobe (≡ƒƒá≡ƒƒó etc.).
--
SPINE.md-52-
SPINE.md-53-- **The dispatch gate (two questions):** (1) multiple stages, files, or surfaces? (2) would doing
SPINE.md-54-  it inline burn frontier quota on non-judgment work? **Both no ΓåÆ just do it**, no orchestration,
SPINE.md-55-  signed by whoever did it. Most small tasks deserve no orchestration at all. Any yes ΓåÆ delegate
SPINE.md-56-  with a ticket.
SPINE.md:57:- **Right-size FIRST (the corrected default).** One builder + ONE cross-vendor reviewer is the
SPINE.md-58-  canon shape for real code; often just the orchestrator for small stuff. A full 3+-seat PANEL is
SPINE.md-59-  a SPECIAL move ΓÇö run it only when the boss asks. When the task looks genuinely gnarly/high-stakes the
SPINE.md-60-  orchestrator may PROPOSE a panel (one line: why + the rough cost of N vendors), but the fan-out
SPINE.md-61-  dispatches only on his explicit go ΓÇö never self-authorized on the orchestrator's own "gnarly" call.
SPINE.md-62-  Scaling seat count is the boss's call to make loud, never a habit. *(This REPLACES the old
--
SPINE.md-64-  right-size first; parallelism is earned per task, not assumed.)*
SPINE.md-65-- **Earn-a-head:** every added seat must be justifiable in one sentence, or it is decoration.
SPINE.md-66-  Breadth is not rigor. Fan-outs cost multiples, not increments (an external multi-agent writeup
SPINE.md-67-  measured ~15x the tokens of a single chat ΓÇö their number, not a law of nature; the gate exists
SPINE.md-68-  because of that shape).
SPINE.md:69:- **A fleet is legal only if all five hold** (the fleet-legality test, Part IV): Declared ┬╖
SPINE.md:70:  Bounded ┬╖ Accounted ┬╖ still-Principle-3 ┬╖ Authority-inheritance. A fleet nobody declared,
SPINE.md-71-  bounded, or counted is banned.
SPINE.md-72-
SPINE.md-73-### 3 ┬╖ THE DIAGNOSE / DESIGN FORK (what KIND of problem is this?)
SPINE.md-74-Before building, classify. The two kinds of hard problem take opposite opening moves:
SPINE.md-75-
SPINE.md-76-- **A BUG ΓåÆ INSTRUMENT, don't guess.** When a bug won't yield to theory, stop hypothesizing and
SPINE.md-77-  BUILD AN INSTRUMENT to see reality ΓÇö a tap, a probe, a debug mode that shows the actual data.
SPINE.md:78:  *(A packet tap on the fleet wire ended hours of "maybe it's the session / the slot / the gate"
SPINE.md-79-  by* proving *the input was arriving ΓÇö collapsing the search space in one read. A splash of
SPINE.md-80-  hypotheses loses to one honest measurement, every time.)*
SPINE.md-81-- **A NOVEL / GNARLY FEATURE ΓåÆ COUNCIL, then SYNTHESIS.** *(A council is proposed to the boss and
SPINE.md-82-  fanned out only on his go ΓÇö never auto-fired; see The Council.)* For a design-space-wide problem, write a
SPINE.md-83-  one-page BRIEF (vision *verbatim* + hard-won context + numbered design questions), dispatch the
--
SPINE.md-95-them and report requested-vs-achieved, loud:
SPINE.md-96-
SPINE.md-97-| # | The contract term | What it means |
SPINE.md-98-|---|---|---|
SPINE.md-99-| 1 | **Observable outcome** | The gradeable, before-dispatch acceptance check ΓÇö what "done" looks like from outside. Can't write it? Not ready to delegate. |
SPINE.md:100:| 2 | **Instrument signal** | The tap/probe/toggle that shows the real end-state (not the builder's account of it). The artifact reports achieved-vs-requested itself. |
SPINE.md-101-| 3 | **Protected invariants** | What must NOT change ΓÇö the fence, the correctness properties, the boss's box staying bootable. Violating one is a BLOCKER even if the feature works. |
SPINE.md-102-| 4 | **Rollback** | How to undo it safely. A guard that reverts itself beats a fix that bricks the box. When a piece can't land safely, FLAG it, never fake it: *"15/16 landed, #16 reverted-and-flagged"* is the house voice; silent slop is the crime. |
SPINE.md-103-| 5 | **Boss handover test-kit** | The in-hand check the boss runs to hit the TOP rung of the Ladder ΓÇö the exact steps/inputs, phone-readable, so reality can outrank the review. |
SPINE.md-104-
SPINE.md-105-*(A toggle's honest self-status once caught the orchestrator's own ACL bug before the boss could ΓÇö
--
SPINE.md-115-1. **DESIGN COUNCIL ΓåÆ SYNTHESIS (before a line is built).** Per the Diagnose/Design fork above ΓÇö
SPINE.md-116-   for a novel/gnarly problem only, and proposed to the boss ΓÇö the multi-vendor fan-out dispatches only
SPINE.md-117-   on his explicit go. Right-size still rules.
SPINE.md-118-2. **BUILD IN ISOLATION.** Real builds run in an isolated git **worktree/branch, NEVER the boss's
SPINE.md-119-   live checkout** ΓÇö his daily-driver must not break mid-build. Disjoint write-sets across lanes.
SPINE.md:120:3. **INDEPENDENT BENCH before merge (Part IV's two paths).** Reviewed from OUTSIDE the builder's
SPINE.md:121:   lineage ΓÇö another effective-model vendor preferred ΓåÆ `FULL CROSS-VENDOR`, or a boss-launched fresh
SPINE.md:122:   seat ΓåÆ `SOLO-VENDOR DEGRADED`; never the builder's lineage; neither reachable ΓåÆ `REVIEW
SPINE.md-123-   UNAVAILABLE`. Adversarial, ranked with Part V's canonical ladder ΓÇö **BLOCKER / MATERIAL / MINOR /
SPINE.md-124-   NOT PROVEN** ΓÇö each finding with a fix. Green gates alone never merge ΓÇö the bench earns its
SPINE.md-125-   keep finding the paths that "looked clean." *(It once caught a feature quietly re-introducing the
SPINE.md-126-   exact bug it was built to kill.)*
SPINE.md-127-4. **BOSS IN-HAND ΓÇö the TOP gate, above all of it.** The bench catches CODE bugs; the boss catches
SPINE.md-128-   REALITY bugs, and reality outranks the review (Ladder of Truth, top rung). Green gates + passed
SPINE.md-129-   bench + working in-hand = shipped. Any two without the third = not yet.
SPINE.md:130:5. **THE FIX LOOP.** Bench findings ΓåÆ back to the builder ΓåÆ re-review ΓåÆ re-gate, as many turns as
SPINE.md-131-   it takes (bounded by the loop cap, Doctrine on review culture below).
SPINE.md-132-
SPINE.md-133-### Doctrine 2 ┬╖ INSTRUMENT, DON'T GUESS
SPINE.md-134-The bug-side of the Diagnose/Design fork, promoted to reflex. When theory stalls, build the
SPINE.md-135-instrument. One honest measurement beats a splash of hypotheses. *(The boss asked for this himself
--
SPINE.md-145-sentence ("we don't have to make them deaf ΓÇö just listen on the right slot"). The crew's job is to
SPINE.md-146-surface the MINIMAL honest version and hand him the scalpel; **a scope cut is a WIN celebrated,
SPINE.md-147-never a loss mourned.** (The rarest, highest-value product skill in the room, and it's his.)
SPINE.md-148-
SPINE.md-149-### Doctrine 5 ┬╖ RIGHT-SIZE THE DISPATCH (boss ruling 2026-07-18)
SPINE.md:150:The DEFAULT is lean: one builder + ONE cross-vendor reviewer for canon code; often just the
SPINE.md-151-orchestrator for small stuff. A full 3+-model PANEL (like the MAC whack-a-mole) is a SPECIAL move ΓÇö
SPINE.md-152-run it only when the boss asks or the task is genuinely gnarly/high-stakes. **The Lineage Ledger
SPINE.md-153-recalibrates WHO gets a job, never "spawn more heads."** Scaling agent count is the boss's call to
SPINE.md-154-make loud, not a habit ΓÇö guard the meter (echoes the anti-token-inferno clause).
SPINE.md-155-
SPINE.md-156-### Doctrine 6 ┬╖ THE LINEAGE ENGINE (boss idea 2026-07-18 ΓÇö track who's actually good)
SPINE.md-157-The routing memory that turns experience into better casting. After an episode/run with REAL
SPINE.md-158-dispatches, the orchestrator appends objective rows to the **shop's declared Model Lineage Ledger**
SPINE.md:159:(default: project-relative `model-lineage-ledger.md` at the project root, next to `PLAN-CARD.md`; a
SPINE.md-160-shop may point it elsewhere on the plan card, and this shop's actual location is recorded in Appendix
SPINE.md-161-A ΓÇö wiring, not law). The engine names no absolute machine path.
SPINE.md-162-- **THE ONE RULE ΓÇö FACTS Γëá FLAVOR (logging form).** Log only OBJECTIVE dispatch signals: vendor,
SPINE.md-163-  seat/wardrobe worn, task type, outcome (APPROVE/REJECT/found-N-real-bugs/shipped/failed),
SPINE.md-164-  wall-time, and the specific real catch or contribution. Banter is the ACT ΓÇö **never logged as
SPINE.md-165-  data.** A line with no real dispatch behind it gets no row. *(SHOW owns the narration form of
SPINE.md-166-  FactsΓëáFlavor ΓÇö the firewall that story may never rewrite a real event. Same principle, two layers;
SPINE.md-167-  SPINE owns what the ledger records.)*
SPINE.md-168-- **Timing is a real column.** Slow-but-right vs fast-but-shallow is genuine signal.
SPINE.md-169-- **THE WEEKLY LINEAGE REVIEW (the recalibration loop).** ~Once a week (the boss calls it ΓÇö "run
SPINE.md:170:  the lineage review" / "dispatch standings" ΓÇö or the orchestrator offers when a fresh batch of
SPINE.md-171-  rows has accrued): (1) **STANDINGS** per vendor from the objective columns only ΓÇö dispatch count,
SPINE.md-172-  approve/reject/bugs-caught, avg wall-time, notable catches vs whiffs, trend since last review;
SPINE.md-173-  (2) **RECALIBRATE** ΓÇö propose concrete routing tweaks to the playbook (`model-dispatch-guide.md`);
SPINE.md-174-  **the boss rules each change**, only then is the guide updated; (3) **HONESTY GATE** ΓÇö flag where
SPINE.md-175-  the sample is too thin to conclude; a jab isn't a metric. Evidence ΓåÆ routing ΓåÆ better dispatches ΓåÆ
--
SPINE.md-184-1. **Distinct, visible identities.** Every seat has a role, a name, and a color, so the human
SPINE.md-185-   always knows which seat *claims* to be acting, and no work arrives anonymous. Precisely: a
SPINE.md-186-   signature identifies the **declared** seat, not a verified model. Nothing here cryptographically
SPINE.md-187-   proves which model produced a message; a session wearing three hats can sign all three colors.
SPINE.md-188-   The signature makes identity **legible and falsifiable**, not proven.
SPINE.md:189:2. **One seat, one job, no UNDECLARED fleets.** Each seat does ONE bounded task and does it itself.
SPINE.md-190-   No hidden sub-agent swarms, no self-appointed "verify the whole codebase" sweeps. *(The
SPINE.md-191-   anti-pattern that motivated the whole method: an unfenced instance spawning a swarm and torching
SPINE.md-192-   a day of frontier budget.)*
SPINE.md:193:3. **Builder is never the reviewer.** The owning-seat lineage that produces the work is never the
SPINE.md:194:   one that approves it. A seat outside that lineage reviews it adversarially: fresh eyes, no
SPINE.md-195-   loyalty to the work. **This is the fixed point ΓÇö it survives every seat flip.**
SPINE.md-196-4. **Files are the shared brain.** Seats do NOT share chat context. They communicate through
SPINE.md-197-   durable, inspectable repo files (assignments, handoffs, a living passdown). Tool-agnostic
SPINE.md-198-   memory any model or human can read to get caught up.
SPINE.md-199-5. **Gates referee, but a gate is only an arbiter if it can FAIL.** Automated tests are the most
--
SPINE.md-221-
SPINE.md-222-**The abstract roles (CREW/SHOW bind names to these; the Deck uses them plain):**
SPINE.md-223-- **Orchestrator** ΓÇö classifies each task's judgment content, routes it to the cheapest seat that
SPINE.md-224-  clearly clears the bar, fences parallel work, tracks the mission, reports to the boss. Gets its
SPINE.md-225-  hands dirty when the dispatch gate says a job is too small to delegate; anything it builds is
SPINE.md:226:  reviewed from outside its own lineage, like anyone's work.
SPINE.md-227-- **Builder** ΓÇö builds/investigates a bounded ticket. Floats between seats per mission (three
SPINE.md-228-  flips, three causes: capability, price, infrastructure).
SPINE.md:229:- **Independent reviewer** ΓÇö the fresh, unloyal read from a different effective-model vendor + lineage
SPINE.md:230:  (not merely a different account hosting the builder's own brain), or a boss-launched fresh seat.
SPINE.md:231:  Never approves its own lineage's work.
SPINE.md-232-- **The human (boss)** ΓÇö the ONLY one who assigns missions, rules forks, and merges.
SPINE.md-233-
SPINE.md-234----
SPINE.md-235-
SPINE.md-236-## PART IV ΓÇö THE FLEET-LEGALITY TEST (character-free)
SPINE.md-237-
SPINE.md:238:Parallel seats are permitted. What is banned is a fleet nobody declared, bounded, or counted.
SPINE.md:239:**A fleet is legal only if all five hold:**
SPINE.md-240-- **Declared.** The human is told the shape of the fan-out before it runs: how many seats, doing
SPINE.md-241-  what. No seat spawns seats nobody asked for.
SPINE.md-242-- **Bounded.** A hard cap on seats, set in advance. "As many as it takes" is not a number.
SPINE.md-243-- **Accounted.** Every seat's output is attributable to a seat. Anonymous work is banned.
SPINE.md-244-- **Still Principle 3.** Fanning out does NOT let a model review its own work by proxy. A reviewer
SPINE.md:245:  inside the builder's **owning-seat lineage** (that seat plus everything it spawns, transitively,
SPINE.md-246-  regardless of vendor or harness) is not a reviewer.
SPINE.md-247-- **Authority inheritance.** Every spawned agent inherits the owning seat's authority limits and
SPINE.md-248-  prohibitions in full. Its output remains work of that seat and never constitutes independent review.
SPINE.md-249-
SPINE.md-250-*If a fan-out cannot be justified in one sentence, it is decoration.*
SPINE.md-251-
SPINE.md:252:**The declared-seat-lineage clause.** Orchestration means the orchestrator technically launches the
SPINE.md:253:workers; a literal reading of owning-seat lineage would swallow the whole crew into the
SPINE.md:254:orchestrator's lineage and ban all internal review. The clause: a **charter-declared seat** is its
SPINE.md:255:own owning-seat lineage even when another seat launches its session. "Spawns" means the *undeclared*
SPINE.md:256:helpers a seat creates for its own work ΓÇö those inherit the creating seat's lineage. When
SPINE.md:257:orchestrator and a builder are hosted in the SAME session (hats, not separate contexts), they are
SPINE.md:258:ONE lineage, and anything that session builds gets its adversarial review from outside it.
SPINE.md-259-
SPINE.md:260:**The anti-laundering guard: a name is not a lineage.** Charter declaration happens in the doctrine,
SPINE.md-261-not mid-mission. Hanging a crew name on a freshly spawned context does not move it out of its
SPINE.md:262:launcher's lineage. The adversarial review of anything a session built must come from a seat that is
SPINE.md:263:(a) a **different effective-model vendor + lineage** (different weights, training, no shared context ΓÇö
SPINE.md-264-reduces correlated blind spots without eliminating them; a different account merely hosting the
SPINE.md:265:builder's OWN brain does NOT count ΓÇö see the effective-model preflight), or (b) **launched by the
SPINE.md:266:boss**, not by the producing session. A producer-launched same-vendor context wearing a crew name is a spawn, whatever
SPINE.md:267:its label; its approval counts for nothing.
SPINE.md-268-
SPINE.md-269-**Continuity.** If a seat goes dark mid-mission, the lane halts and the human reassigns; the
SPINE.md-270-invariant that survives any reassignment is Principle 3. A successor appointed to a seat joins that
SPINE.md:271:seat's lineage and inherits its restrictions in full ΓÇö succession never converts unapproved work
SPINE.md-272-into fresh-eyes material.
SPINE.md-273-
SPINE.md-274----
SPINE.md-275-
SPINE.md-276-## PART V ΓÇö THE ADJUDICATION PROTOCOL (character-free)
SPINE.md-277-
SPINE.md-278-The insight behind every mechanism: **models agree by default. Agreement is the low-energy state,
SPINE.md-279-so disagreement has to be structural, not requested.**
SPINE.md-280-
SPINE.md:281:1. **Per-finding ACCEPT or DISPUTE, in writing.** The builder answers every review finding
SPINE.md-282-   individually, with a basis. Silence is not an option; blanket "good points, I'll incorporate" is
SPINE.md-283-   banned ΓÇö blanket agreement is where false consensus hides.
SPINE.md-284-2. **Findings are ranked and mechanized: BLOCKER / MATERIAL / MINOR / NOT PROVEN.** A finding must
SPINE.md-285-   cite the failure mechanism and a reproduction path; one without them is NOT PROVEN by definition
SPINE.md-286-   and does not block. Vibes don't rank. This raises the price of theater (the reviewer must commit
SPINE.md-287-   to a falsifiable claim that can be checked and can fail); it does not abolish it.
SPINE.md-288-3. **Repairs get a fresh review.** A reviewer never auto-blesses compliance with its own suggested
SPINE.md-289-   fix: a proposed fix is itself unreviewed code.
SPINE.md-290-4. **Claims are capped at what a model can prove.** "Gates pass," never "it works." (Ladder of Truth.)
SPINE.md-291-5. **Three lists, and the containment must hold.** Independence of the reviewer's identity is worth
SPINE.md:292:   nothing if the builder chooses what the reviewer sees. A reviewed mission produces **three lists,
SPINE.md-293-   from three different sources:**
SPINE.md-294-   - **The write set** ΓÇö frozen in the ticket **before** the build (globs resolved at freeze time):
SPINE.md:295:     every path the builder is *permitted* to touch. A fence, normally larger than what changes.
SPINE.md-296-   - **The actual delta** ΓÇö enumerated **after** the build **from the repository itself, never from
SPINE.md:297:     the builder's account** (`git diff --name-status` vs the recorded baseline **plus**
SPINE.md-298-     `git status --porcelain` for untracked files).
SPINE.md-299-   - **The review manifest** ΓÇö echoed by the reviewer as its report's first line: every file it
SPINE.md-300-     actually received, **each with a content hash the reviewer computed from the bytes it was
SPINE.md:301:     given**, not copied from a builder-supplied header. Oversized sets go in acknowledged chunks.
SPINE.md-302-
SPINE.md-303-   **The rule is containment, not equality:** `actual delta Γèå write set` **and**
SPINE.md-304-   `actual delta Γèå review manifest`.
SPINE.md-305-   - Path in delta but not write set = **fence breach** ΓåÆ mission INCOMPLETE even if the code is
SPINE.md-306-     perfect; reported, never tidied away.
SPINE.md-307-   - Path in delta but not manifest = the reviewer never saw something that changed ΓåÆ INCOMPLETE,
SPINE.md-308-     any "no findings" verdict void.
SPINE.md-309-   - Hash mismatch = the reviewer read something other than the code ΓåÆ INCOMPLETE.
SPINE.md-310-
SPINE.md:311:   The builder curates none of the three. The mission report prints all three so a human who was not
SPINE.md-312-   watching can check containment in ten seconds.
SPINE.md-313-6. **A disputed finding escalates on the strongest falsifiable evidence available, and "no test
SPINE.md:314:   exists" NEVER means NOT PROVEN.** When a builder DISPUTEs a BLOCKER or MATERIAL:
SPINE.md-315-   - **Deterministically testable and a harness exists ΓåÆ someone writes the test**, and it must
SPINE.md-316-     **fail against current code**. A red test is necessary, not sufficient: **the oracle must be
SPINE.md:317:     approved by a seat outside the test author's lineage, or by the boss, quoting the clause of the
SPINE.md-318-     original task it rests on.** A reviewer asserting the wrong expected behavior can turn correct
SPINE.md-319-     code red ΓÇö if the task doesn't settle what "correct" is, that's a **requirements fork the boss
SPINE.md-320-     rules before the test counts.**
SPINE.md-321-   - **Not testable that way** (a race, design flaw, security assumption, doc contradiction, an
SPINE.md-322-     in-hand validation no test can perform) ΓåÆ escalate on the **strongest falsifiable evidence
--
SPINE.md-327-When the capped rounds end in disagreement, the dispute goes UP to the human as a formal fork, both
SPINE.md-328-positions stated. **Models do not negotiate their way to consensus. Under this method, convergence
SPINE.md-329-isn't how anything ends. A ruling is.**
SPINE.md-330-
SPINE.md-331-**The amendment scar (kept, because a methodology that hides its own audit is not one).** A
SPINE.md:332:four-seat evaluation fleet was told to break this protocol. The hole it found: every rule fixed
SPINE.md:333:*who* reviews and none fixed *what the reviewer is handed* ΓÇö a builder could pass a curated diff to
SPINE.md-334-a genuinely independent reviewer, collect an honest "no findings," and hand the human a report that
SPINE.md-335-reads exactly like rigor. **Proving a second model was in the room says nothing about what you gave
SPINE.md-336-it.** Mechanisms 5 and 6 above are the fix, and the FIRST DRAFT of both was marked NOT DISCHARGED by
SPINE.md-337-the reviewer: draft-5 derived write set and manifest from the same ticket (moved the curation hole,
SPINE.md-338-didn't close it ΓåÆ hence three lists, one enumerated from the repo, with hashes); draft-6 would have
--
SPINE.md-354-### The dispatch gate (before every task)
SPINE.md-355-Two questions: (1) multiple stages, files, or surfaces? (2) would doing it inline burn frontier
SPINE.md-356-quota on non-judgment work? Both no ΓåÆ just do it, signed by whoever did it. Any yes ΓåÆ delegate with
SPINE.md-357-a ticket. Scale the crew to the job (one worker for a contained task; two-to-four for genuinely
SPINE.md-358-independent workstreams; more only on the boss's explicit ask) and always inside the five-prong
SPINE.md:359:fleet test. **Fan-outs cost multiples, not increments.**
SPINE.md-360-
SPINE.md-361-### Routing: capability classes, never dated model IDs
SPINE.md-362-| Class | Work it gets | Route to |
SPINE.md-363-|---|---|---|
SPINE.md-364-| **FRONTIER** | architecture, ambiguous debugging, final judgment | the strongest VERIFIED seat |
--
SPINE.md-407-**What each posture DOES ΓÇö defined SOLELY as choices over the five levers** (a posture that pulls no
SPINE.md-408-lever is a costume; the label is not the behavior):
SPINE.md-409-
SPINE.md-410-| Posture | When | How it spends the levers |
SPINE.md-411-|---|---|---|
SPINE.md:412:| **WAR CHEST** | primary FLAGSHIP, support MID or better | FRONTIER seat hosts judgment work freely; fan-outs allowed per the fleet test (lever 1 open); full-rigor review on everything nontrivial; builds ride either frontier seat. Down-tier pressure LOW. |
SPINE.md-413-| **CRUISE** | primary FLAGSHIP/MID with lesser or thin support | Implementation defaults to WORKHORSE/FAST seats (lever 3 pushed down); FRONTIER reserved for routing, architecture, and adversarial review; fan-outs modest; soak the idler vendor's quota first when headroom is lopsided (lever 5). Down-tier pressure MEDIUM. |
SPINE.md-414-| **SHOESTRING** | primary ENTRY | Dispatch gate tightens (lever 2): solo work is the default, orchestration only when the job genuinely fans out; fan-outs OFF by default (lever 1 closed); builds ride whichever vendor's window is freshest (lever 5); the strongest VERIFIED seat appears only as the routing brain and the final review pass. Down-tier pressure HIGH. |
SPINE.md-415-| **LIMP HOME** | a vendor rate-limited or down mid-mission (runtime only) | Flip the seats (the three-flips law ΓÇö seat maps are mission state); shed FAST work first; the adversarial channel is the last thing you let fail. |
SPINE.md-416-
SPINE.md-417-**When the support seat is thin or missing.** The adversarial channel does not require a rich second
SPINE.md:418:vendor: the anti-laundering guard's two legal review paths ΓÇö a different effective-model vendor, OR a
SPINE.md-419-boss-launched fresh-context seat ΓÇö are what keep budget shops honest.
SPINE.md-420-- **Support = ENTRY:** the second vendor reviews everything nontrivial; it takes the hammer only when
SPINE.md-421-  the primary's window is drained. (A review reads a diff and a build writes one, so a review is
SPINE.md-422-  *usually* the cheaper of the two ΓÇö "usually" is doing real work there, and it is not a measurement.)
SPINE.md-423-- **Support = MINIMAL (free tier):** spend the tiny allowance where cross-vendor eyes matter most ΓÇö
SPINE.md-424-  the riskiest diffs, safety-rule code, anything about to ship. **Everything else** gets a
SPINE.md-425-  boss-launched fresh-context reviewer on the primary vendor. (Channel selection is intensity, not a
SPINE.md-426-  coverage cut ΓÇö see "Review coverage is NOT a lever.")
SPINE.md:427:- **Support = NONE (solo vendor):** every review is a boss-launched fresh seat on the primary vendor,
SPINE.md:428:  given the original task verbatim and none of the builder's narrative. Stated once, honestly:
SPINE.md-429-  cross-vendor review is the strongest form available (different weights, training, no shared
SPINE.md-430-  context), but it **reduces correlated blind spots; it does not eliminate them** ΓÇö two vendors can
SPINE.md-431-  still share training sources and failure modes. It is a diversity heuristic, not an independence
SPINE.md-432-  proof; a solo shop runs a weaker version of an already-imperfect guarantee. The process still runs,
SPINE.md-433-  the law still binds, and the boss's own eyes matter more.
--
SPINE.md-482-something, worth less than proof. **And the honesty test cannot prove causation:** one mission's
SPINE.md-483-ledger cannot show what the *other* posture would have done. That needs the same missions run at two
SPINE.md-484-postures with token counts compared, by someone who is not us. **This project has never run that
SPINE.md-485-comparison. If you do, we will publish it whichever way it falls.**
SPINE.md-486-
SPINE.md:487:### Reachability & effective-model preflight (declaration Γëá detection)
SPINE.md-488-The three-question interview above is a **declaration** ΓÇö it records the billing bands the boss
SPINE.md-489-*states*, and nothing more. It is NOT detection: it cannot tell you which seats actually answer or
SPINE.md-490-which model is really behind a host. Independence and reviewer-counting require a separate
SPINE.md-491-**preflight**, run before any seat is cast or counted as a reviewer:
SPINE.md:492:- **Reachability.** Probe each candidate seat (e.g. a `--version` or trivial call on each vendor CLI
SPINE.md-493-  or account this session can dispatch to). A seat that does not answer is not in the pool ΓÇö mark it
SPINE.md-494-  UNREACHABLE; never assume reachability from the declaration.
SPINE.md:495:- **Effective model + lineage.** For every reachable seat, establish the **effective model vendor and
SPINE.md:496:  producing lineage** behind the host ΓÇö never the CLI name, the host brand, the billing account, or
SPINE.md-497-  the banner color. A host can rent another vendor's brain (an Antigravity/Gemini host running a
SPINE.md:498:  Claude model is a *Claude* lineage, not an independent reviewer of Claude work). **Independence
SPINE.md:499:  compares the effective model + lineage, and only that.**
SPINE.md-500-- **Fail CLOSED on the unknown.** If the effective identity behind a seat cannot be established, it is
SPINE.md-501-  `UNKNOWN LINEAGE` and may **never** be counted as a cross-vendor reviewer. Unknown fails closed to
SPINE.md-502-  `REVIEW UNAVAILABLE`, never to FULL CROSS-VENDOR.
SPINE.md-503-- **The independence status is an OUTPUT of this preflight**, not of the declaration:
SPINE.md:504:  `FULL CROSS-VENDOR` (a reachable seat on a different effective-model vendor than the build) ┬╖
SPINE.md:505:  `SOLO-VENDOR DEGRADED` (only a boss-launched fresh-context seat on the builder's own vendor is
SPINE.md-506-  available) ┬╖ `REVIEW UNAVAILABLE` (neither reachable). Every launcher runs this preflight, populates
SPINE.md-507-  the cast map only from its result, and prints that status in its receipt.
SPINE.md-508-
SPINE.md-509-### Tickets (the dispatch contract)
SPINE.md:510:Sections: **TASK** (for reviewer tickets, the boss's ORIGINAL words verbatim, never the builder's
SPINE.md-511-restatement) ┬╖ **EXPECTED OUTCOME** (gradeable before dispatch; can't write the acceptance check ΓåÆ
SPINE.md-512-not ready to delegate) ┬╖ **CONTEXT** (file paths, not pasted bulk) ┬╖ **CONSTRAINTS** ┬╖ **MUST DO**
SPINE.md-513-(incl. the exact verify command) ┬╖ **MUST NOT** (incl. "no undeclared spawns") ┬╖ **OUTPUT FORMAT**
SPINE.md-514-┬╖ **WRITE SET** (every file/glob the worker may create or modify ΓÇö mandatory on every implementation
SPINE.md:515:ticket). Every builder ticket carries the load-bearing line: *"'I could not tell what you meant' is
SPINE.md-516-a good outcome. Propose, don't guess."* Ambiguity is a finding, not an input.
SPINE.md-517-
SPINE.md-518-### The WRITE SET fence (parallel dispatch)
SPINE.md-519-Parallel tickets require **provably disjoint write sets**, including shared manifests, lockfiles,
SPINE.md-520-and generated files. Any overlap ΓåÆ serialize, or give each worker worktree isolation. Snapshot the
--
SPINE.md-531-### Escalation (cap the loop, Principle 8 mechanized)
SPINE.md-532-1. Failure caused by the ticket ΓåÆ fix the ticket, same seat (doesn't count against it).
SPINE.md-533-2. First real failure at a seat ΓåÆ retry the same seat with something changed (corrected ticket,
SPINE.md-534-   added context, raised effort).
SPINE.md-535-3. Second real failure ΓåÆ one seat up, **or** the orchestrator takes over (its build reviewed from
SPINE.md:536:   outside its lineage).
SPINE.md-537-4. Top seat failed, or round cap hit ΓåÆ the boss rules, with the evidence.
SPINE.md-538-Never a third identical retry. Never re-try a cheaper seat on a task that proved it needs a bigger one.
SPINE.md-539-
SPINE.md:540:### Review dispatch
SPINE.md-541-**Who may review** (the two legal paths, from Part IV's anti-laundering guard): a **different
SPINE.md:542:effective-model vendor + lineage** (preferred ΓÇö different weights/training/context; a different
SPINE.md:543:account merely hosting the builder's own brain does NOT count, see the effective-model preflight),
SPINE.md-544-OR a **boss-launched fresh
SPINE.md:545:seat** (legal, weaker, flagged) ΓÇö never the builder's own producing lineage. **Route by FIT within
SPINE.md-546-those paths:** send each review to the strongest-fit independent seat for the work TYPE ΓÇö the
SPINE.md-547-sharpest bug-proving seat for code, the frontier seat for architecture/judgment, a cheap independent
SPINE.md:548:seat for a scan or a tie-breaking extra vote ΓÇö always outside the builder's lineage. Which concrete
SPINE.md:549:model that is, is the shop's wiring (Appendix A), not the engine's law.
SPINE.md-550-
SPINE.md-551-**The reviewer ticket carries exactly four things:**
SPINE.md:552:1. The **ORIGINAL task, verbatim** (never the builder's restatement).
SPINE.md:553:2. The **review set: every file the ticket's write set permitted**, whole, uncurated. The builder
SPINE.md-554-   does not choose what the reviewer sees.
SPINE.md-555-3. The **diff over that set**, plus acceptance criteria.
SPINE.md-556-4. The **verify command and its output**, so the reviewer can re-run rather than trust.
SPINE.md:557:**Never the builder's reasoning** ΓÇö anchoring a reviewer on the builder's narrative converts an
SPINE.md-558-adversarial read into a confirmatory one. (Then the three lists + disputed-findings mechanisms of
SPINE.md-559-Part V apply.) Broken tooling does not stop the channel: hand the reviewer the code itself via
SPINE.md-560-stdin. **The adversarial channel is the last thing you let fail.**
SPINE.md-561-
SPINE.md-562-### THE COUNCIL ΓÇö the multi-vendor panel (the orchestrator's special move)
SPINE.md:563:The council is the fan-out turned to full width: instead of one builder + one reviewer, the
SPINE.md-564-orchestrator convenes **every reachable vendor at once** ΓÇö one per seat, each a genuinely different
SPINE.md:565:effective-model lineage ΓÇö for independent reads on a single high-stakes question. It is the SPECIAL
SPINE.md-566-move (Doctrine 5's right-size still rules ΓÇö never the default for small work); reach for it when the
SPINE.md-567-stakes justify the multiples: a design-space-wide fork, a decision that must be right, a bug or claim
SPINE.md-568-that has to survive real scrutiny.
SPINE.md-569-
SPINE.md-570-**Consent gates the convening ΓÇö offered, never auto-fired.** Even when work looks council-worthy, the
--
SPINE.md-594-   load-bearing error is a council WIN.
SPINE.md-595-5. **Two-round cap** (Principle 8): one exchange per dispute, then the bell; unresolved splits go to
SPINE.md-596-   the boss's ruling queue. No looping, no token-inferno.
SPINE.md-597-6. **The boss rules.** The council advises; the human decides and merges ΓÇö always (the Ladder's top rung).
SPINE.md-598-
SPINE.md:599:This is adversarial verification at full width ΓÇö the one cross-lineage-review law (a review comes
SPINE.md:600:from a different effective-model vendor than the build ΓÇö a same-vendor read is a labeled degraded
SPINE.md-601-self-check, never disguised as cross-vendor), scaled to N independent perspectives. Each tier dresses it
SPINE.md-602-differently ΓÇö a plain **panel** (report by model name), a signed **crew council**, or a puppeteered
SPINE.md-603-**set-piece** ΓÇö but the engine underneath is this single procedure. *(A four-model council once MISSED
SPINE.md-604-a bug that one real use surfaced instantly ΓÇö Part I ┬º1. The council widens coverage; it does not
SPINE.md-605-replace in-hand validation.)*
--
SPINE.md-608-Phone-readable (Principle 10): outcome first; per-seat one-liners (name, color, status); rulings
SPINE.md-609-needed as concrete options to react to, never a blank page; a cost note whenever a fan-out ran.
SPINE.md-610-Claims capped: "gates pass," "review adjudicated," "in-hand validation pending" ΓÇö never "it works."
SPINE.md-611-
SPINE.md-612-### The three flips (why seat assignment is mission state, not method state)
SPINE.md:613:The builder seat has flipped for three causes: **capability** (the vendor with local file/shell/git
SPINE.md-614-access got the hammer), **price** (one vendor's budget ran dry, the other had headroom),
SPINE.md-615-**infrastructure** (a sandbox broke; the seat that could still write files built). In each flip the
SPINE.md:616:cold reviewer surfaced defects the builder missed ΓÇö including guard tests that would pass even with
SPINE.md-617-their callback deleted, and a reviewer's own overclaims discarded under the NOT PROVEN rule. **The
SPINE.md:618:seat map is mission state, never method state. The only fixed point is that the lineage which produced
SPINE.md-619-the work does not approve it.**
SPINE.md:620:Practical scars: when the reviewer can't read the repo, HAND IT THE CODE via stdin ┬╖ let the builder
SPINE.md:621:write files and the reviewer/orchestrator run git after the gate passes (the builder does not commit
SPINE.md-622-its own work) ┬╖ a seat given an underspecified task wrote a proposal instead of guessing ΓÇö that
SPINE.md:623:instruction is load-bearing, keep it in every builder ticket.
SPINE.md-624-
SPINE.md-625----
SPINE.md-626-
SPINE.md-627-## PART VII ΓÇö REVIEW-CULTURE MECHANICS (character-free; CREW adds the rivalry, SHOW adds the drama)
SPINE.md-628-
--
SPINE.md-630-tale: a two-agent shop where every review spawned a six-minute all-hands argument about whether a
SPINE.md-631-color was red or pink, and no work ever shipped.)*
SPINE.md-632-- **Reviews never stop the line.** Builders build to the end of their lane; reviews land at the
SPINE.md-633-  CHECKPOINT (lane/episode end), not mid-swing.
SPINE.md-634-- **Circle-backs are scheduled, not ambushed.** Non-blocking findings collect for the scheduled
SPINE.md:635:  circle-back at the checkpoint; a reviewer never ambushes a builder mid-lane with them.
SPINE.md-636-- **Severity ladder, enforced (the canonical four ΓÇö Part V's `BLOCKER / MATERIAL / MINOR / NOT
SPINE.md-637-  PROVEN`).** A **BLOCKER** (breaks correctness, loses data, bricks the boss's box) may surface
SPINE.md-638-  immediately ΓÇö WITH a suggested fix. **MATERIAL** (load-bearing but not a blocker ΓÇö the old "Major")
SPINE.md-639-  and **MINOR** wait for the scheduled circle-back as one-line notes. **NOT PROVEN** (no failure
SPINE.md-640-  mechanism or repro) never blocks and never ships. Never a meeting.
--
SPINE.md-669-## PART VIII ΓÇö THE SIGNATURE MECHANIC & THE CANONICAL INVARIANT BLOCK
SPINE.md-670-
SPINE.md-671-**Signature mechanic (Principle 1 made literal).** Every message from a seat ends with its color.
SPINE.md-672-The colorΓåÆidentity binding is a tier concern: the Deck tags by MODEL (≡ƒƒí orchestrator ┬╖ ≡ƒƒá Claude ┬╖
SPINE.md-673-≡ƒö╡ Codex ┬╖ ΓÜ½ Grok ┬╖ ≡ƒƒó Gemini); CREW binds those colors to CHARACTERS. SPINE owns only the rule
SPINE.md:674:*that every seat signs* and the vendorΓåÆcolor map (Appendix A).
SPINE.md-675-
SPINE.md-676-**The canonical invariant block is defined HERE and nowhere else** (Principle 9). Entry files and
SPINE.md-677-every tier's launcher skill copy it VERBATIM; everything else in them is a pointer:
SPINE.md-678-
SPINE.md-679-```
SPINE.md-680-TRM INVARIANTS (v2026-07-22 r2 ┬╖ doctrine: SPINE.md)
SPINE.md-681-- Whoever built it never approves it; review comes from a different
SPINE.md:682:  effective-model vendor and lineage, or a boss-launched fresh seat.
SPINE.md-683-- Claims are capped at evidence: "gates pass," never "it works."
SPINE.md-684-- Disagreements go UP to the boss; convergence never ends anything, a
SPINE.md-685-  ruling does.
SPINE.md-686-- Every crew message signs its color; the boss alone assigns missions
SPINE.md-687-  and merges.
--
SPINE.md-689-
SPINE.md-690-*Note on the block id: the `v2026-07-22 r2` inside the block is the invariant block's own identity
SPINE.md-691-and is intended CONTINUITY ΓÇö it tracks the invariant text itself, independent of SPINE's minor
SPINE.md-692-version (SPINE may be v1.0, v1.1, ΓÇª while the block stays at its revision until its wording changes ΓÇö
SPINE.md-693-bumped r1 ΓåÆ r2 on 2026-07-22, when "another vendor's account" was tightened to "a different
SPINE.md:694:effective-model vendor and lineage"). The block is
SPINE.md-695-verified byte-identical across SPINE and all three launchers; do not change it to match a spine
SPINE.md-696-version.*
SPINE.md-697-
SPINE.md-698----
SPINE.md-699-
--
SPINE.md-705-
SPINE.md-706-- **Codex (OpenAI)** ΓÇö bounded implementation of a clear spec; the sharpest code reviewer (proves
SPINE.md-707-  bugs, cites sources). `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`.
SPINE.md-708-- **Grok (xAI)** ΓÇö fearless UI/skins/concept pages; surface only, never engine.
SPINE.md-709-  `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <f> --always-approve < /dev/null`. Mandatory trail entry.
SPINE.md:710:- **Gemini / Antigravity (Google)** ΓÇö proven builder (Flash), IMAGE GEN via Nano Banana (on the sub,
SPINE.md-711-  no card), cheap reviews/sweeps, independent 4th vote, and **the Overflow Valve** (rents Claude/GPT
SPINE.md-712-  brains on Google's tab when the Claude meter runs hot ΓÇö count agy as the GOOGLE bloodline only when
SPINE.md-713-  wearing a Gemini model; agy-running-Claude is not an independent reviewer of Claude work).
SPINE.md-714-  `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.6 Flash (High)"`.
SPINE.md-715-  agy `--model` strings are exact-match; Claude tiers need the `(Thinking)` suffix.
--
SPINE.md-717-  independently (render/probe/screenshot) ΓåÆ re-ticket ΓåÆ loop. Trails mandatory where the fence is
SPINE.md-718-  wider than one file.
SPINE.md-719-- **The arsenal is OPTIONAL.** The method works with whatever vendors are reachable (Claude alone is
SPINE.md-720-  a valid, degraded arsenal). No specific vendor, plan, or price is part of the method.
SPINE.md-721-- **This shop's Lineage Ledger location (wiring, NOT law):**
SPINE.md:722:  `<your-brain>\_claude-brain\memory\model-lineage-ledger.md`. The engine (Doctrine 6) names
SPINE.md:723:  no absolute path ΓÇö downloaders default to a project-relative `model-lineage-ledger.md`; this is
SPINE.md:724:  merely where THIS box keeps its shared fleet-wide store.
SPINE.md-725-
SPINE.md-726-## APPENDIX B ΓÇö FIELD NOTES (append-only; proven capabilities & gotchas, inherited by all tiers)
SPINE.md-727-*(When a run PROVES something new, it goes here so future installs inherit it.)*
SPINE.md-728-- **agy `--model` strings are exact-match**: Claude tiers require the `(Thinking)` suffix ΓÇö
SPINE.md-729-  `"Claude Sonnet 4.6 (Thinking)"`, `"Claude Opus 4.6 (Thinking)"`. A bad string exits 1 and prints
--
SPINE.md-745-  permission error and empty output). Headless dispatches must EMBED the evidence in the prompt
SPINE.md-746-  (reviews-by-embed); probe auth cheaply first with a one-word `-p` ping.
SPINE.md-747-- **Secret-gated verification pattern (proven 2026-07-22):** when a reviewer's sandbox denies it a
SPINE.md-748-  secret the proof needs (e.g. an HMAC key), the reviewer AUTHORS the exact verifier script; a
SPINE.md-749-  key-holding seat EXECUTES it unmodified (trivial repairs applied openly and logged); the verdict
SPINE.md:750:  binds to the output. Keeps builder-never-approves intact when secrets gate the evidence ΓÇö the
SPINE.md-751-  reviewer's NOT-PROVEN-until-run discipline is the correct half of the handshake.
SPINE.md-752-
SPINE.md-753----
SPINE.md-754-*SPINE owns the engine. It names no characters and tells no story ΓÇö those are CREW's and SHOW's to
SPINE.md-755-add, never to restate. Provenance of the Team Rocket Method (authorship, credits, status) lives in

web search: 
web search: site:cursor.com/docs agents Task tool subagent model slug Cursor ...
web search: 
web search: site:cursor.com/docs "Task tool" subagent model ...
web search: 
web search: site:cursor.com/docs/agent/subagents Cursor custom subagents model inherit task ...
web search: 
web search: https://cursor.com/docs/subagents
web search: 
web search: 
web search: 
web search: 
web search: 
web search: 
web search: 
web search: 
codex
SIGNED: OpenAI GPT-5 ┬╖ ≡ƒö╡ ┬╖ CLI

### Gold recommendation

Cursor Grok 4.6 should conduct day-to-day, with Composer 2.5 as its default builder. Both draw from the generous Cursor Models pool; Grok 4.6 is explicitly positioned for long-running, tool-using work, while Composer is tuned for file edits and terminal operations. Human picker-switches should be deliberate exceptions for architecture or independent reviewΓÇönot routine orchestration. [Cursor pricing](https://cursor.com/docs/models-and-pricing), [Grok 4.6](https://cursor.com/docs/models/grok-4-6), [Composer 2.5](https://cursor.com/docs/models/cursor-composer-2-5).

### Seat table

| Enforceable agent slug / model ID | Pool or harness | Owns | Never |
|---|---|---|---|
| `grok-conductor` / `grok-4.6[fast=false,effort=high]` | Cursor Models | Conduct, decompose, diagnose, synthesize, difficult implementation | Approve its own edits; review Cursor/CLI Grok as independent |
| `composer-builder` / `composer-2.5[fast=false]` | Cursor Models | Default fenced implementation, tests, mechanical refactors, long tool loops | Architecture authority; approve Composer-built work |
| `claude-architect` / `claude-fable-5[effort=high]` | Cursor Other Models; normally parked | Architecture, requirements judgment, gnarly review | Routine builds; silent dispatch on Pro |
| `gpt-reviewer` / `gpt-5.6-sol` | Cursor Other Models; normally parked | Adversarial code review, validation/security, bounded hard implementation | Approve OpenAI-built work; silent dispatch |
| `gemini-flash-builder` / `gemini-3.7-flash` | Cursor Other Models, or `agy` CLI overflow | First-class high-throughput builder, repo-wide investigation, test generation, cold review of non-Google work | ΓÇ£Fourth-vote/spareΓÇ¥ treatment; approve Google-built work |
| `gemini-pro-analyst` / `gemini-3.1-pro` | Other Models or `agy` overflow | Long-context/vision analysis, UI-from-evidence, architecture escalation | Mechanical work Flash can carry |
| `grok-cli-overflow` / live `grok.exe` roster | Super Grok subscription | Overflow ideation/build, second harness | Review Cursor Grok as independent: same effective lineage |

These are real current Cursor IDs; subagent filenames/names must use lowercase hyphens. Reviewer definitions should set `readonly: true`. Cursor documents that Task calls can select exact model IDs, including options such as `fast=false`. [Subagent configuration](https://cursor.com/docs/subagents).

### Gemini 3.7 seat in one sentence

Gemini 3.7 Flash is the primary high-throughput investigator-builder and test author, with independent-review eligibility whenever Google did not produce the workΓÇönot an overflow spare or ceremonial fourth vote.

### Pro $20 review honesty

Cursor Pro has two separate pools: Grok/Composer consume Cursor Models; Claude, Gemini, and GPT consume the $20 Other Models pool. Default mode must deny the latter. Grok-versus-Composer is useful distinct-lineage internal checking, but Cursor documents both providers as Cursor, so under current SPINEΓÇÖs ΓÇ£different effective-model vendor **and** lineageΓÇ¥ rule it is not `FULL CROSS-VENDOR`.

Legal approval is therefore:

- Explicitly authorized CLI review by Claude, Codex, or Gemini: `FULL CROSS-VENDOR`.
- Boss-launched fresh-context review: `SOLO-VENDOR DEGRADED`.
- Otherwise: `REVIEW UNAVAILABLE`, work reported as review-pending.

A parent-created fresh chat is not ΓÇ£boss-launched.ΓÇ¥ A skill prompt cannot enforce billing alone: use a `subagentStart` hook, which can inspect `subagent_model` and deny the spawn. [Cursor hooks](https://prod.cursor.com/docs/hooks).

### Delete vs keep

Delete Fable-as-permanent-gold, Grok-UI-only, Gemini-as-cheap-spare/fourth-vote, dated model rosters, and automatic CLI probing during Cursor-native startup.

Keep SPINEΓÇÖs Gate-0, tickets, write-set fences, original-task reviewer packet, evidence ladder, council ask-first, lineage ledger, boss-only judgment, and builder-never-approves. If GrokΓåöComposer is to become an approving path, that requires an explicit SPINE revision and a new statusΓÇönot a branch-local euphemism.

### Files

- `SKILL.md`: thin loader and default billing posture.
- `SPINE.md`: one canonical copy, referencedΓÇönot duplicated.
- `CURSOR-NATIVE.md`: Task semantics and Cursor Models-only default.
- `CLI-OVERFLOW.md`: separate, ask-first commands and billing identities.
- `MODEL-DISPATCH-GUIDE.md`: complete strength/ID rewrite.
- `.cursor/agents/*.md`: one pinned definition per seat.
- `.cursor/hooks.json` plus a guard script: deny unapproved models.
- `dispatch-state.schema.json`: record mode, builder model/lineage, write set, reviewer, and approval status.

### Disagreements I expect

Some seats will call GrokΓåöComposer cross-vendor because their underlying weights differ. That is defensible diversity, but contradicts SPINEΓÇÖs current conjunction and CursorΓÇÖs provider labels. Others will park GeminiΓÇÖs capability because its Cursor billing is parked; capability and enabled billing posture must remain separate facts.

### Confidence

High on the repository doctrine, current official Cursor pools, IDs, and hook surface. I read `SKILL.md`, `SPINE.md`, and `MODEL-DISPATCH-GUIDE.md`. I did not inspect the off-repo Cursor draft, execute live Cursor Task calls, verify installed CLI account entitlements, or probe the current `agy`/`grok.exe` model rosters.
tokens used
114,430
SIGNED: OpenAI GPT-5 ┬╖ ≡ƒö╡ ┬╖ CLI

### Gold recommendation

Cursor Grok 4.6 should conduct day-to-day, with Composer 2.5 as its default builder. Both draw from the generous Cursor Models pool; Grok 4.6 is explicitly positioned for long-running, tool-using work, while Composer is tuned for file edits and terminal operations. Human picker-switches should be deliberate exceptions for architecture or independent reviewΓÇönot routine orchestration. [Cursor pricing](https://cursor.com/docs/models-and-pricing), [Grok 4.6](https://cursor.com/docs/models/grok-4-6), [Composer 2.5](https://cursor.com/docs/models/cursor-composer-2-5).

### Seat table

| Enforceable agent slug / model ID | Pool or harness | Owns | Never |
|---|---|---|---|
| `grok-conductor` / `grok-4.6[fast=false,effort=high]` | Cursor Models | Conduct, decompose, diagnose, synthesize, difficult implementation | Approve its own edits; review Cursor/CLI Grok as independent |
| `composer-builder` / `composer-2.5[fast=false]` | Cursor Models | Default fenced implementation, tests, mechanical refactors, long tool loops | Architecture authority; approve Composer-built work |
| `claude-architect` / `claude-fable-5[effort=high]` | Cursor Other Models; normally parked | Architecture, requirements judgment, gnarly review | Routine builds; silent dispatch on Pro |
| `gpt-reviewer` / `gpt-5.6-sol` | Cursor Other Models; normally parked | Adversarial code review, validation/security, bounded hard implementation | Approve OpenAI-built work; silent dispatch |
| `gemini-flash-builder` / `gemini-3.7-flash` | Cursor Other Models, or `agy` CLI overflow | First-class high-throughput builder, repo-wide investigation, test generation, cold review of non-Google work | ΓÇ£Fourth-vote/spareΓÇ¥ treatment; approve Google-built work |
| `gemini-pro-analyst` / `gemini-3.1-pro` | Other Models or `agy` overflow | Long-context/vision analysis, UI-from-evidence, architecture escalation | Mechanical work Flash can carry |
| `grok-cli-overflow` / live `grok.exe` roster | Super Grok subscription | Overflow ideation/build, second harness | Review Cursor Grok as independent: same effective lineage |

These are real current Cursor IDs; subagent filenames/names must use lowercase hyphens. Reviewer definitions should set `readonly: true`. Cursor documents that Task calls can select exact model IDs, including options such as `fast=false`. [Subagent configuration](https://cursor.com/docs/subagents).

### Gemini 3.7 seat in one sentence

Gemini 3.7 Flash is the primary high-throughput investigator-builder and test author, with independent-review eligibility whenever Google did not produce the workΓÇönot an overflow spare or ceremonial fourth vote.

### Pro $20 review honesty

Cursor Pro has two separate pools: Grok/Composer consume Cursor Models; Claude, Gemini, and GPT consume the $20 Other Models pool. Default mode must deny the latter. Grok-versus-Composer is useful distinct-lineage internal checking, but Cursor documents both providers as Cursor, so under current SPINEΓÇÖs ΓÇ£different effective-model vendor **and** lineageΓÇ¥ rule it is not `FULL CROSS-VENDOR`.

Legal approval is therefore:

- Explicitly authorized CLI review by Claude, Codex, or Gemini: `FULL CROSS-VENDOR`.
- Boss-launched fresh-context review: `SOLO-VENDOR DEGRADED`.
- Otherwise: `REVIEW UNAVAILABLE`, work reported as review-pending.

A parent-created fresh chat is not ΓÇ£boss-launched.ΓÇ¥ A skill prompt cannot enforce billing alone: use a `subagentStart` hook, which can inspect `subagent_model` and deny the spawn. [Cursor hooks](https://prod.cursor.com/docs/hooks).

### Delete vs keep

Delete Fable-as-permanent-gold, Grok-UI-only, Gemini-as-cheap-spare/fourth-vote, dated model rosters, and automatic CLI probing during Cursor-native startup.

Keep SPINEΓÇÖs Gate-0, tickets, write-set fences, original-task reviewer packet, evidence ladder, council ask-first, lineage ledger, boss-only judgment, and builder-never-approves. If GrokΓåöComposer is to become an approving path, that requires an explicit SPINE revision and a new statusΓÇönot a branch-local euphemism.

### Files

- `SKILL.md`: thin loader and default billing posture.
- `SPINE.md`: one canonical copy, referencedΓÇönot duplicated.
- `CURSOR-NATIVE.md`: Task semantics and Cursor Models-only default.
- `CLI-OVERFLOW.md`: separate, ask-first commands and billing identities.
- `MODEL-DISPATCH-GUIDE.md`: complete strength/ID rewrite.
- `.cursor/agents/*.md`: one pinned definition per seat.
- `.cursor/hooks.json` plus a guard script: deny unapproved models.
- `dispatch-state.schema.json`: record mode, builder model/lineage, write set, reviewer, and approval status.

### Disagreements I expect

Some seats will call GrokΓåöComposer cross-vendor because their underlying weights differ. That is defensible diversity, but contradicts SPINEΓÇÖs current conjunction and CursorΓÇÖs provider labels. Others will park GeminiΓÇÖs capability because its Cursor billing is parked; capability and enabled billing posture must remain separate facts.

### Confidence

High on the repository doctrine, current official Cursor pools, IDs, and hook surface. I read `SKILL.md`, `SPINE.md`, and `MODEL-DISPATCH-GUIDE.md`. I did not inspect the off-repo Cursor draft, execute live Cursor Task calls, verify installed CLI account entitlements, or probe the current `agy`/`grok.exe` model rosters.
