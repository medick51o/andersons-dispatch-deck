# COUNCIL BRIEF RESPONSE — THE CURSOR BENCH (204-MODEL RESERVE)

**Seat Lens:** 🟢 **Gemini — The Ledger Architect**  
**Focus:** Data schemas, retrieval efficiency, lineage safety, context optimization, and operational doctrine.

---

### 1. The Trigger Rule

The persistent house seats (Claude, Codex, Grok, Gemini) form the flat-rate foundation of the shop ($0 marginal cost). The metered Cursor bench (`wmw-cursor`) must **never** be used as a general-purpose substitute for house seats. It is an **overflow valve** and **specialist reserve**.

#### Allowed Triggers (Checkable Conditions)
Reaching for the Cursor bench is authorized **only** when at least one of the following 5 checkable conditions is satisfied:

1. **`LINEAGE_EXHAUSTION` (Independent Review Requirement):**
   - *Condition:* A mandatory code review or plan audit requires a distinct vendor lineage (SPINE Law #1), but all available house seats share lineage with the build author or previous reviewers.
   - *Check:* `Count(HouseSeats matching UnusedLineage) == 0 AND Count(BenchSeats matching UnusedLineage) > 0`.
2. **`CONTEXT_WINDOW_EXCURSION` (>200k Token Workload):**
   - *Condition:* A single operation requires digesting an ultra-large context (>200k tokens up to 1M) that exceeds standard house session limits or would wipe out persistent house context.
   - *Check:* `InputTokens > 200,000 AND BenchModel.ContextWindow >= InputTokens`.
3. **`SUB_5S_SCRATCH_BURST` (High-Velocity Scratch Iteration):**
   - *Condition:* High-velocity, throwaway micro-edits or scratchpad code generation where persistent house session round-trip latency (>15s) hinders flow, and sub-5-second execution (`composer-2.5` / `composer-2.5-fast`) accelerates execution.
   - *Check:* `TaskType == SCRATCH_PAD_EDIT AND RequiredLatency < 5s`.
4. **`NON_WESTERN_BENCHMARK_DIVERSITY` (Alternative Reasoning Lineage):**
   - *Condition:* Complex architectural validation requiring reasoning outside Western frontier models (e.g., Moonshot/Kimi K3 or Zhipu/GLM 5.2) to detect blind spots.
   - *Check:* `TaskType == DEEP_ARCHITECTURE_AUDIT AND RequireDiverseLineage == true`.
5. **`HOUSE_SEAT_OUTAGE_FALLBACK` (Preflight Failure of House Seat):**
   - *Condition:* A required house seat fails preflight transport probe or hits active provider rate-limits during a critical blocking task.
   - *Check:* `HouseSeat.PreflightStatus == DOWN AND TaskPriority == BLOCKING`.

#### Forbidden Triggers (Strictly Prohibited)
Reaching for the Cursor bench is **WRONG** and strictly blocked if:
- **Default Workhorse Routing:** Invoking a bench model for standard editing, debugging, or planning when an eligible flat-rate house seat is operational.
- **Lineage-Aliased Review:** Summoning a bench model whose effective lineage matches the builder (e.g., using `wmw-cursor/claude-opus-5` to review a Claude-built pull request).
- **Unbounded Fleet/Swarm Execution:** Launching multiple parallel bench subagents without strict per-task budget caps.
- **Unverified Preflight Call:** Attempting to dispatch to a bench model that has not passed a preflight transport and lineage classification check.

---

### 2. Suggest vs. Summon (The Consent Matrix)

Because the Cursor seat is metered against a finite $20/month plan quota with on-demand risk, all invocations must strictly obey the shop law: *"Nothing irreversible without the boss."*

```
                             +-----------------------+
                             |   Orchestrator Task   |
                             +-----------+-----------+
                                         |
                       Is task scratch/read-only AND plan quota < 50%?
                                    /         \
                                  YES          NO
                                  /             \
                   +------------------+    Is monthly quota < 90%
                   |  TIER 1: SILENT  |    AND single call within limit?
                   |  Auto-Summon     |           /         \
                   +------------------+         YES          NO
                                                /             \
                                 +-------------------+   +--------------------+
                                 |  TIER 2: OFFER    |   | TIER 3: EXPLICIT   |
                                 |  Suggest + [y/N]  |   | Boss Ruling (Lock) |
                                 +-------------------+   +--------------------+
```

#### Tier 1: Silent Summon (Automated / Zero-Interruption)
- **Permitted Scope:** Read-only analysis or isolated scratchpad code edits using included plan quota.
- **Allowed Models:** `composer-2.5-fast`, `kimi-k3-low`, `gemini-3.6-flash-minimal`.
- **Hard Constraints:**
  - `bench_policy.auto_summon == true` in project config.
  - Monthly plan quota consumption is **under 50%**.
  - Max 1 call per task; zero workspace side-effects (writes restricted to `/scratch/`).

#### Tier 2: Offer / Suggest First (Default for Standard Bench Ops)
- **Permitted Scope:** Single-model code reviews, specialized non-Western audits, or 1M-token context planning queries.
- **Orchestrator Protocol:** The orchestrator halts execution and presents a standard prompt:
  > 💡 **Bench Suggestion:** Recommending `wmw-cursor/kimi-k3-high` for independent 2nd review (Builder: Claude Code).  
  > **Lineage:** Moonshot (Independent) | **Est. Quota:** 1 unit (~0.2% monthly pool) | **Reason:** Lineage exhaustion on house seats.  
  > *Proceed? [y/N]*
- **Requires:** Explicit single-key user authorization (`y`).

#### Tier 3: Explicit Boss Ruling Required (Mandatory Hard Stop)
- **Permitted Scope:**
  - Any call when monthly plan quota is **>90%** or operating in on-demand overage billing mode.
  - Any call invoking 1M-token context frontier tiers (`claude-opus-5-1m`, `gpt-5.6-sol-1m`).
  - Direct code writes to non-scratch, tracked git workspace files.
  - Batch / multi-model bench sweeps (>2 sequential or parallel calls).
- **Requires:** Formally logged user confirmation with explicit budget review.

---

### 3. The Ledger's Shape (Catalog Architecture & Schema)

To prevent context rot, high token overhead, and stale fiction across 204 models, the catalog is structured as a **Two-Tiered Indexing System**.

```
+-------------------------------------------------------------------------+
|                              LOCAL DISK                                 |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  | bench-catalog.json (Full Tier 2 Registry - 204 Models, ~85 KB)   |  |
|  | - Complete parameters, aliases, raw provider specs, timestamps    |  |
|  +-------------------------------------------------------------------+  |
|                                  |                                      |
|                                  v                                      |
|  +-------------------------------------------------------------------+  |
|  | agy bench query CLI / Script Filter                                |  |
|  +-------------------------------------------------------------------+  |
+----------------------------------+--------------------------------------+
                                   | Filters & Projects
                                   v
+-------------------------------------------------------------------------+
|                           IN-CONTEXT MEMORY                             |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  | bench-index.json (Compact Tier 1 Index - ~28 Archetypes, ~2.5 KB) |  |
|  | - Loaded into Orchestrator prompt or queried mid-project in <2ms  |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

#### Granularity Strategy
- **Do NOT load 204 rows into prompt context.** Loading 204 raw model JSON objects wastes ~15,000 tokens per prompt step and degrades orchestrator attention.
- **Tier 1 (In-Context Index - `bench-index.json`):** A lightweight summary containing **~28-32 Family Archetypes** (categorized by family + effort tier). Size: ~2.5 KB.
- **Tier 2 (Full Registry - `bench-catalog.json`):** The authoritative 204-model disk database queried on-demand by CLI (`agy bench query`).

#### Exact Column Schema (`bench-catalog.json`)

| Field Name | Type | Description / Constraints | Example Value |
|---|---|---|---|
| `model_id` | String (PK) | Exact Cursor API model identifier string | `"cursor/kimi-k3-high"` |
| `family` | String | Family grouping tag | `"kimi"` |
| `display_name` | String | Human-readable alias | `"Kimi K3 (High Effort)"` |
| `effective_lineage` | Enum | True underlying model vendor (FOR INDEPENDENCE LAW) | `"Moonshot"` |
| `tier` | Enum | Operational classification (`frontier`, `workhorse`, `utility`, `fast-scratch`) | `"workhorse"` |
| `effort_level` | Enum | Reasoning depth (`minimal`, `low`, `medium`, `high`, `xhigh`, `max`) | `"high"` |
| `context_limit_k` | Integer | Maximum context window in thousands of tokens | `200` |
| `quota_weight` | Float | Multiplier for plan pool usage burn (1.0 = standard) | `0.5` |
| `primary_niche` | Enum Array | Functional capability tags (`independent_review`, `fast_scratch`, `long_context`, `bulk_doc`) | `["independent_review"]` |
| `status` | Enum | Preflight state (`active`, `degraded`, `disabled`, `unverified`) | `"active"` |
| `last_probed` | ISO-8601 | Timestamp of last automated preflight probe | `"2026-08-23T11:00:00Z"` |

#### Concrete JSON Example Entry
```json
{
  "model_id": "cursor/kimi-k3-high",
  "family": "kimi",
  "display_name": "Kimi K3 (High Effort)",
  "effective_lineage": "Moonshot",
  "tier": "workhorse",
  "effort_level": "high",
  "context_limit_k": 200,
  "quota_weight": 0.5,
  "primary_niche": ["independent_review", "alternative_reasoning"],
  "status": "active",
  "last_probed": "2026-08-23T11:00:00Z"
}
```

#### Anti-Rot Refresh Mechanism
1. **Automated Preflight Probe (`agy bench probe`):**
   - Executed via background cron or on session start.
   - Hits `wmw-cursor` model listing endpoint, verifies response times, and detects new/removed models.
   - Updates `status` and `last_probed` fields in `bench-catalog.json`. Re-generates `bench-index.json`.
2. **Fail-Closed Unverified Quarantine:**
   - Any newly discovered model not yet in `bench-catalog.json` is assigned `effective_lineage: "UNKNOWN"` and `status: "unverified"`.
   - Orchestrator is **strictly forbidden** from routing review calls to `"unverified"` models until human review or automated taxonomy classification runs.

#### Mid-Project Context-Efficient Reading
The orchestrator reads mid-project using **Targeted Local CLI Filtering** rather than context injection:
```powershell
# Example local query executed by Orchestrator tool:
agy bench query --exclude-lineage Anthropic,Google --capability independent_review --max-weight 1.0
```
*Output returned to context (1 line, 80 tokens):*
`{"recommended": "cursor/kimi-k3-high", "lineage": "Moonshot", "context_k": 200, "quota_weight": 0.5}`

---

### 4. What the Bench is Genuinely GOOD For (Model-to-Job Matrix)

#### Skeptical Assessment
**90% of shop work MUST remain on persistent house seats.** House seats offer zero marginal cost, persistent session IDs (full state across invocations), and instant availability. The Cursor bench is inferior for routine work because it lacks persistent seat session context and consumes metered quota.

However, the bench excels in **4 narrow specialized niches**:

```
+-----------------------------------------------------------------------------------+
|                            SPECIALIZED BENCH MATRIX                               |
+----------------------+--------------------------+---------------------------------+
| Phase                | Model Selected           | Exact Target Job                |
+----------------------+--------------------------+---------------------------------+
| 1. Planning          | gpt-5.6-sol (1M)         | Massive Monolith Architecture   |
|                      | claude-opus-5-1m         | Intake (>300k token specs)      |
+----------------------+--------------------------+---------------------------------+
| 2. Building          | composer-2.5             | Sub-5s Boilerplate Burst &      |
|                      | composer-2.5-fast        | Throwaway Scratch File Edits    |
+----------------------+--------------------------+---------------------------------+
| 3. Reviewing         | kimi-k3 (high/max)       | Independent 3rd-Lineage Review  |
|                      | glm-5.2-max              | (Non-Western Vendor Perspective)|
+----------------------+--------------------------+---------------------------------+
| 4. Post-Project      | gemini-3.6-flash-minimal | Bulk Changelogs, Test Log       |
|                      | cursor-grok-4.5-fast     | Parsing, Mechanical Sweeps      |
+----------------------+--------------------------+---------------------------------+
```

#### Phase Breakdown & Specific Model Assignments

1. **Planning Phase — Ultra-Large Context Intake**
   - **Model:** `cursor/gpt-5.6-sol` (1M Context Tier) or `cursor/claude-opus-5-1m`.
   - **Job:** Digesting multi-repository architectural specs, legacy code dumps, or massive PRD documents (>300k tokens) in a single pass to generate project blueprints without cluttering persistent house seat memory.
2. **Building Phase — Rapid Scratch Generation**
   - **Model:** `cursor/composer-2.5` / `cursor/composer-2.5-fast`.
   - **Job:** Sub-5-second rapid scratchpad code generation, unit test scaffolding, and repetitive boilerplate generation where 4.7s round-trip latency outperforms persistent chat session overhead.
3. **Reviewing Phase — True Lineage Independence**
   - **Model:** `cursor/kimi-k3` (high/max effort) or `cursor/glm-5.2-max`.
   - **Job:** Providing 3rd-party independent code reviews when Claude (Anthropic) built the code and Gemini (Google) / Grok (xAI) performed initial passes. Kimi (Moonshot) and GLM (Zhipu) provide non-Western, completely un-aliased model reasoning at low quota burn.
4. **Post-Project Phase — Bulk Mechanical Chores**
   - **Model:** `cursor/gemini-3.6-flash-minimal` or `cursor/cursor-grok-4.5-fast`.
   - **Job:** Mechanical repository sweeps: formatting documentation, parsing thousands of lines of build/test logs, generating changelogs, and performing bulk lint fixes without spending rate limits on house seats.

---

### 5. Lineage Safety (SPINE Law #1 Enforcement)

SPINE Law #1 dictates: *A review must come from a different effective-model vendor and lineage than the build.* A host renting another vendor's brain counts as that vendor's lineage (`cursor/claude-*` IS Anthropic lineage).

#### Effective Lineage Enforcer (ELE) Mechanism

1. **Lineage Mapping Table:**
   Every model in `bench-catalog.json` MUST explicitly map to its `effective_lineage`:
   - `claude-*` $\rightarrow$ `Anthropic`
   - `gpt-*` / `codex-*` $\rightarrow$ `OpenAI`
   - `cursor-grok-*` $\rightarrow$ `xAI`
   - `gemini-*` $\rightarrow$ `Google`
   - `kimi-*` $\rightarrow$ `Moonshot`
   - `glm-*` $\rightarrow$ `Zhipu`
   - `composer-*` $\rightarrow$ `Cursor-Native`

2. **Pre-Dispatch Independence Assertion:**
   Before orchestrating any review task, the SPINE engine runs the following check:
   ```python
   def verify_review_lineage(builder_lineage, prior_reviewer_lineages, target_bench_model):
       target_lineage = catalog.get(target_bench_model).effective_lineage
       
       if target_lineage == "UNKNOWN":
           raise LineageViolation("FAIL_CLOSED: Target model lineage is unverified.")
           
       if target_lineage == builder_lineage:
           raise LineageViolation(
               f"LINEAGE COLLISION: Target {target_bench_model} ({target_lineage}) "
               f"matches Builder ({builder_lineage}). Review rejected."
           )
           
       if target_lineage in prior_reviewer_lineages:
           raise LineageViolation(
               f"LINEAGE COLLISION: Target {target_bench_model} ({target_lineage}) "
               f"already participated in review cycle."
           )
           
       return True
   ```

3. **Orchestrator Enforcement Rule:**
   If Claude Code (Anthropic) builds a feature, the orchestrator's query filter **hard-excludes** all `effective_lineage: Anthropic` models. Passing `cursor/claude-opus-5` as an independent reviewer for a Claude build will throw a hard system exception and fail closed.

---

### 6. The Budget Rule (Metering & Plan Protection)

To prevent erosion of the shop's subscription-only doctrine and eliminate billing surprises, the Cursor bench operates under the **Soft-Cap Circuit Breaker Policy**.

#### Budget Governance Framework

1. **Zero-Overage Default Lock:**
   - On-demand billing is **HARD-DISABLED** at the account/seat config level (`allow_on_demand_overage: false`).
   - The bench seat strictly draws from the $20/month Cursor Pro plan pool. If plan credits exhaust, the bench seat transitions to `EXHAUSTED` state and fails closed.
2. **Quota Pool Metering Ledger (`.system_generated/bench_quota.json`):**
   - Every bench invocation logs token usage and credit burn to a local state file.
   - Monthly quota allocation: **1,000 Standard Units**.

```json
{
  "billing_cycle_start": "2026-08-01T00:00:00Z",
  "monthly_unit_cap": 1000,
  "units_consumed": 245,
  "units_remaining": 755,
  "overage_allowed": false,
  "circuit_breaker_status": "NORMAL"
}
```

3. **Threshold Actions:**
   - **<50% Consumed (`NORMAL`):** Tier 1 Silent Summons allowed for scratch tasks.
   - **50%–90% Consumed (`WARNING`):** Tier 1 Disabled. All bench calls require Tier 2 User Consent (`[y/N]`).
   - **>90% Consumed (`CRITICAL`):** Circuit breaker trips. All bench calls blocked except Tier 3 Explicit Boss Rulings.
   - **100% Consumed (`EXHAUSTED`):** Bench seat automatically disables. Orchestrator seamlessly falls back exclusively to house seats.

---

### 7. Refusal: What I Refuse to Build

#### Refusal Item
I refuse to build an **Automatic Silent Failover Router** that reroutes failed persistent house seat queries to the Cursor bench when a house seat times out or degrades.

#### Architectural Rationale
1. **Uncontrolled Budget Drain:** A temporary API glitch or transient network timeout on a free house seat (e.g., persistent Gemini or Claude Code) would silently dump heavy traffic into the metered Cursor plan pool, draining monthly quota without user awareness.
2. **Lineage Safety Contamination:** Silent auto-rerouting risks breaking SPINE Law #1. If a house review call to Grok times out and silently auto-fails over to `cursor/claude-sonnet-5` while reviewing a Claude build, the system violates lineage independence without logging a warning.
3. **Violation of Shop Doctrine:** Silent budget consumption violates *"Nothing irreversible without the boss."* House seat failures must trigger transparent retry/fallback prompts to the user, never hidden metered spending.

---

### Summary & Sign-off

```
================================================================================
IF YOU ONLY ADOPT ONE THING, ADOPT THIS:
1. Index models by EFFECTIVE LINEAGE (not brand alias) in a lightweight 2.5KB 
   two-tier ledger so independence checks are instant and context-free.
2. Enforce a HARD ZERO-OVERAGE CIRCUIT BREAKER on the metered Cursor seat 
   to preserve the shop's flat-rate subscription doctrine.
3. Keep persistent house seats as 90%+ workhorses; restrict the 204-model bench 
   to 1M context intake, sub-5s scratch bursts, and non-Western review independence.
================================================================================
```

🟢 **Gemini 3.6 Flash** — *The Ledger Architect*
