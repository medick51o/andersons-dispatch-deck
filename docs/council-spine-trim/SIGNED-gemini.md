# SPINE Review — The Reader's Eye

**Seat:** Gemini: the reader's eye  
**Model:** Gemini 3.6 Flash (High)  
**Target:** `SPINE.md` (v2.4, 921 lines, ~71 KB)

---

### Reader's Perspective & Summary

Reading `SPINE.md` as a first-time reader, the core architecture is sharp and disciplined. However, as the document grew from v1.0 through v2.4, it accumulated **accreted scaffolding, duplicate law declarations, and transitional notes**. 

While SPINE asserts **Principle 9 ("One owner per fact")**, the file itself frequently violates this principle by re-explaining the same core rules (e.g., the 2-question Dispatch Gate, the two legal review paths, the 2-round debate cap, and council opt-in rules) in 3 to 7 separate sections.

Trimming these restatements, transitional changelogs, and narrative anecdotes yields significant token savings **without removing a single law, guardrail, or operational distinction.**

---

## 1. Findings (Ordered by Lines Saved, Largest First)

---

### Finding 1: Historical Retrospective ("The Amendment Scar") in Part V
* **Location:** [SPINE.md:L338-350](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L338-L350) (13 lines)
* **What is redundant / bloated:** Lines 338–348 spend 11 lines detailing a narrative history of how a 4-seat evaluation fleet broke an earlier protocol draft (detailing draft-5 and draft-6 flaws). The only load-bearing rule here is the "trace rule" stated in lines 349–350.
* **Replacement Text:**
  ```markdown
  **The trace rule.** An invariant must leave an inspectable repository artifact, never rely on memory or context habit. When choosing between two ways to write a rule, choose the one that leaves a trace.
  ```
* **Lines Saved:** **11 lines** (13 lines reduced to 2 lines)
* **What is Lost:** Historical narrative about discarded draft iterations. Zero active rules or guardrails lost.

---

### Finding 2: Re-stating Council Opt-in and Small-Work Exclusions in THE COUNCIL Section
* **Location:** [SPINE.md:L604-615](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L604-L615) (12 lines)
* **What is redundant / bloated:** Lines 604–615 spend 12 lines restating that councils require explicit boss approval and must never be auto-fired for small tasks ("rewrite this email", "oops into a token-eating dream team"). This rule is already defined in Part I §2 ([L66-68](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L66-L68)), Part I §3 ([L88](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L88)), Doctrine 1 ([L123](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L123)), and Doctrine 5 ([L158](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L158)).
* **Replacement Text:**
  ```markdown
  **Consent gates the convening.** The orchestrator proposes a panel (stating why and rough cost) and dispatches only on the boss's explicit go—never auto-fired (Part I §2, Doctrine 5). Small/trivial tasks default to a single seat; Gate-0 binds absolutely.
  ```
* **Lines Saved:** **8 lines** (12 lines reduced to 4 lines)
* **What is Lost:** Verbose illustrative examples. Zero operational laws lost.

---

### Finding 3: Accumulating Version Changelogs in Header
* **Location:** [SPINE.md:L4-10](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L4-L10) (7 lines)
* **What is redundant / bloated:** Lines 4–10 summarize past point releases (v2.0, v2.1, v2.3, v2.4). Every concept summarized here (The Meter Law, The Council Seat Law, Notation v4.1/v4.2, Transport Law) has its own authoritative section downstream ([L734-862](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L734-L862)). Carrying a changelog in the header bloats the engine prompt on every single invocation across all tiers.
* **Replacement Text:** Remove lines 4–10 completely. Keep line 3 (`**Version line (machine-readable):** spine v2.4 (2026-08-23)`).
* **Lines Saved:** **7 lines**
* **What is Lost:** Historical release notes summary in the header. Nothing lost from the active method.

---

### Finding 4: Re-explaining the Two Legal Review Paths across Multiple Sections
* **Location:** [SPINE.md:L575-579](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L575-L579) (5 lines) & [SPINE.md:L434-440](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L434-L440) (7 lines)
* **What is redundant / bloated:** Part IV's Anti-Laundering Guard ([L269-275](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L269-L275)) and Part VI's Preflight ([L506-512](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L506-L512)) authoritatively define the two legal review paths. Lines 575–579 and 434–440 re-explain what effective models mean and why fresh seats are weaker.
* **Replacement Text for L575–579 (Review Dispatch):**
  ```markdown
  **Who may review.** Must be an independent seat via the two legal paths (Part IV, Preflight): a different effective-model vendor/lineage, or a boss-launched fresh seat. Route by fit for the work type.
  ```
