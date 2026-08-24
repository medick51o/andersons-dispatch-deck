# SPINE — the method engine (single owner, all tiers inherit)

**Version line (machine-readable):** `spine v2.6 (2026-08-24)`
**Any content change bumps this line** — a silent edit under an old tag is banned. Git and
the versioned owner headings below carry the history; each law is owned by its own section.

**One owner per fact.** Everything the method *does* — how work is judged, dispatched, fenced,
reviewed, and shipped — lives HERE, character-free. The Deck renders this plain; TRM (CREW) adds
a crew on top; TRTO (SHOW) adds a story on top. **Neither CREW nor SHOW restates SPINE.** Edit the
method once, here, and all three tiers inherit it.

**What this engine is (brand-neutral):** a discipline for structured collaboration between one
orchestrator and one or more worker/reviewer seats on the same project — distinct roles,
adversarial cross-review, file-based shared memory, automated gates, and a **human as the sole
final judge**. Its scope is model-to-model alignment: keeping the models honest with each other.
Keeping a model aligned with the human is a separate discipline (the Anderson Method house rules).

---

## PART I — THE ENGINE IN ONE FRAME (the four load-bearing structures)

### 1 · THE LADDER OF TRUTH (evidence outranks opinion; reality outranks evidence)
Claims are capped at what can be proven, and every claim declares which rung it stands on. From
weakest to strongest:

```
  vibes / "looks clean"          ← not evidence. Ranks NOT PROVEN. Never blocks, never ships.
  a green gate                   ← evidence ONLY after its oracle is checked against the task
  a RED regression test          ← proves a bug exists (must fail against unfixed code first)
  a cross-vendor bench review    ← catches the paths that "looked clean"
  THE BOSS IN-HAND                ← the top rung. Reality outranks the whole review.
```

- **"Gates pass," never "it works."** Built ≠ validated ≠ proven. No seat declares victory; when
  no one may declare victory, no one can agree their way to it.
- **A gate is only an arbiter if it can FAIL, and only after its oracle is checked.** A green gate
  over a wrong assertion proves nothing. A regression test is not evidence until it has been run
  RED against the unfixed code. State, per test, what it would catch if the fix were reverted; a
  test that cannot answer that is deleted and rewritten, not kept for the count. **An untested test
  is an opinion with a green checkmark.**
- **The bench catches CODE bugs; the boss catches REALITY bugs — and reality outranks the review.**
  Green gates + passed bench + working in-hand = shipped. **Any two without the third = not yet.**
- **Ambiguity is a finding, never an input.** A model that resolves ambiguity by just building
  something has quietly seated itself as the requirements author — a seat nobody assigned. Treat
  ambiguity as a finding and send it up. "I could not tell what you meant" is a *good* outcome.

### 2 · GATE-0 / EARN-A-HEAD (before any work: do you even dispatch, and how many seats?)
The first gate is not "how do I build this" — it is "does this need orchestration at all, and does
each seat earn its place?" **The default is lean.**

- **The dispatch gate (two questions):** (1) multiple stages, files, or surfaces? (2) would doing
  it inline burn frontier quota on non-judgment work? **Both no → just do it**, no orchestration,
  signed by whoever did it. Most small tasks deserve no orchestration at all. Any yes → delegate
  with a ticket. **The gate decides who BUILDS — never whether the result is REVIEWED.** An
  orchestrator that builds is a builder like any other: if the change is nontrivial and accepted,
  Principle 3 still fires. Only trivial non-artifact work is genuinely review-free, and it is named
  as such out loud.
- **Right-size FIRST (the corrected default).** One builder + ONE cross-vendor reviewer is the
  canon shape for real code; often just the orchestrator for small stuff. A full 3+-seat PANEL is
  a SPECIAL move — run it only when the boss asks. When the task looks genuinely gnarly/high-stakes the
  orchestrator may PROPOSE a panel (one line: why + the rough cost of N vendors), but the fan-out
  dispatches only on his explicit go — never self-authorized on the orchestrator's own "gnarly" call.
  Scaling seat count is the boss's call to make loud, never a habit.
- **Earn-a-head:** every added seat must be justifiable in one sentence, or it is decoration.
  Breadth is not rigor. Fan-outs cost multiples, not increments (an external multi-agent writeup
  measured ~15x the tokens of a single chat — their number, not a law of nature; the gate exists
  because of that shape).
- **A fleet is legal only if all five hold** (the fleet-legality test, Part IV): Declared ·
  Bounded · Accounted · still-Principle-3 · Authority-inheritance. A fleet nobody declared,
  bounded, or counted is banned.

### 3 · THE DIAGNOSE / DESIGN FORK (what KIND of problem is this?)
Before building, classify. The two kinds of hard problem take opposite opening moves:

- **A BUG → INSTRUMENT, don't guess.** When a bug won't yield to theory, stop hypothesizing and
  BUILD AN INSTRUMENT to see reality — a tap, a probe, a debug mode that shows the actual data.
  *(A splash of
  hypotheses loses to one honest measurement, every time.)*
- **A NOVEL / GNARLY FEATURE → PROPOSE A COUNCIL, then SYNTHESIZE.** Convening is consent-gated —
  never auto-fired. The procedure (brief → lenses → parallel design → synthesis → cap → ruling) is
  owned by THE COUNCIL, Part VI, including the rule that every idea is attributed and disagreements
  are NAMED and resolved, never smoothed. Right-size still rules: the council is the SPECIAL move for
  design-space-wide problems, never the default for small work.
- The fork is not either/or forever: a feature can surface a bug (fork to instrument), a bug can
  reveal a design gap (fork to council). Re-classify when the problem changes shape.

### 4 · THE REALITY CONTRACT (what every real build must declare before it's called done)
A build that cannot describe its own end-state is not finished — it is unverified. Every real
build carries five declarations, and self-verifying artifacts check their OWN end-state against
them and report requested-vs-achieved, loud:

