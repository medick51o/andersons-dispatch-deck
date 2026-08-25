I'll read the brief in full first, then follow it exactly.The brief is long — I’ll keep reading the rest of the packet so the merge scan is complete.The wrappers and tools are still coming — I’ll finish the packet so the merge proposals rest on the actual code.Still missing the last of the small tools — I’ll read the remainder of the packet.MERGE LIST — ranked

```
[MERGE] The three seat wrappers' JSON-RPC loop, arg helpers, exe lookup, JSON harvest, and cwd guard
        → one mcp_seats/transport.py; each wmw_*_mcp.py keeps only its vendor run_* + TOOLS
WHY:    Same server wearing three filenames. handle() + main() are the same loop
        (initialize / ping / tools/list / tools/call / parse-error / request boundary)
        in wmw_grok_mcp.py:312-370, wmw_gemini_mcp.py:282-340, wmw_cursor_mcp.py:698-762.
        _req_str / _opt_str / _opt_bool are byte-identical. _utf8_stdio, _UUID_RE, _safe_id
        are the same. find_grok / find_agy / find_cursor_agent are one "known path first,
        PATH last" helper with different tuples. _extract_json is the same decoder with
        one strategy flag (first object vs last type==result). _safe_cwd is the same
        decision with three implementations — and that is the live bug: Gemini's reply
        cwd gate lagged Grok's 2026-08-23 fix until a 2026-08-24 audit
        (wmw_gemini_mcp.py:264-270 quotes it). Duplication is how a fix dies in one seat.
SHAPE:  mcp_seats/transport.py (~170 lines):
          serve(name, version, tools, call_fn)   # the JSON-RPC loop
          req_str / opt_str / opt_bool / safe_id / safe_argv
          extract_json(raw, mode="first"|"last_result")
          find_exe(*candidates)
          safe_cwd(cwd, write, allow_under=None)
            union policy, not the weakest:
              exact home + drive root banned (Grok:175-198 — "legitimate parents of projects")
              system-tree CONTAINMENT via realpath+commonpath (Grok:199-205, Cursor:354-358)
              case-insensitive secret segments (Grok:206-211; Gemini's basename/substring
                at :180-182 is the weak one)
              APPDATA / LOCALAPPDATA containment (Cursor:359-368 — only Cursor has it today)
              allow_under=PLAYPEN for Cursor only
          Each wrapper: find-candidates + run_* + TOOLS + call_fn, ends in transport.serve(...)
        Vendor run_* STAYS in the vendor file (see KEEP APART).
SAVES:  ~400 lines of code (370+340+762 = 1472 → ~170 + ~190 Grok + ~175 Gemini + ~530 Cursor
        ≈ 1065). Per-summon tokens: 0 — these servers are not on the conductor's load.
        The earlier "50–150 lines per vendor layer" estimate is RIGHT for Grok and Gemini
        (~175–190), WRONG for Cursor (~530) unless you also lie about meters, YOLO,
        council-lock, playpen, allowance, and guard wiring. Those are real Cursor law,
        not transport.
RISK:   Unifying cwd is a behavior change on Gemini: it currently bans the entire home
        *subtree* (wmw_gemini_mcp.py:168-179; armcheck.py:75-76 asserts ~/Documents is
        refused). Grok/Cursor only ban exact home. Pick Grok's rule (projects live under
        the profile) or Gemini's armcheck goes red. extract_json mode must stay a
        parameter — Cursor streams status lines; first-object would steal a status
        blob, last-result would miss Grok's banner-tolerant parse. Three *processes*
        stay three (see KEEP APART).
```

```
[MERGE] Gate-0's consent/right-size rule × THE COUNCIL's "ask first / when NOT" ×
        Council Seat Law clause 6 × the dispatch-gate seat-count restatement
WHY:    One decision wearing four names: "a 3+-seat panel is a SPECIAL move and
        dispatches only on the boss's explicit go." Gate-0 already claims ownership
        (SPINE Part I §2: "This clause OWNS the consent gate. It is deliberately
        restated at the dispatch gate and THE COUNCIL"). THE COUNCIL:409-418 is that
        restatement plus "When NOT to convene." Council Seat Law #6 (SPINE:570-571)
        is the same sentence again. Diagnose-fork (Part I §3:84-88) points at the
        procedure, which is fine; the consent copy is not.
SHAPE:  Gate-0 keeps the rule (default lean; 1+1 canon; panel = ask, never self-auth;
        two questions decide who BUILDS).
        Part VI dispatch gate keeps only the *distinction* it uniquely adds: parallel
        BUILDERS on disjoint write-sets (fleet test, told not asked) vs N-way PANEL
        (Gate-0, asked). Two bullets, not a reprint of right-size.
        THE COUNCIL keeps the procedure (brief → lenses → gather → synthesize → cap
        → boss) and one line: "Convening is Gate-0. This section is the procedure."
        Delete :409-418. Council Seat Law #6 becomes "Gate-0 still binds."
SAVES:  ~20–25 SPINE lines ≈ ~300–400 tokens per summon (SPINE is the whole method load).
RISK:   A conductor who only opens THE COUNCIL and never Gate-0 could miss "ask first"
        unless the one-line pointer is the first line of that section, not a footnote.
```

