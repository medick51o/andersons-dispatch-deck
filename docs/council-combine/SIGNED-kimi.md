Read the packet in full: the brief, SPINE v2.8, SKILL.md, and all eight code files (three seat wrappers, dispatch-guard, allowance, read-meters, calibrate-pool, armcheck). Findings below, in the brief's format. Nothing written, merges only.

---

## MERGE LIST — ranked

```
[MERGE] The three seat wrappers' shared transport → one wmw_common.py
WHY:    wmw_grok_mcp.py, wmw_gemini_mcp.py and wmw_cursor_mcp.py carry byte-near-identical
        copies of the same machinery: _utf8_stdio (7 lines ×3), _UUID_RE/_safe_id (×3),
        _safe_argv (×2), _req_str/_opt_str/_opt_bool (23 lines ×3), handle() (31 lines ×3,
        differing only in the serverInfo literal), main() (27 lines ×3), the _tool_call
        skeleton, and the find-exe pattern (three finders, same shape, different candidate
        lists). Worst is _safe_cwd: the SAME guard in three divergent bodies — grok
        (10 secrets, case-insensitive segments, home banned at root only), gemini (6
        secrets, case-SENSITIVE substring, home banned subtree-wide, no isdir check),
        cursor (10 secrets + APPDATA/LOCALAPPDATA containment + playpen exception).
        The packet itself documents the cost: grok's reply-escalation cwd guard (fixed
        2026-08-23, comment at grok _tool_call) "was never propagated here (Audit
        2026-08-24, Gemini seat, CONFIRMED)" at gemini _tool_call; cursor's APPDATA ban
        is annotated "(Audit 2026-08-24, Kimi, CONFIRMED gap)" and exists nowhere else.
        What genuinely differs per vendor: prompt transport (grok --prompt-file; gemini
        argv with the 25K cap; cursor playpen-file + ASCII pointer, injection-driven),
        read-only enforcement (deny-rules vs --mode plan vs --mode ask --trust), resume
        flag, response JSON shape (cursor streams, last-result-wins), and cursor's entire
        meter/allowance/council-lock/playpen/bloodline stack. That differing part is real
        and stays per vendor.
SHAPE:  mcp-seats/wmw_common.py holds: _utf8_stdio, _safe_id, _safe_argv, _req_str/_opt_str/
        _opt_bool, extract_json_first() and extract_json_last_result() (BOTH — see KEEP
        APART), find_exe(candidates, path_name), one _safe_cwd(cwd, always_approve,
        extra_allow=()) taking the STRICTEST union (grok/cursor's 10-secret case-insensitive
        segment match + gemini's home-subtree ban + cursor's APPDATA containment; the
        playpen passed as extra_allow by cursor only), serve(server_name, version, tools,
        tool_call) replacing handle()+main(), and one cached load_sibling(name). Each
        wrapper keeps: its exe candidates, argv builder, response parser, footer, TOOLS
        table, and vendor guards. SPEND_LEDGER's path (defined twice today: cursor wrapper
        lines 84-86 and dispatch-guard lines 186-188 — the guard's own comment admits
        reading the old path "made this report a confident zero") is defined once in
        wmw_common and imported by both.
SAVES:  ~350 lines of ~1,470 (24%). On the earlier seat's "50–150 lines per vendor layer"
        estimate: TRUE for grok (~370→~150) and gemini (~340→~140) only if the TOOLS
        tables are discounted as data; with TOOLS they land ~190/~180. FALSE for cursor —
        its meter/allowance/council-lock stack is honestly ~600 lines of vendor-only code.
        Template-generating the TOOLS skeletons could save ~90 more lines but is not
        counted: the descriptions carry vendor-specific warnings that are the seat's
        documentation surface.
RISK:   Unifying _safe_cwd forces one policy where three exist: the strictest union newly
        refuses some previously-legal calls (grok writing under ~/Documents; anything
        case-variant like ".SSH" on gemini). That is a loud behavior change to name in the
        commit, not a silent one. A shared module also makes wmw_common a single point of
        failure — armcheck's "all three seats start and list tools" canary already covers
        import failure, keep it.
```

```
[MERGE] wmw_cursor_mcp.py's four sibling-loaders → one cached load_sibling
WHY:    _allowance, _allowance_window_s, _allowance_calls and _guard (wrapper lines
        191-251) are the same importlib dance copied four times; three of them re-exec
        allowance.py from disk on EVERY guarded dispatch. Same loader, four names.
SHAPE:  One _load_sibling(name) with a module cache: ~15 lines replaces ~60. Must
        preserve _guard's return-the-exception semantics — its comment documents the
        fail-open scar ("A control that disappears when its file breaks is not a
        control"). Doable standalone inside the cursor wrapper, or in wmw_common if
        merge #1 lands.
SAVES:  ~45 lines + three disk-execs per guarded dispatch down to one cached load.
RISK:   Low. The only subtlety is the guard's fail-closed return; a generic loader that
        raises instead of returning the exception would reintroduce the fail-open shape
        at the call site.
```

