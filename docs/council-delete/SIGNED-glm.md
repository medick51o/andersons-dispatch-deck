I've read the brief in full. Before voting, I need to gather evidence on the prime suspects — the code the brief names as dead, broken, or duplicative. Let me read the actual filesI have enough evidence. Here is my seat's vote.

---

```
DELETE LIST — ranked

[DELETE] armcheck.py lines 104-111 — the two static-source-grep canaries
  ("cursor: spend ledger is NOT inside the playpen" and
   "cursor: --approve-mcps confined to the write-capable path")
EVIDENCE: These do not execute the wrapper. They string-split the SOURCE TEXT of
  wmw_cursor_mcp.py and assert about line layout ("if always_approve:" must sit one
  line above 'cmd += ["--approve-mcps"]'). A canary that greps source passes when the
  string is present regardless of behavior, and fails when a refactor moves the
  string without changing behavior. The file's own audit comment at lines 122-126
  already concedes this suite "was ENTIRELY argument-validation and never once
  attempted the thing the rig exists to prevent." The behavioural canaries (2b)
  were added to fix that; these two greps are the leftover ceremony the fix did not
  remove. This is precisely "canaries that test the wrong thing."
COST IF WRONG: A refactor that moves --approve-mcps off the approved path would no
  longer trip a check here. But the behavioural canary at lines 162-181 (broken
  guard REFUSES a write dispatch, run against a copy in the playpen) already
  catches the real failure mode behaviorally. The shop would notice nothing,
  because the behavioral canary covers it.

[DELETE] SPINE.md lines 334-336 — THE AMENDMENT LAW
EVIDENCE: Usage count 6 = loaded only, never referenced in reasoning across 25
  sessions. It is a meta-heuristic ("choose the rule that leaves a trace"), not a
  load-bearing law: no other clause in SPINE invokes it, and nothing in the code
  or canaries depends on it. Unlike THE FLEET-LEGALITY TEST (referenced by THE
  COUNCIL SEAT LAW clause 6 and the dispatch gate) or THE TEN PRINCIPLES
  (Principle 3 is "the fixed point," Principle 8 defines ROUND/EXCHANGE units Part
  VII uses), THE AMENDMENT LAW is substrate for nothing active. By the brief's
  own thesis — "a rule nobody reads dilutes every rule around it" — this is the
  cleanest named-law deletion in the engine.
COST IF WRONG: A future author loses the tiebreaker heuristic for "two ways to
  write a rule, pick the one that leaves a trace." The shop would notice only if
  someone re-introduces a habit-only invariant that dies at context compaction —
  the exact scar SPINE-PROVENANCE.md records. The scar survives the deletion; the
  prose does not, and the prose was never invoked.

[DELETE] bench-burn.py (mcp-seats/bench-burn.py, 94 lines, entire file)
EVIDENCE: bench-burn.py does not burn — it READS bench-spend.jsonl and prints
  token counts by model. dispatch-guard.py's `yield` subcommand (lines 300-459)
  reads the SAME ledger (WMW_CURSOR_LEDGER, same default path) and reports the
  same tokens PLUS cost-per-accepted-line PLUS the vendor-export cross-check that
  the brief's own evidence (the "yield reported zero" bug) was about. bench-burn
  is the weaker subset of `yield`: no repo arg, no accepted-output denominator, no
  vendor ground-truth lane. The brief names "two burn tools" as duplicate
  machinery; this is the one whose function is fully subsumed.
COST IF WRONG: A user loses the one-line `python bench-burn.py` for a quick
  month-to-date token total without naming a repo. The shop would notice when
  someone reaches for the quick number — and `dispatch-guard.py yield --days 30`
  on any repo gives the same tokens-plus-more. Recoverable in one command.
```

---

```
DEFEND — what must NOT go

- THE FLEET-LEGALITY TEST (SPINE.md Part IV, lines 228-276). Wallpaper by count
  (6), but substrate: THE COUNCIL SEAT LAW clause 6 ("the fleet test bind first")
  and the dispatch gate's parallel-builder case both invoke it by name. Deleting
  orphans two active laws. The count measures invocation in reasoning, not
  load-bearing reference.

- THE TEN PRINCIPLES (Part III) and THE SIX DOCTRINES (Part II). Same wallpaper
  count, same substrate defense: Principle 3 is "the fixed point — it survives
  every seat flip"; Principle 8 defines the ROUND/EXCHANGE units Part VII's
  review-culture caps depend on; Doctrine 1 is the 5-gate ship pipeline; Doctrine
  5 is the actively-invoked RIGHT-SIZE DISPATCH (21). Deleting the wallpaper
  container deletes the active clauses it houses.

- THE ADJUDICATION PROTOCOL (Part V). Wallpaper by count, but it OWNS the
  BLOCKER/MATERIAL/MINOR/NOT PROVEN ladder that Part VII and the bench both rank
  findings on. Substrate, not standalone.

- dispatch-guard.py. The brief's "dead code that crashed on every use" was the
  PRE-fix state; the fixes are in the committed file (release's owner-check
  removed line 270-278; yield's ledger path and shape fixed lines 377-400). The
  guard is honest about its own limits (docstring lines 24-28: it governs only
  the through-it lane; the 96% it cannot see is the vendor's control plane). The
  reserve/release machinery is the atomic reservation that prevents the
  time-of-check/time-of-use race — that is real accident-prevention, not
  ceremony. The cwd-refusal canaries in armcheck.py (System32, APPDATA, HOME
  profile) are likewise honest accident-prevention: they stop an accidental
  write-capable launch in a system directory, which is a real fence even though
  cwd is not an OS sandbox.

- The behavioural canaries in armcheck.py section 2b (lines 132-181). These are
  the ones that actually attack the seats and check the disk — the thing the rig
  exists to prevent. The broken-guard-fails-closed test runs against a playpen
  copy, so it can no longer corrupt production source. These are the opposite of
  ceremony.

- read-meters.py. Reads the actual vendor billing endpoints; honest, read-only,
  and the ground truth the whole meter law rests on. Not redundant with
  anything.

- allowance.py. Small, referenced by THE COUNCIL SEAT LAW, and the real record
  the transport checks before spending. Earns its 153 lines.
```

---

```
THE ONE THING I would delete if I could only pick one
armcheck.py lines 104-111 — the two static-source-grep canaries. They are the
purest instance of the brief's named failure mode: canaries that test the wrong
thing. They assert about the text of the wrapper, not the behavior of the guard,
and the behavioral canary at lines 162-181 already covers the real failure mode
they gesture at. Removing them deletes zero real coverage and removes a test
that would pass on a broken-but-pretty source and fail on a working-but-refactored
one.
```

---

```
CONFIDENCE
Medium-high on the two canary deletions and bench-burn.py — those rest on code I
read in full and a clear subsumption/behavior-vs-text argument. Medium on THE
AMENDMENT LAW: the usage count is strong evidence and no active clause references
it, but it is a named law and the decision rule needs 3 seats for a clean delete,
so this seat's vote is a contribution to that count, not a verdict. I did not
vote against dispatch-guard.py despite the brief's "dead code" framing because
the fixes are in the committed file and the guard is honest about the 3% it can
govern; deleting working, honest, fixed code on the strength of a prior day's
bug would be sentiment about the scar, not evidence about the code.
```