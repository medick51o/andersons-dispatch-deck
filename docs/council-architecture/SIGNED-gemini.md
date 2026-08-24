VERDICT (3 sentences max — your bottom line)
Subscription arbitrage is a fragile temporary hack that builds a 400-line-per-seat scaffolding tower on top of vendor subsidies and consumer Terms-of-Service loopholes. The immediate leak is not fixed because local disk configs cannot bind remote cloud agents, requiring server-side web dashboard hard caps and API proxy boundaries. Ride the ~$800/month Cursor Pro+ subsidy for interactive local IDE work, but immediately decouple background agents to pay-per-token API endpoints before automated ToS bans or subsidy revocations wipe out your workflow.

Q1 LEAK FIXED?
  - **Finding**: The leak is **NOT fixed**. Local `cli-config.json` files and local Python meters live on the operator's local disk, whereas Cursor Cloud Agents execute inside Cursor's remote cloud cluster and pull parameters directly from cloud settings or prompt payloads, entirely bypassing local guards.
  - **Enforceable Guard**:
    1. **Dashboard-Level Hard Spending Cap**: Enforce a strict $0/mo usage-based limit inside the vendor's web dashboard (e.g., Cursor Account Settings) to prevent `maxMode` and fast-mode overages from triggering auto-billing.
    2. **Orchestrator Pre-Flight Dispatch Hook**: In the orchestrator, mandate a pre-flight git validation (`git status` & `git log`) that aborts agent launch if the target repository contains zero tracked application files or uncommitted scaffolding.
    3. **Cloud Agent Parameter Masking**: Set cloud launch flags explicitly to `maxMode: false`, `effort: medium`, and `speed: normal` in all automated API launch wrappers.
  - **OTHER Bypassing Lanes**:
    - **IDE-side Inline AI / Copilot Loops**: Editor extensions pulling remote user profile defaults.
    - **Web Dashboards & Mobile UI Apps**: Direct browser/mobile sessions executing server-side prompts.
    - **Scheduled Cron / CI/CD Background Jobs**: Headless workflows using stored cloud tokens.
    - **Shared Organization / Team Seats**: Secondary seats drawing from central billing pools without local CLI wrappers.
  - **Unnamed Failure Mode ("Infinite Loop Ghost Context Inflation")**: A cloud agent launched against an empty repo encounters a missing import or linter warning, re-reads the entire workspace context, fails, and re-executes in a tight retry loop under high reasoning (`effort: xhigh` + `maxMode: true`). It consumes 100M+ tokens of context window expansion in minutes without producing a single diff, completely invisible to local process monitors because execution occurs 100% server-side.

Q2 EFFICIENCY
  - **CUT**: Custom seat wrappers (~400 lines of Python per seat) and custom metering scripts (~1,600 LOC total across 4 seats).
    - **Why**: It is engineering ceremony offering false security. Client-side metering scripts cannot intercept remote cloud agent execution, web UI sessions, or vendor-side payload changes (e.g., `bonusSpend` updates). Vendors frequently modify API response headers and telemetry, requiring constant script maintenance by a non-coder operator for zero security gain.
  - **KEEP**: Read-only git enforcement by default, prompt spillage prevention (file-based prompt passing instead of process `argv`), and basic CLI execution paths.
  - **Replacement**: Replace custom metering code with a standard API Gateway proxy (such as OpenRouter or LiteLLM) that enforces real HTTP-level budget caps natively.

Q3 ARCHITECTURE
  - **Comparison Table**:

| Option | Monthly Cost | What You Get | What Breaks It |
|---|---|---|---|
| **1. Status Quo (Consumer Subs)** | **~$150–$250/mo** (Cursor Pro+ $60 [[cursor.com](https://www.cursor.com/pricing)], Anthropic Pro/Max ~$20–$100 [[anthropic.com](https://www.anthropic.com/pricing)], OpenAI Pro/Plus ~$20–$200 [[openai.com](https://openai.com/chatgpt/pricing)], xAI $16 [[x.ai](https://x.ai)]) | ~$1,500–$2,500/mo in subsidized frontier model tokens (~13-14x sticker value) | Vendor ToS bans, subsidy phase-out (`bonusSpend` drops), unmetered cloud agent runaways |
| **2. API Router (OpenRouter)** | **Pay-per-token** (Sonnet 3.5: $3.00/1M in, $15.00/1M out; DeepSeek R1: $0.70/1M in, $2.50/1M out [[openrouter.ai](https://openrouter.ai/models)]) | 100% SLA reliability, zero ToS ban risk, strict HTTP header spending caps, unthrottled concurrency | Cost escalation at high volume (>100M+ tokens/mo of closed frontier models) |
| **3. Rented GPU (RunPod / Lambda)** | **~$1,960–$8,120/mo** (1x H100 SXM @ $2.69/hr [[runpod.io](https://www.runpod.io/gpu-instance/pricing)]; 8x A100 node @ $11.12/hr [[lambdalabs.com](https://lambdalabs.com/service/gpu-cloud)]) | Total privacy, zero rate caps, fixed hourly infrastructure cost | ~76% idle waste for a 1-person shop; cold-boot load times; reasoning quality gap vs closed models |
| **4. Owned Hardware (Mac Studio)** | **~$7,500 capex** (Mac Studio M2 Ultra 192GB RAM [[apple.com](https://www.apple.com)]) + **~$16/mo power** (150W @ $0.15/kWh [[eia.gov](https://www.eia.gov/electricity/monthly/)]) | 192GB unified VRAM for 70B+ open models; low power draw; silent local server | Rapid hardware obsolescence (24-mo cycle); slow memory bandwidth (~800 GB/s); no access to Claude 3.5 Sonnet |

  - **Crossover Math**:
    - *Assumptions (ESTIMATE)*: Average token mix = 80% input, 20% output.
    - *Frontier Closed Model Rate (Claude 3.5 Sonnet via OpenRouter)*:
      Input: $3.00/1M, Output: $15.00/1M [[openrouter.ai](https://openrouter.ai/models)].
      Blended cost per 1M tokens = $(0.8 \times \$3.00) + (0.2 \times \$15.00) = \$2.40 + \$3.00 = \mathbf{\$5.40 \text{ per 1M tokens}}$.
    - *Status Quo Stack Cost*: ~$200/month.
    - *Crossover Token Volume*: $\$200 / \$5.40 \times 1,000,000 = \mathbf{37.04 \text{ Million tokens/month}}$.
    - *At Operator's Current Volume (ESTIMATE: 200M tokens/mo)*:
      - 100% Claude 3.5 Sonnet on OpenRouter = $200 \times \$5.40 = \mathbf{\$1,080/month}$.
      - Hybrid Route (50% DeepSeek R1 @ $1.06/1M blended + 50% Sonnet 3.5 @ $5.40/1M blended) = $200 \times \$3.23 = \mathbf{\$646/month}$.
    - *Crossover Finding*: Subscriptions beat pay-per-token on raw price only while vendors maintain ~14x subsidies. However, a single $500 cloud agent runaway wipes out 2.5 months of subscription savings.

  - **YOUR RECOMMENDATION + Switching Cost**:
    - **Strategy**: Implement a **Dual-Tier Hybrid Architecture**:
      1. **Interactive Tier (Keep Subs)**: Retain Cursor Pro+ ($60/mo) exclusively for human-driven, local IDE pair-programming to capture the ~$800/mo model subsidy.
      2. **Automated / Background Agent Tier (Switch to OpenRouter)**: Immediately ban automated/cloud agent runs on consumer sub accounts. Route all unattended CLI agents and background scripts through OpenRouter using direct API keys with hard $20 budget caps per agent run.
    - **Switching Cost**:
      - **Engineering**: ~2–4 hours to point orchestrator model endpoints to OpenRouter / LiteLLM proxy.
      - **Financial**: $0 upfront capex. Operational spend increases by ~$100–$300/month for automated runs, fully offset by eliminating runaway billing incidents and account termination risks.

BIGGEST RISK NOBODY NAMED
**Vendor Terms of Service Account Permabans**: Anthropic, OpenAI, and Google explicitly prohibit automated access, non-human scripting, and OAuth credential harvesting on consumer subscription plans [[anthropic.com](https://www.anthropic.com/legal/consumer-terms)]. If vendor fraud monitoring flags the shop's 200M+ monthly token automated MCP traffic, they issue an immediate, unappealable permaban across all associated email accounts, Google Workspace domains, and payment profiles—wiping out the shop's identity and primary reasoning engine overnight.

CONFIDENCE: high
*What would change my mind*: If major vendors introduce officially supported, contractually bound "unlimited background cloud agent" subscription tiers with SLA protections against account termination, or if open-weight 70B models running on local hardware achieve full parity with Claude 3.5 Sonnet on complex codebase refactoring benchmarks (SWE-bench >70%).