```
[MERGE] SKILL.md ON INVOCATION step 2 + NARRATE IN COLOR's vendor list
        → pointers at SPINE, which SKILL already says it does not restate
WHY:    SKILL:33-39: "The Deck adds NOTHING to the method. This file does not restate it."
        Then SKILL:68-79 restates the entire Part VI preflight (transport vs binary,
        effective-model, UNKNOWN LINEAGE, independence status, degrade-gracefully)
        and SKILL:41-49 reprints THE NOTATION's vendor→color map. The doubled
        "adds nothing / adds nothing" paragraph (:33-39) is the same claim twice.
SHAPE:  Step 2 becomes: load SPINE-WIRING, run SPINE Part VI preflight, print the
        arsenal line and the independence status. Color section keeps the gold-baton
        *example* (that's Deck rendering) and drops the 🟠🔵⚫🟢 roster. Keep FUEL MODE
        (it is the only real Deck delta besides plain names). Invariant block stays
        verbatim (Principle 9).
SAVES:  ~15–20 SKILL lines ≈ ~250–350 tokens per summon.
RISK:   A conductor who skims SKILL and never opens SPINE could probe `cli --version`
        and call a seat "online." Mitigate: the step-2 pointer names "TRANSPORT first,
        not the binary" in the pointer itself so the failure mode stays visible.
```

```
[MERGE] calibrate-pool.py + dispatch-guard.yield + read-meters.py → one meters CLI;
        dispatch-guard.py becomes preflight-only
WHY:    Three programs answer "what did we spend / what's left / what does a token
        cost." calibrate-pool.meter() (calibrate-pool.py:27-40) reimplements
        read-meters.read_cursor() (read-meters.py:118-149) against the same
        GetCurrentPeriodUsage endpoint. calibrate-pool.find_cli() duplicates
        find_cursor_agent. yield_report (dispatch-guard.py:163-265) already reads
        the same spend ledger the Cursor wrapper writes and the same vendor CSV
        family; it lives in dispatch-guard only because "two findings drove this"
        (guard docstring:7-14) — one finding was a write-dispatch gate, the other
        was a shop metric. The reservation husk (dispatch-guard.py:106-108) is
        empty after today's delete. Allowance is NOT in this merge (KEEP APART).
SHAPE:  meters.py (or keep the name read-meters.py) subcommands:
          (default)   live needle — current read-meters
          yield <repo> [--days N] [--events csv] — moved from dispatch-guard
          calibrate [--probe|--calls N] — current calibrate-pool, calling read_cursor()
        dispatch-guard.py: preflight() + CLI `preflight` only. Wrapper import
        unchanged: `guard.preflight(workdir, model=chosen)` (wmw_cursor_mcp.py:478-480).
SAVES:  ~90–110 lines (duplicate Cursor HTTP client + find_cli + three argparsers
        + reservation husk + yield's second home). Not a 4-file collapse; the
        functions mostly move. The size win is the duplicates and the husk.
RISK:   calibrate SPENDS; read does not. Default subcommand must stay the free
        read, or a habit of `python read-meters.py` becomes a burn. yield's git
        clock is local, vendor events are UTC (already footnoted at guard:263-264) —
        that warning has to travel with the function.
```

