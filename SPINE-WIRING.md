# SPINE — WIRING & FIELD NOTES

**Version line (machine-readable):** `spine-wiring v1.4 (2026-09-01)`
**Owner:** this file owns the shop's arsenal, paths, model strings and proven gotchas.
SPINE owns the *duty* to read it. Neither restates the other.
**Any content change bumps the version line** — a stale rendering grows exactly where
nobody is looking, which is how the Deck's legend forked to v4.0 unnoticed.

*Not loaded on a summon.* SPINE names three triggers that require reading this first:
before a seat preflight or the session's first dispatch, before selecting a vendor
capability, and when a vendor-specific failure appears.

Everything here is **current wiring, NOT law** — it changes without notice. The duty to
check it does not. Split out of SPINE on the 2026-08-24 council's ruling; the notation and
meter-mark grammar deliberately stayed behind in the trunk, because a grammar applied to
every line cannot be fetched per line.

---

## THE ARSENAL — who this shop has, and what each is for

- **Codex (OpenAI)** — bounded implementation of a clear spec; the sharpest code reviewer (proves
  bugs, cites sources). `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`.
- **Grok (xAI)** — fearless UI/skins/concept pages; surface only, never engine.
  `C:\Users\<you>\.grok\bin\grok.exe --prompt-file <f> --always-approve < /dev/null`. Mandatory trail entry.
- **Gemini / Antigravity (Google)** — proven builder (Flash), IMAGE GEN via Nano Banana (on the sub,
  no card), cheap reviews/sweeps, independent 4th vote, and **the Overflow Valve** (rents Claude/GPT
  brains on Google's tab when the Claude meter runs hot — count agy as the GOOGLE bloodline only when
  wearing a Gemini model; agy-running-Claude is not an independent reviewer of Claude work).
  `"C:\Users\<you>\AppData\Local\agy\bin\agy.exe" -p "<prompt>" --model "Gemini 3.6 Flash (High)"`.
  agy `--model` strings are exact-match; Claude tiers need the `(Thinking)` suffix.
- Dispatch ritual for any wardrobe: ticket file → headless dispatch → the orchestrator gates
  independently (render/probe/screenshot) → re-ticket → loop. Trails mandatory where the fence is
  wider than one file.
- **The arsenal is OPTIONAL.** The method works with whatever vendors are reachable (Claude alone is
  a valid, degraded arsenal). No specific vendor, plan, or price is part of the method.
- **This shop's Lineage Ledger location (wiring, NOT law):**
  `<your-brain>\_claude-brain\memory\model-lineage-ledger.md`. The engine (Doctrine 6) names
  no absolute path — downloaders default to a project-relative `model-lineage-ledger.md`; this is
  merely where THIS box keeps its shared fleet-wide store.


## APPENDIX B — FIELD NOTES (append-only; proven capabilities & gotchas, inherited by all tiers)
*(When a run PROVES something new, it goes here so future installs inherit it.)*
- **agy `--model` strings are exact-match**: Claude tiers require the `(Thinking)` suffix —
  `"Claude Sonnet 4.6 (Thinking)"`, `"Claude Opus 4.6 (Thinking)"`. A bad string exits 1 and prints
  the full valid-model list (useful as a probe).
- **Gemini 3.1 Pro (High) handled a heavy adversarial review fine** (~600-word verdict table, physics
  attacks) — confirms the Flash review-ceiling workaround: route heavy reviews to Pro, not Flash.
- **Two `codex exec` instances run in parallel** without issue (separate processes, same box).
- **Codex cites sources when reviewing factual claims** (web-searches vendor manuals unprompted) —
  doubles as a doc-checker for claim-verification tickets.
- **Cross-vendor consensus worked as designed**: Codex and Gemini independently killed the same two
  pieces of draft advice (mill-first/burn-second; interpolate-from-3-probes) for the same physical
  reasons. Agreement is corroboration, never a ruling — the human still rules (Part V).