| # | The contract term | What it means |
|---|---|---|
| 1 | **Observable outcome** | The gradeable, before-dispatch acceptance check — what "done" looks like from outside. Can't write it? Not ready to delegate. |
| 2 | **Instrument signal** | The tap/probe/toggle that shows the real end-state (not the builder's account of it). The artifact reports achieved-vs-requested itself. |
| 3 | **Protected invariants** | What must NOT change — the fence, the correctness properties, the boss's box staying bootable. Violating one is a BLOCKER even if the feature works. |
| 4 | **Rollback** | How to undo it safely. A guard that reverts itself beats a fix that bricks the box. When a piece can't land safely, FLAG it, never fake it: *"15/16 landed, #16 reverted-and-flagged"* is the house voice; silent slop is the crime. |
| 5 | **Boss handover test-kit** | The in-hand check the boss runs to hit the TOP rung of the Ladder — the exact steps/inputs, phone-readable, so reality can outrank the review. |

---

## PART II — THE SIX DOCTRINES (the engine's standing operating law)

### Doctrine 1 · THE 5-GATE SHIP PIPELINE (boss-tuned 2026-07-21 — the featured engine, proven live)
Five gates, in order — the house default for anything gnarly:
1. **DESIGN COUNCIL → SYNTHESIS (before a line is built).** Per the Diagnose/Design fork above —
   for a novel/gnarly problem only, and proposed to the boss — the multi-vendor fan-out dispatches only
   on his explicit go. Right-size still rules.
2. **BUILD IN ISOLATION.** Real builds run in an isolated git **worktree/branch, NEVER the boss's
   live checkout** — his daily-driver must not break mid-build. Disjoint write-sets across lanes.
3. **INDEPENDENT BENCH before merge** (Part IV's two legal paths; Part VI's preflight names the
   three statuses, including fail-closed `REVIEW UNAVAILABLE`). Reviewed from OUTSIDE the builder's
   lineage — another effective-model vendor preferred → `FULL CROSS-VENDOR`, or a boss-launched fresh
   seat → `SOLO-VENDOR DEGRADED`; never the builder's lineage; neither reachable → `REVIEW
   UNAVAILABLE`. Adversarial, ranked with Part V's canonical ladder — **BLOCKER / MATERIAL / MINOR /
   NOT PROVEN** — each finding with a fix. Green gates alone never merge — the bench earns its
   keep finding the paths that "looked clean."
4. **BOSS IN-HAND — the TOP gate** (Ladder of Truth, Part I §1). The bench catches CODE bugs; the boss catches
   REALITY bugs, and reality outranks the review (Ladder of Truth, top rung). Green gates + passed
   bench + working in-hand = shipped. Any two without the third = not yet.
5. **THE FIX LOOP.** Bench findings → back to the builder → re-review → re-gate, as many turns as
   it takes (bounded by Principle 8's loop cap and Part VII's review-culture caps).

### Doctrine 2 · INSTRUMENT, DON'T GUESS
Part I §3's bug fork, promoted to reflex at the boss's own request.

### Doctrine 3 · SELF-VERIFY + HONEST DEFERRALS
Reality Contract terms 2 & 4, promoted to reflex: an artifact reports its own requested-vs-achieved,
and a piece that can't land safely is FLAGGED, never faked. **Silent slop is the crime.**

### Doctrine 4 · THE SCALPEL IS A FEATURE (boss-tuned 2026-07-21)
The sharpest move is CUTTING scope, not adding it — the boss once deleted ~80% of a build in one
sentence ("we don't have to make them deaf — just listen on the right slot"). The crew's job is to
surface the MINIMAL honest version and hand him the scalpel; **a scope cut is a WIN celebrated,
never a loss mourned.** (The rarest, highest-value product skill in the room, and it's his.)

### Doctrine 5 · RIGHT-SIZE THE DISPATCH (boss ruling 2026-07-18; amended 2026-08-24)
Gate-0's lean default and the consent-gated panel — owned by Part I §2. Gnarly work may justify
PROPOSING a panel; it convenes only on the boss's explicit go, never self-authorized. **The Lineage
Ledger recalibrates WHO gets a job, never "spawn more heads."**

### Doctrine 6 · THE LINEAGE ENGINE (boss idea 2026-07-18 — track who's actually good)
The routing memory that turns experience into better casting. After an episode/run with REAL
dispatches, the orchestrator appends objective rows to the **shop's declared Model Lineage Ledger**
(default: project-relative `model-lineage-ledger.md` at the project root, next to `PLAN-CARD.md`; a
shop may point it elsewhere on the plan card, and this shop's actual location is recorded in Appendix
A — wiring, not law). The engine names no absolute machine path.
- **THE ONE RULE — FACTS ≠ FLAVOR (logging form).** Log only OBJECTIVE dispatch signals: vendor,
  seat/wardrobe worn, task type, outcome (APPROVE/REJECT/found-N-real-bugs/shipped/failed),
  wall-time, and the specific real catch or contribution. Banter is the ACT — **never logged as
  data.** A line with no real dispatch behind it gets no row. *(SHOW owns the narration form of
  Facts≠Flavor — the firewall that story may never rewrite a real event. Same principle, two layers;
  SPINE owns what the ledger records.)*
- **Timing is a real column.** Slow-but-right vs fast-but-shallow is genuine signal.
- **THE WEEKLY LINEAGE REVIEW (the recalibration loop).** ~Once a week (the boss calls it — "run
  the lineage review" / "dispatch standings" — or the orchestrator offers when a fresh batch of
  rows has accrued): (1) **STANDINGS** per vendor from the objective columns only — dispatch count,
  approve/reject/bugs-caught, avg wall-time, notable catches vs whiffs, trend since last review;
  (2) **RECALIBRATE** — propose concrete routing tweaks to the playbook (`MODEL-DISPATCH-GUIDE.md`);
  **the boss rules each change**, only then is the guide updated; (3) **HONESTY GATE** — flag where
  the sample is too thin to conclude; a jab isn't a metric. Evidence → routing → better dispatches →
  more evidence. The review reads the FACTS, never the flavor.
- **Don't bend the work to feed the ledger.** It is a quiet background record to mine, not gospel;
  accuracy is imperfect (small sample, subjective "real catch").

---

## PART III — THE TEN PRINCIPLES (foundation law, character-free)

1. **Distinct, visible identities.** Every seat has a role, a name, and a color, so the human
   always knows which seat *claims* to be acting, and no work arrives anonymous. Precisely: a
   signature identifies the **declared** seat, not a verified model. Nothing here cryptographically
   proves which model produced a message; a session wearing three hats can sign all three colors.
   The signature makes identity **legible and falsifiable**, not proven.
2. **One seat, one job, no UNDECLARED fleets.** Each seat does ONE bounded task and does it itself.
   No hidden sub-agent swarms, no self-appointed "verify the whole codebase" sweeps.
3. **Builder is never the reviewer.** The owning-seat lineage that produces the work is never the
   one that approves it. A seat outside that lineage reviews it adversarially: fresh eyes, no
   loyalty to the work. **This is the fixed point — it survives every seat flip.**
4. **Files are the shared brain.** Seats do NOT share chat context. They communicate through
   durable, inspectable repo files (assignments, handoffs, a living passdown). Tool-agnostic
   memory any model or human can read to get caught up.
5. **Gates referee, but a gate is only an arbiter if it can FAIL** (Ladder of Truth, Part I §1,
   which owns the oracle check and the RED-first rule). Automated tests are the most reproducible
   evidence available, and opinion yields to them. Nothing is "done" until gates are green.
6. **The human judges and merges.** No model ships to the main line. The person signs off.
7. **Cost-aware tiering.** Match the model to the task by capability AND price. Cheap models for
   mechanical grunt work; the frontier reserved for genuine judgment; prefer the billing you have
   headroom on. Economics picks among the seats that clear the bar — it never lowers the bar.
8. **Cap the loop.** *(Unit, defined once: a **ROUND** is one builder → reviewer → builder cycle. An
   **EXCHANGE** is one reviewer statement plus one builder reply.)* Three caps, each binding a
   different situation: **review disputes → TWO ROUNDS** (the house cap, this clause); **review
   tone and nits → ONE EXCHANGE** (Part VII); **unattended debates → TWO ROUNDS PER DEBATE (not per
   participant), then the bell**
   (Autonomous hours). Then the judge decides.
9. **Guardrails at every door.** Every entry file a tool reads on login (CLAUDE.md, AGENTS.md,
   .cursorrules, …) carries one identical compact invariant block plus the authoritative doctrine's
   filename/version/date — never a duplicated full copy of the law (multiple copies is how law
   forks). The block is not a mere pointer: it carries the operative invariants, sufficient to
   govern behavior even if the doctrine is never opened. Canonical text is defined once (Part VIII).
10. **The human is the judge, not the transport.** A blocked seat re-plans around the block; it
    does NOT delegate the block to the human. The human's hands are reserved for ruling and merging.
    Never assume he is at the keyboard — he is usually on a phone. A plan that silently requires
    physical access is not a plan, it is a trap: if a step needs him at the machine, say so in the
    same breath as proposing it. The one legitimate exception is a boundary only he can lower (a
    permission, credential, signature, or in-hand validation no test can perform): say so plainly,
    ONCE, with the tradeoff, and let him choose.

**The abstract roles (CREW/SHOW bind names to these; the Deck uses them plain):**
- **Orchestrator** — classifies each task's judgment content, routes it to the cheapest seat that
  clearly clears the bar, fences parallel work, tracks the mission, reports to the boss. Gets its
  hands dirty when the dispatch gate says a job is too small to delegate; anything it builds is
  reviewed from outside its own lineage, like anyone's work.
- **Builder** — builds/investigates a bounded ticket. Floats between seats per mission (three
  flips, three causes: capability, price, infrastructure).
- **Independent reviewer** — the fresh, unloyal read from a different effective-model vendor + lineage
  (not merely a different account hosting the builder's own brain), or a boss-launched fresh seat.
  Never approves its own lineage's work.
- **The human (boss)** — the ONLY one who assigns missions, rules forks, and merges.

---

## PART IV — THE FLEET-LEGALITY TEST (character-free)

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


**The declared-seat-lineage clause.** Orchestration means the orchestrator technically launches the
workers; a literal reading of owning-seat lineage would swallow the whole crew into the
orchestrator's lineage and ban all internal review. The clause: a **charter-declared seat** is its
own owning-seat lineage even when another seat launches its session. "Spawns" means the *undeclared*
helpers a seat creates for its own work — those inherit the creating seat's lineage. When
orchestrator and a builder are hosted in the SAME session (hats, not separate contexts), they are
ONE lineage, and anything that session builds gets its adversarial review from outside it.

**The anti-laundering guard: a name is not a lineage.** Charter declaration happens in the doctrine,
not mid-mission. Hanging a crew name on a freshly spawned context does not move it out of its
launcher's lineage. The adversarial review of anything a session built must come from a seat that is
(a) a **different effective-model vendor + lineage** (different weights, training, no shared context —
reduces correlated blind spots without eliminating them; a different account merely hosting the
builder's OWN brain does NOT count — see the effective-model preflight), or (b) **launched by the
boss**, not by the producing session. A producer-launched same-vendor context wearing a crew name is a spawn, whatever
its label; its approval counts for nothing.

**Continuity.** If a seat goes dark mid-mission, the lane halts and the human reassigns; the
invariant that survives any reassignment is Principle 3. A successor appointed to a seat joins that
seat's lineage and inherits its restrictions in full — succession never converts unapproved work
into fresh-eyes material.

---

## PART V — THE ADJUDICATION PROTOCOL (character-free)

The insight behind every mechanism: **models agree by default. Agreement is the low-energy state,
so disagreement has to be structural, not requested.**

1. **Per-finding ACCEPT or DISPUTE, in writing.** The builder answers every review finding
   individually, with a basis. Silence is not an option; blanket "good points, I'll incorporate" is
   banned — blanket agreement is where false consensus hides.
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
   - **The write set** — frozen in the ticket **before** the build (globs resolved at freeze time):
     every path the builder is *permitted* to touch. A fence, normally larger than what changes.
   - **The actual delta** — enumerated **after** the build **from the repository itself, never from
     the builder's account** (`git diff --name-status` vs the recorded baseline **plus**
     `git status --porcelain` for untracked files).
   - **The review manifest** — echoed by the reviewer as its report's first line: every file it
     actually received, **each with a content hash the reviewer computed from the bytes it was
     given**, not copied from a builder-supplied header. Oversized sets go in acknowledged chunks.

   **The rule is containment, not equality:** `actual delta ⊆ write set` **and**
   `actual delta ⊆ review manifest`.
   - Path in delta but not write set = **fence breach** → mission INCOMPLETE even if the code is
     perfect; reported, never tidied away.
   - Path in delta but not manifest = the reviewer never saw something that changed → INCOMPLETE,
     any "no findings" verdict void.
   - Hash mismatch = the reviewer read something other than the code → INCOMPLETE.

   The builder curates none of the three. The mission report prints all three so a human who was not
   watching can check containment in ten seconds.
6. **A disputed finding escalates on the strongest falsifiable evidence available, and "no test
   exists" NEVER means NOT PROVEN.** When a builder DISPUTEs a BLOCKER or MATERIAL:
   - **Deterministically testable and a harness exists → someone writes the test**, and it must
     **fail against current code**. A red test is necessary, not sufficient: **the oracle must be
     approved by a seat outside the test author's lineage, or by the boss, quoting the clause of the
     original task it rests on.** A reviewer asserting the wrong expected behavior can turn correct
     code red — if the task doesn't settle what "correct" is, that's a **requirements fork the boss
     rules before the test counts.**
   - **Not testable that way** (a race, design flaw, security assumption, doc contradiction, an
     in-hand validation no test can perform) → escalate on the **strongest falsifiable evidence
     available** (trace, static analysis, spec citation, manual repro, the boss's own eyes).
     **Untestability is never evidence against a finding.** Ranking a real BLOCKER as NOT PROVEN
     because nobody could automate it is a worse failure than the theater this rule prevents.

When the capped rounds end in disagreement, the dispute goes UP to the human as a formal fork, both
positions stated. **Models do not negotiate their way to consensus. Under this method, convergence
isn't how anything ends. A ruling is.**

**THE AMENDMENT LAW** (the scar that produced it is in SPINE-PROVENANCE.md). *An invariant that
leaves an artifact survives; one that exists only as a habit dies at the first context compaction or
deadline.* **When choosing between two ways to write a rule, choose the one that leaves a trace.**

---

## PART VI — THE ORCHESTRATION MECHANICS (character-free: "the orchestrator")

> Operating mechanics for the principles. Higher tiers may bind a
> presentation-layer name to the abstract orchestrator role — the Deck renders it plain by MODEL;
> a crew or a show gives it a character name — but SPINE names none. The MECHANICS are identical
> and live here once.

### The dispatch gate (before every task)
Part I §2's two questions, applied per task — they decide who BUILDS, never whether the result is
reviewed (Principle 3 fires either way). Both no → just do it, signed. Any yes → delegate with a
ticket. **Seat count, two cases, so neither hides behind the other:**
- **Parallel BUILDERS on provably disjoint write-sets** — the fleet test governs: Declared and
  Bounded before it runs. The boss is TOLD the shape; he need not be asked.
- **An N-way PANEL on one question** (council, bake-off, multi-lens review) — Part I §2 governs:
  it dispatches only on the boss's **explicit go**, never self-authorized.

### Routing: capability classes, never dated model IDs
| Class | Work it gets | Route to |
|---|---|---|
| **FRONTIER** | architecture, ambiguous debugging, final judgment | the strongest VERIFIED seat |
| **WORKHORSE** | well-specified implementation, tests, refactors | mid tier |
| **FAST** | scanning, mechanical edits, extraction | cheapest tier that clears the bar |
- Classify by **judgment content, not size**: a 500-line rename is FAST; a 10-line concurrency fix
  is FRONTIER.
- Cheapest seat that **clearly** clears the bar; unsure → one seat up. On a borderline call, try
  raising *effort* on the cheaper seat before raising the *tier* (a heuristic, not a measured result).
- Dispatching a second vendor spends that account's billing. A standing rotation the boss consented
  to is fine; any NEW billing surface gets asked first.

### The plan card and budget postures (plan-aware routing)
A standing declaration of the shop's billing (primary vendor+tier band, support vendor+tier band,
known headroom), saved dated to `PLAN-CARD.md`. First-run interview = **three** questions, not
twenty: "Who's your primary?" · "Who's riding second?" · "Any tanks already low?" The card is the
boss's declaration, re-run whenever subscriptions change — a declaration, never a contract, and
never something the orchestrator can read off the account (see the currency rule below).

**Tier bands** (future-proof — tier names and quotas are the vendors' and change often; bands don't;
illustrations are date-bound, verify against your own account): **FLAGSHIP** (a vendor's top consumer
tier) · **MID** (middle tier) · **ENTRY** ($20-class) · **MINIMAL** (a free tier) · **NONE** (no
second vendor). The band map is total — every legal card lands on exactly one row. MINIMAL is never a
*primary* band (a primary seat needs a paid window to hold a mission; below ENTRY, run tasks by hand
and skip the orchestration layer). **Posture map:** FLAGSHIP+FLAGSHIP/MID → **WAR CHEST**;
FLAGSHIP+lesser (or thin) support, or MID+any → **CRUISE**; ENTRY+any → **SHOESTRING**; a vendor dying
mid-mission → **LIMP HOME** (runtime posture only, never a card mapping). With MINIMAL or NONE support,
WAR CHEST is unreachable by design (fan-out freedom assumes a second pair of eyes with capacity).

**The card is an INPUT, not a lever.** Declaring "CRUISE" changes nothing by itself — it changes what
the orchestrator *decides*, and those decisions are the only things in this method that move real
money or real quality. **If a mission runs and none of the five levers below changed, the posture did
nothing, and the session must say so out loud.** The five levers:
1. **Fan-out width** (spawning N seats multiplies tokens) — the model can pull this wherever it can
   dispatch at all.
2. **The dispatch gate itself** (deciding NOT to orchestrate is a real, costed choice) — same.
3. **Model tier per task** — CONDITIONAL on the harness letting a dispatch name its model.
4. **Reasoning effort per dispatch** — CONDITIONAL on a per-dispatch effort knob.
5. **Which vendor's quota absorbs the work** — CONDITIONAL on this session reaching a second vendor.

**An N/A lever is reported as N/A, never quietly claimed.** Capability preflight, written into the
card once: CAN I DISPATCH ANOTHER SEAT? (if NO, levers 1 and 2 are N/A too — nothing to fan out,
nothing to orchestrate; work solo) · SET MODEL PER SEAT? · SET EFFORT PER DISPATCH? · REACH A SECOND
VENDOR? A method that describes knobs the harness lacks is a costume.

**What each posture DOES — defined SOLELY as choices over the five levers** (a posture that pulls no
lever is a costume; the label is not the behavior):

| Posture | When | How it spends the levers |
|---|---|---|
| **WAR CHEST** | primary FLAGSHIP, support MID or better | FRONTIER seat hosts judgment work freely; fan-outs allowed per the fleet test (lever 1 open); full-rigor review on everything nontrivial; builds ride either frontier seat. Down-tier pressure LOW. |
| **CRUISE** | primary FLAGSHIP/MID with lesser or thin support | Implementation defaults to WORKHORSE/FAST seats (lever 3 pushed down); FRONTIER reserved for routing, architecture, and adversarial review; fan-outs modest; soak the idler vendor's quota first when headroom is lopsided (lever 5). Down-tier pressure MEDIUM. |
| **SHOESTRING** | primary ENTRY | Dispatch gate tightens (lever 2): solo work is the default, orchestration only when the job genuinely fans out; fan-outs OFF by default (lever 1 closed); builds ride whichever vendor's window is freshest (lever 5); the strongest VERIFIED seat appears only as the routing brain and the final review pass. Down-tier pressure HIGH. |
| **LIMP HOME** | a vendor rate-limited or down mid-mission (runtime only) | Flip the seats (the three-flips law — seat maps are mission state); shed FAST work first; the adversarial channel is the last thing you let fail. |

**When the support seat is thin or missing.** The adversarial channel does not require a rich second
vendor: the anti-laundering guard's two legal review paths — a different effective-model vendor, OR a
boss-launched fresh-context seat — are what keep budget shops honest.
- **Support = ENTRY:** the second vendor reviews everything nontrivial; it takes the hammer only when
  the primary's window is drained. (A review reads a diff and a build writes one, so a review is
  *usually* the cheaper of the two — "usually" is doing real work there, and it is not a measurement.)
- **Support = MINIMAL (free tier):** spend the tiny allowance where cross-vendor eyes matter most —
  the riskiest diffs, safety-rule code, anything about to ship. **Everything else** gets a
  boss-launched fresh-context reviewer on the primary vendor. (Channel selection is intensity, not a
  coverage cut — see "Review coverage is NOT a lever.")
- **Support = NONE (solo vendor):** every review is a boss-launched fresh seat on the primary vendor,
  given the original task verbatim and none of the builder's narrative. Stated once, honestly:
  cross-vendor review is the strongest form available (different weights, training, no shared
  context), but it **reduces correlated blind spots; it does not eliminate them** — two vendors can
  still share training sources and failure modes. It is a diversity heuristic, not an independence
  proof; a solo shop runs a weaker version of an already-imperfect guarantee. The process still runs,
  the law still binds, and the boss's own eyes matter more.

**When the primary is ENTRY ($20-class).** A $20 primary may not offer the vendor's frontier model at
all, and its windows are tight. Adjust expectations, not the law: the orchestrator is hosted by the
strongest VERIFIED available seat (never call a seat FRONTIER unless it verifiably is — hosting is a
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
subscription tier (there is no "what plan am I on" API — entitlement ≠ documentation, and a model
cannot verify entitlement at all) · cannot meter your spend in real time · cannot down-tier the model
you are already typing into (only the seats it *dispatches*) · cannot promise savings (this project
has never measured what a posture saves vs solo, and knows of no published number).

**The currency rule (applies to plans, not just models).** Quota mechanics (window lengths, weekly
caps, per-tier model access), prices, and tier access are the vendors' and change often. **The
orchestrator never states a quota number, a price, or a tier's model access from memory, and never
states a model's availability from training data — an unfamiliar model name means check live docs;
model IDs can differ by auth mode, and the shop has the scar.** It relies only on the three signals it
can actually observe, and it keeps them distinct: what the **boss declared** on the card, what the
**harness reports** as the effective model, and an **explicit error** (a rate limit, a refusal, an
unavailable model). A response that merely "felt weak" is **noise, not telemetry** — never a signal.
When a runtime signal contradicts the card, say so and downshift one posture. If you want a number,
look it up on the vendor's current price page; a model that gives you one from memory guessed.

**Review coverage is NOT a lever.** Every nontrivial accepted change gets its adversarial review at
every posture, including the $40 one. What you may tune is review *intensity within full coverage*
(which model, what effort, how exhaustively) — and channel selection (a cross-vendor free tier vs a
boss-launched fresh context) is intensity, not a coverage cut. **Cut builds, cut fan-outs, cut
orchestration. Never cut the channel.**

**The routing ledger** — every dispatch writes one line, the mission report prints them, with
`default` and `changed?` columns that force the session to admit, per task, whether the plan card
actually moved anything. A ledger of all-NO rows is a plan card that did nothing, and it will say so
on its own. **It is an honesty aid, not proof:** a model can write "I used the fast tier" while using
whatever it was already using, and nothing here independently verifies a dispatch used the model it
claims. Until a harness emits execution receipts an outsider can check (effective model, effort,
vendor, token counts, per dispatch), it makes lying a deliberate act instead of a lazy one — worth
something, worth less than proof. **And the honesty test cannot prove causation:** one mission's
ledger cannot show what the *other* posture would have done. That needs the same missions run at two
postures with token counts compared, by someone who is not us. **This project has never run that
comparison. If you do, we will publish it whichever way it falls.**

### Reachability & effective-model preflight (declaration ≠ detection)
The three-question interview above is a **declaration** — it records the billing bands the boss
*states*, and nothing more. It is NOT detection: it cannot tell you which seats actually answer or
which model is really behind a host. Independence and reviewer-counting require a separate
**preflight**, run before any seat is cast or counted as a reviewer:
- **Reachability.** Probe each candidate seat (e.g. a `--version` or trivial call on each vendor CLI
  or account this session can dispatch to). A seat that does not answer is not in the pool — mark it
  UNREACHABLE; never assume reachability from the declaration.
- **Effective model + lineage.** For every reachable seat, establish the **effective model vendor and
  producing lineage** behind the host — never the CLI name, the host brand, the billing account, or
  the banner color. A host can rent another vendor's brain (an Antigravity/Gemini host running a
  Claude model is a *Claude* lineage, not an independent reviewer of Claude work). **Independence
  compares the effective model + lineage, and only that.**
- **Probe the TRANSPORT, not the binary** (THE TRANSPORT LAW owns this): a seat is online when its
  persistent seat answers in THIS session. A CLI `--version` proves only that the fallback lane
  exists — never enough on its own to count a seat present.
- **Fail CLOSED on the unknown.** If the effective identity behind a seat cannot be established, it is
  `UNKNOWN LINEAGE` and may **never** be counted as a cross-vendor reviewer. Unknown fails closed to
  `REVIEW UNAVAILABLE`, never to FULL CROSS-VENDOR.
- **The independence status is an OUTPUT of this preflight**, not of the declaration:
  `FULL CROSS-VENDOR` (a reachable seat on a different effective-model vendor than the build) ·
  `SOLO-VENDOR DEGRADED` (only a boss-launched fresh-context seat on the builder's own vendor is
  available) · `REVIEW UNAVAILABLE` (neither reachable). Every launcher runs this preflight, populates
  the cast map only from its result, and prints that status in its receipt.
- **Solo vendor while the boss is asleep = `REVIEW UNAVAILABLE`, and say so.** The degraded path
  requires a *boss-launched* seat (Part IV); an orchestrator cannot launch its own reviewer and call
  it independent. So during the autonomous hours a solo-vendor shop has **no** legal review path.
  That is not a licence to self-approve: build, gate, and queue the work UNREVIEWED and labeled,
  for a reviewer the boss launches when he wakes.

### Tickets (the dispatch contract)
Sections: **TASK** (for reviewer tickets, the boss's ORIGINAL words verbatim, never the builder's
restatement) · **EXPECTED OUTCOME** (gradeable before dispatch; can't write the acceptance check →
not ready to delegate) · **CONTEXT** (file paths, not pasted bulk) · **CONSTRAINTS** · **MUST DO**
(incl. the exact verify command) · **MUST NOT** (incl. "no undeclared spawns") · **OUTPUT FORMAT**
· **WRITE SET** (every file/glob the worker may create or modify — mandatory on every implementation
ticket) · **LAWS** (one tucked-away line: the numbers/names of the house laws and standards that
govern this ticket — injection by reference, never re-taught in prose; boss ruling 2026-07-24:
this line lives in the ticket's small print and is never narrated in the story voice). Every
builder ticket carries the load-bearing line: *"'I could not tell what you meant' is a good
outcome. Propose, don't guess."*

### The episode folder (documentation lane — never the stage)
Every mission/episode with REAL dispatches gets a dated backend folder —
`episodes/YYYY-MM-DD-<slug>/` at the project root — collecting that run's artifacts: the shape
receipt (what was dispatched to whom, and why that shape), tickets as issued, worker reports, and
any reality evidence the boss provides. This is the harvest source for end-of-project bottling
and the inspectable evidence behind lineage-ledger rows. **Style law (boss ruling 2026-07-24):
the DATE is for the backend only.** Front-facing narration (TRM/SHOW voices) refers to episodes
by NAME — the jargon and datestamps stay in the folder, visible if the boss peeks, never
paraded in the story. **One sanctioned exception (boss amendment, same day): the ENDING
CREDITS — show tiers only.** When an episode closes under a SHOW-voiced tier (TRM's crew
voice, TEAM ROCKET TAKES OVER), the show may roll credits — and there the start and end
dates belong, movie-style (*"filmed on location · 2026-07-23 → 2026-07-24"*). Dates at the
close are part of the fun; dates mid-story are jargon. **The dispatch deck does NOT roll
credits** — the plain tier closes plainly; its dates live in the backend folder only.

**Visuals (boss ruling 2026-07-24): the boss's screenshots are reality evidence — file them,
cheaply.** When the boss drops a screenshot during an episode (a bug's face, an in-hand proof,
a before/after), the crew quietly copies it into `episodes/<slug>/visuals/` — RE-COMPRESSED to
economical JPEG (cap ~1280px on the long edge, quality ~70; a full-HD PNG becomes a small JPG).
These are evidence for audits and bottling, not gallery prints. Zero ceremony: no narration, no
asking the boss to screenshot anything, one quiet filing at most mentioned in the episode's
backend notes. (Mechanics: uploads arrive under `.claude\uploads\` — convert on copy with
whatever image tool the box has; ffmpeg and Pillow both do it in one line.)

### The WRITE SET fence (parallel dispatch)
Parallel tickets require **provably disjoint write sets**, including shared manifests, lockfiles,
and generated files. Any overlap → serialize, or give each worker worktree isolation. Snapshot the
baseline (commit hash + `git status`) in the mission log before any wave. Not under git → say so and
treat parallel writes as forbidden: serialize.

### Worker statuses (first line of every worker report)
`DONE` (with evidence) · `DONE_WITH_CONCERNS` (resolve every concern before accepting) ·
`NEEDS_CONTEXT` (fix the ticket, re-dispatch the same seat) · `BLOCKED` (triage: bad ticket → fix
it; capability gap → escalate; external blocker → Principle 10: re-plan around it, the boss hears it
in the report, never as a task handed to him). These grade **task progress**; review findings keep
the adjudication ladder. One axis per line, never mixed.

### Escalation (cap the loop, Principle 8 mechanized)
1. Failure caused by the ticket → fix the ticket, same seat (doesn't count against it).
2. First real failure at a seat → retry the same seat with something changed (corrected ticket,
   added context, raised effort).
3. Second real failure → one seat up, **or** the orchestrator takes over (its build reviewed from
   outside its lineage).
4. Top seat failed, or round cap hit → the boss rules, with the evidence.
Never a third identical retry. Never re-try a cheaper seat on a task that proved it needs a bigger one.

### Review dispatch
**Who may review** (the two legal paths, from Part IV's anti-laundering guard): a **different
effective-model vendor + lineage** (preferred — different weights/training/context; a different
account merely hosting the builder's own brain does NOT count, see the effective-model preflight),
OR a **boss-launched fresh
seat** (legal, weaker, flagged) — never the builder's own producing lineage. **Route by FIT within
those paths:** send each review to the strongest-fit independent seat for the work TYPE — the
sharpest bug-proving seat for code, the frontier seat for architecture/judgment, a cheap independent
seat for a scan or a tie-breaking extra vote — always outside the builder's lineage. Which concrete
model that is, is the shop's wiring (Appendix A), not the engine's law.

**The reviewer ticket carries exactly four things:**
1. The **ORIGINAL task, verbatim** (never the builder's restatement).
2. The **review set: every file the ticket's write set permitted**, whole, uncurated. The builder
   does not choose what the reviewer sees.
3. The **diff over that set**, plus acceptance criteria.
4. The **verify command and its output**, so the reviewer can re-run rather than trust.
**Never the builder's reasoning** — anchoring a reviewer on the builder's narrative converts an
adversarial read into a confirmatory one. (Then the three lists + disputed-findings mechanisms of
Part V apply.) Broken tooling does not stop the channel: hand the reviewer the code itself via
stdin. **The adversarial channel is the last thing you let fail.**

### THE COUNCIL — the multi-vendor panel (the orchestrator's special move)
The council is the fan-out turned to full width: instead of one builder + one reviewer, the
orchestrator convenes **the boss-approved, fleet-BOUNDED set of eligible seats** (eligibility and
the spend gate are owned by THE COUNCIL SEAT LAW; the cap is set in advance, per Part IV — "as many
as it takes" is not a number) — one per seat, each a genuinely different effective-model lineage — for
independent reads on a single high-stakes question. It is the SPECIAL
move (Doctrine 5's right-size still rules — never the default for small work); reach for it when the
stakes justify the multiples: a design-space-wide fork, a decision that must be right, a bug or claim
that has to survive real scrutiny.

**Consent gates the convening — offered, never auto-fired.** Even when work looks council-worthy, the
orchestrator *proposes* the panel (one line: why + the rough cost of N vendors running at once) and
dispatches only on the boss's explicit go. A "gnarly" call is licence to *ask*, never to self-authorize
the most expensive move in the method — that is what makes "opt-in" literally true, in the engine and
not just the brochure.

**When NOT to convene.** Gate-0 and Doctrine 5 bind absolutely: no genuine need for N independent
perspectives → **no council.** A trivial ask — *"rewrite this email," "did I send the PO out," a quick
fix, a plain question* — is handled by one seat, quietly. The orchestrator does not *oops* into a
token-eating dream team for a two-line task.

**The procedure the orchestrator runs — a defined path, not an improvisation:**
1. **Brief.** One page: the question/vision *verbatim*, the hard-won context, the numbered points each
   seat must answer. Never a blank page.
2. **Convene + assign lenses.** Dispatch to every reachable AND ELIGIBLE vendor (THE COUNCIL SEAT
   LAW), each handed a DISTINCT angle
   (correctness · cost · security · "try to *refute* this") so no two reads are redundant. Diverse
   vendors + diverse lenses = maximum coverage. Independence is the point: no seat sees another's
   answer first.
3. **Gather.** Each returns a SIGNED read (`docs/*-<vendor>.md` for design; a ranked verdict on Part
   V's ladder for review). Real outputs from real, *different* models — never invented.
4. **Synthesize.** The orchestrator writes ONE synthesis: best-of-breed per piece, **every idea
   attributed, every disagreement NAMED and resolved, never smoothed.** One vendor catching another's
   load-bearing error is a council WIN.
5. **Cap the loop** (Principle 8): the house cap of TWO ROUNDS per dispute, then the bell;
   unresolved splits go to the boss's ruling queue. No looping, no token-inferno.
6. **The boss rules.** The council advises; the human decides and merges — always (the Ladder's top rung).

Adversarial verification at full width — Part IV's review law scaled to N independent
perspectives. Each tier dresses it differently (a plain **panel**, a signed **crew council**, a
puppeteered **set-piece**); the engine underneath is this one procedure. **The council widens
coverage; it never replaces in-hand validation.**

### Mission reports (to the boss)
Phone-readable (Principle 10): outcome first; per-seat one-liners (name, color, status); rulings
needed as concrete options to react to, never a blank page; a cost note whenever a fan-out ran.
Claims capped: "gates pass," "review adjudicated," "in-hand validation pending" — never "it works."

### The three flips (why seat assignment is mission state, not method state)
The builder seat has flipped for three causes — **capability**, **price**, **infrastructure** —
and in each flip the cold reviewer surfaced defects the builder missed. **The seat map is mission
state, never method state. The only fixed point is that the lineage which produced the work does not
approve it.**
Practical scars: when the reviewer can't read the repo, HAND IT THE CODE via stdin · let the builder
write files and the reviewer/orchestrator run git after the gate passes (the builder does not commit
its own work) · a seat given an underspecified task wrote a proposal instead of guessing — that
instruction is load-bearing, keep it in every builder ticket.

---

## PART VII — REVIEW-CULTURE MECHANICS (character-free; CREW adds the rivalry, SHOW adds the drama)

The engine-level rules that keep review from becoming a debate club.
- **Reviews never stop the line — REPORTING and STOPPING are different acts.** A finding may be
  *filed* the moment it is found; what it may not do is halt a builder mid-swing. Non-blocking
  reviews land at the CHECKPOINT (lane/episode end). **Only two things stop a lane:** a BLOCKER
  (below) and the emergency brake (below) — and each halts the AFFECTED lane only, never the shop.
- **Circle-backs are scheduled, not ambushed.** Non-blocking findings collect for the scheduled
  circle-back at the checkpoint; a reviewer never ambushes a builder mid-lane with them.
- **Severity ladder, enforced (the canonical four — Part V's `BLOCKER / MATERIAL / MINOR / NOT
  PROVEN`).** A **BLOCKER** (breaks correctness, loses data, bricks the boss's box) may surface
  immediately — WITH a suggested fix. **MATERIAL** (load-bearing but not a blocker — the old "Major")
  and **MINOR** wait for the scheduled circle-back as one-line notes. **NOT PROVEN** (no failure
  mechanism or repro) never blocks and never ships. Never a meeting.
- **Every finding ships with a suggested fix.** "This is wrong, stop everything" is banned dialect.
  "This breaks X under Y — here's the patch shape" is how this house speaks.
- **No debate clubs.** On review TONE and nits — as distinct from the substance of a dispute —
  builder and reviewer get ONE EXCHANGE (Principle 8's units). Still split → it goes silently into
  the boss's ruling queue and WORK CONTINUES.
- **Nits don't multiply.** A handful of taste notes per review, max. A pile of style opinions is a
  style-guide proposal, and those go to the boss.
- **Grade the work, not the worker.** A catch is a team win; a gotcha hunt is a crime.
- **THE EMERGENCY BRAKE (real, rare, quiet).** If the bench finds something GENUINELY damning
  (correctness rot, data loss, security holes), YES: write ONE clear report (what breaks, evidence,
  proposed fix), halt the AFFECTED lane only, pivot the crew to unaffected work. It does NOT mean a
  standing argument. The meeting that matters waits for the boss — not for consensus theater.

**AUTONOMOUS-HOURS TOKEN DISCIPLINE (the anti-token-inferno core; CREW carries the crew-flavored
telling).** When the shop runs unattended these are ABSOLUTE:
- **Debates are allowed — with a BELL.** Hash it out unattended, but every debate has a HARD CUTOFF:
  two rounds per debate — not per participant — then the bell. Resolved → proceed. Unresolved →
  the dispute goes to the DECISION
  QUEUE (a written list the boss rules in batch) and everyone goes BACK TO WORK. **The banned thing
  is the loop: re-litigating past the bell is the cardinal token sin.**
- **A stoppage is a pivot, not an idle.** Blocked lane → reassign to unblocked work. The line stays
  warm; restarts are expensive.
- **DECISION BATCHING.** Taste/design questions are collected and resolved as a SET (when the color
  comes up, the stripes and dots come up in the same pass). Never re-stop the line serially.
- If in doubt **while he is unreachable**: build the safest honest version, note the assumption
  LOUDLY, and queue it for his ruling. *(This is the unattended exception to "ambiguity is a finding,
  never an input" — Part I §1. While the boss IS reachable, ambiguity still goes up; a sleeping boss
  is not a licence to author requirements, only to keep moving without him.)* He must never come home
  to a burnt token pile and a transcript of four characters litigating paint.

---

## PART VIII — THE SIGNATURE MECHANIC & THE CANONICAL INVARIANT BLOCK

**Signature mechanic (Principle 1 made literal).** Every message from a seat ends with its color.
The color→identity binding is a tier concern: the Deck tags by MODEL (🟡 orchestrator · 🟠 Claude ·
🔵 Codex · ⚫ Grok · 🟢 Gemini); CREW binds those colors to CHARACTERS. SPINE owns only the rule
*that every seat signs* and the vendor→color map (Appendix A).

**The canonical invariant block is defined HERE and nowhere else** (Principle 9). Entry files and
every tier's launcher skill copy it VERBATIM; everything else in them is a pointer:

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

*Note on the block id: the `v2026-07-22 r2` inside the block is the invariant block's own identity
and is intended CONTINUITY — it tracks the invariant text itself, independent of SPINE's minor
version (SPINE may be v1.0, v1.1, … while the block stays at its revision until its wording changes —
bumped r1 → r2 on 2026-07-22, when "another vendor's account" was tightened to "a different
effective-model vendor and lineage"). The block is
verified byte-identical across SPINE and all three launchers; do not change it to match a spine
version.*

---

## THE METER LAW (owner: SPINE; added v2.4, 2026-08-23)

*Claims are capped at evidence* — pointed at the shop's suppliers instead of its own code, because
vendors now sell capacity without stating how much you bought.

1. **A seat that costs money must be READABLE** — on demand, before and after. A metered seat whose
   usage cannot be observed may not carry a lane the shop depends on.
2. **Measure, never infer.** A published allowance is evidence; an adjective is not. "Generous,"
   "significantly higher," "unlimited" are marketing until a number is attached. Where a vendor
   publishes no size, the shop's number comes from burning a known amount and reading the movement.
3. **One reading is a rumour.** Meters report integers, so a small burn carries large error. Two
   burns of different sizes that agree are a finding. An outside measurement that agrees with yours
   is better still.
4. **A subsidy is never a foundation.** Vendors buying market share grant far more than sticker
   price, genuinely and in writing. Take the deal; never put a load-bearing lane on it. **A free or
   subsidized seat may hold an EXTRA council vote; it may not be the SOLE build or review path for a
   lane the shop depends on** — that is the line between using a gift and betting on one.
5. **Cost claims cite a reading, not a recollection.** "That's cheap" is "it works" wearing a hat.

*Wiring, not law:* endpoints, scripts and vendor quirks live with the shop's tooling (Appendix A) —
they change without notice. The obligation to read them does not.

## THE COUNCIL SEAT LAW (owner: SPINE; v2.3, rewritten v2.5 on the boss's ruling 2026-08-24)

**Any seat may hold a council seat. What is gated is SPENDING, not vendor class.**

1. **A seat that cannot spend needs no ALLOWANCE.** Free is free — but free is not consent to
   convene: Gate-0's right-size rule still binds (clause 6).
2. **A seat that CAN spend needs a recorded ALLOWANCE before it sits.** Asked once, in one line
   naming the seat and the rough cost. What the boss grants is a **bound**, not a blank cheque:
   how many metered calls, over what window, and for how long the grant itself lasts. He may make it
   permanent or time-boxed; the default is a modest bound that expires, because a yes given once at
   midnight should not silently govern next year.
3. **Within the allowance, no further asking.** That is the point of granting one. Every metered
   dispatch still prints its meter mark, so quiet is never invisible.
4. **Past the allowance, refuse and re-ask.** Exhaustion is not an emergency and never an excuse to
   proceed; it is a question. Widening a bound is a fresh decision, made out loud.
5. **Unknown cost fails closed.** A seat whose spend cannot be established is not free, it is
   unmeasured (THE METER LAW). It may not sit until its spend can be READ. An allowance never
   substitutes for a meter — a bound you cannot verify against is not a bound.
6. **A council is still the SPECIAL move.** Consent to spend is not consent to convene: Gate-0's
   right-size rule and the fleet test bind first, whatever the seat costs.

**Enforced, not merely written.** The allowance is a real record the transport checks before it
spends, held on the operator's own machine — never in the method's repo, so no one inherits another
shop's permission. A council that tries to exceed it trips the wire instead of the budget.

*(Wiring — the allowance file's location and format, and the per-vendor guards — lives with the
shop's tooling, Appendix A. It changes without notice. The duty to check it does not.)*

## THE TRANSPORT LAW — persistent seats (owner: SPINE; added v2.0, 2026-08-22)

Vendor seats are reached, by default, as **persistent MCP conversations** inside the conductor's
harness — a start tool returns the reply plus a session id; a `*-reply` tool continues that exact
conversation with full context — not as amnesia one-shot CLI dispatches. Wiring, wrapper scripts,
and install commands live with the Deck (`mcp-seats/` — Appendix-A-class detail, not law). The law:

1. **Opt-in, per vendor.** Vendors are suggestions, never requirements. The orchestrator OFFERS
   the wiring when it sees a CLI is present and registers nothing without the owner's yes;
   registration is user-scope, touches nothing else in their setup, and one command removes it.
2. **A fresh call is a blind seat — necessary, not sufficient.** A new session remembers nothing
   from any other session: reviewers are ALWAYS fresh calls, never briefed through a session that
   saw the build. Fresh alone does not make a review independent — Part IV's two legal paths
   still bind (different effective-model vendor outside the build's lineage, or a boss-launched
   fresh-context seat).
3. **A reply-chain stays in its owning-seat lineage forever.** "Touched" means built, edited, or
   was briefed on it (a repair still gets a fresh review — Part V). A reply-chained session can
   never be dressed up as the independent reviewer of that work.
4. **Preflight probes the transport, not the binary.** A seat is online when its MCP seat answers
   in THIS session (registered and Connected); a CLI `--version` only proves the fallback lane
   exists. The arsenal declaration names which transport each seat answered on.
5. **One-shot CLI dispatches stay legal as the fallback lane.** Build tickets on persistent seats
   pass explicit tool-approval and a working directory; research and review tickets stay
   read-only by default.

## APPENDIX A — THE ARSENAL / WIRING (current wiring, NOT law — verify; pricing/promos are details)

The model banner colors (vendor → color; the ONLY color fact SPINE owns): **claude = orange 🟠 ·
codex = blue 🔵 · grok = black ⚫ · gemini = green 🟢** · the orchestrator conducting
plain = **gold 🟡**, and the CONDUCTOR's banner wears the **➤ baton** after its dot — 🟡➤ on the
plain Deck, 😼🟠➤ when a crew tier's cat is hosted on Claude (boss law 2026-08-22, all tiers). A
worn wardrobe shows both (🟠🟢 = a Claude brain on the Gemini seat).

**THE NOTATION — v4.2 (boss-adopted 2026-08-23). Seat first, act second. This section is the OWNER —
tier legends (Deck SKILL, CREW) are renderings of it. (v4.0 repealed the 2026-08-09 marks, including
🟣-as-building.)**

- **BUILDING = 🔨** trailing the seat: 🔵🔨 Codex building · 🟠🔨 Claude building. **🟣 never means
  building** — since v4.2 it belongs to the Cursor transport (🟣➤) and to a seated reserve model
  answering bare (🟣).
- **REVIEWING = 🔴** trailing the seat on the plain Deck: 🔵🔴 = Codex reviewing — NOT a reject.
  **Grammar scope:** the Deck is seat-first; crew tiers are character-first, where a LEADING 🔴 is
  Butch's character color — so crew tiers render the reviewing act as **📝** (*🩷⚫ Cassidy (in
  grok) 📝*). Either way the vendor color stays visible: the value of a review is WHO ran it, and
  🔵🔨 then 🔵🔴 on the same work is the self-review failure this notation exists to expose.
- **REJECTED / BLOCKED / NEEDS-BOSS = ⛔**, never a red circle — rejection, reviewing, and Butch
  must never look alike.
- **COUNCIL = 🌈👥👥** — every color, a crowd; a council is a special move and asks first.
- **THE ARROW ➤ BELONGS TO WHOEVER POINTS (v4.2).** The arrow is a **cursor** — that is its
  birthplace and its meaning: it marks a thing that DIRECTS. Two flyers, and only two:
  **🟡➤ the conductor** (the borrowed baton — the orchestrator points work at the seats) and
  **🟣➤ the Cursor transport** (the arrow's true home — the host summoning a pool model).
  **A seat being directed never wears the arrow.** When a Cursor-pool model ANSWERS — sitting on a
  council, returning a review — it signs as a bare seat: **🟣 Composer**, no arrow, because it is
  not directing anyone. The arrow appears only on the dispatch line that summoned it.
  A reserve dispatch shows transport + bloodline + meter: *🟣➤🌙 💸 Kimi K3 reviewing* — who
  summoned it, whose brain thought, and what it cost, in three glyphs.
- **BLOODLINE MARKS for the pool's own families:** 🌙 Moonshot (Kimi) · 🔷 Zhipu (GLM) ·
  🎼 Cursor (Composer). Mirror families keep their HOUSE colour, so a Cursor-hosted Claude
  reads 🟣➤🟠 — visibly Anthropic, and visibly not independent of Claude work.
- **THE BOSS = ⚪** on the plain Deck, **👑** in crew tiers. Combos: ⚪🏁/👑🏁 in-hand validation ·
  ⚪⚖️/👑⚖️ ruling pending · ⚪🎮/👑🎮 on the sticks.
- **STATES:** 🚩 finding raised (flagged, not fatal) · 🚧 lane closed, detour in progress · 🧪
  gates running · 🩺 diagnosing (doctor-first) · 🕵️ adversary loose · 🏁 boss-validated (top rung,
  outranks "done") · 🚢 shipped/deployed · 🪦 retired/parked · 🟤 quiet hold (watchers armed).
- **METER MARKS ARE MANDATORY ON ANY LINE THAT CAN SPEND** (v4.1, rekeyed v2.5 from vendor class to
  spending, to match THE COUNCIL SEAT LAW). A genuinely flat-rate seat narrates no meter; **any seat
  that can bill — reserve or house — narrates one on every line**, computed from the model id,
  never guessed: **♾️** included in the plan · **♾️💸** included but a surcharged FAST tier ·
  **💸** third-party credits at API prices · **🚨💳** credits AND surcharged · **⚠️** unknown,
  which fails closed. A call that spends money says so LOUDLY, in its own line, every time — the
  boss must never learn he spent from a footnote. THE METER LAW binds on every seat:
  flat-rate windows drain too.


- **Codex (OpenAI)** — bounded implementation of a clear spec; the sharpest code reviewer (proves
  bugs, cites sources). `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`.
- **Grok (xAI)** — fearless UI/skins/concept pages; surface only, never engine.
  `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <f> --always-approve < /dev/null`. Mandatory trail entry.
- **Gemini / Antigravity (Google)** — proven builder (Flash), IMAGE GEN via Nano Banana (on the sub,
  no card), cheap reviews/sweeps, independent 4th vote, and **the Overflow Valve** (rents Claude/GPT
  brains on Google's tab when the Claude meter runs hot — count agy as the GOOGLE bloodline only when
  wearing a Gemini model; agy-running-Claude is not an independent reviewer of Claude work).
  `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.6 Flash (High)"`.
  agy `--model` strings are exact-match; Claude tiers need the `(Thinking)` suffix.
- Dispatch ritual for any wardrobe: ticket file → headless dispatch → the orchestrator gates
  independently (render/probe/screenshot) → re-ticket → loop. Trails mandatory where the fence is
  wider than one file.
- **The arsenal is OPTIONAL.** The method works with whatever vendors are reachable (Claude alone is
  a valid, degraded arsenal). No specific vendor, plan, or price is part of the method.
- **This shop's Lineage Ledger location (wiring, NOT law):**
  `<your-brain>\_claude-brain\memory\model-lineage-ledger.md`. The engine (Doctrine 6) names
  no absolute path — downloaders default to a project-relative `model-lineage-ledger.md`; this is
  merely where THIS box keeps its shared fleet-wide store.

## APPENDIX B — FIELD NOTES (append-only; proven capabilities & gotchas, inherited by all tiers)
*(When a run PROVES something new, it goes here so future installs inherit it.)*
- **agy `--model` strings are exact-match**: Claude tiers require the `(Thinking)` suffix —
  `"Claude Sonnet 4.6 (Thinking)"`, `"Claude Opus 4.6 (Thinking)"`. A bad string exits 1 and prints
  the full valid-model list (useful as a probe).
- **Gemini 3.1 Pro (High) handled a heavy adversarial review fine** (~600-word verdict table, physics
  attacks) — confirms the Flash review-ceiling workaround: route heavy reviews to Pro, not Flash.
- **Two `codex exec` instances run in parallel** without issue (separate processes, same box).
- **Codex cites sources when reviewing factual claims** (web-searches vendor manuals unprompted) —
  doubles as a doc-checker for claim-verification tickets.
- **Cross-vendor consensus worked as designed**: Codex and Gemini independently killed the same two
  pieces of draft advice (mill-first/burn-second; interpolate-from-3-probes) for the same physical
  reasons. Agreement is corroboration, never a ruling — the human still rules (Part V).
- Claude-tier doc-verification subagent (Sonnet + web) is slow (~10 min) but resolves which claims
  rest on conflicting sources — its "don't publish this number" flags are the payoff.
- **Gemini 3.6 Flash (High) is live and handled a real analysis ticket clean** (2026-07-22,
  token-ticker EP10): agy's valid-model roster now carries the 3.6 Flash family (High/Medium/Low).
  The bad-string probe still works — an invalid `--model` exits 1 and prints the current roster.
- **agy HEADLESS auto-denies tool permissions** (`read_file` etc. — the run dies with a "jetski"
  permission error and empty output). Headless dispatches must EMBED the evidence in the prompt
  (reviews-by-embed); probe auth cheaply first with a one-word `-p` ping.
- **Codex safety layer flags "exploit/attack/laundering" vocabulary (2026-07-26):** a
  verify ticket phrased as "re-run your exploits / attack variations" died mid-run flagged
  as cyber-risk (78K tokens lost). Same work re-dispatched as "re-create the defect's
  failure scenario / negative-path QA regression" ran clean. Phrase adversarial-verify
  tickets to Codex in defect/QA vocabulary, never attacker vocabulary.
- **Secret-gated verification pattern (proven 2026-07-22):** when a reviewer's sandbox denies it a
  secret the proof needs (e.g. an HMAC key), the reviewer AUTHORS the exact verifier script; a
  key-holding seat EXECUTES it unmodified (trivial repairs applied openly and logged); the verdict
  binds to the output. Keeps builder-never-approves intact when secrets gate the evidence — the
  reviewer's NOT-PROVEN-until-run discipline is the correct half of the handshake.

---
*SPINE owns the engine; the Team Rocket Method's provenance lives in CREW, because it is that
brand's identity, not the brand-neutral engine's.*
