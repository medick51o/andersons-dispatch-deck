# SECURITY AUDIT — the harness, the MCP seats, and the canaries

You are one seat on a multi-vendor audit. Others are reading the same package independently
and are not told what you say. **This is an adversarial security review of code that is already
in production on one machine and published for others to install.** Findings that would let an
attacker or a careless operator cause real damage rank above everything else.

---

## What this system is

A one-person AI-orchestration shop. A human directs several AI models through a CLI
orchestrator (Claude Code). Each rival vendor is wired in as an **MCP stdio server** — a small
Python program speaking newline-delimited JSON-RPC 2.0 on stdin/stdout, which shells out to
that vendor's own CLI.

Everything bills flat-rate consumer subscriptions. **No API keys anywhere.** Credentials are
read at runtime from each vendor's own login file (`~/.grok/auth.json`, `%APPDATA%\Cursor\auth.json`);
none are stored by this code.

**The seats:**
- `wmw_grok_mcp.py` — xAI Grok Build CLI
- `wmw_gemini_mcp.py` — Google, via the Antigravity CLI (`agy`)
- `wmw_cursor_mcp.py` — the Cursor CLI, which fronts a pool of 200+ models, some free to the
  plan and some billing real credit. This one is the largest and the only one that can spend.

**The controls:**
- `allowance.py` — a recorded, bounded, expiring grant a metered seat must hold before spending
- `dispatch-guard.py` — preflight (refuse a dispatch with no destination), an ATOMIC
  reservation (concurrency cap), and a cost-per-accepted-change report
- `armcheck.py` — 17 canary checks that must pass before the rig is trusted
- `read-meters.py`, `calibrate-pool.py`, `bench-burn.py` — measurement

## The threat model this code was written against

The operator is a **non-coder**. The orchestrator is an LLM that can be steered by content it
reads. Untrusted text reaches these wrappers constantly — web pages, repo files, other models'
output. So a prompt is **hostile input**, not a string.

## What has ALREADY been found and fixed — verify these, do not merely re-report them

Three real vulnerabilities were reproduced on this machine and closed. **Your first job is to
confirm each fix actually holds, and to find the variant that was missed.**

1. **Command injection through the Windows CLI shim.** The Cursor CLI on Windows is a `.cmd`
   file that forwards its arguments to PowerShell. A crafted prompt containing shell
   metacharacters executed a host command and wrote a file. *Fix:* no caller-controlled string
   ever reaches argv. Prompts are spilled to a file and referenced by a generated ASCII-only
   pointer; model ids must match a strict pattern; session ids must be UUIDs.

2. **A "read-only" mode that was not read-only.** The wrapper passed `--trust`, believing it
   restricted the agent. `--trust` *authorises* a workspace; it does not restrict. A read-only
   call wrote an 11.7KB file. *Fix:* `--mode ask` for the Cursor seat, explicit deny-rules for
   the Grok seat, `--mode plan` for Gemini.

3. **Privilege escalation between seats.** A read-only Grok seat wrote a file **through the
   Codex MCP seat** — it could not write itself, so it asked a neighbour. *Fix:* `MCPTool` added
   to the deny list, plus `--disallowed-tools Agent`, after `--no-subagents` was proven to be a
   no-op that still permitted a spawn.

## YOUR JOB

**Q1. Do those three fixes actually hold?** Read the code, not the description. For each, name
the bypass that still works, or state plainly that it is closed and why.

**Q2. What else is broken?** Everything is in scope: argument construction, path handling and
the `cwd` allow/deny logic, the JSON-RPC parse loop, the atomic lock and its stale-reclaim,
the allowance and reservation stores (they live in the user's home directory as plain JSON —
who else can write them?), TOCTOU races, symlink and junction handling, resource exhaustion,
error paths that leak, and anything that fails OPEN rather than closed.

**Q3. Are the canaries real?** `armcheck.py` claims 17 passing checks and is the thing that says
"ALL ARMED." A test suite that cannot fail is a prayer with a green checkmark.
- Which checks would still pass if the guard they cover were deleted?
- What is NOT covered at all?
- Could the arm test itself be made to pass while the rig is unsafe?

**Q4. The honest scope question.** These controls bind dispatches that pass through them.
Cloud agents, IDE agent modes, web dashboards and CI execute on the vendor's infrastructure and
never touch this code. Given that, **is this harness worth its complexity, or does it provide
false assurance?** Say so plainly if you think it does.

## Rules

- **Quote the exact line or function** you are attacking. An unanchored finding is unusable.
- Rank by real-world impact: what an attacker or a careless operator actually achieves.
- Distinguish **CONFIRMED** (you can trace the failing path in the code) from **SUSPECTED**.
- Say when something is well-built. A review with no positives is not credible.
- Do not write any file. Report only.

## Output format

```
VERDICT (3 sentences)

Q1 THE THREE FIXES
  1. injection      HOLDS / BROKEN + the exact bypass
  2. read-only      HOLDS / BROKEN + the exact bypass
  3. escalation     HOLDS / BROKEN + the exact bypass

Q2 NEW FINDINGS  (ranked; SEVERITY / file:line or function / attack / fix)
Q3 CANARY AUDIT  (which checks are real, which are theatre, what is uncovered)
Q4 IS IT WORTH IT
WHAT IS WELL BUILT
CONFIDENCE + what would change your mind
```
