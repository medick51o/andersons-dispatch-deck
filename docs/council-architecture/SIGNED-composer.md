Reading the document in full and following its instructions.
Exploring the codebase for concrete engineering details and gathering current pricing for the architecture comparison.
```
VERDICT
The leak is not fixed — only understood. The MCP guards are real engineering that earned its keep on the paths they cover, but they are a fence around 30% of the attack surface while cloud agents burned 67% of the pool through a lane that never touches them. Keep the subscription stack while the ~13x subsidy is measurable (docs/BASELINE-cursor-pro-20.md); delete ceremony, not the proven security code; plan for gradual subsidy decay, not a single cliff day.

Q1 LEAK FIXED?
  - No. Brief states "nothing has been changed yet except knowledge." Repo confirms guards live only in MCP stdio paths (mcp-seats/wmw_cursor_mcp.py, allowance.py, armcheck.py) — not in cloud-agent launch.
  - Repeat-prevention guard (enforceable): **hard block on cloud-agent launch until repo has (a) non-empty target tree, (b) MCP seats connected, (c) explicit model/effort/speed caps in the launch payload** — maxMode off, effort ≤ high, speed off, model = composer-2.5 or allowlisted equivalent. Must live in **the launch path Cursor controls** (cloud-agent API/UI defaults, org/account policy, or operator rule: zero cloud agents — local MCP only). Local cli-config.json is worthless here; incident doc confirms cloud agents "never read it" (docs/BASELINE-cursor-pro-20.md L219–221).
  - Secondary guard: **pre-flight spend gate on account meter** — refuse launch if cursor_models_percent_used > N% without operator typed confirmation. Must live in **account-level automation or human ritual**, not MCP Python; read-meters.py already reads the needle (mcp-seats/read-meters.py) but nothing blocks launch from it.
  - Other bypass lanes (same class of failure — local guards irrelevant):
    · Cursor IDE chat / Agent mode / Auto (79.8M "Cursor Models" tokens in baseline; cursor-grok-4.6-xhigh-fast = 51.9M, 21.8% of pool — docs/BASELINE-cursor-pro-20.md L13–14, L77–80)
    · Cloud agents (the actual leak)
    · Vendor CLIs invoked directly by human or orchestrator outside MCP (grok -p, codex exec, agy -p) — mcp-seats/README.md L99–100 lists these as legal fallback with no allowance check
    · Codex built-in MCP server (claude mcp add codex — mcp-seats/README.md L32–34) — no allowance.py, no armcheck coverage
    · Web/mobile Cursor dashboards, background/scheduled agents, future "team seat" sharing
    · xAI/Gemini/Anthropic native apps with their own agent modes
  - Failure mode nobody named: **failed-work multiplier** — burn scales with dispatch attempts, not shipped output. Eleven of thirteen agents produced zero lines into an empty repo (brief L45–46). The shop will burn fastest during the immature phase when guards matter most — a catch-22 where "learning the rig" is the most expensive activity.

Q2 EFFICIENCY
  - KEEP (earned, proven, not ceremony):
    · Prompt spill-to-file + strict model-id validation in wmw_cursor_mcp.py (674 lines — brief says ~400; cursor seat is heavier because fixes were reproduced live, L25–38)
    · MCPTool denial + deny-rules on Grok seat — live reproduction documented (wmw_grok_mcp.py L36–40)
    · allowance.py (140 lines) — credit-model gate on the one metered seat; enforced in wmw_cursor_mcp.py L381–394
    · read-meters.py — only way to size opaque pools (mcp-seats/read-meters.py L9–14); baseline math depends on it
    · armcheck.py (73 lines, 15 checks) — cheap regression suite; keep, maybe trim redundant startup checks later
    · DEFAULT_MODEL = "composer-2.5" non-fast — measured 3.6x cheaper than fast (docs/BASELINE-cursor-pro-20.md L72–75)
  - CUT (day-one engineer deletes):
    · **~900-line SPINE.md loaded every summon** (892 lines per repo) — split already exists (SPINE-PROVENANCE.md) but daily load is still a tax; operator card ≤100 lines, SPINE on demand only
    · **Triplicate MCP boilerplate** — grok 370 + gemini 317 + cursor 674 lines share identical JSON-RPC loops; extract ~120-line shared transport (mcp-seats/README.md itself says "bottom never changes" L86–87)
    · **calibrate-pool.py + bench-burn.py overlap** — one burn harness
    · **Council lock in cursor seat** (wmw_cursor_mcp.py L58–71) — didn't stop cloud agents; complexity without incident coverage
    · **mcp-seats/README.md vs SETUP.md duplication** — one install doc
    · **Codex wrapper fantasy** — Codex ships native MCP; no ~400-line Python seat exists here and doesn't need to (mcp-seats/README.md L32–34)
  - Where the waste is: engineering budget went to MCP-lane hardening while the burn came from an ungated IDE lane. ~1,400 lines of seat code protect orchestrator dispatch; $0 of code protects cloud-agent launch. The 900-line method doc optimizes agent behavior; it cannot enforce account spend.
  - Concrete ratio: armcheck validates MCP path; incident burn was 51.9M tokens of xhigh-fast (docs/BASELINE-cursor-pro-20.md) vs 5 MCP seat calls logged (L208). Guards are ~95% theater against last week's actual threat.

Q3 ARCHITECTURE
  - table:
    | option | monthly cost | what you get | what breaks it |
    |---|---:|---|---|
    | Status quo (subs) | ~$150–250/mo (brief L86) | Measured ~$800/mo Cursor model value on $60 Pro+ (docs/BASELINE-cursor-pro-20.md L257–258); ~$279/mo on old $20 Pro (L42); flat caps, no per-token anxiety | bonusSpend subsidy shrinks (read-meters.py L24, API field); TOS on automation; cloud-agent lanes ignore local guards; vendor reprice (Pro+ upgraded today) |
    | API router (OpenRouter-class) | ESTIMATE — see crossover below | Full model choice, no pool caps, programmable spend limits, guards you own | Hundreds of M tokens/mo at API rates; no subsidy; operator must learn API ops |
    | Rented GPU (RunPod/Lambda/Vast) | ESTIMATE $300–800/mo at 15–25% util | Open-weight models, data control | One-person shop idle ~20h/day; frontier open weights still below Claude/GPT/Grok for orchestration; ops burden on non-coder operator |
    | Owned hardware (e.g. RTX 4090 / multi-GPU) | ESTIMATE $1,600–4,000 capex + $40–80/mo power | Zero marginal per token at high util | Cannot run frontier closed models; 70B+ needs multi-GPU; 18–24mo obsolescence; break-even vs subs measured in years at this utilization |

  - crossover math (ESTIMATE — web pricing unavailable this session; arithmetic shown, sources flagged stale):
    · Measured subsidy ratio: $800 value / $60 paid ≈ **13.3x** (docs/BASELINE-cursor-pro-20.md L257–258). Stack at $200/mo buys roughly **$2,000–2,600/mo** of API-face-value if the same ratio held across seats — ESTIMATE extrapolation from Cursor measurement only.
    · API blended agentic rate: ESTIMATE **$4–6 per million tokens** (heavy tool-loop mix; frontier-class published API pricing typically $3–15/MTok input+output blended — stale, verify at openrouter.ai / vendor API pages).
    · Crossover (subs lose price advantage when subsidy → 1x):
      - At $200/mo budget, 1x face value → **33–50M tokens/mo** ($200 ÷ $4–6/MTok)
      - Shop's measured partial-cycle Cursor alone: **79.8M tokens** in days, not a month (docs/BASELINE-cursor-pro-20.md L13) → **already ~2–4x above naive crossover** on one seat
      - At **500M tokens/mo** (brief: "hundreds of millions"): API ESTIMATE **$2,000–3,000/mo** vs subs **~$200/mo** with subsidy → subs win by **10–15x** today
      - At **1B tokens/mo**: API ESTIMATE **$4,000–6,000/mo** vs subsidized subs ~$200 → subs win by **20–30x**; even at 1x subsidy, API ≈ **$4,000–6,000** vs ~$200–250 subs until caps throttle you
    · **Conclusion on crossover:** With measured 13x subsidy, API router does not beat subs on price at 100M, 500M, or 1B tokens/mo. Crossover only becomes real when bonusSpend → 0 AND caps bind — then this shop's volume is catastrophically expensive on API and catastrophically capped on subs. Pick your poison.

  - YOUR RECOMMENDATION: **Keep subscriptions while measured subsidy ≥ ~5x.** The arbitrage is real (documented), temporary (bonusSpend field), and at hundreds of M tokens/mo the API bill would be thousands (ESTIMATE above). Do NOT migrate to GPU/owned hardware — quality gap + ops burden for a non-coder orchestrator shop is disqualifying.
    · **Move first when subsidy dies:** Cursor bench → API router with hard monthly cap ($300–500) + cheapest included orchestrator sub, not GPU.
    · **Switching cost:** Low for orchestrator (swap MCP endpoint); high for habit — entire method assumes flat pools, hidden caps, and meter-by-percentage (MEASURING-POOLS.md pattern). Budget 2–4 weeks to re-derive cost model on per-token billing.
    · **Plan for "the week it ends":** It won't be a week. bonusSpend will **creep** (13.3x → 8x → 4x) while workflows stay maxed. Run read-meters.py weekly; track $/value ratio; pre-commit API cap account before ratio hits 3x.

BIGGEST RISK NOBODY NAMED
Gradual subsidy decay masked by pool-percent UI — operator optimizes for a 13x world that is silently becoming 3x, while cloud-agent and IDE lanes remain ungated. The bankruptcy is slow and looks like "Cursor got worse," not "architecture failed."

CONFIDENCE: medium — Q2 high (repo-inspected: line counts, guard locations, incident timeline in docs/BASELINE-cursor-pro-20.md). Q3 medium-low on dollar figures: Cursor measurements are sourced and current; API/GPU prices are ESTIMATE only (web search blocked this session). Would change mind if: (1) fresh OpenRouter/frontier API pricing shows blended <$2/MTok at this shop's actual input:output mix, (2) bonusSpend drops below 3x on next monthly read, (3) Cursor adds enforceable org policy on cloud-agent model tiers.
```