* **Replacement Text for L434–440 (Support = NONE):**
  ```markdown
  - **Support = NONE (solo vendor):** Every review is a boss-launched fresh seat on the primary vendor, given the original task verbatim. This runs a degraded diversity heuristic (correlated blind spots remain), but the process and law still bind.
  ```
* **Lines Saved:** **6 lines** total (3 lines saved from L575–579; 3 lines saved from L434–440)
* **What is Lost:** Philosophical restatements of correlated model blind spots. Zero guardrails lost.

---

### Finding 5: Comparative Token Testing Speculation in the Routing Ledger Section
* **Location:** [SPINE.md:L488-493](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L488-L493) (6 lines)
* **What is redundant / bloated:** Lines 488–493 speculate on comparative token testing across postures ("one mission's ledger cannot show what the other posture would have done... This project has never run that comparison. If you do, we will publish it..."). This is an informal essay/invitation rather than a method rule.
* **Replacement Text:** Remove lines 488–493. End the section at line 487 (`...it makes lying a deliberate act instead of a lazy one—worth something, worth less than proof.`).
* **Lines Saved:** **6 lines**
* **What is Lost:** An unexecuted research invitation. Zero operational rules lost.

---

### Finding 6: SHOW-Voiced Ending Credits Exception in Episode Folders Section
* **Location:** [SPINE.md:L536-541](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L536-L541) (6 lines)
* **What is redundant / bloated:** Lines 536–541 describe how SHOW-tier implementations (e.g. Team Rocket) roll movie-style ending credits with datestamps ("filmed on location"). SPINE explicitly declares in line 13 and line 918 that it is the brand-neutral engine that names no characters, tells no story, and leaves presentation voices to CREW/SHOW. Describing Team Rocket credit style in SPINE violates SPINE's declared scope.
* **Replacement Text:** Remove lines 536–541.
* **Lines Saved:** **6 lines**
* **What is Lost:** Presentation-layer fiction notes for SHOW tier. Zero engine mechanics lost.

---

### Finding 7: Duplicate Debate Cap / One-Exchange Rule in Part VII
* **Location:** [SPINE.md:L677-678](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L677-L678) (2 lines) & [SPINE.md:L689-693](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L689-L693) (5 lines)
* **What is redundant / bloated:** Bullet 5 ("No debate clubs") and Autonomous-Hours Bullet 1 ("Debates are allowed — with a BELL") state the exact same 2-round / 1-exchange debate cap within 10 lines of each other in Part VII.
* **Replacement Text:** Combine into a single bullet under Part VII:
  ```markdown
  - **Debates have a 2-round cap (Principle 8).** Maximum one exchange (two rounds each); unresolved splits go silently to the boss's decision queue while work continues on unblocked paths. Re-litigating past the bell is banned.
  ```
* **Lines Saved:** **4 lines**
* **What is Lost:** Duplicate bullet point. Zero mechanics lost.

---

### Finding 8: Duplicate Posture Mapping in Plan Card Posture Text vs Table
* **Location:** [SPINE.md:L392-396](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L392-L396) (5 lines)
* **What is redundant / bloated:** Lines 392–396 list the posture mappings in prose (`Posture map: FLAGSHIP+FLAGSHIP/MID → WAR CHEST...`). The posture table immediately following ([L417-422](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L417-L422)) duplicates these exact mappings in its "When" column (`primary FLAGSHIP, support MID or better`, etc.).
* **Replacement Text:**
  ```markdown
  **Posture map.** The plan card maps to one of four postures (see table below); with MINIMAL or NONE support, WAR CHEST is unreachable by design.
  ```
* **Lines Saved:** **3 lines**
* **What is Lost:** Redundant prose list duplicating table contents.

---

### Finding 9: Doctrine 5 ("RIGHT-SIZE THE DISPATCH") Full Restatement
* **Location:** [SPINE.md:L156-161](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L156-L161) (6 lines)
* **What is redundant / bloated:** Doctrine 5 restates Gate-0 / Right-Sizing from Part I §2 ([L64-68](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L64-L68)).
* **Replacement Text:**
  ```markdown
  ### Doctrine 5 · RIGHT-SIZE THE DISPATCH
  The default is lean: one builder + one reviewer (Part I §2). Full panels are special moves on explicit boss approval. Lineage recalibrates *who* gets a job, not head count.
  ```