```
[MERGE] THE METER LAW + THE COUNCIL SEAT LAW → one SPEND LAW
WHY:    Both gate money, not method. Meter Law: a seat that costs must be readable;
        unknown fails closed; subsidy is not a foundation; meter output.
        Council Seat Law: a seat that can spend needs a recorded allowance; within
        it, no re-ask; past it, refuse; unknown fails closed (clause 5 already
        points at Meter Law). Clause 6 is the Gate-0 restatement from merge 2.
        THE NOTATION:641-648 then restates "meter marks mandatory / unknown fails
        closed" a third time. Three headers, one axis (may this call spend).
SHAPE:  ## THE SPEND LAW
          1. Readable before and after. Unknown fails closed.
          2. Allowance before a metered sit; bound + expiry; within = no re-ask;
             past = refuse and re-ask. Free seats need no allowance.
          3. An allowance never substitutes for a meter.
          4. Subsidy is never a foundation (extra vote, never sole path).
          5. Meter the output (cost per accepted change), not only the input.
          6. Marks on every spending line: ♾️ ♾️💸 💸 🚨💳 ⚠️ — computed from the
             model id, never guessed. (THE NOTATION keeps the glyph table, loses
             the sermon.)
        Wiring footnote stays once: allowance.py is the record; wrappers refuse
        before spend. Gate-0 is not restated here.
SAVES:  ~12–18 SPINE lines ≈ ~200–280 tokens per summon.
RISK:   "Council Seat Law" is the name the Cursor wrapper comments cite
        (wmw_cursor_mcp.py:430). Rename in code comments the same day or the
        wrapper points at a ghost. Spend-permission and pool-measurement stay
        distinct *operations* (see KEEP APART on allowance.py vs meters).
```

```
[MERGE] Part IV anti-laundering "who may review" × Part VI Review dispatch's reprint
        × Transport Law #2–#4's reprint of the same two legal paths / transport probe
WHY:    Part IV:196-203 owns the two legal reviewer paths (different effective-model
        vendor+lineage, or boss-launched) and "a name is not a lineage."
        Part VI Review dispatch:377-386 reprints them. Transport Law #2 (fresh call
        is blind, two paths still bind) and #3 (reply-chain stays in lineage) are
        Part IV applied to MCP. Transport Law #4 (probe the transport, not the
        binary) is already a bullet of Part VI preflight:321-323. Principle 3 is
        the fixed point; the rest are copies.
SHAPE:  Part IV keeps the law. Review dispatch opens "Who: Part IV's two paths.
        Route by FIT within them:" and keeps the four-thing reviewer ticket
        (that's unique). Transport Law keeps only what is MCP-specific:
          1. Opt-in per vendor (already unique)
          2. A *-reply chain is the same owning-seat lineage (one sentence, not a
             restatement of the two paths)
          3. CLI one-shot remains the fallback
        Preflight keeps the transport-vs-binary probe (it is the procedure).
        Transport Law #4 dies as a duplicate.
SAVES:  ~12–16 SPINE lines ≈ ~180–250 tokens per summon.
RISK:   Transport Law is the one place that names `*-reply` as a lineage trap.
        If that sentence moves only to Part IV, a wrapper author never reading
        Part IV will chain a reviewer. Keep the *-reply sentence in Transport Law
        even after the two-paths reprint goes.
```

```
[MERGE] Part IV fleet-legality list with Gate-0's "all five hold" list — they disagree
WHY:    Same test, two counts. Gate-0:73-75: "all five hold … Declared · Bounded ·
        Accounted · still-Principle-3 · Authority-inheritance" (no Destined, no
        Governed). Part IV:164-185 says "all five hold" then lists seven bullets
        (adds Destined and Governed where it RUNS). Destined is the clause
        dispatch-guard.preflight implements ("an agent with no destination still
        spends at full rate"). Governed-where-it-runs is why the reservation
        subsystem was deleted today. Both are load-bearing; Gate-0 dropped them.
SHAPE:  Part IV owns one numbered list. Count it honestly (seven, or six if
        Still-P3 and Authority stay as the last two of the five-plus-two).
        Gate-0 becomes "the fleet test in Part IV — every clause, not a subset."
        Do not reprint the bullets.
SAVES:  ~4–6 lines, plus it stops the conductor from running a 5-clause test that
        silently omits the two clauses this shop already burned on.
RISK:   Low if the pointer is mandatory. Do not "merge" Bounded (seat-count) with
        the spend allowance — see KEEP APART.
```

KEEP APART

