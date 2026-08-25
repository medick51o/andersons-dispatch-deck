I've read the brief in full. Before voting, let me verify the evidence against the actual files — the brief demands anchored votes, so I need to see the code and docs as they stand.Now let me read the prime suspects — the guard ruled dead code, the duplicate burn tools, the three seat wrappers, and the armcheck.All evidence gathered. The ladder is alive in actual council outputs, the allowance is enforced only where money can move, and the legacy/field-notes forks are confirmed. Here is my vote.

---

**DELETE LIST — ranked**

```
[DELETE] SPINE.md — Part VI, "The plan card and budget postures" (lines 542–651)
EVIDENCE: ~110 lines, roughly 2,700 of the 16,664 tokens loaded on EVERY summon — the
single largest dead-or-unproven chunk of the recurring tax. No PLAN-CARD.md exists in
this shop; the interview, the dated card, the posture map, and the routing ledger are a
ritual with no artifact. It appears in neither column of the 25-session usage scan. Its
own text confesses non-validation three times: the ledger is "an honesty aid, not proof,"
the honesty test "cannot prove causation," and "this project has never measured what a
posture saves." The living core (never state quotas/prices from memory) is already
carried by THE METER LAW clauses 5–7, which ARE invoked (102).
COST IF WRONG: SKILL.md step 3's "five levers" pointer dangles. If the boss actually
declares postures in sessions the scan didn't capture, the billing-routing discipline is
gone; the shop notices at the next subscription change or mid-mission vendor death, when
LIMP HOME has no name and the downshift has to be re-derived live.
```

```
[DELETE] mcp-seats/dispatch-guard.py — the reservation machinery: reserve() (lines
217–267), release() (270–297), the `status` subcommand (514–528), the Lock/lease-store
layer that exists only for them (44–51, 85–157), and the guard.reserve() call site in
wmw_cursor_mcp.py (~line 491)
EVIDENCE: Added today; the least proven code in the system and the day's fix-for-a-fix
epicenter — dead code that crashed on every use (NameError), then an owner-token fix that
broke the working release path, then a third patch. The audit ruled the harness false
assurance, and the reservation layer is the least honest part: it atomically records
ESTIMATES THE CALLER INVENTS (-t 20, env default "2") against a vendor meter it cannot
read, governing only the MCP lane the yield report itself proved was 3% of real account
spend. The 13-launch incident it cites ran on cloud agents — a lane its own docstring
admits it cannot govern. Atomic arithmetic on fiction is still fiction.
COST IF WRONG: Part IV's "Bounded — claimed atomically" loses its only implementation;
the shop's fan-out pacing returns to Gate-0 discipline (the boss's explicit go), which is
the control that was actually violated in the incident. The shop notices only if it runs
>2 concurrent write dispatches through the cursor wrapper — armcheck's lease checks fail
first, loudly.
```

```
[DELETE] legacy/ — cursor-native/SPINE.md (v1.2), cursor-native/SKILL.md,
cursor-native/CURSOR-NATIVE.md, SKILL-standalone.md
EVIDENCE: A full, self-declared SUPERSEDED copy of the law ("do not run the method from
this file") sitting in the repo. Principle 9 bans duplicated full copies precisely because
they fork — and this shop has the scar (the Deck's legend forked to v4.0 for two days).
"Kept for history" is what git is; the history is in the object store, not the working
tree. Zero summon tax, but pure dilution plus a live fork hazard for any fresh seat that
globs the repo.
COST IF WRONG: Nothing breaks. The v1.2 text remains recoverable from git history
forever. The shop would notice only if someone needed the Cursor-era rendering — a
`git log` away.
```

```
[DELETE] FIELD-NOTES.md (repo root)
EVIDENCE: SPINE line 991 rules that field notes live in SPINE-WIRING.md — and
SPINE-WIRING.md's APPENDIX B is the living copy. The two have ALREADY forked: each holds
gotchas the other lacks (root-only: Grok CLI PATH, MSIX PowerShell err 5; wiring-only:
Codex safety-vocabulary, secret-gated verification). Two field-note files is the exact
multiple-copies failure Principle 9 exists to prevent. Nothing alive references the root
file — SKILL.md points to BENCH-LEDGER and MEASURING-POOLS, SPINE points to WIRING.
COST IF WRONG: Two or three unique crumbs are lost; a fresh install re-discovers the
Grok-PATH and MSIX gotchas in one afternoon of failed dispatches. The shop notices as a
one-time stumble on next install, not as a recurring cost.
```

```
[DELETE] SPINE.md — Part II, Doctrine 6 · THE LINEAGE ENGINE (lines 319–341)
EVIDENCE: Wallpaper by the scan (6 = load-only across 25 sessions), and the weaker kind
of dead: not a mechanism firing under another name, but a ritual with no performed
instance on record. The weekly lineage review has never been called by name; the ledger
it writes doesn't even live in this repo (wiring points it at an external brain path).
~23 lines of every summon describing a recalibration loop that has never looped. On the
"is never-invoked sufficient grounds" question: yes, WHEN the law is a named ritual the
boss must speak to fire — a ritual nobody speaks is a ritual nobody performs. (Contrast
Part III/V, defended below, whose mechanisms fire without their names.)
COST IF WRONG: Routing stays habit-fed instead of evidence-fed — which is the current
state, so nothing changes on delete. The boss loses the named handle "run the lineage
review" and the ledger rows lose their writer; if he reaches for standings in session 26,
the absence is visible in one breath and the ledger file still exists with its rows.
```