* **Lines Saved:** **3 lines**
* **What is Lost:** Inline MAC whack-a-mole reference. Zero rules lost.

---

### Finding 10: Redundant Dispatch Gate Questions in Part VI
* **Location:** [SPINE.md:L361-366](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L361-L366) (6 lines)
* **What is redundant / bloated:** Lines 361–366 re-quote the exact 2 dispatch questions from Part I §2 ([L60-63](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L60-L63)).
* **Replacement Text:**
  ```markdown
  ### The dispatch gate (before every task)
  Run Gate-0 (Part I §2). If both questions are no → do it inline. If any yes → delegate with a ticket. Scale the crew inside the five-prong fleet test (Part IV); fan-outs cost multiples.
  ```
* **Lines Saved:** **3 lines**
* **What is Lost:** Word-for-word restatement of Gate-0. Zero rules lost.

---

### Finding 11: Transitional Version Scaffolding in Gate-0
* **Location:** [SPINE.md:L69-72](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L69-L72) (4 lines)
* **What is redundant / bloated:** Lines 69–72 contain historical transitional wording: `*(This REPLACES the old "whip-crack parallel delegation as default" — that instinct contradicts Gate-0...)*`. This explains what v2.0 replaced from a v1.x version nobody runs.
* **Replacement Text:** Remove lines 69–72.
* **Lines Saved:** **3 lines**
* **What is Lost:** Historical note about past v1.x bad habits. Zero active rules lost.

---

### Finding 12: Restated Ticket Scars in "The Three Flips" Section
* **Location:** [SPINE.md:L654-657](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L654-L657) (4 lines)
* **What is redundant / bloated:** Lines 654–657 state: `when the reviewer can't read the repo, HAND IT THE CODE via stdin... a seat given an underspecified task wrote a proposal instead of guessing...`. Both instructions are exact restatements of line 593 (`hand the reviewer the code itself via stdin`) and line 526 (`Propose, don't guess`).
* **Replacement Text:**
  ```markdown
  Practical scars: let the builder write files and the orchestrator run git after the gate passes (the builder does not commit its own work).
  ```
* **Lines Saved:** **3 lines**
* **What is Lost:** Duplicate ticket guidelines. Zero rules lost.

---

### Finding 13: Doctrine 2 ("INSTRUMENT, DON'T GUESS") Full Restatement
* **Location:** [SPINE.md:L140-142](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L140-L142) (3 lines)
* **What is redundant / bloated:** Doctrine 2 restates the exact sentence from Part I §3 ("When theory stalls, build the instrument...").
* **Replacement Text:**
  ```markdown
  ### Doctrine 2 · INSTRUMENT, DON'T GUESS
  The bug-side reflex: when theory stalls, build an instrument to observe reality (Part I §3).
  ```
* **Lines Saved:** **2 lines**
* **What is Lost:** Duplicate sentence. Zero rules lost.

---

### Finding 14: Doctrine 3 ("SELF-VERIFY + HONEST DEFERRALS") Full Restatement
* **Location:** [SPINE.md:L143-146](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L143-L146) (4 lines)
* **What is redundant / bloated:** Doctrine 3 copies the exact sentences from Part I §4 ("Build things that check their OWN end-state... When a piece can't land safely, FLAG it...").
* **Replacement Text:**
  ```markdown
  ### Doctrine 3 · SELF-VERIFY + HONEST DEFERRALS
  Build artifacts that check their own end-state and report requested-vs-achieved with rollback (Reality Contract terms 2 & 4). Flag unlandable work; silent slop is the crime.
  ```
* **Lines Saved:** **2 lines**
* **What is Lost:** Duplicate sentences. Zero rules lost.

---

### Finding 15: Prior Draft Scar Note in Review Coverage Section
* **Location:** [SPINE.md:L479-481](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L479-L481) (3 lines)
* **What is redundant / bloated:** Lines 479–481 contain a historical note about a bad prior draft: `*(A prior draft said "review only the risky diffs to save money"...)*`. The core rule ("Never cut the channel") is already stated clearly.
* **Replacement Text:** Remove lines 479–481.
* **Lines Saved:** **2 lines**
* **What is Lost:** Historical note about a discarded prior draft. Zero active rules lost.

---