- **The three `run_*` bodies.** Same job (put prompt in front of a CLI, bring text back), three incompatible machines. Grok: `--prompt-file` + DENY_RULES + `--disallowed-tools Agent` + `--permission-mode default` (sandbox fails open on Windows, MCPTool was the live write-through). Gemini: prompt on argv with a 25k cap, `--mode plan` vs `--dangerously-skip-permissions`, `status==SUCCESS`, brain UNREPORTED on purpose. Cursor: playpen spill + ASCII pointer because the .cmd shim executes metacharacters (reproduced), `--mode ask` vs `--yolo`, spend_credits, YOLO allowlist, council lock, allowance, dispatch-guard. Merging these is how Gemini shipped a "read-only" that was "omit the skip flag and hope config is kind." Shared transport, vendor `run_*`.

- **Three MCP processes into one server.** Sharing a *library* is the merge. Sharing a *process* means a hung Gemini blocks Grok. Registration is per-server; isolation is the point.

- **allowance.py vs meters.** Council Seat Law (and Spend Law, if merged) says an allowance never substitutes for a meter. One is the operator's grant on disk (`~/.anderson-method/allowances.json`). One is the vendor's needle. Cursor already loads them separately (`_allowance` vs `_recent_billable` vs `read-meters.py`). One file would make "the grant is the tank" thinkable, which is the bug the law exists to prevent.

- **preflight vs meters.** preflight is a fail-closed WRITE gate on the hot path (`wmw_cursor_mcp.py:467-487`). Meters are advisory and may be empty. A combined CLI teaches "preflight is optional, like a meter read." Keep `dispatch-guard.preflight` importable and boring.

- **Escalation (Part VI:368-375) vs Principle 8's review-round cap.** One is "this builder failed the ticket" (fix ticket → retry → one seat up → boss). The other is "builder and reviewer disagree." Same word "round," two clocks. Merging them lets a ticket-fix consume the dispute cap.

- **Worker statuses vs finding ranks.** SPINE already: "These grade task progress; review findings keep the adjudication ladder. One axis per line, never mixed" (Part VI:365-366). Merge and a BLOCKED worker looks like a BLOCKER finding.

- **Reality Contract (Part I §4) vs the three lists (Part V.5).** Both are "declare the files/outcomes." One is what *done* means before dispatch (observable / instrument / invariants / rollback / in-hand kit). The other is containment after the fact (write set ⊇ delta ⊆ manifest). Folding them produces a ticket that cannot tell a missing rollback from a fence breach.

- **Principle 9's invariant block copies.** SKILL:83-93 is required to be byte-identical with SPINE Part VIII. That duplication is the law. Do not "merge" it into a pointer; a pointer is exactly what Principle 9 forbids.

- **SKILL.md vs SPINE.md.** Engine vs render. Fuel mode and gold-baton narration are the Deck's only delta. Absorbing SKILL into SPINE either puts FUEL in the engine or kills the thin-loader claim.

- **Cursor BLOODLINE_MARK / METER_MARK (code) vs THE NOTATION (doctrine).** Same glyphs, two consumers. The wrapper cannot parse SPINE to print a footer. Keep the table in code; Notation stays the conductor-facing legend.

- **armcheck.py vs the wrappers.** A test that lives in production is how the guard-break canary used to rewrite live `dispatch-guard.py` (armcheck.py:147-151). Stay a canary.

- **Bounded (fleet seat-count) vs allowance (spend bound).** "N seats" is not "N paid calls." Cursor can be one seat and still drain the credit pool. The deleted reservation subsystem already proved a seat-count lock does not see vendor-hosted spend.

THE ONE MERGE worth doing if only one happens

Shared `transport.py` for the three seat wrappers (merge 1), with `safe_cwd` taken from Grok's containment + Cursor's APPDATA extra + Cursor's playpen allowlist.

It is the only merge that both shrinks the tree (~400 lines) and closes the class of bug this round is for: a guard fixed on Grok, missing on Gemini, still missing in pieces on the cwd policy. The 50–150 estimate is the right target for Grok and Gemini; do not flatten Cursor's meter/YOLO/allowance/guard into that number.

It does **not** cut the ~13,797 per-summon load. If the single move must hit the conductor's context, do merge 2 (Gate-0 owns council consent; delete the reprints) instead — smaller code win, real token win.

CONFIDENCE

High on the wrappers (function-by-function overlap; the Gemini lag is in the file comments). High on SKILL restating a preflight it claims not to restate. Medium-high on the Gate-0 / Council / Seat-Law collapse (the ownership sentence is already in Gate-0). Medium on Spend Law and on meters-CLI (right shape; size save is the duplicates, not the moved yield). Medium on "who may review" collapse (Transport Law still needs the `*-reply` sentence). The 50–150 vendor-layer estimate: confirmed for two seats, rejected for Cursor.

⚫