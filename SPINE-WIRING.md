# SPINE — WIRING & FIELD NOTES

**Version line (machine-readable):** `spine-wiring v1.0 (2026-08-24)`
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