### Finding 16: Historical Version Note in Appendix A Notation v4.1 Header
* **Location:** [SPINE.md:L825-826](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L825-L826) (2 lines)
* **What is redundant / bloated:** Lines 825–826 contain historical changelog references in parentheses: `v4.0 2026-08-22; supersedes the 2026-08-09 marks: 🟣-building is repealed and the ⚪/🟤 reservations are spent`.
* **Replacement Text:**
  ```markdown
  **THE NOTATION — v4.1** (boss-adopted 2026-08-23: Cursor 🟣➤ arrow, bloodline marks, mandatory reserve meters). Seat first, act second. This section is the OWNER—tier legends (Deck SKILL, CREW) are renderings of it.
  ```
* **Lines Saved:** **2 lines**
* **What is Lost:** Historical transitional note from 2026-08-09/v4.0. Zero active notation rules lost.

---

### Finding 17: Lineage Ledger Engine Rule Restatement in Appendix A
* **Location:** [SPINE.md:L880-883](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L880-L883) (4 lines)
* **What is redundant / bloated:** Lines 880–883 re-explain Doctrine 6's rule that the engine names no absolute path and that downloaders default to a project-relative path.
* **Replacement Text:**
  ```markdown
  - **This shop's Lineage Ledger location (wiring, NOT law):** `<your-brain>\_claude-brain\memory\model-lineage-ledger.md` (overrides engine default; Doctrine 6).
  ```
* **Lines Saved:** **2 lines**
* **What is Lost:** Re-explanation of Doctrine 6. Zero facts lost.

---

### Finding 18: Repeated Sentence in Part IV Fleet Legality
* **Location:** [SPINE.md:L257](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L257) (1 line)
* **What is redundant / bloated:** Line 257 states: `*If a fan-out cannot be justified in one sentence, it is decoration.*`. This exact sentence was already stated in line 73 under Earn-a-head.
* **Replacement Text:** Remove line 257.
* **Lines Saved:** **1 line**
* **What is Lost:** Verbatim repeated sentence.

---

## 2. Review Total

* **Total Lines Saved:** **74 lines**
* **Total File Length:** **921 lines**
* **Percentage Cut:** **8.03%** (~8.0% of the entire file)

---

## 3. "Do Not Touch" List (Load-Bearing Passages)

The following passages may appear verbose or candidate targets for compression to an outside eye, but are **load-bearing engine invariants** that must **NOT** be cut:

1. **Part V Mechanisms 5 & 6 (Three Lists + Containment Rule & Disputed Findings Tests, [L298-333](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L298-L333)):**
   * *Why it looks verbose:* Spans ~35 lines detailing write set, actual delta, review manifest, content hashes, `actual delta ⊆ review manifest`, and untestability rules.
   * *Why it is load-bearing:* This is the core protocol defense against the "curated diff" vulnerability. Cutting or shortening this re-opens the security hole where a builder passes a sanitized diff to an independent reviewer.

2. **The Canonical Invariant Block (Part VIII, [L713-722](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L713-L722)):**
   * *Why it looks verbose:* Repeats 4 core rules that are stated elsewhere in the document.
   * *Why it is load-bearing:* Principle 9 requires this exact block to be copied byte-identically across all entry files (CLAUDE.md, .cursorrules, launcher skills). It must remain untouched so system verification tests pass.

3. **Part IV Anti-Laundering Guard & Declared-Seat Lineage Clause ([L259-275](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L259-L275)):**
   * *Why it looks verbose:* Spans ~17 lines distinguishing between charter-declared seats, launcher lineages, and vendor accounts.
   * *Why it is load-bearing:* Without this precise operational definition, either all internal reviews are accidentally banned (by swallowing workers into the orchestrator's lineage) or fake reviews are permitted (by dressing up a same-session context in a crew name).

4. **Part VI Section 3 Plan Card Posture Levers & N/A Clause ([L398-414](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L398-L414)):**
   * *Why it looks verbose:* Enumerates 5 specific levers and insists that an N/A lever must be declared N/A out loud.
   * *Why it is load-bearing:* It prevents posture switching from becoming pure theater when a harness lacks the actual knobs to control model tier, effort, or vendor routing.

5. **Appendix B Field Notes ([L885-916](file:///C:/Sync/Projects/andersons-dispatch-deck/SPINE.md#L885-L916)):**
   * *Why it looks verbose:* A bulleted list of 10 empirical gotchas, CLI flags, safety keyword triggers, and model strings.
   * *Why it is load-bearing:* These are hard-won operational workarounds (e.g. Codex safety bans on "exploit" vocabulary, agy headless tool auto-denials) that prevent catastrophic tool crashes in live dispatches.

---

**Signed:**  
Gemini 3.6 Flash (High)  
*Gemini: the reader's eye*
