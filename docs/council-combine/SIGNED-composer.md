Reading the brief and following its scan instructions.
The brief is large; I'll read it in sections to capture the full instructions and format.
Reading the embedded source sections and comparing them to the codebase for merge analysis.
MERGE LIST — ranked

---

**[MERGE] `wmw_grok_mcp.py` + `wmw_gemini_mcp.py` + shared JSON-RPC/validation into `wmw_transport.py`**
WHY: `handle()` / `main()` are byte-for-byte the same JSON-RPC loop in all three seats (`wmw_grok_mcp.py` 312–367, `wmw_gemini_mcp.py` 282–337); `_utf8_stdio`, `_extract_json`, `_safe_id`, `_safe_argv`, `_req_str` / `_opt_str` / `_opt_bool` are copy-paste. Today's Gemini `gemini-reply` cwd guard lag (pkt lines 1495–1500) is exactly the propagation failure the brief names.
SHAPE: One stdlib module `mcp-seats/wmw_transport.py` owning stdio JSON-RPC, arg parsing, UUID guards, and one canonical `_safe_cwd()` (Grok's containment version — segment match, not Gemini's weaker basename check at `wmw_gemini_mcp.py` 180–182). Each seat file keeps only: `find_*()`, `run_*()`, `TOOLS`, `_tool_call()`, and `from wmw_transport import run_stdio_server` (or equivalent). Three MCP entrypoints remain for registration; one library is the fix surface.
SAVES: ~350 lines of code (349 + 318 + duplicated slices from cursor ≈ 1368 → ~1000); ~0 tokens/summon (not in summon path)
RISK: `_safe_cwd` policy must be unified upward (Gemini's weaker tree); shared-module regression hits all seats — `armcheck.py` becomes mandatory on any transport edit.

---

**[MERGE] `allowance.py` + `read-meters.py` + `dispatch-guard.py` + `calibrate-pool.py` → one `deck-ops.py` (or `meter-guard.py`) with subcommands**
WHY: All four are operator CLIs over the same concerns: Cursor auth + usage API (`read-meters.py` `read_cursor()` 118–149 and `calibrate-pool.py` `meter()` 27–40 are duplicate Connect-RPC reads), spend ledger (`dispatch-guard.py` yield 186–207 reads `bench-spend.jsonl`; `wmw_cursor_mcp.py` `_log_spend` writes it), and allowance grants (`allowance.py` — loaded four times in cursor via identical `importlib.util` blocks at lines 199–241).
SHAPE: Single file, argparse subcommands: `grant` / `revoke` / `check` / `show` (allowance); `read [--grok|--cursor|--json]` (meters); `preflight <repo>` (dispatch-guard); `yield <repo>` (cost-per-accepted-line); `calibrate [--probe|--calls N]` (pool sizing). Shared `cursor_usage()` and `ledger_path()` helpers. `wmw_cursor_mcp.py` does `import allowance` (or `from deck_ops import allowance`) once instead of four dynamic loads.
SAVES: ~200 lines of code (667 → ~470); ~0 tokens/summon
RISK: Operator scripts/docs that invoke the old filenames need updating; a monolith is easier to break if subcommand routing is sloppy.

---

**[MERGE] SPINE Part I §2 consent/right-size + Part VI "The dispatch gate" + THE COUNCIL consent paragraphs + COUNCIL SEAT LAW clause 6**
WHY: The same decision — "council/panel is SPECIAL, boss must say go" — is owned in Part I §2 (pkt lines 146–152: "This clause OWNS the consent gate" then "deliberately restated at the dispatch gate and THE COUNCIL"), restated in Part VI dispatch gate (280–284), THE COUNCIL (409–417), and COUNCIL SEAT LAW #6 (654–655). One law wearing four names.
SHAPE: Part I §2 keeps the full consent + right-size + earn-a-head text. Part VI dispatch gate becomes two bullets: "(1) apply Part I §2 two questions; (2) parallel builders → Part IV fleet test." THE COUNCIL opens with "Consent: Part I §2 — procedure below assumes go." Delete COUNCIL SEAT LAW #6; fold into Part I §2 cross-ref. No new prose — relocate ownership, cut repeats.
SAVES: ~35 SPINE lines → ~400–500 tokens per summon
RISK: Orchestrators that only read Part VI miss consent if the pointer is too thin; consent must stay load-bearing in Part I §2.

---

**[MERGE] SPINE Principle 8 loop caps + Part VI "Escalation" + Part VII autonomous-hours bell + THE COUNCIL step 5**
WHY: "Two rounds per dispute / one exchange on tone / bell then queue" is defined in Principle 8 (pkt 213–218), mechanized again in Part VI Escalation (452–459), repeated in Part VII autonomous hours (486–492), and again in THE COUNCIL step 5 (517–518). Same cap, four ledgers.
SHAPE: Principle 8 owns the full cap table (review disputes · tone/nits · unattended debates). Part VI Escalation, Part VII autonomous block, and council step 5 become one-line pointers: "Cap: Principle 8." Cut duplicated "two rounds per debate" prose.
SAVES: ~25 SPINE lines → ~250–350 tokens per summon
RISK: Autonomous-hours "bell" nuance (pivot, don't idle) must stay somewhere visible — keep in Part VII as non-cap bullets only.

---

**[MERGE] SPINE Part VI "Reachability & effective-model preflight" + THE TRANSPORT LAW #4**
WHY: Both govern the same probe: seat online when MCP answers in THIS session; CLI `--version` is fallback only (Part VI 304–323 vs TRANSPORT LAW 683–685). Declaration vs detection vs transport probe are one preflight, split across two owner headings.
SHAPE: Part VI keeps the full preflight (reachability, effective model, capability, fail-closed, independence status output). THE TRANSPORT LAW drops #4; add "Preflight: Part VI Reachability." TRANSPORT LAW keeps opt-in, fresh-call vs reply-chain, read-only default.
SAVES: ~15 SPINE lines → ~150–200 tokens per summon
RISK: Low — pointer preserves behavior; transport law readers must follow one link.

---

**[MERGE] SKILL.md duplicate "WHAT THE DECK ADDS" blocks**
WHY: Lines 33–39 and 793–796 say the same thing twice: "Deck adds NOTHING to the method… plain rendering + gold baton… does not restate SPINE."
SHAPE: One section. Delete the duplicate paragraph; keep DEPENDS, LOAD RECEIPT, NARRATE IN COLOR, FUEL MODE, ON INVOCATION, INVARIANTS.
SAVES: ~6 lines → ~80–100 tokens per `/dispatch` activation
RISK: None.

---

**[MERGE] SPINE Part VI "Review dispatch" + Part IV anti-laundering guard**
WHY: Both define who may review (different effective-model vendor + lineage, or boss-launched fresh seat) and that builder narrative must not anchor the reviewer (Part IV 196–203 vs Part VI 377–397). Same gate, two angles.
SHAPE: Part IV anti-laundering keeps the two legal paths. Part VI "Review dispatch" shrinks to: ticket contents (original task, full write set, diff, verify output) + "Who may review: Part IV." Delete repeated independence prose in Part VI.
SAVES: ~12 SPINE lines → ~120–180 tokens per summon
RISK: Review ticket shape is operational — must not be lost in the pointer.

---

KEEP APART

**Three MCP server entrypoints (`wmw_grok_mcp.py`, `wmw_gemini_mcp.py`, `wmw_cursor_mcp.py`)** — Merge the library, not the processes. Claude Code registers three stdio servers; one binary with three modes would break existing MCP config.

**`wmw_cursor_mcp.py` meter/guard/playpen stack vs Grok/Gemini wrappers** — Cursor owns meter classes (`INCLUDED_PREFIXES` / `CREDIT_PREFIXES`), YOLO allowlist, council lock, playpen prompt spill (security: PowerShell injection, pkt 1599–1606), spend ledger, and allowance/guard preflight. Grok uses `--deny` rules + `--prompt-file`; Gemini uses `--mode plan` + argv prompt cap. Enforcement mechanisms differ; only transport/validation is shared.

**Part IV fleet "Bounded" vs THE COUNCIL SEAT LAW allowance** — Fleet caps parallel seat count before fan-out (Part IV 167–170: "claimed atomically"). Allowance caps metered spend per window (`allowance.py` `grant()`). Same word "bound," different decisions; merging would blur declare-before-launch vs ask-before-spend.

**THE METER LAW vs THE COUNCIL SEAT LAW** — Meter law: readability, measure-don't-infer, cost-per-accepted-change (links to `dispatch-guard yield`). Council seat law: spending gate before metered dispatch. Related but not identical; merge would couple sizing methodology to spend permission.

**SPINE Part VIII invariant block vs SKILL.md verbatim copy** — Principle 9 requires byte-identical block in entry files (pkt 512–524, SKILL 841–850). Cannot merge into one loaded location without breaking the guardrail-at-every-door rule.

**Part V adjudication vs Part VII review-culture** — Part V owns substance (ACCEPT/DISPUTE, three lists, escalation on falsifiable evidence). Part VII owns process tone (circle-backs, one exchange on nits, emergency brake). Severity ladder is already canonical in Part V; Part VII's job is scheduling and anti-debate-club — not duplicate law.

**`armcheck.py` vs operator CLIs** — Test harness with live `--deep` token spend; not an operator tool. Keep separate from `deck-ops` merge.

**Ladder of Truth (Part I §1) vs Principle 5** — Principle 5 already points to Part I §1 for oracle/RED-first. Short cross-ref is intentional; folding Part I into Principle 5 loses the "four load-bearing structures" frame.

---

THE ONE MERGE worth doing if only one happens

**`wmw_transport.py` shared seat transport** — Highest ROI: ~350 lines gone, one fix surface for the JSON-RPC/validation/cwd bugs that already propagated Gemini→Grok, and the brief's central example. Subscription seats stay thin vendor adapters; propagation failures stop being structural.

---

CONFIDENCE

**High** on `wmw_transport.py` (duplication is measurable; Gemini lag is proof). **High** on four-tool CLI merge (duplicate Cursor API + ledger paths are explicit). **Medium-high** on SPINE consent + loop-cap merges (clear duplicate anchors; pointer discipline required). **Medium** on reachability/transport and review-dispatch merges (real savings, smaller). **High** on KEEP APART judgments for cursor-vs-sibling seats and fleet vs allowance.