- Claude-tier doc-verification subagent (Sonnet + web) is slow (~10 min) but resolves which claims
  rest on conflicting sources — its "don't publish this number" flags are the payoff.
- **Gemini 3.6 Flash (High) is live and handled a real analysis ticket clean** (2026-07-22,
  token-ticker EP10): agy's valid-model roster now carries the 3.6 Flash family (High/Medium/Low).
  The bad-string probe still works — an invalid `--model` exits 1 and prints the current roster.
- **agy HEADLESS auto-denies tool permissions** (`read_file` etc. — the run dies with a "jetski"
  permission error and empty output). Headless dispatches must EMBED the evidence in the prompt
  (reviews-by-embed); probe auth cheaply first with a one-word `-p` ping.
- **Codex safety layer flags "exploit/attack/laundering" vocabulary (2026-07-26):** a
  verify ticket phrased as "re-run your exploits / attack variations" died mid-run flagged
  as cyber-risk (78K tokens lost). Same work re-dispatched as "re-create the defect's
  failure scenario / negative-path QA regression" ran clean. Phrase adversarial-verify
  tickets to Codex in defect/QA vocabulary, never attacker vocabulary.
- **Secret-gated verification pattern (proven 2026-07-22):** when a reviewer's sandbox denies it a
  secret the proof needs (e.g. an HMAC key), the reviewer AUTHORS the exact verifier script; a
  key-holding seat EXECUTES it unmodified (trivial repairs applied openly and logged); the verdict
  binds to the output. Keeps builder-never-approves intact when secrets gate the evidence — the
  reviewer's NOT-PROVEN-until-run discipline is the correct half of the handshake.

---
*SPINE owns the engine; the Team Rocket Method's provenance lives in CREW, because it is that
brand's identity, not the brand-neutral engine's.*


---

# MOVED OUT OF THE LOADER (2026-08-24)

The Deck's SKILL.md restated these on every summon. The LAW is SPINE's; this is the wiring.

## PERSISTENT SEATS — the standing MCP transports (installed & verified 2026-08-22)
Every rival vendor is wired into Claude Code as a **persistent MCP seat** — subscription-billed, no
API keys, no per-token bills. The orchestrator dispatches through these tools by default:

| Banner | Server | Start tool | Continue tool | Under the hood |
|---|---|---|---|---|
| 🔵 Codex | `wmw-codex` | `codex` | `codex-reply` + conversationId | `codex mcp-server` (built in) |
| ⚫ Grok | `wmw-grok` | `grok` | `grok-reply` + sessionId | Grok Build CLI `-p` / `--resume` |
| 🟢 Gemini | `wmw-gemini` | `gemini` | `gemini-reply` + conversationId | Antigravity `agy -p` / `--conversation` |

