DELETE LIST — ranked

[DELETE] `mcp-seats/dispatch-guard.py` reservation-subsystem corpse (lines 35–49, plus the empty `# ---------------------------------------------------------------- reservation` section marker at line 117 and the historical docstring paragraph at lines 16–20)
EVIDENCE: The reservation subsystem was already deleted by a council vote, but its state variables still load on every summon: `HOME`, `STORE`, `LOCK`, `MAX_CONCURRENT`, `LEASE_TTL_MIN`, `LOCK_STALE_S`, `MAX_SINGLE_CLAIM_PCT`, `MAX_OUTSTANDING_PCT`, and `import time` are all unused by the surviving `preflight` and `yield` functions. The file even still contains the empty section comment `# ---------------------------------------------------------------- reservation` and a docstring story explaining why the deleted code existed.
COST IF WRONG: Zero functional breakage. Removing dead constants and imports only shrinks the loaded file and removes misleading state about a subsystem that no longer exists. The two live functions (`preflight`, `yield_report`) are untouched.

[DELETE] `mcp-seats/read-meters.py` dead `bench-burn.py` references (line 14 and line 196)
EVIDENCE: `bench-burn.py` was already deleted by an earlier council, yet the docstring still says "`bench-burn.py` reports what a burn cost" and the CLI output still tells the user to "see bench-burn.py". Both references point to a file that is no longer in the repo.
COST IF WRONG: None. The references are pure documentation drift; the meter-reading logic does not depend on them.

[DELETE] `mcp-seats/armcheck.py` dead `RESV` variable (line 15)
EVIDENCE: `RESV = os.path.join(os.path.expanduser("~"), ".anderson-method", "reservations.json")` is defined but never read anywhere in the file. It is a leftover handle for the deleted reservation subsystem.
COST IF WRONG: None. Removing an unused variable does not affect any canary test.

[DELETE] `SPINE.md` dead Amendment Law reference (Part I §2, lines 66–68)
EVIDENCE: The text says "This clause OWNS the consent gate... and the Amendment Law prefers the rule that leaves a trace." The Amendment Law was already cut by an earlier council, so this sentence cites a law that no longer exists and is itself a dated scar.
COST IF WRONG: The remaining clause is still intelligible; removing the parenthetical explanation about the deleted Amendment Law only removes confusion, not content.

[DELETE] Dated-scar attributions and error-message dates across the code files
EVIDENCE: The brief already cut "every dated scar, (boss ruling YYYY-MM-DD) attribution and this shop's wiring aside" from the loaded doctrine, but many remain in code comments and user-facing strings:
- `mcp-seats/dispatch-guard.py`: line 2 ("the 2026-08-24 council"), lines 16–20 (deleted reservation story), line 134 ("2026-08-24"), line 185 ("Codex, 2026-08-24"), line 259 ("On 2026-08-24").
- `mcp-seats/armcheck.py`: lines 56, 66, 82–84, 107–111, 140, 151.
- `mcp-seats/wmw_cursor_mcp.py`: lines 59 ("boss ruling 2026-08-23"), 110 ("2026-08-23"), 116 ("boss ruling 2026-08-23"), 249 ("Audit 2026-08-24"), 361 ("Audit 2026-08-24"), 427 ("Boss ruling 2026-08-23"), 453 ("Standing boss ruling (2026-08-23)"), 467 ("council 2026-08-24"), 493 ("reproduced 2026-08-23"), 524 ("proved on wmw-grok, 2026-08-23"), 528 ("2026-08-23"), 530 ("Audit 2026-08-24"), 734 ("Audit 2026-08-24").
- `mcp-seats/allowance.py`: line 79 ("Audit 2026-08-24").
- `mcp-seats/read-meters.py`: line 16 ("found 2026-08-23").
- `SPINE.md`: line 345 ("boss ruling 2026-07-24").
These are exactly the historical asides the owner asked to remove from the loaded engine.
COST IF WRONG: Low. The operational rules stay intact; removing the dates only strips shop history out of the live doctrine. Any line that is a warning (e.g., "State the guards READ must not live where the guarded agent may WRITE") remains meaningful without the parenthetical audit date.

[DELETE] `SPINE.md` "Practical scars" paragraph (Part VI, lines 471–474)
EVIDENCE: The paragraph begins "Practical scars: when the reviewer can't read the repo, hand it the code directly..." and recounts three historical anecdotes. The first two bullets are shop history; only the last sentence ("that instruction is load-bearing, keep it in every builder ticket") is operational, and that instruction is already stated elsewhere in the ticket section. This is content that describes the shop rather than instructing the reader.
COST IF WRONG: Minimal. The operational instruction it ends on is already encoded in the ticket requirements (Part VI "Tickets").

[DELETE] Unused `import time` in `mcp-seats/dispatch-guard.py` (line 35) and `mcp-seats/wmw_cursor_mcp.py` (line 52)
EVIDENCE: Neither `time` module is referenced anywhere after the import line in the surviving code.
COST IF WRONG: None. Removing an unused import is a pure deletion.

DEFEND — what must NOT go

- `mcp-seats/dispatch-guard.py`: `preflight()` (the Aug 21–22 empty-repo guard) and `yield_report()` (cost-per-accepted-change metric). These are the two live findings.
- `mcp-seats/allowance.py`: the entire file, including `status()`, `window_seconds()`, and `_load()`. This is the real spend bound the Cursor seat checks.
- `mcp-seats/wmw_cursor_mcp.py`: `COUNCIL_LOCK`, `_safe_cwd()`, `_safe_model()`, `_safe_id()`, `_guard()`, `_allowance()`, `meter_class()`, and `yolo_allowed()`. These are the actual safety/meter guards.
- `mcp-seats/armcheck.py`: the argument-validation checks and the behavioral canaries (the `--deep` read-only-write tests). These are the only tests that actually attack the guards.
- `mcp-seats/read-meters.py`: the `_get()` calls and the public CLI output. This is the shop's visibility into vendor pools.
- `SPINE.md`: the canonical invariant block (Part VIII), the Ladder of Truth, the fleet-legality test, the ticket contract, and the meter/transport/council-seat laws.
- `SKILL.md`: the `DEPENDS` version check and the load-receipt line. These enforce SPINE inheritance on activation.

THE ONE THING I would delete if I could only pick one

`mcp-seats/dispatch-guard.py` reservation-subsystem corpse (lines 35–49 and the associated empty section marker / historical docstring). It is the largest, most obviously dead block left after a subsystem that was already voted out, and it keeps loading paths and constants (`reservations.json`, `WMW_MAX_CONCURRENT_JOBS`, etc.) that mislead any fresh reader about what the file actually does.

CONFIDENCE

High for the dead-code items (reservation constants, `RESV`, `bench-burn.py` references, unused imports). Medium for the dated-scar sweep: the dates are clearly what the owner already ordered removed, but some are embedded in comments that also sit next to real warnings, so a purely mechanical delete must leave the warning text intact.