```
[MERGE] calibrate-pool.py's meter() + find_cli() → read-meters.py + the shared finder
WHY:    calibrate's meter() (lines 27-40) re-implements read-meters' read_cursor() core
        (lines 118-148): same URL, same %APPDATA%\Cursor\auth.json, same Connect-RPC
        headers, same planUsage extraction — differing only in precision (raw floats vs
        formatted). calibrate's find_cli (lines 43-51) copies find_cursor_agent's
        candidate list. When Cursor changes the endpoint, two files drift — the same
        failure mode as the wrappers. (read-meters' docstring line 14 also still points
        at the deleted bench-burn.py; calibrate IS the burn tool now — one-line stale
        pointer folded into this merge.)
SHAPE:  read-meters gains read_cursor_raw() returning (auto%, api%, totalSpend_cents);
        read_cursor() formats its result; calibrate imports it via the established
        importlib sibling-load pattern (read-meters.py's dash makes plain import
        illegal — the pattern already accepted for allowance.py/dispatch-guard.py
        covers it). find_cli comes from wmw_common's find_exe if merge #1 lands.
SAVES:  ~40 lines; one endpoint definition instead of two.
RISK:   Low. read_cursor_raw must return full-precision floats (the formatted reader
        rounds for display; calibration divides by tiny deltas).
```

```
[MERGE] SPINE Part VI "Who may review" → a pointer to Part IV's anti-laundering guard
WHY:    Part VI review dispatch restates Part IV's two legal paths near-verbatim:
        "a different effective-model vendor + lineage (preferred — different
        weights/training/context; a different account merely hosting the builder's own
        brain does NOT count...) OR a boss-launched fresh seat (legal, weaker, flagged)"
        vs Part IV's "(a) a different effective-model vendor + lineage (different weights,
        training, no shared context... a different account merely hosting the builder's
        OWN brain does NOT count...), or (b) launched by the boss". SPINE's own header
        law says "One owner per fact" — this is SPINE restating SPINE.
SHAPE:  Part VI keeps: "Who may review: Part IV's two legal paths. Route by FIT within
        them:" + the fit-routing sentence + the SPINE-WIRING pointer. The restated paths
        are deleted.
SAVES:  ~70 tokens per summon.
RISK:   Low — Part IV is one PART away and already named as the owner in the restated
        text itself.
```

```
[MERGE] SPINE preflight's "Probe the TRANSPORT, not the binary" bullet → THE TRANSPORT LAW #4
WHY:    The same sentence lives twice. Preflight bullet: "a seat is online when its
        persistent seat answers in THIS session. A CLI --version proves only that the
        fallback lane exists — never enough on its own to count a seat present."
        TRANSPORT LAW #4: "A seat is online when its MCP seat answers in THIS session
        (registered and Connected); a CLI --version only proves the fallback lane exists."
        The bullet even confesses "(THE TRANSPORT LAW owns this)" — then says it anyway.
SHAPE:  Preflight keeps a half-line: "Probe the transport, not the binary (THE TRANSPORT
        LAW #4 owns this)." The law keeps the operative text.
SAVES:  ~45 tokens per summon.
RISK:   Minimal — the owner is already named at the point of use.
```

```
[MERGE] SKILL.md ON INVOCATION step 2 → a pointer to SPINE Part VI's preflight
WHY:    Step 2 (SKILL lines 68-79) re-teaches the whole preflight in prose: transport-first
        probe, CLI --version as fallback-only, effective-model/lineage, UNKNOWN LINEAGE
        fails closed, graceful degradation. SPINE Part VI "Reachability & effective-model
        preflight" owns every one of those and is already loaded and version-enforced by
        the same SKILL's DEPENDS block.
SHAPE:  Step 2 becomes: "Load SPINE-WIRING.md, run SPINE Part VI's preflight (transport
        first), then DECLARE the live arsenal + independence status in one line: 'Online:
        🟠 Claude · 🔵 Codex · ⚫ Grok · 🟢 Gemini — FULL CROSS-VENDOR.' No independent
        reviewer reachable → say so; unreviewed work is never reported as done." The
        declaration-line format and the honesty clause are the Deck-specific residue;
        everything else is a pointer.
SAVES:  ~140 tokens per summon.
RISK:   Low-medium — step 2 is the operational trigger actually read at invocation; the
        compression is safe only because DEPENDS already guarantees SPINE is loaded.
```