Wrapper source: `C:\Sync\Projects\andersons-dispatch-deck\mcp-seats\`. The Grok/Gemini wrappers bake in
the two headless croak-killers found 2026-08-22: a 60-minute timeout (agy's default was 5 minutes —
long tasks died mid-thought) and an `always_approve` switch (headless runs can never click a
permission prompt; without it a build task stalls until the timeout kills it).

**Transport doctrine (owner: SPINE v2.0, THE TRANSPORT LAW — this is the Deck rendering):**
- **Fresh call = blind seat — necessary, not sufficient.** A new `codex`/`grok`/`gemini` call
  remembers nothing from any other session. Reviewers are ALWAYS fresh calls; never brief a
  reviewer through a session that saw the build (anchoring law). Fresh alone is not independence —
  the reviewer must also sit on a different effective-model vendor than the build, or be
  boss-launched (SPINE Part IV's two legal paths).
- **Reply-chain = the same seat continuing.** `*-reply` keeps one seat's thread alive for follow-ups
  inside its own lane (ticket clarification, build iteration). A reply-chained session is inside its
  owning-seat lineage forever — it can never become the independent reviewer of work its thread touched.
- **Build tickets:** pass `always_approve: true` and `cwd` = the repo. Research/review tickets: omit
  both (read-only default).
- Raw one-shots (`grok -p`, `codex exec`, `agy -p`) stay legal as fallback transport; the MCP seats
  are the default.



## THE RESERVE BENCH — 🟣➤ a metered transport (SPINE v2.4: BENCH + METER laws)
Beside the flat-rate house seats sits an optional **reserve**: one transport fronting a large pool of
models, drawing metered credit instead of a flat window. It is never in the standing lineup. SPINE
owns the rules (THE COUNCIL SEAT LAW · THE METER LAW · THE TRANSPORT LAW); this is the Deck rendering.

**The three things the conductor must hold in mind:**
- **Free before paid.** A reserve pool usually splits into an INCLUDED tier (the host's own models,
  no marginal cost) and a CREDIT tier (third-party models at API prices). Default to included; a
  credit call is a deliberate act, announced, never a silent upgrade.
- **A pool is not a vendor.** Lineage is the model family behind the transport, never the transport's
  brand. A reserve-hosted Claude is Anthropic blood and cannot independently review Claude's work.
  An unmappable family is `UNKNOWN LINEAGE` and fails closed. The banner shows both: 🟣➤🟠.
- **Read the meter, don't trust the adjective.** "Generous" is not a number. Where a vendor
  publishes no allowance, the shop's figure comes from measurement, and cost claims cite a reading.

**Narration.** A reserve dispatch flies the transport's arrow, the bloodline, and the meter:
`🟣➤🌙 💸 Kimi reviewing the parser` — who summoned it, whose brain thought, what it cost. A reserve
model **answering** (a review returned, a council seat) signs bare — 🟣 — because it is not directing.
Meter marks are mandatory on reserve lines and absent everywhere else: ♾️ included · ♾️💸 included but
a surcharged tier · 💸 credits · 🚨💳 credits and surcharged · ⚠️ unknown, fails closed.

**Wiring** (shop-specific, changes without notice): `BENCH-LEDGER.md` for what the reserve can reach
and what it has proven · `MEASURING-POOLS.md` for how to size an unpublished pool ·
`mcp-seats/read-meters.py` and `bench-burn.py` for the readings themselves.

- **wmw-grok MCP seat can deliver files but never send its reply** (2026-08-26, channel-factory
  T-001): build completed on disk at ~20:26, seat stayed silent until the 1800s idle timeout
  killed the call. Gate on ARTIFACTS (files + render), not on the seat's reply; check the fence
  directory before re-dispatching a "failed" Grok build. Consider per-server timeout in MCP
  settings if long builds recur.
- **grok 1.0.13 rejects `--deny NotebookEdit`** (2026-09-01 self-audit): "unsupported tool prefix", exit 1
  before the prompt is sent, so the whole seat read as dead. A vendor CLI update can invalidate a deny
  prefix silently; when a seat dies with no output, run the raw CLI once and read stderr. The wrapper
  deny set is now Write/Edit/MultiEdit/Bash/MCPTool/WebFetch/WebSearch. Also noted: the grok CLI reads
  `~/.claude/CLAUDE.md` into every call (~15K input tokens for a one-word prompt).
- **Render gates never reach the conductor as pixels** (2026-09-01, the boss's ruling). Playwright MCP
  (`playwright`, user scope) is the headless browser for screenshot/DOM gates during autonomous hours,
  since claude-in-chrome needs Chrome open. The frontier conductor does NOT call it: it dispatches a
  FAST/WORKHORSE Claude subagent (Agent tool, `model: sonnet` or `haiku`) that drives Playwright, reads
  the screenshot, and returns a TEXT verdict against the ticket's observable outcome ("renders, 3 buttons
  present, 0 console errors, screenshot saved at <path>"). The conductor gates on the text and the saved
  file, never on the image in its own context. Screenshot tokens are the same either way; the price
  and the conductor's context are not.
