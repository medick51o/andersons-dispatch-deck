# BUILD SPEC — the merges a six-seat council carried

**Round 3, 2026-08-24. Six seats: Grok, Codex, Gemini, Composer, Cursor-Grok, Kimi K3 Max.**
Decision rule fixed before any seat reported: **3+ seats proposing the same merge → it gets
built.** Five carried.

This is a spec, not a change. Nothing here has been applied.

---

## THE TALLY

| Merge | Votes |
|---|---:|
| allowance + meters consolidation | **6** — unanimous |
| Part IV anti-laundering + Part VI review dispatch | 5 |
| **shared seat transport (3 wrappers → 1 core)** | 5 |
| THE METER LAW + THE COUNCIL SEAT LAW | 4 |
| Gate-0 + fleet test → one seat-admission gate | 3 |

**Five of six named the shared transport as their single most valuable merge.** Not one argued
tidiness. Every one argued it closes a bug class this shop demonstrated today.

---

## MERGE 1 — the shared seat transport (build this first)

### Why, in the shop's own evidence

Today's audit found `gemini-reply` accepting no `cwd` while passing `always_approve` through,
`_safe_cwd` comparing paths by equality so `C:\Windows\System32` was legal under a banned
`C:\Windows`, and a missing `MCPTool` deny. **Every one of those was a fix that already existed
in a sibling wrapper and never travelled.** The Grok seat had been correct since August.

> ⚫ Grok: *"the only merge that both shrinks the tree AND closes the class of bug this round is
> for: a guard fixed on Grok, missing on Gemini, still missing in pieces on Cursor."*

> 🌙 Kimi: *"the only one whose cost is already proven inside the code itself."*

### Shape (Codex's, which is the most specific)

`seat_core.py` owns: the newline-delimited JSON-RPC loop · initialize/ping/list/call dispatch ·
MCP result and error envelopes · UTF-8 setup · required/optional string and boolean validation ·
UUID and model-id validation · reply truncation · executable discovery · the subprocess
timeout/error boundary · **and one canonical `safe_write_cwd()`**.

That path policy is the **union of what each seat learned separately** (⚫ Grok's specification):

```
Grok's containment  +  Cursor's APPDATA/LOCALAPPDATA ban  +  Cursor's playpen allowlist
    resolves symlinks · requires an explicit existing directory for write-capable calls
    bans filesystem root, system trees, application-data trees, credential segments
    accepts adapter-declared safe exceptions (Cursor's playpen)
```

Each adapter supplies only: tool names and descriptions · executable candidates · prompt
transport · read/write CLI flags · output parser · footer · optional preflight and spend hooks.

### Honest savings — Codex corrected the other seats here

```
Grok adapter      ~100-150 lines     (was 370)
Gemini adapter    ~100-150 lines     (was 317)
Cursor adapter    ~300-450 lines     — will NOT reach 150
TOTAL SAVED       ~500-650 lines of 1,472
```

> 🔵 Codex: *"The earlier 50–150-line estimate is credible for Grok and Gemini, **but not for
> Cursor.**"* Cursor keeps meter classes, allowance, playpen, YOLO allowlist and guard policy —
> genuinely different behaviour, not duplication. **Do not force it to the same size.**

Earlier estimates of ~1,000 lines were optimistic. Publish 500–650.

---

## KEEP APART — the guard rail, and the most valuable part of this spec

🔵 Codex was explicit that merging these would cause harm. **Treat this list as binding.**

- **Vendor command builders and result parsers stay separate.** Grok's deny rules and
  `--disallowed-tools Agent`; Gemini's argv ceiling, `--mode plan` and `--print-timeout`;
  Cursor's `.cmd` injection defence, ASCII pointer spill and `--mode ask` vs `--yolo`.
  *"Treating those as configurable flag lists would hide the exact security behavior that needs
  review."*
- **The three MCP processes stay separate** even after the code merges. One multi-vendor server
  couples availability, credentials and failure domains — a crash or malformed response would
  take the whole bench offline.
- **Read-only enforcement stays vendor-specific.** *"A generic `readonly=True` flag is a useful
  normalized input, not a generic implementation."*
- **Allowance authority stays apart from meter observation.** `allowance.py` answers *may this
  seat spend*; `read` answers *what has been spent*; `calibrate` deliberately spends.
  **Permission must never be inferred from a healthy meter.**
- **`preflight` stays apart from `yield_report`.** Preflight is synchronous refusal before a
  write dispatch; yield is retrospective analytics. Making the wrapper depend on the reporting
  stack would enlarge the fail-closed runtime boundary.
- **armcheck's free and deep modes stay distinct execution modes** — they may share a harness,
  but the side-effect boundary is real.

---

## MERGE 2 — allowance + meters (6 votes, unanimous)

`read-meters.py::read_cursor` and `calibrate-pool.py::meter` independently open the same auth
file, call the same endpoint with the same headers, and decode the same object. `read-meters`
even ends on the unfinished line *"To learn the size,"* — and calibration is the operation that
completes that sentence.

`meters.py read [--grok|--cursor] [--json]` stays read-only. `meters.py calibrate cursor
--probe|--calls N` performs the metered burn **behind an unmistakable spending banner printed
before the first call.** Saves ~35–55 lines, and ends the situation where an observational
command sits beside a spending one with no boundary.

Also folds Cursor's three separate allowance lookups (`_allowance`, `_allowance_window_s`,
`_allowance_calls` — three dynamic imports of the same file, one reaching through a private
`_load()`) into a single `snapshot(seat)`. **One snapshot per dispatch, never cached across
requests.**

---

## MERGES 3–5 — the engine (SPINE)

- **Part IV anti-laundering + Part VI review dispatch** (5 votes) — one statement of who may
  review and what they are handed.
- **THE METER LAW + THE COUNCIL SEAT LAW** (4 votes) — one law about spending.
- **Gate-0 + fleet test → one SEAT ADMISSION GATE** (3 votes) — answers one question: *may this
  seat or seat-set enter this mission?*

The last one also **fixes a live contradiction** that two seats found independently: Gate-0 says
*"all five hold"* while Part IV lists **seven** conditions, omitting `Destined` and `Governed
where it RUNS`. That is a defect, not a preference.

---

## HOW THIS SHOULD BE BUILT

**Not by the orchestrator, and not in one pass.** Today's clearest lesson is that this session's
own rewrites introduced defects — a `NameError` that made a guard dead code, an owner token that
broke its own CLI, a `MAX_FRAME` check that fired after the damage. Three working wrappers
rewritten by the same hand that made those mistakes, unreviewed, is the exact shape to avoid.

1. **Build MERGE 1 alone**, by a seat that is not the orchestrator. Codex is the strongest
   candidate: it wrote the most precise shape and did not write the original wrappers.
2. **Review cross-vendor** — a different effective-model lineage than the builder.
3. **Gate on `armcheck --deep`**, which attacks all three seats. It must stay green: every
   read-only seat still refuses a direct request to write.
4. Only then MERGE 2, then the SPINE merges, each with its own gate.

**The write set for MERGE 1 is exactly:** `mcp-seats/seat_core.py` (new),
`mcp-seats/wmw_grok_mcp.py`, `mcp-seats/wmw_gemini_mcp.py`, `mcp-seats/wmw_cursor_mcp.py`.
Nothing else. `armcheck.py` may not be edited in the same pass — **a builder must not be able to
adjust the test that grades it.**
