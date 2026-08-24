I'll read `SPINE.md` as the adversary seat: hunt ceremony, restatement, and unenforceable rules, then only keep cuts that lose nothing.SPINE is the whole method engine — I'll read it in full before hunting restatements, ceremony, and rules with no test.The notation block changed under me — I’ll re-read the current file so line numbers and cuts match what’s actually there.The file is not already tight. The **ideas** are tight. The **file** accreted: Part I states four structures, Part II promotes three of them to doctrines without deleting Part I, Part VI restates Gate-0, THE COUNCIL restates both. Principle 9 (“one owner per fact”) is obeyed for the invariant block versus launchers and **violated inside the file**.

I am not padding. ~11% comes out. Past that you start eating the do-not-touch list.

---

## Findings (largest first)

### 1. THE COUNCIL preamble restates Gate-0 three times in a row
**Lines 596–615.** Intro (“special move / right-size / never the default”) + “Consent gates the convening” + “When NOT to convene” are the same rule in three costumes, plus Gate-0’s two-questions test, plus Doctrine 5, plus “fan-outs cost multiples,” plus worked examples a reader can infer from “just do it.”

The **procedure** (617–631) is the owner. The preamble is ceremony around consent, which Gate-0 already owns.

**Replacement** (keep 617–631 untouched):

```markdown
### THE COUNCIL — the multi-vendor panel (the orchestrator's special move)
The council is the fan-out at full width: every reachable vendor, one per seat, each a different effective-model lineage, on one high-stakes question. Reach for it when the stakes justify the multiples: a design-space-wide fork, a decision that must be right, a claim that has to survive real scrutiny. **Gate-0 owns whether to propose it.** Offered, never auto-fired: one line (why + rough cost of N vendors), dispatch only on the boss's explicit go. A "gnarly" call is licence to *ask*, never to self-authorize. No genuine need for N independent perspectives → no council.
```

**Saves ~13 lines.** Loses the email/PO examples (inferable) and the brochure sentence “that is what makes opt-in literally true, in the engine and not just the brochure” (that sentence is the tell: the engine is talking about its brochure).

---

### 2. Diagnose/Design fork restates THE COUNCIL’s whole procedure
**Lines 80–97.** The unique law is the *fork* (bug → instrument, novel → council, re-classify when the shape changes). Lines 88–95 then re-teach BRIEF / `docs/*-<vendor>.md` / `*-SYNTHESIS.md` / attribution / “disagreements NAMED” / “council WIN” — all of which live in THE COUNCIL steps 1–4 (617–628). The packet-tap parenthetical is a worked example, not a rule.

**Replacement:**

```markdown
### 3 · THE DIAGNOSE / DESIGN FORK (what KIND of problem is this?)
Before building, classify. The two kinds of hard problem take opposite opening moves:

- **A BUG → INSTRUMENT, don't guess.** When a bug won't yield to theory, stop hypothesizing and BUILD AN INSTRUMENT to see reality — a tap, a probe, a debug mode that shows the actual data. One honest measurement beats a splash of hypotheses.
- **A NOVEL / GNARLY FEATURE → COUNCIL, then SYNTHESIS.** Proposed to the boss and fanned out only on his go (THE COUNCIL). Right-size still rules: never the default for small work.
- The fork is not either/or forever: a feature can surface a bug (fork to instrument), a bug can reveal a design gap (fork to council). Re-classify when the problem changes shape.
```

**Saves ~9 lines.** Loses the packet-tap story. Loses nothing of the procedure (THE COUNCIL keeps it).

---

