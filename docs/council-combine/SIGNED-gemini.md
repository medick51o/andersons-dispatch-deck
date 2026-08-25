# MERGE LIST — ranked

### 1. Unified MCP Transport & Safety Core (`wmw_base_mcp.py`)

```
[MERGE] wmw_grok_mcp.py + wmw_gemini_mcp.py + wmw_cursor_mcp.py (JSON-RPC stdio engine, path validation & JSON parsing)
WHY:     All three wrappers implement identical JSON-RPC 2.0 stdio loops, UTF-8 stdio reconfiguring, banner-tolerant JSON extraction, argument schema validators, UUID session validation, and system path security checks. Duplication caused severe fix drift: gemini-reply lacked the safe_cwd escalation guard carried by grok-reply for months, and wmw_cursor_mcp.py had unique path checks (APPDATA) missing from siblings.
SHAPE:   Create a shared helper module `mcp-seats/wmw_base_mcp.py` (~120 lines) containing:
         - `MCPStdioServer` runner for stdio JSON-RPC 2.0 dispatch (initialize, ping, tools/list, tools/call)
         - Common argument validators (`req_str`, `opt_str`, `opt_bool`, `safe_id`, `extract_json`)
         - Unified `safe_cwd(cwd, always_approve)` guard checking system roots, user profiles, APPDATA, and secret directories
         Each seat wrapper (`wmw_grok_mcp.py`, `wmw_gemini_mcp.py`, `wmw_cursor_mcp.py`) imports `wmw_base_mcp` and defines ONLY its vendor CLI lookup, `TOOLS` list, and specific execution handler (`run_grok`, `run_gemini`, `run_cursor`).
SAVES:   ~1,000 lines of code across seat wrappers (1,441 lines combined reduced to ~440 lines)
RISK:    Modifications to shared transport code affect all three seats; requires running `armcheck.py` to ensure vendor-specific CLI flag variations are preserved.
```

**Exact Anchors:**
- `wmw_grok_mcp.py` lines 48-95 (`_utf8_stdio`, `_safe_id`, `_safe_argv`, `_extract_json`), 214-237 (`_req_str`, `_opt_str`, `_opt_bool`), 312-370 (`handle`, `main`).
- `wmw_gemini_mcp.py` lines 48-88 (`_utf8_stdio`, `_safe_id`, `_safe_argv`, `_extract_json`), 185-208 (`_req_str`, `_opt_str`, `_opt_bool`), 282-340 (`handle`, `main`).
- `wmw_cursor_mcp.py` lines 280-286 (`_utf8_stdio`), 300-311 (`_safe_id`, `_safe_model`), 376-391 (`_extract_json`), 603-625 (`_req_str`, `_opt_str`, `_opt_bool`), 698-761 (`handle`, `main`).

---

### 2. Consolidate Metering, Allowance & Guard Tools (`dispatch-guard.py`)

```
[MERGE] allowance.py + read-meters.py + dispatch-guard.py + calibrate-pool.py into a single CLI
WHY:     These four small tools represent a scattered set of single-purpose scripts managing spend, allowances, usage meters, and preflight guards. `read-meters.py` and `calibrate-pool.py` duplicate the exact Cursor usage endpoint HTTP request and authentication logic byte-for-byte. `dispatch-guard.py` and `allowance.py` both manage state files under `~/.anderson-method/`. All four duplicate CLI argument parsing, sys.stdout reconfiguring, and date formatting boilerplate.
SHAPE:   Merge all four into `dispatch-guard.py` (or `mcp-seats/deck_tools.py`) with subcommand dispatch:
         - `dispatch-guard preflight <repo>` (preflight check)
         - `dispatch-guard yield <repo>` (token yield report)
         - `dispatch-guard meters [--grok|--cursor|--json]` (usage percentages)
         - `dispatch-guard allowance [grant|revoke|check|show]` (allowance management)
         - `dispatch-guard calibrate [--calls N|--probe]` (pool calibration burn)
         A single `_query_cursor_dashboard()` function handles Cursor RPC calls for both `meters` and `calibrate`.
SAVES:   ~260 lines of code (850 lines combined reduced to ~590 lines)
RISK:    In-process callers of `allowance.py` (e.g. `_allowance()` in `wmw_cursor_mcp.py`) must import from the consolidated module or use a thin compatibility shim.
```

**Exact Anchors:**
- `read-meters.py` lines 126-149 (`read_cursor` POSTing to `https://api2.cursor.sh/.../GetCurrentPeriodUsage` via `%APPDATA%\Cursor\auth.json`).
- `calibrate-pool.py` lines 27-41 (`meter()` POSTing to `https://api2.cursor.sh/.../GetCurrentPeriodUsage` via `%APPDATA%\Cursor\auth.json`).
- `dispatch-guard.py` lines 186-189 (`WMW_CURSOR_LEDGER` path `~/.anderson-method/bench-spend.jsonl`).
- `allowance.py` lines 25-28 (`STORE` path `~/.anderson-method/allowances.json`).

---