```
[DELETE] mcp-seats/bench-burn.py
EVIDENCE: One of the two burn tools, and the dishonest one. It reads only the seat
ledger (bench-spend.jsonl) — the instrument dispatch-guard's own yield report proved was
blind to 97% of real account spend on 2026-08-24 — and prints it under the heading
"CURSOR BENCH BURN." A meter that sees 3% of the bill manufactures the exact false
comfort the METER LAW exists to kill. Its function is subsumed by dispatch-guard's
`yield`, which reads the same ledger PLUS the vendor's per-event export PLUS git output,
and says the 3% caveat out loud.
COST IF WRONG: Two dangling pointers (read-meters.py docstring, SKILL.md line 126) and
the loss of the per-model billable-by-lineage breakdown — a cut of a 3%-complete dataset.
The shop notices as one fewer way to misread a corner of the bill as the bill.
```

**DEFEND — what must NOT go, and why**

- **SPINE.md Part III (THE TEN PRINCIPLES) and Part V (THE ADJUDICATION PROTOCOL).** The phrase-count is the wrong instrument for these two, and deleting on it would be the council's one irreversible error. The plural NAMES are never spoken, but the mechanisms fire constantly by number and by rank: Part IV's "Still Principle 3," Part VI's "Principle 3 fires either way," Part VII's "Principle 8's units," mission reports' Principle 10 — and the BLOCKER / MATERIAL / MINOR / NOT PROVEN ladder appears in actual council verdicts (docs/council-lighten/SIGNED-*.md, the OUT-*.json files), not just in loaded text. "THE FIX LOOP" at 4 is the same lesson from the other side: the loop RUNS every review cycle without being NAMED. Never-invoked is sufficient grounds for a named ritual (Doctrine 6); it is not sufficient for law whose parts are cited by the alive parts. Deleting Part III orphans a dozen cross-references inside the sections that ARE invoked.
- **SPINE.md Part IV's anti-laundering guard and the two legal review paths.** The only thing standing between cross-vendor review and self-approval-by-proxy; cited by SKILL.md, the preflight, and the review-dispatch section. (Noted for the record, not as a vote: the header says "all five hold" above SEVEN bullets — the count drifted when Destined and Governed were accreted in. The content binds regardless.)
- **SPINE.md Part VIII.** The canonical invariant block is the one piece of law copied verbatim into every entry file — the actual enforcement surface of Principle 9. Delete its owner and the block floats ownerless; the next edit forks it.
- **mcp-seats/allowance.py.** 153 lines implementing THE COUNCIL SEAT LAW (alive, 86 invocations), and verified wired exactly where spending exists: the cursor wrapper checks it (lines 191–226, 433–447) while the flat-rate grok/gemini wrappers correctly carry no check. "Enforced, not merely written" is true at the one seat that can bill.
- **mcp-seats/read-meters.py and calibrate-pool.py.** The only instruments for THE METER LAW (alive, 102). Read-only meters are the shop's sole vendor truth; clause 3 ("one reading is a rumour") requires repeat burns, and calibrate-pool is the only re-runnable burn. MEASURING-POOLS.md documents the method; the tool is its reproducibility.
- **mcp-seats/armcheck.py.** One day old, and I am being unsentimental — but it is the only suite that has ever ATTACKED the guards instead of validating arguments, and the audit it pins is the audit that burned the day. The --deep behavioral canaries (ask a read-only seat to write, check the disk) are the honest core the previous suite lacked. Deleting the regression net the week of the incident is how the incident repeats. (Its two source-grep checks — ledger-path and --approve-mcps confinement — are its weakest members, but they are 8 lines, free, and pinned to today's scars.)
- **dispatch-guard.py's preflight() and yield_report().** If the council deletes the file wholesale rather than at my function-level vote, these go with it — name the collateral: preflight is honest accident-prevention against the OBSERVED empty-repo failure (11 of 13 agents, zero lines), and yield is the only implementation of METER LAW clause 6, already proven by the 3%-visibility finding.
- **The three wmw_* wrappers.** Near-identical structure is the price of three independent vendor lanes, not duplication; deleting one amputates a review path and a council vote. Merging them is a rewrite — out of scope for this council.
- **The docs/ archive.** None of it loads on a summon, so deleting it buys zero relief against the stated thesis — and it is the only empirical record behind the shop's routing beliefs and the lineage ledger's evidence base. The filing cabinet is not the bloat.

**THE ONE THING I would delete if I could only pick one**

The dispatch-guard reservation machinery (`reserve` / `release` / `status` and their lock-and-lease layer). It is the day's fix-for-a-fix epicenter in its third patch, it crashed on every use within hours of birth, and its central act — atomically reserving a caller-invented percentage of a meter it cannot read, on the one lane already proven to be 3% of the bill — is ceremony that wears the costume of a budget control. The honest accident-prevention in that file (preflight) and the honest measurement (yield) survive the cut; the theater does not.

**CONFIDENCE**

High: legacy/, FIELD-NOTES.md, the reservation machinery, bench-burn.py — all four rest on positive evidence (self-declared supersession, an observed fork, a crash record plus a false-assurance ruling, a measured 97% blind spot), not absence. Medium: the plan-card section and Doctrine 6 — absence-of-artifact and absence-of-invocation votes, argued both ways above; I weighted the phrase-count as necessary-not-sufficient, which is why Part III and Part V sit in DEFEND while the two ritual-laws sit in DELETE. If the boss produces a PLAN-CARD.md or a filled lineage ledger from outside this repo, those two votes withdraw themselves.