### 3. Doctrine 1 is a sequence wrapped in restatement
**Lines 119–138.** The unique contribution is the **order**: council → isolate → bench → in-hand → fix loop. Gate 1 restates the fork + consent. Gate 3 restates Part IV’s two paths **and** the preflight status enums (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` / `REVIEW UNAVAILABLE`) **and** Part V’s ranks. Gate 4 restates Ladder top-rung. The origin story (“why won’t my controller work”) is ceremony. The “quietly re-introducing the exact bug” parenthetical is ceremony.

**Replacement:**

```markdown
### Doctrine 1 · THE 5-GATE SHIP PIPELINE (the house default for anything gnarly)
1. **DESIGN COUNCIL → SYNTHESIS (before a line is built).** Diagnose/Design fork; novel/gnarly only; proposed to the boss; fan-out only on his go.
2. **BUILD IN ISOLATION.** Isolated git worktree/branch, NEVER the boss's live checkout (daily-driver must not break mid-build). Disjoint write-sets across lanes.
3. **INDEPENDENT BENCH before merge.** Part IV's two paths; status from the Part VI preflight; findings ranked on Part V's ladder, each with a fix. Green gates alone never merge.
4. **BOSS IN-HAND — the TOP gate.** Ladder of Truth: green gates + passed bench + working in-hand = shipped. Any two without the third = not yet.
5. **THE FIX LOOP.** Bench findings → builder → re-review → re-gate, bounded by the loop cap (Principle 8).
```

**Saves ~10 lines.** Loses the origin story and the “looked clean” anecdote. Does **not** lose the status enum names — those stay owned by the preflight (510–514).

---

### 4. Doctrines 2, 3, and 5 are Part I wearing a second hat
**Lines 140–143, 145–148, 156–161.**

- Doctrine 2 = Part I §3 bug-side, “promoted to reflex,” plus “the boss asked for this himself.”
- Doctrine 3 = Reality Contract terms 2 and 4, copied. “Silent slop is the crime” already lives at line 109.
- Doctrine 5 = Gate-0’s right-size, **and it is the softer copy**. Gate-0 / THE COUNCIL: propose, never self-authorize. Doctrine 5: “when the boss asks **or** the task is genuinely gnarly/high-stakes.” That “or” is a loophole the owners already closed. Cutting Doctrine 5’s restatement *removes a contradiction*, it does not remove a law.

Unique sentence in Doctrine 5, keep it: *The Lineage Ledger recalibrates WHO gets a job, never “spawn more heads.”*

**Replacement:**

```markdown
### Doctrine 2 · INSTRUMENT, DON'T GUESS — Part I §3 (bug side), as reflex.

### Doctrine 3 · SELF-VERIFY + HONEST DEFERRALS — Reality Contract terms 2 and 4, as reflex.

### Doctrine 5 · RIGHT-SIZE THE DISPATCH — Gate-0 is the owner. **The Lineage Ledger recalibrates WHO gets a job, never "spawn more heads."**
```

**Saves ~10 lines.** Loses the MAC-whack-a-mole insider aside and the “celebrated” rhetoric (Doctrine 4 still owns the scalpel). Loses Doctrine 5’s looser “or gnarly” reading, which was already false against Gate-0.

---

### 5. Autonomous-hours is Part VII plus Principle 8, plus a second horror story
**Lines 687–699.** The attended section already has: reviews don’t stop the line, one exchange then the boss’s queue, emergency brake = pivot the affected lane, red-vs-pink cautionary tale (663–665). Autonomous-hours then retells it as “four agents litigating paint.”

Unique content: the caps are **absolute when unattended**; **decision batching** (taste questions resolve as a set); “if in doubt, build the safest honest version, note the assumption, keep moving.”

**Replacement:**

```markdown
**AUTONOMOUS-HOURS (unattended, the caps above are absolute).** Two rounds, then the bell; unresolved → the decision queue, work continues. A stoppage is a pivot onto unblocked work. **Decision batching:** taste/design questions resolve as a set in one pass — never re-stop the line serially. If in doubt: build the safest honest version, note the assumption, keep moving. The cardinal sin is the loop past the bell.
```

**Saves ~8 lines.** Loses the second horror story. One origin tale is enough; two is liturgy.

---

### 6. The three flips restates Principle 3, Review dispatch, and Tickets
**Lines 646–657.** Unique law: seat map is **mission state**; three causes (capability / price / infrastructure), each defined; **the builder does not commit its own work**.

The rest is duplicate: “the only fixed point is Principle 3”; “HAND IT THE CODE via stdin” (already 593–594); “proposal instead of guessing” (already 525–526 and 52–54). The tautological-guard-test aside is a teaching story, not a rule.

**Replacement:**

```markdown
### The three flips (seat assignment is mission state, not method state)
The builder seat flips for three causes: **capability** (the vendor with file/shell/git access got the hammer), **price** (one budget ran dry, the other had headroom), **infrastructure** (a sandbox broke; the seat that could still write built). The seat map is mission state; the only fixed point is Principle 3.
Practical: reviewer can't read the repo → hand it the code (Review dispatch) · the builder does not commit its own work (orchestrator/reviewer run git after the gate).
```

**Saves ~8 lines.** Loses the guard-test anecdote. Does **not** lose “builder does not commit its own work” — that sentence is the only place it is stated as law.

---

### 7. Review dispatch “who may review” restates Part IV
**Lines 575–583.** Part IV’s anti-laundering guard (267–274) is the owner of the two paths, including “a different account hosting the builder’s OWN brain does NOT count.” Review dispatch then repeats it before the unique bit: **route by FIT**.

**Replacement** (keep 585–594 — the four things — untouched):

```markdown
### Review dispatch
**Who may review:** Part IV's two legal paths (preferred: different effective-model vendor + lineage; or a boss-launched fresh seat, flagged) — never the builder's producing lineage. **Route by FIT within those paths:** sharpest bug-proving seat for code, frontier for architecture/judgment, cheap independent seat for a scan or extra vote. Concrete model = Appendix A (wiring).
```

**Saves ~6 lines.** Loses nothing. The weights/training/hosting-the-same-brain clauses stay in Part IV.

---

### 8. Ending credits are SHOW ceremony living in the engine
**Lines 533–541.** Law: a dated backend folder exists. Ceremony: “dates mid-story are jargon,” “filmed on location,” “the dispatch deck does NOT roll credits.” Header already says SHOW adds a story on top and does not restate SPINE. The inverse should hold.

**Replacement** (keep 528–532, the folder itself):

```markdown
**Style:** the DATE is for the backend folder; front-facing narration refers to runs by name. **Exception (SHOW tiers only):** ending credits may carry start/end dates. The dispatch deck does not roll credits.
```

**Saves ~6 lines.** Loses the worked “filmed on location · 2026-07-23 → 2026-07-24” example. Keeps the exception. If SHOW does not already carry the credits ritual, copy that one sentence into SHOW — do not keep a movie-credits paragraph in the method engine every tier loads.

This is decoration. Beloved decoration. Still decoration.

---

### 9. Header changelog recaps laws that have their own headings
**Lines 3–10.** v2.4 / v2.3 / v2.1 / v2.0 one-liners restate THE METER LAW, THE COUNCIL SEAT LAW, THE NOTATION, THE TRANSPORT LAW. Transitional: “the SPINE fork is healed,” “the trm copy had carried silent edits under v1.1’s tag.” Nobody runs those copies.

Standing rule inside the recap, **keep**: any content change bumps this line; inheriting copies are byte-identical.

**Replacement** (after the version line):

```markdown
Any content change bumps this line (silent edits under a stale version tag are banned). Inheriting copies are byte-identical to this one. Added-law summaries live on the law's own heading.
```

**Saves ~6 lines.** Loses a top-of-file map of v2.x. Each law’s section heading still carries `added v2.X`. Composer-vs-cursor-grok stays in the free-seat exception (780–785), which is the owner.

---

### 10. Ladder parentheticals hide a rule inside a story, then THE COUNCIL retells the story
**Lines 45–47 and 49–51**, plus the retell at **637–639**.

The shipping formula — “Green gates + passed bench + working in-hand = shipped. Any two without the third = not yet.” — currently lives *inside* the parenthetical. Lift it. Cut the stories.

**Replacement for 42–51:**

```markdown
- **A gate is only an arbiter if it can FAIL, and only after its oracle is checked.** A green gate over a wrong assertion proves nothing. A regression test is not evidence until it has been run RED against the unfixed code. State, per test, what it would catch if the fix were reverted; a test that cannot answer that is deleted and rewritten, not kept for the count.
- **The bench catches CODE bugs; the boss catches REALITY bugs — and reality outranks the review.** Green gates + passed bench + working in-hand = shipped. Any two without the third = not yet.
```

**Replacement for 633–639:**

```markdown
This is Part IV's cross-lineage law at full width. A same-vendor read is a labeled degraded self-check, never disguised as cross-vendor. Tiers dress the procedure (plain panel / crew council / set-piece); the engine is this one. The council widens coverage; it does not replace in-hand validation (Ladder, top rung).
```

**Saves ~8 lines combined** (4 + 4). Loses “no virtual controller spawns” and “an untested test is an opinion with a green checkmark” (phrases, not rules). **Keeps** “never disguised as cross-vendor” — that honesty rule is not stated as sharply in the preflight.

---

### 11. Part VI opens with a restatement of the header
**Lines 356–359.** “SPINE names none / mechanics live here once / Deck vs crew vs show.” Lines 11–14 and 229 already said this.

**Replacement:** delete the blockquote.

**Saves ~4 lines.** Loses nothing.

---

### 12. Visuals spec is a paragraph for a three-bullet rule
**Lines 543–550.** Unique: file boss screenshots into `episodes/<slug>/visuals/`, recompress, don’t ask, don’t narrate, uploads land under `.claude\uploads\`. The rest is “a bug’s face,” “not gallery prints,” “ffmpeg and Pillow both do it in one line.”

**Replacement:**

```markdown
**Visuals:** boss screenshots are reality evidence — copy into `episodes/<slug>/visuals/`, recompressed JPEG (~1280px long edge, quality ~70). No narration, no asking him to screenshot; mention at most once in backend notes. Uploads arrive under `.claude\uploads\`; convert on copy with whatever image tool the box has.
```

**Saves ~4 lines.** Loses named converters (the line already says “whatever image tool”). Keeps the numeric spec and the “don’t ask” rule.

---

### 13. Part VI dispatch gate copies Gate-0’s two questions
**Lines 361–366.** Unique addition: scale “two-to-four for genuinely independent workstreams.” Everything else is Gate-0 + Part IV.

**Replacement:**

```markdown
### The dispatch gate (before every task)
Gate-0's two questions. Scale to the job (one worker for a contained task; two-to-four for genuinely independent workstreams; more only on the boss's explicit ask), always inside Part IV's fleet test.
```

**Saves ~3 lines.** Loses the third copy of “fan-outs cost multiples” (Gate-0 keeps the 15x citation, which is the honest one).

---

### 14. Invariant-block footnote is an editor’s note wearing seven lines
**Lines 724–730.** Load-bearing: the block id is independent of SPINE’s minor version; r1→r2 tightened “another vendor’s account”; do not “fix” it to match a spine version. The “SPINE may be v1.0, v1.1, …” tour is inferable.

**Replacement:**

```markdown
*The `v2026-07-22 r2` is the block's own identity, independent of SPINE's minor version. Bumped r1→r2 when "another vendor's account" was tightened to "a different effective-model vendor and lineage." Verified byte-identical across SPINE and all three launchers; do not change it to match a spine version.*
```

**Saves ~3 lines.** Loses nothing of the trap this note exists to prevent.

---

### 15. Appendix B “Gemini 3.6 Flash is live” is a changelog entry
**Lines 900–902.** Appendix A’s Gemini command (874) already uses `Gemini 3.6 Flash (High)`. The “bad-string probe still works” is the third copy of 887–889.

**Replacement:** delete the bullet.

**Saves ~3 lines.** Loses a 2026-07-22 timestamp. The wiring line is the live proof.

---

## Smaller cuts I would also take (not padded; just smaller)

| Where | What | Replacement | Save | Lost |
|---|---|---|---|---|
| 801–805 Transport Law #2 | Restates Part IV’s two paths in parens | Keep “fresh call = blind seat; reviewers ALWAYS fresh; never briefed through a session that saw the build.” End with “Fresh is not independence — Part IV’s two legal paths still bind.” | ~2 | nothing |
| 424–426 support-seat opener | Restates the two paths before applying them | `**When the support seat is thin or missing.** Part IV's two legal paths keep budget shops honest; a rich second vendor is not required.` Then keep ENTRY/MINIMAL/NONE. | ~2 | nothing |
| 112–113 | Toggle/ACL anecdote | Delete. | ~2 | a story |
| 257 | “If a fan-out cannot be justified in one sentence, it is decoration.” | Delete. Earn-a-head (72) already says it; Part IV’s **Declared** prong is the version with an artifact. | 1 | a slogan duplicate |
| 866, 868–869, 874 | CLI one-liners | Delete the command strings. Transport Law already says wiring lives in `mcp-seats/`. Keep the routing sentences (Codex = sharpest code reviewer; Grok = surface only, never engine; Overflow Valve + bloodline counting). Keep “Mandatory trail entry.” | ~4 | stale argv that the currency rule forbids stating from memory |
| 918–920 | Header restated as a closer | Keep only: `*Provenance of the Team Rocket Method (authorship, credits, status) lives in CREW, not in this engine.*` | ~2 | nothing (provenance stays) |

**+~15 lines** if you take the small pile.

---

## Three defects that are not “too many words” — they teach the wrong rule

These are the adversary finds. Other seats will trim restatement. These **cost tokens and mis-train**.

**A. Part VI preflight still tells you to probe `--version` (499–501).** Transport Law #4 (809–811) is the later, stricter owner: a CLI `--version` only proves the **fallback** lane; a seat is online when its MCP seat answers in **this** session. As written, a launcher can follow Part VI, print a live arsenal from binaries, and skip the transport probe.

Replacement for the reachability bullet:

```markdown
- **Reachability.** Probe the transport (Transport Law #4): a seat is online when its persistent seat answers in THIS session. A seat that does not answer is UNREACHABLE; never assume reachability from the declaration.
```

**Saves ~1 line. Loses a superseded instruction that currently contradicts the law.**

**B. Appendix B line 898: “Two-vendor agreement = treat as settled.”** That is a **counter-law**. Part V and the invariant block: *convergence never ends anything; a ruling does.* The rest of the bullet is a real field note (Codex and Gemini independently killed the same two claims). Reword:

```markdown
- **Cross-vendor consensus worked as designed**: Codex and Gemini independently killed the same two pieces of draft advice (mill-first/burn-second; interpolate-from-3-probes) for the same physical reasons — the council-WIN shape. It is still not a ruling.
```

**Saves ~0. Loses a sentence that should never have been law.**

**C. Doctrine 5’s “or gnarly” loophole** — already folded into finding 4. Mentioned here so it does not survive a timid trim that pointerizes Doctrine 2/3 and leaves 5 intact.

---

## Ceremony I will name and **not** count as cuts

These have no test, no artifact, no consequence. They cost tokens. Cutting them still loses an *intended* distinction (tone), so I will not pretend they are free.

- **Line 681** — “Grade the work, not the worker. A catch is a team win; a gotcha hunt is a crime.” No artifact. Costume. One line; leave it.
- **Lines 679–680** — “A handful of taste notes.” The file’s own Bounded prong says *“as many as it takes” is not a number.* This rule fails that test. I will not invent “≤5.” Leave it or, later, give it a number in a separate ruling.
- **Lines 72–73 Earn-a-head** — “justifiable in one sentence” never has to be written down. **Declared** (247–248) is the enforceable twin. Keep the slogan at Gate-0; I already cut the duplicate at 257.
- **Line 176** — “~Once a week.” Soft trigger. The three-step procedure is real if it runs. Do not cut the procedure because the clock is fuzzy.
- **The state-glyph catalog (853–855)** and the timeline (864) look like sticker sheets. They are the **owner** of the marks (Principle 9). Leave them.

The routing-ledger paragraph (482–492) *looks* like the most unenforceable thing in the file. It is also the file **admitting** it is unenforceable. That admission is load-bearing (see do-not-touch). Do not “help” it.

---

## Total

| | Lines |
|---|---|
| Main findings 1–15 | **~101** |
| Smaller cuts | **~15** |
| **Confident total** | **~115** |
| File | 920 |
| **Share** | **~12.5%** |

I would ship the main 101 without hesitation. I would ship the smaller 15 on a second pass. I would not go past ~12.5%. The remaining length is either unique mechanism or subtlety that gets misread if shortened.

That is not “the file is already tight.” It is: **the fat is concentrated in restatement clusters and origin stories, and it is finite.**

---

## Do not touch

Passages that look like they could lose 20 lines and must not:

1. **Part IV declared-seat-lineage + anti-laundering (259–274).** This is the hole every compression will re-open. “A name is not a lineage” is long because the wrong short version is how you launder a self-review.
2. **Part V mechanisms 5 and 6, and the amendment scar (298–350).** Three lists, hashes, containment-not-equality, “untestability is never evidence,” and the explicit record of the two drafts that read as rigorous and were worse than the disease. The file says it keeps the scar *because a methodology that hides its own audit is not one.* Believe it. The meta-rule (“choose the rule that leaves a trace”) governs every future amendment.
3. **Plan-card / five levers / honesty limits / currency rule / “review coverage is NOT a lever” / routing ledger (381–492).** Long because every sentence closes a costume hole. The posture table is the owner of what a posture *does*. The “we have never measured savings” clauses are the opposite of decoration — they stop the method lying.
4. **Support = NONE paragraph (434–440).** “Diversity heuristic, not an independence proof.” Shorten this and solo shops will report `FULL CROSS-VENDOR` with a straight face.
5. **Principle 1 (191–195).** Signature is *declared*, not proven. The three-hats sentence is the whole point.
6. **Principle 10 (221–227).** Phone, physical access, “a plan that silently requires him at the machine is a trap,” the one legitimate exception. Subtle. Leave it long.
7. **Reality Contract table (104–110).** Five terms, five different artifacts. Not restated once you pointerize Doctrine 3.
8. **Fleet-legality five prongs (246–255).** Named test. Do not collapse into “be reasonable.”
9. **Reviewer ticket’s four things (585–594) and “never the builder’s reasoning.”** This is how mechanism 5 gets into the dispatcher’s hands.
10. **Preflight fail-closed / UNKNOWN LINEAGE / independence status as OUTPUT (502–514).** Owner of the three status names. Doctrine 1 should point here, not recopy.
11. **Meter Law (734–752).** Tight already. Five tests, each with a consequence.
12. **Free-seat exception, both tests, and the named Composer / cursor-grok rulings (771–785).** The named rulings change behaviour. Do not “infer them from the tests” and drop the names.
13. **Transport Law #3 (806–808).** Reply-chain stays in lineage forever. One of the few transport rules that is not a restatement.
14. **Notation grammar: 🔴 reviewing vs ⛔ reject vs crew 📝 (831–837).** Looks like emoji trivia. It exists so reviewing and rejection never share a mark, and so 🔵🔨 then 🔵🔴 on the same work is *visible* self-review. Leave it.
15. **Invariant block verbatim (713–722).** Canonical. Copy, don’t edit.
16. **Doctrine 4 scalpel (150–154), including the 80% anecdote.** Unique law (scope of the *feature*, not seat count). The anecdote is the only picture of what a cut looks like.
17. **Doctrine 6 logging form + weekly three-step (169–185).** Only owner. Verbose because the columns are the artifact.
18. **Escalation ladder (565–572).** Unique. Already short.
19. **Appendix B gotchas that change dispatch:** agy headless auto-deny (904–906), Codex attacker-vocabulary (907–911), secret-gated verification (912–916), named `(Thinking)` model strings (887–890). These are the opposite of ceremony: they are scars you pay for again if you delete them.
20. **“Review coverage is NOT a lever” scar (478–480).** Prevents a regression to “review only the risky diffs.” Same family as the amendment scar. Leave it.

If a later pass starts trimming Part V or the plan-card “because they’re long,” that pass has stopped doing this job.

---

**Adversary’s one-line diagnosis:** SPINE does not have a length problem. It has an **ownership** problem. Four structures were written, then promoted, then restated at the point of use, then restated again at the special move. Restore one owner per fact and the file loses a tenth of itself without losing a law. The credits, the dual horror stories, and “Gemini 3.6 is live” were never laws.

**Signed:** Grok 4.6 · ⚫ adversary seat · 2026-08-23