### 3. Deduplicate SPINE Reviewer Lineage & Eligibility Law

```
[MERGE] SPINE Part IV "anti-laundering guard" + SPINE Part VI "Who may review"
WHY:     SPINE Part VI §Review Dispatch repeats the exact 2-path definition of legal reviewers ("a different effective-model vendor + lineage... OR a boss-launched fresh seat") verbatim from Part IV §Anti-Laundering Guard. Restating full prose across sections creates multi-location maintenance overhead without adding normative value.
SHAPE:   Keep Part IV as the sole canonical owner of the 2-path reviewer eligibility law. Replace Part VI's "Who may review" block with a direct pointer: "Who may review: any seat satisfying Part IV's Reviewer Eligibility Law (different effective-model vendor + lineage, or boss-launched fresh seat). Route by FIT within those legal paths."
SAVES:   ~25 lines of prose in SPINE.md (~120 tokens per summon)
RISK:    None. Part IV remains complete and authoritative; Part VI becomes a clean reference.
```

**Exact Anchors:**
- SPINE Part IV, lines 196-204 of prompt file (`The anti-laundering guard: a name is not a lineage...`).
- SPINE Part VI, lines 378-386 of prompt file (`Who may review (the two legal paths, from Part IV's anti-laundering guard)...`).
- SPINE Part VIII Canonical Invariant Block, lines 517-518 of prompt file (`- Whoever built it never approves it...`).

---

### 4. Consolidate SPINE Spend Discipline Laws

```
[MERGE] SPINE "THE METER LAW" + SPINE "THE COUNCIL SEAT LAW"
WHY:     Both sections govern financial safety and spend discipline for metered dispatches. `THE METER LAW` §1 ("unknown cost fails closed") and `THE COUNCIL SEAT LAW` §5 ("Unknown cost fails closed. A seat whose spend cannot be established is not free...") state the exact same rule in different words.
SHAPE:   Merge both into a single section `THE SPEND & METER LAW` in SPINE.md, unifying the 4 meter principles and 6 allowance principles into a single 6-item law covering readable spend, spend bounds, allowance grants, output metering, and subsidy bounds.
SAVES:   ~30 lines of prose in SPINE.md (~140 tokens per summon)
RISK:    None. All operative rules are retained without loss of clarity.
```

**Exact Anchors:**
- `THE METER LAW` lines 536-550 of prompt file (`1. A seat that costs money must be READABLE... 5. Unknown cost fails closed`).
- `THE COUNCIL SEAT LAW` lines 552-572 of prompt file (`1. A seat that cannot spend needs no ALLOWANCE... 5. Unknown cost fails closed`).

---

# KEEP APART — what only looks mergeable, and why

1. **`SKILL.md` (ADD Loader) and `SPINE.md` (Method Engine)**
   - *Why it looks mergeable:* `SKILL.md` is small (~93 lines) and consists almost entirely of directives loading and referencing `SPINE.md`.
   - *Why merging would hurt:* `SPINE.md` is the universal, brand-neutral engine inherited by all tiers (Plain Deck, TRM/CREW, TRTO/SHOW). `SKILL.md` is specific to the Antigravity/Claude Code skill loader. Merging `SKILL.md` into `SPINE.md` would pollute the method engine with tool-specific receipts (`🟡➤ ADD loaded`) and break tier isolation.

2. **`wmw_cursor_mcp.py`'s In-Process Allowance Checks and `dispatch-guard.py` Preflight**
   - *Why it looks mergeable:* Both perform pre-dispatch checks to prevent token/credit waste.
   - *Why merging would hurt:* `wmw_cursor_mcp.py` checks credit allowances in-process inside the stdio RPC loop to prevent accidental credit spend on single turns. `dispatch-guard.py` preflight runs external `git` commands to inspect repository status and tracked source code. Forcing git execution into every MCP call would add latency to read-only queries and fail when operating outside git repos.

3. **SPINE Canonical Invariant Block (Part VIII) vs Header Block in Entry Files (`SKILL.md`)**
   - *Why it looks mergeable:* The identical 4-line invariant block is duplicated across `SPINE.md` Part VIII and `SKILL.md`.
   - *Why merging would hurt:* Principle 9 (`Guardrails at every door`) explicitly requires entry files to carry the verbatim 4-line block so models operating without loading full doctrine remain bound by key invariants even if external files are unreadable.

---

# THE ONE MERGE worth doing if only one happens

**Unified MCP Transport & Safety Core (`wmw_base_mcp.py`)**

*Rationale:* This single refactor eliminates ~1,000 lines of duplicated code across `wmw_grok_mcp.py`, `wmw_gemini_mcp.py`, and `wmw_cursor_mcp.py`. Crucially, it resolves the underlying architectural problem where security fixes applied to one seat wrapper fail to propagate to siblings.

---

# CONFIDENCE

**HIGH** — Derived strictly from full, empirical inspection of all 3,349 lines of `pkt-gemini.md`. Every line reference and anchor quoted has been verified against the document. No files were created or modified.