```
[MERGE] SKILL.md's doubled "the Deck adds nothing" paragraph → one telling
WHY:    Lines 33-39 say the same thing twice in adjacent paragraphs: "The Deck adds
        NOTHING to the method. Its whole delta is plain rendering... This file does not
        restate it." then "The Deck adds nothing to the *method*. Its entire delta is
        plain rendering + the gold-baton color narration. Every rule below is SPINE's..."
        One paragraph wearing two coats — an edit scar, not a defended redundancy.
SHAPE:  Keep the second (it carries the "every rule below is SPINE's; this section only
        presents" framing), delete the first.
SAVES:  ~50 tokens per summon.
RISK:   None found.
```

```
[MERGE] SKILL.md NARRATE IN COLOR's restated vendor→color map → THE NOTATION's ownership
WHY:    SKILL lines 42-44 re-list the map ("🟡➤ conductor · 🟠 Claude · 🔵 Codex · ⚫ Grok ·
        🟢 Gemini") while parenthetically admitting "(SPINE's THE NOTATION owns the
        vendor→color map)". THE NOTATION is loaded with SPINE on the same summon, so the
        restatement buys nothing at runtime and can drift (SKILL's map omits the 🟣 pool
        and bloodline marks THE NOTATION added at v4.2).
SHAPE:  Keep the pointer, the "color is a status light, not a costume" rule, the banner-
        never-lies example, and the narration sample. Delete the re-listed map.
SAVES:  ~40 tokens per summon.
RISK:   Minimal — the map is one scroll away in the same loaded context.
```

## KEEP APART — what only looks mergeable

- **The canonical invariant block copies (SPINE Part VIII ↔ SKILL "THE INVARIANTS" ↔ entry files).** Byte-identical duplication is the *mechanism* here (Principle 9: "never a duplicated full copy of the law... the block carries the operative invariants, sufficient to govern behavior even if the doctrine is never opened"). Collapsing it to a pointer is the exact fork-failure it exists to prevent.
- **The consent gate's three tellings (Part I §2 / Part VI dispatch gate / THE COUNCIL).** The text defends the redundancy in place: "a reflex wants redundancy." It guards the most expensive move in the method; ~100 tokens is the wrong savings to chase. One real finding inside it, though: §2 still cites "the Amendment Law prefers the rule that leaves a trace" — the Amendment Law was deleted today, so that's a dangling reference needing a one-line fix, not a merge.
- **Worker statuses (DONE / NEEDS_CONTEXT / BLOCKED…) vs the adjudication ladder (BLOCKER / MATERIAL / MINOR / NOT PROVEN).** Two ranking vocabularies that look collapsible; they grade different axes (task progress vs finding severity) and the text bans mixing them: "One axis per line, never mixed."
- **allowance.py ↔ dispatch-guard.py as files.** Both are "controls," but they share zero functions — permission record vs preflight/yield. Merging the files is "reorganised, same length," which the brief disqualifies. Share only the ledger-path constant and the loader (merges #1/#2).
- **read-meters.py ↔ dispatch-guard's yield.** Both "read meters," but different sources answering different questions: live vendor percentages ("what's left") vs seat ledger + vendor CSV ("what did it buy"). The only actual shared code is the Cursor-usage read, and merge #3 already takes it.
- **`_extract_json` first-object (grok/gemini) vs last-result-wins (cursor).** Genuinely different CLI stream shapes — cursor's CLI streams status lines before the result. The shared module carries both functions; it must never "unify" them into one with a flag.
- **armcheck.py ↔ the wrappers.** Its `seat()`/rpc helper is a fourth JSON-RPC implementation, but it's the *client* side attacking the *server* side. The suite already carries the scar: "A test must never be able to break the thing it is testing." Merging attacker into attacked would let a self-test pass itself.

## THE ONE MERGE worth doing if only one happens

**Merge #1 — the shared seat transport (`wmw_common.py`).** It is the largest saving (~350 lines) and the only one whose cost is already proven inside the code itself: the Gemini seat shipped a reply-escalation hole eleven months after... no — one day after the audit, eleven weeks after the Grok fix; its `_safe_cwd` is simultaneously the weakest (6 secrets, case-sensitive) and the strictest (home subtree) of the three; and the ledger path lived in two files until one silently zeroed a report. Every future guard fix lands in one place the day it is written, instead of being propagated by memory across three files — which today proved does not happen.

## CONFIDENCE

- **High** on merges #1–#3: duplication verified byte-level across all three wrappers and both tools in this packet; line counts counted from the source, not estimated. The "50–150 lines per vendor layer" verdict (true for grok/gemini modulo TOOLS tables, false for cursor) is stated from counted lines.
- **Medium-high** on merges #4–#8: anchors are exact and quoted; token deltas are honest estimates, and SPINE's deliberately-defended redundancies (consent gate, invariant block) were kept OUT of the merge list on purpose.
- **Medium** on merge #3's wiring detail: read-meters.py's dash makes it non-importable, so it needs either the importlib sibling pattern (precedent exists) or a rename — a build-time choice, not a blocker.