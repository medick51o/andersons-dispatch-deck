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

---

# THE SOURCE UNDER AUDIT

## ===== wmw_cursor_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-cursor — MCP stdio server wrapping the Cursor Agent CLI. v2.0
     3	
     4	A persistent seat on the Cursor model pool:
     5	  cursor(prompt, ...)          start a new conversation -> reply + sessionId
     6	  cursor-reply(sessionId, ...) continue that conversation with full context
     7	
     8	⚠ THE ONE METERED SEAT. Every other seat in this shop rides a flat subscription
     9	at $0 marginal. This one draws Cursor's pools, and there are TWO of them:
    10	
    11	  ♾️ INCLUDED  "Cursor Models" — composer-*, cursor-grok-*. Cursor's own models,
    12	               generous included usage on a Pro plan. The pool you vibe-code with.
    13	  💸 CREDITS   "Other Models" — claude-*, gpt-*, gemini-*, kimi-*, glm-*, billed
    14	               at API prices (~$20/month included, then pay-as-you-go).
    15	  ⚠️ UNKNOWN   Anything unrecognised, incl. `auto`. Refused unconditionally.
    16	
    17	"Fast" tiers are a surcharge, not a convenience: Composer 2.5 goes $0.5/$2.5 ->
    18	$3/$15 per million (6x output); Cursor Grok 4.6 doubles. Their own louder class.
    19	
    20	THE PLAYPEN. Cursor gets a directory of its own to work in, so scratch files,
    21	prompt handoffs and temp work never land in a real project and never block a
    22	run. Everything the seat needs to write, it writes there. Override with
    23	WMW_CURSOR_PLAYPEN.
    24	
    25	SECURITY (v2.0 — after a live command-injection reproduction on this machine):
    26	The Windows Cursor CLI is a .cmd shim that forwards its arguments to PowerShell,
    27	so a prompt containing shell metacharacters could execute host commands. Proven,
    28	not theoretical: a crafted prompt wrote a file. Therefore NO caller-controlled
    29	string is ever placed on the command line. Prompts are always spilled to a file
    30	in the playpen and referenced by a generated ASCII pointer; model ids must match
    31	a strict identifier pattern; session ids must be UUIDs; cwd is passed to the OS
    32	as a working directory, never as an argument.
    33	
    34	Read-only is REAL and canary-verified: without always_approve the CLI runs with
    35	`--mode ask`, its own read-only mode. (v1.0 used `--trust` alone, which
    36	AUTHORISES a workspace rather than restricting it, and a "read-only" call wrote
    37	a file straight through it.) `always_approve: true` passes --yolo and REQUIRES an
    38	explicit cwd, which may not be a home, system or credential directory.
    39	
    40	Requires Python 3.10+ and a logged-in Cursor CLI (`cursor-agent login`).
    41	Known limitation: one request at a time; no cancellation mid-run.
    42	"""
    43	import datetime
    44	import io
    45	import json
    46	import os
    47	import re
    48	import shutil
    49	import subprocess
    50	import sys
    51	import tempfile
    52	
    53	CURSOR_TIMEOUT_S = 3600
    54	MAX_REPLY_CHARS = 400_000
    55	DEFAULT_MODEL = "composer-2.5"   # NON-fast on purpose: fast tiers are a surcharge
    56	
    57	# ---------------------------------------------------------------------------
    58	# THE COUNCIL LOCK (boss ruling 2026-08-23, revisitable).
    59	# A COUNCIL runs on SUBSCRIPTION seats only — house Claude / Codex / Grok /
    60	# Gemini. Never on the Cursor pool. One cheap Cursor review is fine; a fan-out of
    61	# several metered seats answering the same brief is not, and that is exactly the
    62	# shape that quietly drains a pool.
    63	#
    64	# Enforced, not merely written down: at most COUNCIL_LOCK_MAX billable calls in
    65	# any COUNCIL_LOCK_WINDOW_S seconds. A normal review sails through; a 4-seat
    66	# metered council trips the wire and is refused.
    67	# Lift deliberately with WMW_CURSOR_COUNCIL_LOCK=off (and say so to the boss).
    68	# ---------------------------------------------------------------------------
    69	COUNCIL_LOCK_MAX = int(os.environ.get("WMW_CURSOR_COUNCIL_MAX", "2"))
    70	COUNCIL_LOCK_WINDOW_S = int(os.environ.get("WMW_CURSOR_COUNCIL_WINDOW", "600"))
    71	COUNCIL_LOCK_ON = os.environ.get("WMW_CURSOR_COUNCIL_LOCK", "on").lower() != "off"
    72	
    73	# ---------------------------------------------------------------------------
    74	# THE PLAYPEN — Cursor's own corner of the disk.
    75	# ---------------------------------------------------------------------------
    76	PLAYPEN = os.path.abspath(os.environ.get(
    77	    "WMW_CURSOR_PLAYPEN", os.path.join("C:" + os.sep, "Sync", "_playpen", "cursor")))
    78	PROMPTS_DIR = os.path.join(PLAYPEN, "prompts")
    79	SPEND_LEDGER = os.environ.get("WMW_CURSOR_LEDGER", os.path.join(PLAYPEN, "bench-spend.jsonl"))
    80	
    81	def _ensure_playpen():
    82	    """Create the playpen on demand. Never let this break a call."""
    83	    for d in (PLAYPEN, PROMPTS_DIR, os.path.join(PLAYPEN, "scratch")):
    84	        try:
    85	            os.makedirs(d, exist_ok=True)
    86	        except OSError:
    87	            return False
    88	    readme = os.path.join(PLAYPEN, "README.md")
    89	    if not os.path.exists(readme):
    90	        try:
    91	            with io.open(readme, "w", encoding="utf-8", newline="") as f:
    92	                f.write(
    93	                    "# Cursor's playpen\n\n"
    94	                    "Scratch space for the `wmw-cursor` MCP seat. The seat writes prompt\n"
    95	                    "handoffs (`prompts/`), scratch work (`scratch/`) and its spend ledger\n"
    96	                    "here so none of that lands in a real project.\n\n"
    97	                    "Safe to delete when nothing is running; it is recreated on demand.\n")
    98	        except OSError:
    99	            pass
   100	    return True
   101	
   102	# ---------------------------------------------------------------------------
   103	# METER CLASSES (verified against Cursor's published pricing, 2026-08-23)
   104	# ---------------------------------------------------------------------------
   105	INCLUDED_PREFIXES = ("composer-", "cursor-grok-")
   106	CREDIT_PREFIXES = ("claude-", "gpt-", "gemini-", "kimi-", "glm-")
   107	
   108	# ---------------------------------------------------------------------------
   109	# THE YOLO ALLOWLIST (boss ruling 2026-08-23).
   110	# Only these families may run write-capable (--yolo). They are the two FREE,
   111	# trusted seats: Composer and Cursor Grok. Everything else in the pool -- the
   112	# Codex/Gemini/Claude mirrors, Kimi, GLM -- may read and advise, never write or
   113	# execute, however the call is phrased.
   114	#
   115	# The boss's stated path: open cursor-codex and cursor-gemini next if this works
   116	# out; Kimi and other foreign-lab models are explicitly NOT candidates today.
   117	# Widening this tuple is the whole change -- keep it a deliberate, visible act.
   118	# ---------------------------------------------------------------------------
   119	YOLO_ALLOWLIST = ("composer-", "cursor-grok-")
   120	
   121	def yolo_allowed(model_id):
   122	    return (model_id or "").strip().lower().startswith(YOLO_ALLOWLIST)
   123	
   124	# A model id may only ever be a plain identifier. Anything else cannot reach argv.
   125	_MODEL_RE = re.compile(r"\A[a-z0-9][a-z0-9._-]{0,63}\Z")
   126	_UUID_RE = re.compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
   127	                      r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")
   128	
   129	def meter_class(model_id):
   130	    m = (model_id or "").strip().lower()
   131	    if not m or m == "auto" or not _MODEL_RE.match(m):
   132	        return "UNKNOWN"
   133	    fast = m.endswith("-fast")
   134	    if m.startswith(INCLUDED_PREFIXES):
   135	        return "INCLUDED-FAST" if fast else "INCLUDED"
   136	    if m.startswith(CREDIT_PREFIXES):
   137	        return "CREDITS-FAST" if fast else "CREDITS"
   138	    return "UNKNOWN"
   139	
   140	METER_MARK = {"INCLUDED": "♾️", "INCLUDED-FAST": "♾️💸",
   141	              "CREDITS": "💸", "CREDITS-FAST": "🚨💳", "UNKNOWN": "⚠️"}
   142	
   143	# THE CURSOR BANNER. The arrow is a CURSOR — its birthplace; the conductor's 🟡➤
   144	# baton is the borrowed cousin. Every line this seat produces flies 🟣➤.
   145	CURSOR_BANNER = "🟣➤"
   146	
   147	BLOODLINE_MARK = {
   148	    "Moonshot": "🌙",   # Kimi — Moonshot AI, literally the moon
   149	    "Zhipu": "🔷",      # GLM
   150	    "Cursor": "🎼",     # Composer — a composer writes the score
   151	    "Anthropic": "🟠", "OpenAI": "🔵", "xAI": "⚫", "Google": "🟢",
   152	    "UNKNOWN": "❓",
   153	}
   154	
   155	def _lineage(model_id):
   156	    m = (model_id or "").lower()
   157	    for pre, vendor in (("claude-", "Anthropic"), ("gpt-", "OpenAI"),
   158	                        ("cursor-grok-", "xAI"), ("gemini-", "Google"),
   159	                        ("kimi-", "Moonshot"), ("glm-", "Zhipu"),
   160	                        ("composer-", "Cursor")):
   161	        if m.startswith(pre):
   162	            return vendor
   163	    return "UNKNOWN"
   164	
   165	def _log_spend(model, lineage, klass, usage, sid, ok, write_capable):
   166	    """One append-only row per LAUNCHED call, success or not. Never breaks a call."""
   167	    try:
   168	        _ensure_playpen()
   169	        row = {
   170	            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
   171	            "model": model, "lineage": lineage, "meter": klass,
   172	            "billable": bool(klass and klass.startswith("CREDITS")),
   173	            "surcharged": bool(klass and klass.endswith("FAST")),
   174	            "in": (usage or {}).get("inputTokens"),
   175	            "out": (usage or {}).get("outputTokens"),
   176	            "cache_read": (usage or {}).get("cacheReadTokens"),
   177	            "session": sid, "ok": ok, "write_capable": write_capable,
   178	        }
   179	        with io.open(SPEND_LEDGER, "a", encoding="utf-8", newline="") as f:
   180	            f.write(json.dumps(row) + "\n")
   181	    except Exception as e:
   182	        print(f"[wmw-cursor] spend-ledger write failed: {e}", file=sys.stderr)
   183	
   184	def _allowance(seat):
   185	    """Ask the operator's allowance record whether this seat may spend.
   186	
   187	    The record lives on the operator's own machine, never in the repo. Absent or
   188	    expired means NO -- a metered seat asks before it spends, every time, until a
   189	    bounded grant exists. See mcp-seats/allowance.py.
   190	    """
   191	    try:
   192	        import importlib.util
   193	        spec = importlib.util.spec_from_file_location(
   194	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowance.py"))
   195	        mod = importlib.util.module_from_spec(spec)
   196	        spec.loader.exec_module(mod)
   197	        return mod.status(seat)
   198	    except Exception as e:
   199	        return False, f"the allowance record could not be read ({e}); failing closed"
   200	
   201	def _allowance_calls(seat, fallback):
   202	    """The granted call bound, so the rolling cap enforces the operator's number."""
   203	    try:
   204	        import importlib.util
   205	        spec = importlib.util.spec_from_file_location(
   206	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowance.py"))
   207	        mod = importlib.util.module_from_spec(spec)
   208	        spec.loader.exec_module(mod)
   209	        g = mod._load().get(seat) or {}
   210	        return int(g.get("calls", fallback))
   211	    except Exception:
   212	        return fallback
   213	
   214	def _guard():
   215	    """Load dispatch-guard, the council's controls. None if unavailable."""
   216	    try:
   217	        import importlib.util
   218	        spec = importlib.util.spec_from_file_location(
   219	            "_guard_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   220	                                       "dispatch-guard.py"))
   221	        mod = importlib.util.module_from_spec(spec)
   222	        spec.loader.exec_module(mod)
   223	        return mod
   224	    except Exception as e:
   225	        print(f"[wmw-cursor] dispatch-guard unavailable: {e}", file=sys.stderr)
   226	        return None
   227	
   228	def _recent_billable(window_s):
   229	    """How many billable calls landed in the last window_s seconds, per the ledger."""
   230	    if not os.path.exists(SPEND_LEDGER):
   231	        return 0
   232	    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=window_s)
   233	    n = 0
   234	    try:
   235	        for line in io.open(SPEND_LEDGER, encoding="utf-8"):
   236	            line = line.strip()
   237	            if not line:
   238	                continue
   239	            try:
   240	                r = json.loads(line)
   241	            except json.JSONDecodeError:
   242	                continue
   243	            if not r.get("billable"):
   244	                continue
   245	            try:
   246	                ts = datetime.datetime.fromisoformat(r.get("ts", ""))
   247	            except ValueError:
   248	                continue
   249	            if ts >= cutoff:
   250	                n += 1
   251	    except OSError:
   252	        return 0
   253	    return n
   254	
   255	def _utf8_stdio():
   256	    for stream in (sys.stdin, sys.stdout):
   257	        try:
   258	            stream.reconfigure(encoding="utf-8", errors="replace")
   259	        except Exception:
   260	            pass
   261	
   262	def find_cursor_agent():
   263	    # Known install path first (substitute-binary defence); PATH is the fallback.
   264	    home = os.path.expanduser("~")
   265	    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
   266	    for cand in (
   267	        os.path.join(local, "cursor-agent", "cursor-agent.cmd"),   # Windows
   268	        os.path.join(home, ".local", "bin", "cursor-agent"),       # macOS / Linux
   269	        os.path.join(home, ".cursor", "bin", "cursor-agent"),
   270	    ):
   271	        if os.path.isfile(cand):
   272	            return cand
   273	    return shutil.which("cursor-agent")
   274	
   275	def _safe_id(value, label):
   276	    if not isinstance(value, str) or not _UUID_RE.match(value):
   277	        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
   278	    return value
   279	
   280	def _safe_model(value):
   281	    if value is None:
   282	        return None
   283	    if not isinstance(value, str) or not _MODEL_RE.match(value.strip().lower()):
   284	        raise ValueError("'model' must be a plain model id such as 'composer-2.5' "
   285	                         "(letters, digits, dot, dash, underscore only)")
   286	    return value.strip().lower()
   287	
   288	def _norm(path):
   289	    return os.path.normcase(os.path.realpath(path))
   290	
   291	def _is_within(child, parent):
   292	    """True when child == parent or sits underneath it. Symlink-resolved, case-folded."""
   293	    c, p = _norm(child), _norm(parent)
   294	    if c == p:
   295	        return True
   296	    try:
   297	        return os.path.commonpath([c, p]) == p
   298	    except ValueError:      # different drives
   299	        return False
   300	
   301	def _safe_cwd(cwd, always_approve):
   302	    """A write-capable seat needs an explicit cwd, and it may not be a sensitive one.
   303	
   304	    Returns the CANONICAL path, so a symlink cannot be validated and then
   305	    dereferenced somewhere else afterwards.
   306	    """
   307	    if not always_approve:
   308	        return os.path.realpath(cwd) if cwd else None
   309	    if cwd is None:
   310	        raise ValueError("always_approve requires an explicit cwd naming the project "
   311	                         "directory the seat may write in (the playpen is a fine choice: "
   312	                         + PLAYPEN + ")")
   313	    real = os.path.realpath(cwd)
   314	    if not os.path.isdir(real):
   315	        raise ValueError(f"cwd is not a directory: {cwd}")
   316	    # The playpen is always allowed — that is its whole purpose.
   317	    if _is_within(real, PLAYPEN):
   318	        return real
   319	    roots = [os.path.expanduser("~"), os.path.abspath(os.sep)]
   320	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)",
   321	                "ProgramData", "USERPROFILE"):
   322	        v = os.environ.get(env)
   323	        if v:
   324	            roots.append(v)
   325	    for r in roots:
   326	        if _norm(real) == _norm(r):
   327	            raise ValueError(f"refusing a write-capable session rooted at {real} — "
   328	                             f"point cwd at a project directory or the playpen")
   329	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
   330	        v = os.environ.get(env)
   331	        if v and _is_within(real, v):
   332	            raise ValueError(f"refusing a write-capable session inside a system directory "
   333	                             f"({v}) — point cwd at a project directory or the playpen")
   334	    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
   335	                   ".config", ".azure", ".kube", ".gnupg"):
   336	        parts = [p.lower() for p in _norm(real).split(os.sep)]
   337	        if secret in parts:
   338	            raise ValueError(f"refusing a write-capable session inside {secret}")
   339	    return real
   340	
   341	def _extract_json(raw):
   342	    """Last complete result object wins — the CLI streams status lines first."""
   343	    dec = json.JSONDecoder()
   344	    found = None
   345	    idx = raw.find("{")
   346	    while idx != -1:
   347	        try:
   348	            obj, _ = dec.raw_decode(raw[idx:])
   349	            if isinstance(obj, dict) and obj.get("type") == "result":
   350	                found = obj
   351	            elif isinstance(obj, dict) and found is None:
   352	                found = obj
   353	        except json.JSONDecodeError:
   354	            pass
   355	        idx = raw.find("{", idx + 1)
   356	    return found
   357	
   358	def run_cursor(prompt, session_id=None, cwd=None, model=None, always_approve=False,
   359	               spend_credits=False):
   360	    exe = find_cursor_agent()
   361	    if not exe:
   362	        return True, ("Cursor CLI not found. Install it, then `cursor-agent login`. "
   363	                      "(Windows: %LOCALAPPDATA%\\cursor-agent\\cursor-agent.cmd)")
   364	    chosen = model or DEFAULT_MODEL
   365	    klass = meter_class(chosen)
   366	
   367	    # THE METER GUARD. UNKNOWN is refused unconditionally — spend_credits unlocks
   368	    # only RECOGNISED third-party models, never an unidentified or auto-routed one.
   369	    if klass == "UNKNOWN":
   370	        return True, (
   371	            f"{CURSOR_BANNER} ⚠️ REFUSED — '{chosen}' is not a recognised model id, or is "
   372	            f"`auto` (which may route anywhere). Unknown lineage fails closed and cannot be "
   373	            f"unlocked with spend_credits. Name an explicit model: composer-2.5 (free) or "
   374	            f"cursor-grok-4.6-high (free); see BENCH-LEDGER.md for the metered ones.")
   375	    if klass.startswith("CREDITS") and not spend_credits:
   376	        return True, (
   377	            f"{CURSOR_BANNER} 🚨 CREDIT GUARD — REFUSED BEFORE SPENDING\n\n"
   378	            f"'{chosen}' is meter class {klass} ({_lineage(chosen)} lineage). It draws "
   379	            f"Cursor's third-party CREDIT pool (~$20/month included, then pay-as-you-go at "
   380	            f"API prices), not the included Cursor Models pool.\n\n"
   381	            f"To spend credits deliberately, pass spend_credits: true. To stay free, use an "
   382	            f"INCLUDED model: composer-2.5 (default) or cursor-grok-4.6-high.\n\n"
   383	            f"'-fast' variants are a surcharge (Composer 2.5 costs 6x more output on Fast), "
   384	            f"never a free speed-up.")
   385	
   386	    if always_approve and not yolo_allowed(chosen):
   387	        return True, (
   388	            f"{CURSOR_BANNER} 🛑 WRITE REFUSED — '{chosen}' is not on the YOLO allowlist.\n\n"
   389	            f"Only the free, trusted seats may run write-capable: composer-* and "
   390	            f"cursor-grok-*. Every other pool model ({_lineage(chosen)} here) may read and "
   391	            f"advise, never write or execute.\n\n"
   392	            f"Boss ruling 2026-08-23. Re-run this as a read-only call (drop always_approve), "
   393	            f"or hand the build to composer-2.5 / cursor-grok-4.6-high.")
   394	
   395	    # THE COUNCIL SEAT LAW (SPINE v2.5): spending is gated by a recorded ALLOWANCE,
   396	    # not by vendor class. No grant, or an expired one, means this seat may not spend.
   397	    if klass.startswith("CREDITS"):
   398	        ok, why = _allowance("cursor")
   399	        if not ok:
   400	            return True, (
   401	                f"{CURSOR_BANNER} 🛑 NO ALLOWANCE — REFUSED BEFORE SPENDING\n\n"
   402	                f"'{chosen}' bills the third-party credit pool, and {why}\n\n"
   403	                f"Grants are bounded and expire on purpose. Free INCLUDED models "
   404	                f"(composer-2.5, cursor-grok-4.6-*) are unaffected and need no allowance.")
   405	
   406	    if klass.startswith("CREDITS") and COUNCIL_LOCK_ON:
   407	        recent = _recent_billable(COUNCIL_LOCK_WINDOW_S)
   408	        if recent >= _allowance_calls("cursor", COUNCIL_LOCK_MAX):
   409	            return True, (
   410	                f"{CURSOR_BANNER} 🛑 COUNCIL LOCK — REFUSED\n\n"
   411	                f"{recent} billable Cursor calls already landed in the last "
   412	                f"{COUNCIL_LOCK_WINDOW_S // 60} minutes, at the operator's granted bound. "
   413	                f"This looks like a COUNCIL fanning out onto metered seats.\n\n"
   414	                f"Standing boss ruling (2026-08-23): a council runs on SUBSCRIPTION seats "
   415	                f"only — house Claude, Codex, Grok, Gemini. Cursor-hosted models are not "
   416	                f"council seats right now.\n\n"
   417	                f"Free INCLUDED models (composer-2.5, cursor-grok-4.6-*) are unaffected. To "
   418	                f"lift this deliberately set WMW_CURSOR_COUNCIL_LOCK=off — and say so to "
   419	                f"the boss first."
   420	            )
   421	
   422	    _ensure_playpen()
   423	    # No cwd? Work in the playpen — the seat always has somewhere legitimate to be.
   424	    workdir = cwd or PLAYPEN
   425	    if not os.path.isdir(workdir):
   426	        return True, f"cwd is not a directory: {workdir}"
   427	
   428	    # ---- THE GUARD (council 2026-08-24) ------------------------------------
   429	    # Two controls, and they only bind a WRITE-capable dispatch at a real repo —
   430	    # the shape that burned two thirds of a month on 2026-08-21/22. A read-only
   431	    # question costs little and is left alone deliberately.
   432	    guard, lease = _guard(), None
   433	    if guard and always_approve and cwd:
   434	        # PREFLIGHT: an agent with no destination still spends at full rate.
   435	        rc, problems, _notes = guard.preflight(workdir, model=chosen)
   436	        if rc:
   437	            return True, (
   438	                f"{CURSOR_BANNER} 🛑 PREFLIGHT REFUSED — dispatch would spend for nothing\n\n"
   439	                + "\n".join(f"  • {p}" for p in problems) +
   440	                "\n\nThis is the Aug 21-22 shape: 13 agents into a repo staged empty, 11 of "
   441	                "them returning zero lines. Point the seat at a repo with real source, or "
   442	                "run read-only (omit always_approve) to ask a question instead of building.")
   443	
   444	        # RESERVE: atomic, so N launches cannot each pass on the same headroom.
   445	        lease = f"cursor-{os.getpid()}-{int(time.time())}"
   446	        ok, why = guard.reserve(lease, est_pct=float(os.environ.get("WMW_EST_PCT", "2")),
   447	                                note=f"{chosen} @ {os.path.basename(workdir)}")
   448	        if not ok:
   449	            return True, (
   450	                f"{CURSOR_BANNER} 🛑 NO HEADROOM RESERVED — REFUSED BEFORE SPENDING\n\n{why}\n\n"
   451	                "Concurrency is the control. Thirteen launches each passed their own check "
   452	                "on 2026-08-21 and together took the month.")
   453	
   454	    # ---- PROMPT TRANSPORT --------------------------------------------------
   455	    # NOTHING caller-controlled goes on the command line. The Windows CLI is a
   456	    # .cmd shim forwarding to PowerShell; a crafted prompt CAN execute host
   457	    # commands (reproduced 2026-08-23). The prompt always travels as a file in
   458	    # the playpen; only a generated ASCII pointer is passed as an argument.
   459	    spill_path = None
   460	    try:
   461	        fd, spill_path = tempfile.mkstemp(prefix="prompt_", suffix=".md", dir=PROMPTS_DIR)
   462	        try:
   463	            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
   464	                f.write(prompt)
   465	        except OSError as e:
   466	            return True, f"could not write the prompt handoff file: {e}"
   467	
   468	        # ASCII ONLY, deliberately: this string is the single thing that reaches argv,
   469	        # and the Windows .cmd shim mangles (or executes) anything exotic.
   470	        pointer = ("Read the file at " + spill_path.replace("\\", "/") +
   471	                   " which contains your full instructions. Follow them exactly and answer "
   472	                   "them directly. Do not modify or delete that file; it is a scratch "
   473	                   "handoff and is cleaned up automatically.")
   474	        if not pointer.isascii():
   475	            return True, ("the prompt handoff path contains non-ASCII characters; set "
   476	                          "WMW_CURSOR_PLAYPEN to a plain ASCII path")
   477	
   478	        cmd = [exe]
   479	        if session_id:
   480	            cmd += [f"--resume={session_id}"]
   481	        cmd += ["--model", chosen]
   482	        cmd += ["--yolo"] if always_approve else ["--mode", "ask", "--trust"]
   483	        # Let the seat use the MCP servers configured in ~/.cursor/mcp.json, so a
   484	        # Cursor seat gets the same workshop the house seats have. NOTE: this
   485	        # auto-approves whatever is in that file — keep it to read-only tools, and
   486	        # deliberately NOT the sibling wmw-* seats: a seat that can drive another
   487	        # seat can escalate around its own read-only mode (proved on wmw-grok,
   488	        # 2026-08-23, where a read-only Grok wrote a file via the Codex seat).
   489	        cmd += ["--approve-mcps"]
   490	        cmd += ["-p", pointer, "--output-format", "json"]
   491	
   492	        try:
   493	            proc = subprocess.run(
   494	                cmd, capture_output=True, text=True, encoding="utf-8",
   495	                errors="replace", timeout=CURSOR_TIMEOUT_S, cwd=workdir,
   496	                stdin=subprocess.DEVNULL,
   497	            )
   498	        except subprocess.TimeoutExpired:
   499	            _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   500	            return True, f"cursor-agent timed out after {CURSOR_TIMEOUT_S}s"
   501	        except OSError as e:
   502	            return True, f"could not launch cursor-agent: {e}"
   503	    finally:
   504	        if spill_path:
   505	            try:
   506	                os.unlink(spill_path)
   507	            except (FileNotFoundError, OSError):
   508	                pass
   509	        # Release the lease HERE, in the finally, so a crash, a timeout or a launch
   510	        # failure can never leave a slot held. A stuck lease would deny the operator
   511	        # his own rig, which is a worse failure than the one being prevented.
   512	        if guard and lease:
   513	            try:
   514	                guard.release(lease)
   515	            except Exception as e:
   516	                print(f"[wmw-cursor] lease release failed: {e}", file=sys.stderr)
   517	
   518	    raw = (proc.stdout or "").strip()
   519	    err = (proc.stderr or "").strip()
   520	    data = _extract_json(raw)
   521	    # Only a run that produced NO result can be a trust refusal. Checking raw text
   522	    # first was a self-inflicted false positive: a model reviewing this very file
   523	    # quoted the phrase back and the wrapper refused its own review.
   524	    if data is None and ("Workspace Trust Required" in raw or "Workspace Trust Required" in err):
   525	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   526	        return True, (f"Cursor refused {workdir} as untrusted. Point cwd at a project "
   527	                      f"directory you trust, or leave cwd unset to use the playpen.")
   528	    if data is None:
   529	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   530	        return True, (f"cursor-agent exited {proc.returncode} with no parseable JSON.\n"
   531	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
   532	    if data.get("is_error") or data.get("subtype") not in (None, "success"):
   533	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"),
   534	                   data.get("session_id") or session_id, False, always_approve)
   535	        return True, (f"cursor-agent reported an error: {str(data.get('result'))[:1500]}\n"
   536	                      f"stderr: {err[:800]}")
   537	    text = data.get("result")
   538	    sid = data.get("session_id")
   539	    if proc.returncode != 0 or not isinstance(sid, str) or not sid:
   540	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"), sid or session_id,
   541	                   False, always_approve)
   542	        return True, (f"cursor-agent run failed (exit {proc.returncode}, session_id={sid!r}).\n"
   543	                      f"result: {str(text)[:1000]}\nstderr: {err[:1000]}")
   544	    if not isinstance(text, str):
   545	        text = "" if text is None else str(text)
   546	    if len(text) > MAX_REPLY_CHARS:
   547	        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-cursor] ...truncated at {MAX_REPLY_CHARS} chars]"
   548	
   549	    usage = data.get("usage") or {}
   550	    tok = (f"{usage.get('inputTokens', '?')} in / {usage.get('outputTokens', '?')} out"
   551	           if usage else "usage unreported")
   552	    mark = METER_MARK.get(klass, "⚠️")
   553	    vendor = _lineage(chosen)
   554	    blood = BLOODLINE_MARK.get(vendor, "❓")
   555	    pool = ("Cursor Models pool — INCLUDED, no credits spent" if klass == "INCLUDED"
   556	            else "Cursor Models pool — included, but a FAST-tier surcharge applies"
   557	            if klass == "INCLUDED-FAST"
   558	            else "third-party CREDIT pool — billed at API prices")
   559	    _log_spend(chosen, vendor, klass, usage, sid, True, always_approve)
   560	    money = ""
   561	    if klass.startswith("CREDITS") or klass == "INCLUDED-FAST":
   562	        money = (f"\n{CURSOR_BANNER} {mark} —— THIS CALL SPENT MONEY —— {mark} {CURSOR_BANNER}"
   563	                 f"\n   {pool}")
   564	    footer = (f"\n\n---\n{CURSOR_BANNER}{blood} [wmw-cursor] {mark} {vendor} · {chosen}"
   565	              f"\n   sessionId: {sid} · meter: {klass} · {tok}{money}")
   566	    return False, text + footer
   567	
   568	def _req_str(args, key):
   569	    v = args.get(key)
   570	    if not isinstance(v, str) or not v.strip():
   571	        raise ValueError(f"'{key}' must be a non-empty string")
   572	    return v
   573	
   574	def _opt_str(args, key):
   575	    v = args.get(key)
   576	    if v is None:
   577	        return None
   578	    if not isinstance(v, str) or not v.strip():
   579	        raise ValueError(f"'{key}' must be a non-empty string when given")
   580	    return v
   581	
   582	def _opt_bool(args, key):
   583	    v = args.get(key)
   584	    if v is None:
   585	        return False
   586	    if isinstance(v, bool):
   587	        return v
   588	    if isinstance(v, str) and v.lower() in ("true", "false"):
   589	        return v.lower() == "true"
   590	    raise ValueError(f"'{key}' must be a boolean")
   591	
   592	_MODEL_NOTE = ("Model id (default composer-2.5 — the free, non-fast door). Free/INCLUDED: "
   593	               "composer-2.5, cursor-grok-4.6-{low,medium,high,xhigh}, cursor-grok-4.5-*. "
   594	               "Metered/CREDITS (need spend_credits): claude-*, gpt-*, gemini-*, kimi-*, "
   595	               "glm-*. `auto` is refused. See BENCH-LEDGER.md; `cursor-agent models` lists all.")
   596	
   597	TOOLS = [
   598	    {
   599	        "name": "cursor",
   600	        "description": (
   601	            "Start a NEW persistent conversation on the CURSOR MODEL POOL (Composer 2.5 by "
   602	            "default; Cursor Grok, Codex, Kimi, GLM and other tiers via `model`). Returns the "
   603	            "reply plus a sessionId footer; continue it with cursor-reply. ⚠ THE ONE METERED "
   604	            "SEAT: composer-* and cursor-grok-* are INCLUDED (free); everything else bills "
   605	            "Cursor's credit pool and is refused unless spend_credits is true. DEFAULT IS "
   606	            "READ-ONLY (no code execution, no file writes). Set always_approve true only for "
   607	            "build tickets, and then cwd is REQUIRED. With no cwd the seat works in its own "
   608	            "playpen directory."
   609	        ),
   610	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   611	        "inputSchema": {
   612	            "type": "object",
   613	            "properties": {
   614	                "prompt": {"type": "string", "description": "The task or message."},
   615	                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory. Omit to work in the playpen."},
   616	                "model": {"type": "string", "description": _MODEL_NOTE},
   617	                "always_approve": {"type": "boolean", "description": "DANGEROUS: pass --yolo so the agent may write files and run commands under cwd. Default false = read-only."},
   618	                "spend_credits": {"type": "boolean", "description": "Required to reach any THIRD-PARTY model (claude-/gpt-/gemini-/kimi-/glm-), billed at API prices against Cursor's credit pool. Ask the boss first."},
   619	            },
   620	            "required": ["prompt"],
   621	        },
   622	    },
   623	    {
   624	        "name": "cursor-reply",
   625	        "description": (
   626	            "Continue an existing Cursor-pool conversation by sessionId (from a prior cursor "
   627	            "call's footer), with full prior context. Same meter rules apply."
   628	        ),
   629	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   630	        "inputSchema": {
   631	            "type": "object",
   632	            "properties": {
   633	                "sessionId": {"type": "string", "description": "sessionId from a previous cursor/cursor-reply call."},
   634	                "prompt": {"type": "string", "description": "The follow-up message."},
   635	                "model": {"type": "string", "description": _MODEL_NOTE},
   636	                "cwd": {"type": "string", "description": "Working directory for this turn."},
   637	                "always_approve": {"type": "boolean", "description": "Pass --yolo for this turn (write-capable); requires cwd."},
   638	                "spend_credits": {"type": "boolean", "description": "Required to reach a third-party (credit-billed) model."},
   639	            },
   640	            "required": ["sessionId", "prompt"],
   641	        },
   642	    },
   643	]
   644	
   645	def _tool_call(name, args):
   646	    if not isinstance(args, dict):
   647	        return True, "arguments must be an object"
   648	    try:
   649	        if name in ("cursor", "cursor-reply"):
   650	            approve = _opt_bool(args, "always_approve")
   651	            cwd = _safe_cwd(_opt_str(args, "cwd"), approve)
   652	            sid = _safe_id(args.get("sessionId"), "sessionId") if name == "cursor-reply" else None
   653	            return run_cursor(
   654	                _req_str(args, "prompt"), session_id=sid, cwd=cwd,
   655	                model=_safe_model(_opt_str(args, "model")),
   656	                always_approve=approve,
   657	                spend_credits=_opt_bool(args, "spend_credits"),
   658	            )
   659	    except ValueError as e:
   660	        return True, f"invalid arguments: {e}"
   661	    return None
   662	
   663	def handle(msg):
   664	    method = msg.get("method")
   665	    mid = msg.get("id")
   666	    is_notification = "id" not in msg
   667	    if method == "initialize":
   668	        return {
   669	            "jsonrpc": "2.0", "id": mid,
   670	            "result": {
   671	                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
   672	                "capabilities": {"tools": {}},
   673	                "serverInfo": {"name": "wmw-cursor", "version": "2.3.0"},
   674	            },
   675	        }
   676	    if method == "ping":
   677	        return {"jsonrpc": "2.0", "id": mid, "result": {}}
   678	    if method == "tools/list":
   679	        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
   680	    if method == "tools/call":
   681	        params = msg.get("params") or {}
   682	        name = params.get("name")
   683	        result = _tool_call(name, params.get("arguments") or {})
   684	        if result is None:
   685	            return {"jsonrpc": "2.0", "id": mid,
   686	                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
   687	        is_err, text = result
   688	        return {"jsonrpc": "2.0", "id": mid,
   689	                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
   690	    if not is_notification:
   691	        return {"jsonrpc": "2.0", "id": mid,
   692	                "error": {"code": -32601, "message": f"method not found: {method}"}}
   693	    return None
   694	
   695	def main():
   696	    _utf8_stdio()
   697	    _ensure_playpen()
   698	    for line in sys.stdin:
   699	        line = line.strip()
   700	        if not line:
   701	            continue
   702	        try:
   703	            msg = json.loads(line)
   704	        except json.JSONDecodeError:
   705	            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
   706	                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
   707	            sys.stdout.flush()
   708	            continue
   709	        if not isinstance(msg, dict):
   710	            continue
   711	        try:
   712	            resp = handle(msg)
   713	        except Exception as e:
   714	            print(f"[wmw-cursor] internal error: {e}", file=sys.stderr)
   715	            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
   716	                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
   717	        if resp is not None:
   718	            sys.stdout.write(json.dumps(resp) + "\n")
   719	            sys.stdout.flush()
   720	
   721	if __name__ == "__main__":
   722	    main()
```

## ===== wmw_grok_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-grok — MCP stdio server wrapping the Grok Build CLI. v1.3
     3	
     4	Gives Claude Code a persistent Grok seat:
     5	  grok(prompt, ...)            start a new Grok conversation -> reply + sessionId
     6	  grok-reply(sessionId, ...)   continue that conversation with full context
     7	
     8	v1.1 (2026-08-22, council findings): prompt passed via --prompt-file (no Windows
     9	32K command-line limit), honest error detection (nonzero exit / error JSON /
    10	missing sessionId => isError), strict UTF-8 stdio, argument validation,
    11	per-request exception boundary.
    12	v1.4: read-only now also denies MCPTool/WebFetch/WebSearch and pins
    13	--permission-mode default -- without those a "read-only" seat could call another
    14	MCP seat and have IT write (reproduced live, then verified fixed).
    15	v1.2: UUID-validated session ids + no-leading-dash argv guard (a crafted id could
    16	otherwise smuggle CLI flags), --resume= equals form, real read-only argv when
    17	always_approve is false, absolute-path-first exe lookup, stdin closed. Requires Python 3.10+ on PATH.
    18	
    19	Transport: newline-delimited JSON-RPC 2.0 over stdio. Stdlib only.
    20	Known limitation (documented, queued): requests are handled one at a time; a
    21	long-running call blocks the loop and cancellation is not supported.
    22	"""
    23	import json
    24	import os
    25	import shutil
    26	import subprocess
    27	import sys
    28	import tempfile
    29	
    30	GROK_TIMEOUT_S = 3600
    31	MAX_REPLY_CHARS = 400_000   # cap what we hand back to the client
    32	
    33	# Tools a read-only seat may never use. Deny rules bind on every platform; the CLI's
    34	# --sandbox does not (Landlock/Seatbelt only, silently unenforced on Windows).
    35	#
    36	# MCPTool IS THE IMPORTANT ONE. Denying Write/Edit/Bash locks the front door and
    37	# leaves every other door open: a "read-only" seat can call ANOTHER MCP server --
    38	# including the sibling wmw-* seats -- and have it do the writing. Reproduced live
    39	# 2026-08-23: a read-only Grok wrote a file through the Codex seat. Verified fixed
    40	# by re-running that canary with MCPTool denied.
    41	#
    42	# NOTE: MultiEdit is NOT a recognised permission name in this CLI (unknown names
    43	# are skipped with a warning); the real edit classes are Edit / Write /
    44	# NotebookEdit. It is kept only as a harmless alias guard.
    45	DENY_RULES = ("Write", "Edit", "MultiEdit", "NotebookEdit", "Bash",
    46	              "MCPTool", "WebFetch", "WebSearch")
    47	
    48	def _utf8_stdio():
    49	    for stream in (sys.stdin, sys.stdout):
    50	        try:
    51	            stream.reconfigure(encoding="utf-8", errors="replace")
    52	        except Exception:
    53	            pass
    54	
    55	def find_grok():
    56	    # Known install path FIRST: a stray "grok" earlier on PATH would run with this user's
    57	    # credentials. PATH is only the fallback.
    58	    home = os.path.expanduser("~")
    59	    for cand in (
    60	        os.path.join(home, ".grok", "bin", "grok.exe"),   # Windows
    61	        os.path.join(home, ".grok", "bin", "grok"),       # macOS / Linux
    62	        os.path.join(home, ".local", "bin", "grok"),
    63	    ):
    64	        if os.path.isfile(cand):
    65	            return cand
    66	    return shutil.which("grok")
    67	
    68	_UUID_RE = __import__("re").compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")
    69	
    70	def _safe_id(value, label):
    71	    """Session ids are argv values: a leading '-' would be reparsed as a CLI flag."""
    72	    if not isinstance(value, str) or not _UUID_RE.match(value):
    73	        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
    74	    return value
    75	
    76	def _safe_argv(value, label):
    77	    if value is None:
    78	        return None
    79	    if not isinstance(value, str) or not value.strip() or value.lstrip().startswith("-"):
    80	        raise ValueError(f"'{label}' must be a non-empty string that does not start with '-'")
    81	    return value
    82	
    83	def _extract_json(raw):
    84	    """Find the first complete JSON object in raw text (banner-noise tolerant)."""
    85	    dec = json.JSONDecoder()
    86	    idx = raw.find("{")
    87	    while idx != -1:
    88	        try:
    89	            obj, _ = dec.raw_decode(raw[idx:])
    90	            if isinstance(obj, dict):
    91	                return obj
    92	        except json.JSONDecodeError:
    93	            pass
    94	        idx = raw.find("{", idx + 1)
    95	    return None
    96	
    97	def run_grok(prompt, session_id=None, cwd=None, model=None, always_approve=False,
    98	             allow_web_search=False):
    99	    exe = find_grok()
   100	    if not exe:
   101	        return True, "grok CLI not found on PATH or in ~/.grok/bin — is Grok Build installed?"
   102	    if cwd and not os.path.isdir(cwd):
   103	        return True, f"cwd is not a directory: {cwd}"
   104	    tmp = None
   105	    try:
   106	        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md",
   107	                                         delete=False) as f:
   108	            f.write(prompt)
   109	            tmp = f.name
   110	        cmd = [exe]
   111	        if session_id:
   112	            cmd += [f"--resume={session_id}"]
   113	        if model:
   114	            cmd += ["-m", model]
   115	        if cwd:
   116	            cmd += ["--cwd", cwd]
   117	        if always_approve:
   118	            cmd += ["--always-approve"]
   119	        if not always_approve:
   120	            # Read-only enforced by DENY RULES, not --sandbox: the CLI's sandbox is
   121	            # Landlock/Seatbelt only and fails OPEN on Windows (council 2026-08-22 proved a
   122	            # write succeeded under --sandbox read-only). Deny rules were verified to block it.
   123	            for rule in DENY_RULES:
   124	                cmd += ["--deny", rule]
   125	            # The user's ~/.grok/config.toml may set permission_mode = "always-approve".
   126	            # Deny rules still win for names they match, but everything NOT denied is
   127	            # then auto-approved. Pin the mode explicitly so config cannot widen us.
   128	            # --no-subagents does NOT stop a spawn: Grok proved it live on 2026-08-23 by
   129	            # spawning a general-purpose child that ran to completion (it could not write,
   130	            # because children inherit the deny rules, but it ran). `Agent` is not a valid
   131	            # --deny class, so removing the tool outright is the only real kill switch.
   132	            cmd += ["--disallowed-tools", "Agent"]
   133	            cmd += ["--permission-mode", "default", "--no-subagents", "--no-memory"]
   134	            if not allow_web_search:
   135	                cmd += ["--disable-web-search"]
   136	        cmd += ["--prompt-file", tmp, "--output-format", "json"]
   137	        try:
   138	            proc = subprocess.run(
   139	                cmd, capture_output=True, text=True, encoding="utf-8",
   140	                errors="replace", timeout=GROK_TIMEOUT_S,
   141	                stdin=subprocess.DEVNULL,
   142	            )
   143	        except subprocess.TimeoutExpired:
   144	            return True, f"grok timed out after {GROK_TIMEOUT_S}s"
   145	        except OSError as e:
   146	            return True, f"could not launch grok: {e}"
   147	    finally:
   148	        if tmp:
   149	            try:
   150	                os.unlink(tmp)
   151	            except OSError:
   152	                pass
   153	    raw = (proc.stdout or "").strip()
   154	    err = (proc.stderr or "").strip()
   155	    data = _extract_json(raw)
   156	    if data is None:
   157	        return True, (f"grok exited {proc.returncode} with no parseable JSON.\n"
   158	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
   159	    if data.get("type") == "error":
   160	        return True, f"grok error: {data.get('message', '(no message)')}\nstderr: {err[:1000]}"
   161	    text = data.get("text")
   162	    sid = data.get("sessionId")
   163	    if proc.returncode != 0 or not isinstance(sid, str) or not sid:
   164	        return True, (f"grok run failed (exit {proc.returncode}, sessionId={sid!r}).\n"
   165	                      f"text: {str(text)[:1000]}\nstderr: {err[:1000]}")
   166	    if not isinstance(text, str):
   167	        text = "" if text is None else str(text)
   168	    if len(text) > MAX_REPLY_CHARS:
   169	        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-grok] ...truncated at {MAX_REPLY_CHARS} chars]"
   170	    usage = data.get("modelUsage") or {}
   171	    model_used = next(iter(usage), "unknown-model")
   172	    footer = f"\n\n---\n[wmw-grok] sessionId: {sid} · model: {model_used} · turns: {data.get('num_turns', '?')}"
   173	    return False, text + footer
   174	
   175	def _safe_cwd(cwd, always_approve):
   176	    """A write-capable seat may not be pointed at a home or system directory."""
   177	    if not always_approve:
   178	        return cwd
   179	    if cwd is None:
   180	        raise ValueError("always_approve requires an explicit cwd naming the project "
   181	                         "directory the seat may write in")
   182	    real = os.path.realpath(cwd)
   183	    if not os.path.isdir(real):
   184	        raise ValueError(f"cwd is not a directory: {cwd}")
   185	    norm = lambda x: os.path.normcase(os.path.realpath(x))
   186	    def within(child, parent):
   187	        c, pa = norm(child), norm(parent)
   188	        if c == pa:
   189	            return True
   190	        try:
   191	            return os.path.commonpath([c, pa]) == pa
   192	        except ValueError:      # different drives
   193	            return False
   194	    # Exact-root bans first (home and drive root are legitimate parents of projects).
   195	    for r in (os.path.expanduser("~"), os.path.abspath(os.sep)):
   196	        if norm(real) == norm(r):
   197	            raise ValueError(f"refusing a write-capable session rooted at {real} — "
   198	                             f"point cwd at a project directory")
   199	    # System trees are banned by CONTAINMENT: an exact-match check let
   200	    # C:\Windows\System32 through as a mere descendant. Found by Grok, 2026-08-23.
   201	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
   202	        v = os.environ.get(env)
   203	        if v and within(real, v):
   204	            raise ValueError(f"refusing a write-capable session inside a system directory "
   205	                             f"({v}) — point cwd at a project directory")
   206	    # Case-insensitive segment match: ".SSH" used to slip past a case-sensitive test.
   207	    parts = [x.lower() for x in norm(real).split(os.sep)]
   208	    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
   209	                   ".config", ".azure", ".kube", ".gnupg"):
   210	        if secret in parts:
   211	            raise ValueError(f"refusing a write-capable session inside {secret}")
   212	    return real   # return the CANONICAL path, so a symlink cannot be re-pointed after validation
   213	
   214	def _req_str(args, key):
   215	    v = args.get(key)
   216	    if not isinstance(v, str) or not v.strip():
   217	        raise ValueError(f"'{key}' must be a non-empty string")
   218	    return v
   219	
   220	def _opt_str(args, key):
   221	    v = args.get(key)
   222	    if v is None:
   223	        return None
   224	    if not isinstance(v, str) or not v.strip():
   225	        raise ValueError(f"'{key}' must be a non-empty string when given")
   226	    return v
   227	
   228	def _opt_bool(args, key):
   229	    v = args.get(key)
   230	    if v is None:
   231	        return False
   232	    if isinstance(v, bool):
   233	        return v
   234	    if isinstance(v, str) and v.lower() in ("true", "false"):
   235	        return v.lower() == "true"
   236	    raise ValueError(f"'{key}' must be a boolean")
   237	
   238	TOOLS = [
   239	    {
   240	        "name": "grok",
   241	        "description": (
   242	            "Start a NEW persistent conversation with Grok (Grok Build CLI, xAI subscription seat). "
   243	            "Returns Grok's reply plus a sessionId footer. To continue the same conversation with "
   244	            "full context, call grok-reply with that sessionId. DEFAULT IS READ-ONLY: file writes, "
   245	            "edits and shell are denied, and web search is off unless allow_web_search is true. "
   246	            "Set always_approve true ONLY for build tickets — it lets Grok write files and run "
   247	            "commands under cwd. Use for build dispatches, research, and council seats."
   248	        ),
   249	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   250	        "inputSchema": {
   251	            "type": "object",
   252	            "properties": {
   253	                "prompt": {"type": "string", "description": "The task or message for Grok."},
   254	                "cwd": {"type": "string", "description": "Working directory for the session (repo path for build work). Required when always_approve is true; must not be a home/system directory."},
   255	                "model": {"type": "string", "description": "Optional Grok model ID override."},
   256	                "always_approve": {"type": "boolean", "description": "DANGEROUS: auto-approve all of Grok's tool use, including file writes and shell commands under cwd. Required for build work; default false = deny-listed read-only."},
   257	                "allow_web_search": {"type": "boolean", "description": "Allow web search/fetch on a read-only call (default false; ignored when always_approve is true)."},
   258	            },
   259	            "required": ["prompt"],
   260	        },
   261	    },
   262	    {
   263	        "name": "grok-reply",
   264	        "description": (
   265	            "Continue an existing Grok conversation by sessionId (from a prior grok call's footer). "
   266	            "Grok retains the full prior context of that session."
   267	        ),
   268	        "inputSchema": {
   269	            "type": "object",
   270	            "properties": {
   271	                "sessionId": {"type": "string", "description": "The sessionId returned by a previous grok/grok-reply call."},
   272	                "prompt": {"type": "string", "description": "The follow-up message."},
   273	                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory."},
   274	                "always_approve": {"type": "boolean", "description": "Auto-approve Grok's tool use this turn (file writes, shell). Requires cwd."},
   275	            },
   276	            "required": ["sessionId", "prompt"],
   277	        },
   278	    },
   279	]
   280	
   281	def _tool_call(name, args):
   282	    if not isinstance(args, dict):
   283	        return True, "arguments must be an object"
   284	    try:
   285	        if name == "grok":
   286	            approve = _opt_bool(args, "always_approve")
   287	            cwd = _safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve)
   288	            return run_grok(
   289	                _req_str(args, "prompt"), cwd=cwd,
   290	                model=_safe_argv(_opt_str(args, "model"), "model"),
   291	                always_approve=approve,
   292	                allow_web_search=_opt_bool(args, "allow_web_search"),
   293	            )
   294	        if name == "grok-reply":
   295	            # A reply may escalate a read-only thread to write-capable, so it must clear the
   296	            # SAME cwd guard the start tool does. Without this, the legal sequence was:
   297	            # grok(cwd=<somewhere sensitive>) read-only, then grok-reply(always_approve=true)
   298	            # with no path check at all. Found by Grok, 2026-08-23.
   299	            approve = _opt_bool(args, "always_approve")
   300	            reply_cwd = _safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve)
   301	            return run_grok(
   302	                _req_str(args, "prompt"),
   303	                session_id=_safe_id(args.get("sessionId"), "sessionId"),
   304	                cwd=reply_cwd,
   305	                always_approve=approve,
   306	                allow_web_search=_opt_bool(args, "allow_web_search"),
   307	            )
   308	    except ValueError as e:
   309	        return True, f"invalid arguments: {e}"
   310	    return None
   311	
   312	def handle(msg):
   313	    method = msg.get("method")
   314	    mid = msg.get("id")
   315	    is_notification = "id" not in msg
   316	    if method == "initialize":
   317	        return {
   318	            "jsonrpc": "2.0", "id": mid,
   319	            "result": {
   320	                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
   321	                "capabilities": {"tools": {}},
   322	                "serverInfo": {"name": "wmw-grok", "version": "1.5.0"},
   323	            },
   324	        }
   325	    if method == "ping":
   326	        return {"jsonrpc": "2.0", "id": mid, "result": {}}
   327	    if method == "tools/list":
   328	        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
   329	    if method == "tools/call":
   330	        params = msg.get("params") or {}
   331	        name = params.get("name")
   332	        result = _tool_call(name, params.get("arguments") or {})
   333	        if result is None:
   334	            return {"jsonrpc": "2.0", "id": mid,
   335	                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
   336	        is_err, text = result
   337	        return {"jsonrpc": "2.0", "id": mid,
   338	                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
   339	    if not is_notification:
   340	        return {"jsonrpc": "2.0", "id": mid,
   341	                "error": {"code": -32601, "message": f"method not found: {method}"}}
   342	    return None  # notification — no response
   343	
   344	def main():
   345	    _utf8_stdio()
   346	    for line in sys.stdin:
   347	        line = line.strip()
   348	        if not line:
   349	            continue
   350	        try:
   351	            msg = json.loads(line)
   352	        except json.JSONDecodeError:
   353	            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
   354	                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
   355	            sys.stdout.flush()
   356	            continue
   357	        if not isinstance(msg, dict):
   358	            continue
   359	        try:
   360	            resp = handle(msg)
   361	        except Exception as e:  # request boundary: never let one request kill the server
   362	            print(f"[wmw-grok] internal error: {e}", file=sys.stderr)
   363	            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
   364	                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
   365	        if resp is not None:
   366	            sys.stdout.write(json.dumps(resp) + "\n")
   367	            sys.stdout.flush()
   368	
   369	if __name__ == "__main__":
   370	    main()
```

## ===== wmw_gemini_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-gemini — MCP stdio server wrapping the Antigravity CLI (Google seat). v1.3
     3	
     4	Persistent Gemini/Antigravity seat for Claude Code, sibling of wmw-grok:
     5	  gemini(prompt, ...)              start a new conversation -> reply + conversationId
     6	  gemini-reply(conversationId, ..) continue that conversation with full context
     7	
     8	v1.1 (2026-08-22, council findings): honest error detection, strict UTF-8 stdio,
     9	argument validation, per-request exception boundary, prompt-length guard (the
    10	CLI takes the prompt as an argv argument; Windows caps a command line at 32K
    11	chars — oversized prompts get a clean error, not a crash), and the reply footer
    12	reports the effective model/brain (`brain: UNREPORTED` when the CLI's JSON
    13	does not say — so an independence preflight can fail closed instead of assuming
    14	green = Gemini). v1.2: UUID-validated conversation ids + no-leading-dash argv guard (a crafted id
    15	could otherwise smuggle CLI flags), --conversation= equals form, absolute-path-first
    16	exe lookup, stdin closed. Install/registration: see README.md in this folder.
    17	Requires Python 3.10+ on PATH.
    18	
    19	v1.4: the read-only path now pins `--mode plan` explicitly instead of
    20	inheriting whatever the machine's settings happen to allow.
    21	
    22	Bakes in the two headless croak-fixes: --print-timeout 60m (the CLI default of
    23	5 minutes killed long tasks) and --dangerously-skip-permissions behind
    24	`always_approve` (headless runs can never click a permission prompt).
    25	
    26	Transport: newline-delimited JSON-RPC 2.0 over stdio. Stdlib only.
    27	Known limitation (documented, queued): requests are handled one at a time; a
    28	long-running call blocks the loop and cancellation is not supported.
    29	"""
    30	import json
    31	import os
    32	import shutil
    33	import subprocess
    34	import sys
    35	
    36	PRINT_TIMEOUT = "60m"
    37	PROC_TIMEOUT_S = 3900
    38	MAX_ARGV_PROMPT = 25000
    39	MAX_REPLY_CHARS = 400_000  # chars; Windows command-line hard cap is 32767 for the whole line
    40	
    41	def _utf8_stdio():
    42	    for stream in (sys.stdin, sys.stdout):
    43	        try:
    44	            stream.reconfigure(encoding="utf-8", errors="replace")
    45	        except Exception:
    46	            pass
    47	
    48	def find_agy():
    49	    # Known install path FIRST (substitute-binary defence); PATH is the fallback.
    50	    home = os.path.expanduser("~")
    51	    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    52	    for cand in (
    53	        os.path.join(local, "agy", "bin", "agy.exe"),        # Windows
    54	        os.path.join(home, ".antigravity", "bin", "agy"),    # macOS / Linux
    55	        os.path.join(home, ".local", "bin", "agy"),
    56	        os.path.join(home, "agy", "bin", "agy"),
    57	    ):
    58	        if os.path.isfile(cand):
    59	            return cand
    60	    return shutil.which("agy")
    61	
    62	_UUID_RE = __import__("re").compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")
    63	
    64	def _safe_id(value, label):
    65	    """Session ids are argv values: a leading '-' would be reparsed as a CLI flag."""
    66	    if not isinstance(value, str) or not _UUID_RE.match(value):
    67	        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
    68	    return value
    69	
    70	def _safe_argv(value, label):
    71	    if value is None:
    72	        return None
    73	    if not isinstance(value, str) or not value.strip() or value.lstrip().startswith("-"):
    74	        raise ValueError(f"'{label}' must be a non-empty string that does not start with '-'")
    75	    return value
    76	
    77	def _extract_json(raw):
    78	    dec = json.JSONDecoder()
    79	    idx = raw.find("{")
    80	    while idx != -1:
    81	        try:
    82	            obj, _ = dec.raw_decode(raw[idx:])
    83	            if isinstance(obj, dict):
    84	                return obj
    85	        except json.JSONDecodeError:
    86	            pass
    87	        idx = raw.find("{", idx + 1)
    88	    return None
    89	
    90	def run_gemini(prompt, conversation_id=None, cwd=None, model=None, always_approve=False):
    91	    exe = find_agy()
    92	    if not exe:
    93	        return True, "Antigravity CLI not found (PATH or %LOCALAPPDATA%\\agy\\bin\\agy.exe)."
    94	    if cwd and not os.path.isdir(cwd):
    95	        return True, f"cwd is not a directory: {cwd}"
    96	    if len(prompt) > MAX_ARGV_PROMPT:
    97	        return True, (f"prompt is {len(prompt)} chars; this seat's CLI takes the prompt on the "
    98	                      f"command line and Windows caps that at ~32K. Keep prompts under "
    99	                      f"{MAX_ARGV_PROMPT} chars — write long material to a file and (with "
   100	                      f"always_approve: true) ask Gemini to read the file instead.")
   101	    cmd = [exe]
   102	    if conversation_id:
   103	        cmd += [f"--conversation={conversation_id}"]
   104	    if model:
   105	        cmd += ["--model", model]
   106	    if always_approve:
   107	        cmd += ["--dangerously-skip-permissions"]
   108	    else:
   109	        # Read-only used to mean "we simply omit the skip-permissions flag", i.e. we
   110	        # trusted whatever the machine's own settings allowed. Both Grok seats flagged
   111	        # that independently on 2026-08-23. Pin the CLI's own planning mode instead, so
   112	        # the restraint is ours and explicit rather than inherited from a config file.
   113	        cmd += ["--mode", "plan"]
   114	    cmd += ["-p", prompt, "--output-format", "json", "--print-timeout", PRINT_TIMEOUT]
   115	    try:
   116	        proc = subprocess.run(
   117	            cmd, capture_output=True, text=True, encoding="utf-8",
   118	            errors="replace", timeout=PROC_TIMEOUT_S, cwd=cwd or None,
   119	            stdin=subprocess.DEVNULL,
   120	        )
   121	    except subprocess.TimeoutExpired:
   122	        return True, f"Antigravity timed out after {PROC_TIMEOUT_S}s"
   123	    except OSError as e:
   124	        return True, f"could not launch agy: {e}"
   125	    raw = (proc.stdout or "").strip()
   126	    err = (proc.stderr or "").strip()
   127	    data = _extract_json(raw)
   128	    if data is None:
   129	        return True, (f"agy exited {proc.returncode} with no parseable JSON.\n"
   130	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
   131	    text = data.get("response")
   132	    cid = data.get("conversation_id")
   133	    status = data.get("status", "unknown")
   134	    if proc.returncode != 0 or status != "SUCCESS" or not isinstance(cid, str) or not cid:
   135	        return True, (f"agy run failed (exit {proc.returncode}, status {status}, "
   136	                      f"conversationId={cid!r}).\ntext: {str(text)[:1000]}\nstderr: {err[:1000]}")
   137	    if not isinstance(text, str):
   138	        text = "" if text is None else str(text)
   139	    if len(text) > MAX_REPLY_CHARS:
   140	        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-gemini] ...truncated at {MAX_REPLY_CHARS} chars]"
   141	    # Effective model/brain: agy can rent non-Gemini brains (the Overflow Valve), and an
   142	    # independence preflight must be able to fail closed when the brain is unknown.
   143	    # NEVER promote the REQUESTED model into the brain slot: the CLI can rent a non-Gemini
   144	    # brain, and a preflight must be able to fail closed. Only the CLI's own JSON counts.
   145	    reported = data.get("model") or data.get("model_name")
   146	    brain = reported if isinstance(reported, str) and reported else (
   147	        f"UNREPORTED (requested: {model})" if model else "UNREPORTED")
   148	    footer = (f"\n\n---\n[wmw-gemini] conversationId: {cid} · status: {status}"
   149	              f" · brain: {brain} · turns: {data.get('num_turns', '?')}")
   150	    return False, text + footer
   151	
   152	def _safe_cwd(cwd, always_approve):
   153	    """A write-capable seat may not be pointed at a home or system directory."""
   154	    if not always_approve or cwd is None:
   155	        return cwd
   156	    real = os.path.realpath(cwd)
   157	    home = os.path.realpath(os.path.expanduser("~"))
   158	    banned = {home, os.path.realpath(os.path.abspath(os.sep))}
   159	    for env in ("SystemRoot", "windir", "ProgramFiles", "USERPROFILE"):
   160	        v = os.environ.get(env)
   161	        if v:
   162	            banned.add(os.path.realpath(v))
   163	    if real in banned:
   164	        raise ValueError(f"refusing a write-capable session rooted at {real} — "
   165	                         f"point cwd at a project directory")
   166	    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".config"):
   167	        if os.path.basename(real) == secret or os.sep + secret in real + os.sep:
   168	            raise ValueError(f"refusing a write-capable session inside {secret}")
   169	    return cwd
   170	
   171	def _req_str(args, key):
   172	    v = args.get(key)
   173	    if not isinstance(v, str) or not v.strip():
   174	        raise ValueError(f"'{key}' must be a non-empty string")
   175	    return v
   176	
   177	def _opt_str(args, key):
   178	    v = args.get(key)
   179	    if v is None:
   180	        return None
   181	    if not isinstance(v, str) or not v.strip():
   182	        raise ValueError(f"'{key}' must be a non-empty string when given")
   183	    return v
   184	
   185	def _opt_bool(args, key):
   186	    v = args.get(key)
   187	    if v is None:
   188	        return False
   189	    if isinstance(v, bool):
   190	        return v
   191	    if isinstance(v, str) and v.lower() in ("true", "false"):
   192	        return v.lower() == "true"
   193	    raise ValueError(f"'{key}' must be a boolean")
   194	
   195	TOOLS = [
   196	    {
   197	        "name": "gemini",
   198	        "description": (
   199	            "Start a NEW conversation with Gemini via the Antigravity CLI (Google "
   200	            "subscription seat). Returns the reply plus a conversationId footer (including the "
   201	            "effective brain — check it before counting this seat as an independent Gemini vote); "
   202	            "continue the same conversation with gemini-reply. Each fresh call is an independent, "
   203	            "blind session. Set always_approve true when Gemini must edit files or run commands "
   204	            "(headless permission prompts otherwise stall the run). Keep prompts under ~25K chars; "
   205	            "put long material in a file for Gemini to read."
   206	        ),
   207	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   208	        "inputSchema": {
   209	            "type": "object",
   210	            "properties": {
   211	                "prompt": {"type": "string", "description": "The task or message for Gemini."},
   212	                "cwd": {"type": "string", "description": "Working directory (repo path for build work)."},
   213	                "model": {"type": "string", "description": "Optional model override (agy models lists them; exact-match strings)."},
   214	                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts. Required for build work; default false."},
   215	            },
   216	            "required": ["prompt"],
   217	        },
   218	    },
   219	    {
   220	        "name": "gemini-reply",
   221	        "description": (
   222	            "Continue an existing Gemini/Antigravity conversation by conversationId (from a "
   223	            "prior gemini call's footer). Gemini retains the full prior context."
   224	        ),
   225	        "inputSchema": {
   226	            "type": "object",
   227	            "properties": {
   228	                "conversationId": {"type": "string", "description": "conversationId from a previous gemini/gemini-reply call."},
   229	                "prompt": {"type": "string", "description": "The follow-up message."},
   230	                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts this turn."},
   231	            },
   232	            "required": ["conversationId", "prompt"],
   233	        },
   234	    },
   235	]
   236	
   237	def _tool_call(name, args):
   238	    if not isinstance(args, dict):
   239	        return True, "arguments must be an object"
   240	    try:
   241	        if name == "gemini":
   242	            approve = _opt_bool(args, "always_approve")
   243	            return run_gemini(
   244	                _req_str(args, "prompt"),
   245	                cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve),
   246	                model=_safe_argv(_opt_str(args, "model"), "model"),
   247	                always_approve=approve,
   248	            )
   249	        if name == "gemini-reply":
   250	            return run_gemini(
   251	                _req_str(args, "prompt"),
   252	                conversation_id=_safe_id(args.get("conversationId"), "conversationId"),
   253	                always_approve=_opt_bool(args, "always_approve"),
   254	            )
   255	    except ValueError as e:
   256	        return True, f"invalid arguments: {e}"
   257	    return None
   258	
   259	def handle(msg):
   260	    method = msg.get("method")
   261	    mid = msg.get("id")
   262	    is_notification = "id" not in msg
   263	    if method == "initialize":
   264	        return {
   265	            "jsonrpc": "2.0", "id": mid,
   266	            "result": {
   267	                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
   268	                "capabilities": {"tools": {}},
   269	                "serverInfo": {"name": "wmw-gemini", "version": "1.4.0"},
   270	            },
   271	        }
   272	    if method == "ping":
   273	        return {"jsonrpc": "2.0", "id": mid, "result": {}}
   274	    if method == "tools/list":
   275	        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
   276	    if method == "tools/call":
   277	        params = msg.get("params") or {}
   278	        name = params.get("name")
   279	        result = _tool_call(name, params.get("arguments") or {})
   280	        if result is None:
   281	            return {"jsonrpc": "2.0", "id": mid,
   282	                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
   283	        is_err, text = result
   284	        return {"jsonrpc": "2.0", "id": mid,
   285	                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
   286	    if not is_notification:
   287	        return {"jsonrpc": "2.0", "id": mid,
   288	                "error": {"code": -32601, "message": f"method not found: {method}"}}
   289	    return None
   290	
   291	def main():
   292	    _utf8_stdio()
   293	    for line in sys.stdin:
   294	        line = line.strip()
   295	        if not line:
   296	            continue
   297	        try:
   298	            msg = json.loads(line)
   299	        except json.JSONDecodeError:
   300	            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
   301	                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
   302	            sys.stdout.flush()
   303	            continue
   304	        if not isinstance(msg, dict):
   305	            continue
   306	        try:
   307	            resp = handle(msg)
   308	        except Exception as e:
   309	            print(f"[wmw-gemini] internal error: {e}", file=sys.stderr)
   310	            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
   311	                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
   312	        if resp is not None:
   313	            sys.stdout.write(json.dumps(resp) + "\n")
   314	            sys.stdout.flush()
   315	
   316	if __name__ == "__main__":
   317	    main()
```

## ===== dispatch-guard.py =====
```python
     1	#!/usr/bin/env python3
     2	"""dispatch-guard — the controls the 2026-08-24 council said were missing.
     3	
     4	    python dispatch-guard.py preflight <repo>      # refuse a dispatch set up to fail
     5	    python dispatch-guard.py reserve <job> -t 20   # ATOMIC claim on the month's allowance
     6	    python dispatch-guard.py release <job> -t 18   # reconcile a finished job
     7	    python dispatch-guard.py status                # outstanding leases + headroom
     8	    python dispatch-guard.py yield <repo>          # cost per ACCEPTED change
     9	
    10	Three findings drove this, none of them mine:
    11	
    12	  Codex  — a time-of-check/time-of-use race. Thirteen launches each read the same
    13	           apparently-available balance before delayed vendor telemetry recorded any
    14	           of them; every check passed and their sum blew the month. A meter that
    15	           re-reads a percentage cannot prevent that. Only an ATOMIC reservation can.
    16	
    17	  Kimi   — "the rig optimizes the vendor's metric, not the shop's." Everything here
    18	           measured spend against an allowance the vendor defines and reports, and
    19	           nothing anywhere measured cost per accepted change. Hence `yield`.
    20	
    21	  Boss   — the agents had nowhere to put the code. Eleven of thirteen produced zero
    22	           lines into a repo staged deliberately empty. Hence `preflight`.
    23	
    24	WHAT THIS CANNOT DO, stated plainly so nobody mistakes it for a fence:
    25	it governs dispatches that pass THROUGH it. Cloud agents, IDE agent mode, the web
    26	dashboard, the mobile app and CI all execute on the vendor's infrastructure and obey
    27	the vendor's settings, not this file. Those lanes are closed in the vendor's control
    28	plane or not at all — see VENDOR-CHECKLIST.md.
    29	"""
    30	import argparse
    31	import datetime
    32	import io
    33	import json
    34	import os
    35	import subprocess
    36	import sys
    37	import time
    38	
    39	HOME = os.path.expanduser("~")
    40	STORE = os.environ.get("WMW_GUARD_FILE",
    41	                       os.path.join(HOME, ".anderson-method", "reservations.json"))
    42	LOCK = STORE + ".lock"
    43	
    44	MAX_CONCURRENT = int(os.environ.get("WMW_MAX_CONCURRENT_JOBS", "2"))
    45	LEASE_TTL_MIN = int(os.environ.get("WMW_LEASE_TTL_MIN", "90"))
    46	LOCK_STALE_S = 30
    47	
    48	# a dispatch may not claim more than this share of the month in one go
    49	MAX_SINGLE_CLAIM_PCT = float(os.environ.get("WMW_MAX_SINGLE_CLAIM_PCT", "10"))
    50	# total outstanding reservations may not exceed this share of the month
    51	MAX_OUTSTANDING_PCT = float(os.environ.get("WMW_MAX_OUTSTANDING_PCT", "25"))
    52	
    53	BANNED_STACK = (("maxmode", "true"), ("effort", "xhigh"), ("speed", "fast"))
    54	
    55	
    56	# ---------------------------------------------------------------- locking
    57	class Lock:
    58	    """Atomic across processes. O_EXCL create is the portable primitive.
    59	
    60	    Without this the whole tool is theatre: two launches would read the same
    61	    headroom, both pass, and both spend. That is the exact race Codex named.
    62	    """
    63	
    64	    def __enter__(self):
    65	        start = time.time()
    66	        while True:
    67	            try:
    68	                fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    69	                os.write(fd, str(os.getpid()).encode())
    70	                os.close(fd)
    71	                return self
    72	            except FileExistsError:
    73	                try:
    74	                    if time.time() - os.path.getmtime(LOCK) > LOCK_STALE_S:
    75	                        os.unlink(LOCK)       # holder died; reclaim
    76	                        continue
    77	                except OSError:
    78	                    pass
    79	                if time.time() - start > LOCK_STALE_S * 2:
    80	                    raise SystemExit("guard: could not acquire lock; is a job wedged?")
    81	                time.sleep(0.05)
    82	
    83	    def __exit__(self, *a):
    84	        try:
    85	            os.unlink(LOCK)
    86	        except OSError:
    87	            pass
    88	
    89	
    90	def _load():
    91	    try:
    92	        return json.load(io.open(STORE, encoding="utf-8"))
    93	    except (OSError, json.JSONDecodeError):
    94	        return {"jobs": {}}
    95	
    96	
    97	def _save(d):
    98	    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    99	    tmp = STORE + ".tmp"
   100	    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
   101	        json.dump(d, f, indent=2)
   102	    os.replace(tmp, STORE)      # atomic swap; never a half-written ledger
   103	
   104	
   105	def _now():
   106	    return datetime.datetime.now()
   107	
   108	
   109	def _expire(d):
   110	    """Drop leases past their TTL. A crashed job must not hold the month hostage."""
   111	    live, dropped = {}, []
   112	    for k, v in d.get("jobs", {}).items():
   113	        if v.get("state") != "open":
   114	            continue
   115	        try:
   116	            if datetime.datetime.fromisoformat(v["expires"]) < _now():
   117	                dropped.append(k)
   118	                continue
   119	        except (KeyError, ValueError):
   120	            dropped.append(k)
   121	            continue
   122	        live[k] = v
   123	    d["jobs"] = live
   124	    return dropped
   125	
   126	
   127	# ---------------------------------------------------------------- preflight
   128	def _git(repo, *args):
   129	    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
   130	                       text=True, encoding="utf-8", errors="replace")
   131	    return p.returncode, (p.stdout or "").strip()
   132	
   133	
   134	def preflight(repo, model=None, mode_flags=None, min_files=1):
   135	    """Refuse a dispatch that is set up to produce nothing, or to cost too much.
   136	
   137	    This is the boss's finding turned into a gate: an agent with no destination
   138	    still spends at full rate.
   139	    """
   140	    problems, notes = [], []
   141	
   142	    if not os.path.isdir(repo):
   143	        return 1, [f"target is not a directory: {repo}"], []
   144	
   145	    rc, _ = _git(repo, "rev-parse", "--git-dir")
   146	    if rc != 0:
   147	        problems.append(f"{repo} is not a git repository — no write-set can be verified")
   148	    else:
   149	        rc, out = _git(repo, "ls-files")
   150	        tracked = [l for l in out.splitlines() if l.strip()]
   151	        code = [f for f in tracked
   152	                if os.path.splitext(f)[1].lower() in
   153	                (".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".go", ".rs", ".java",
   154	                 ".c", ".cpp", ".h", ".rb", ".php", ".swift", ".kt", ".sh", ".ps1")]
   155	        if len(tracked) < min_files:
   156	            problems.append(f"repo has {len(tracked)} tracked files — "
   157	                            f"an agent dispatched here has nowhere to put code "
   158	                            f"(this is the Aug 21-22 failure, exactly)")
   159	        elif not code:
   160	            problems.append(f"repo has {len(tracked)} tracked files but NO source files — "
   161	                            f"staging pad, not a build target")
   162	        else:
   163	            notes.append(f"{len(tracked)} tracked files, {len(code)} source")
   164	
   165	        rc, out = _git(repo, "status", "--porcelain")
   166	        if out:
   167	            notes.append(f"{len(out.splitlines())} uncommitted changes present")
   168	
   169	    flags = {k.lower(): str(v).lower() for k, v in (mode_flags or {}).items()}
   170	    stacked = [f"{k}={v}" for k, v in BANNED_STACK if flags.get(k) == v]
   171	    if len(stacked) >= 2:
   172	        problems.append("expensive mode stack: " + " + ".join(stacked) +
   173	                        " — measured 5.5x the cheapest included model")
   174	    elif stacked:
   175	        notes.append("surcharged flag: " + stacked[0])
   176	
   177	    if model and "-fast" in model.lower():
   178	        notes.append(f"{model} is a FAST tier — measured 3.6x its non-fast twin")
   179	
   180	    return (1 if problems else 0), problems, notes
   181	
   182	
   183	# ---------------------------------------------------------------- reservation
   184	def reserve(job, est_pct, note=""):
   185	    """Claim headroom BEFORE dispatch. Atomic: the whole point.
   186	
   187	    Returns (ok, message). A refusal here is cheap; the alternative is thirteen
   188	    agents that each passed a check and together took two thirds of the month.
   189	    """
   190	    with Lock():
   191	        d = _load()
   192	        dropped = _expire(d)
   193	        open_jobs = d["jobs"]
   194	
   195	        if job in open_jobs:
   196	            return False, f"job '{job}' already holds a lease ({open_jobs[job]['est_pct']}%)"
   197	        if len(open_jobs) >= MAX_CONCURRENT:
   198	            held = ", ".join(sorted(open_jobs))
   199	            return False, (f"{len(open_jobs)} leases already open (cap {MAX_CONCURRENT}): {held}\n"
   200	                           f"  Finish or release one first. Concurrency IS the control — "
   201	                           f"the incident was 13 launches, not one bad model.")
   202	        if est_pct > MAX_SINGLE_CLAIM_PCT:
   203	            return False, (f"single claim of {est_pct}% exceeds the {MAX_SINGLE_CLAIM_PCT}% cap. "
   204	                           f"Split the job or raise WMW_MAX_SINGLE_CLAIM_PCT deliberately.")
   205	
   206	        outstanding = sum(v["est_pct"] for v in open_jobs.values())
   207	        if outstanding + est_pct > MAX_OUTSTANDING_PCT:
   208	            return False, (f"outstanding {outstanding}% + this {est_pct}% would exceed the "
   209	                           f"{MAX_OUTSTANDING_PCT}% ceiling on committed-but-unspent allowance.")
   210	
   211	        open_jobs[job] = {
   212	            "est_pct": est_pct,
   213	            "state": "open",
   214	            "note": note,
   215	            "opened": _now().isoformat(timespec="seconds"),
   216	            "expires": (_now() + datetime.timedelta(minutes=LEASE_TTL_MIN)
   217	                        ).isoformat(timespec="seconds"),
   218	        }
   219	        _save(d)
   220	        msg = (f"RESERVED  {job}  {est_pct}% for up to {LEASE_TTL_MIN} min "
   221	               f"({len(open_jobs)}/{MAX_CONCURRENT} leases, {outstanding + est_pct}% committed)")
   222	        if dropped:
   223	            msg += f"\n  (expired and reclaimed: {', '.join(dropped)})"
   224	        return True, msg
   225	
   226	
   227	def release(job, actual_pct=None, lines=None):
   228	    with Lock():
   229	        d = _load()
   230	        _expire(d)
   231	        v = d["jobs"].pop(job, None)
   232	        if not v:
   233	            return False, f"no open lease named '{job}'"
   234	        hist = d.setdefault("history", [])
   235	        hist.append({"job": job, "est_pct": v["est_pct"], "actual_pct": actual_pct,
   236	                     "lines": lines, "closed": _now().isoformat(timespec="seconds"),
   237	                     "note": v.get("note", "")})
   238	        d["history"] = hist[-200:]
   239	        _save(d)
   240	        out = f"released {job} (reserved {v['est_pct']}%"
   241	        if actual_pct is not None:
   242	            out += f", actual {actual_pct}%"
   243	        out += ")"
   244	        if lines is not None and actual_pct:
   245	            if lines == 0:
   246	                out += "\n  ZERO LINES for a real spend — this is the failed-work multiplier."
   247	            else:
   248	                out += f"\n  {actual_pct/lines:.4f}% of the month per accepted line"
   249	        return True, out
   250	
   251	
   252	# ---------------------------------------------------------------- yield
   253	FAST_SURCHARGE = ("-fast",)          # measured 3.6x-5.5x their non-fast twins
   254	
   255	
   256	def find_events_csv():
   257	    """Newest Cursor usage export, if the operator dropped one somewhere obvious.
   258	
   259	    Desktop is OneDrive-redirected on this fleet, so it is resolved, never guessed.
   260	    """
   261	    import glob
   262	    home = os.path.expanduser("~")
   263	    spots = [os.path.join(home, "Downloads"),
   264	             os.path.join(home, "OneDrive", "Desktop"),
   265	             os.path.join(home, ".claude", "uploads")]
   266	    hits = []
   267	    for s in spots:
   268	        hits += glob.glob(os.path.join(s, "**", "*usageevents*.csv"), recursive=True)
   269	    return max(hits, key=os.path.getmtime) if hits else None
   270	
   271	
   272	def load_events(path, since=None):
   273	    """Parse Cursor's per-event usage export — the ONLY meter that sees every lane.
   274	
   275	    Our own ledger records what the MCP seats dispatched. This file records what the
   276	    ACCOUNT spent, cloud agents and IDE included, which is precisely the 96% our
   277	    ledger was blind to on 2026-08-24.
   278	    """
   279	    import csv
   280	    rows = []
   281	    with io.open(path, encoding="utf-8-sig", newline="") as f:
   282	        for r in csv.DictReader(f):
   283	            d = (r.get("Date") or "")[:10]
   284	            if since and d < since:
   285	                continue
   286	            model = (r.get("Model") or "(unnamed)").strip()
   287	            try:
   288	                tok = int(r.get("Total Tokens") or 0)
   289	            except ValueError:
   290	                tok = 0
   291	            cost = 0.0
   292	            c = (r.get("Cost") or "").strip()
   293	            if c and c.lower() != "included":
   294	                try:
   295	                    cost = float(c.lstrip("$"))
   296	                except ValueError:
   297	                    pass
   298	            lane = ("cloud-agent" if (r.get("Cloud Agent ID") or "").strip()
   299	                    else "automation" if (r.get("Automation ID") or "").strip()
   300	                    else "interactive")
   301	            rows.append({"date": d, "model": model, "tokens": tok, "cost": cost,
   302	                         "lane": lane, "max": (r.get("Max Mode") or "").strip() == "Yes"})
   303	    return rows
   304	
   305	
   306	def yield_report(repo, days=7, events_csv=None):
   307	    """Cost per ACCEPTED change — the shop's own metric, not the vendor's."""
   308	    since = (_now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
   309	    rc, out = _git(repo, "log", f"--since={since}", "--pretty=%H", "--numstat")
   310	    if rc != 0:
   311	        return 1, f"not a git repo: {repo}"
   312	    added = removed = commits = 0
   313	    for line in out.splitlines():
   314	        parts = line.split("\t")
   315	        if len(parts) == 3:
   316	            try:
   317	                added += int(parts[0]); removed += int(parts[1])
   318	            except ValueError:
   319	                pass
   320	        elif len(parts) == 1 and len(line) == 40:
   321	            commits += 1
   322	
   323	    d = _load()
   324	    hist = [h for h in d.get("history", []) if h.get("closed", "") >= since]
   325	
   326	    # Token truth comes from the spend ledger the seats already write, not from
   327	    # hand-entered numbers. A metric nobody has to remember to record is the only
   328	    # kind that survives contact with a real week.
   329	    ledger = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bench-spend.jsonl")
   330	    calls, toks = 0, 0
   331	    if os.path.exists(ledger):
   332	        for line in io.open(ledger, encoding="utf-8"):
   333	            line = line.strip()
   334	            if not line:
   335	                continue
   336	            try:
   337	                r = json.loads(line)
   338	            except json.JSONDecodeError:
   339	                continue
   340	            if r.get("ts", "") < since:
   341	                continue
   342	            calls += 1
   343	            u = r.get("usage") or {}
   344	            if isinstance(u, dict):
   345	                toks += sum(int(u.get(k, 0) or 0) for k in
   346	                            ("inputTokens", "outputTokens", "cacheReadTokens"))
   347	
   348	    L = [f"YIELD — {os.path.basename(os.path.abspath(repo))}, last {days} days",
   349	         "",
   350	         f"  ACCEPTED OUTPUT:  {commits} commits, +{added}/-{removed} lines"]
   351	
   352	    # ---- vendor ground truth, if an export is available ------------------
   353	    ev = load_events(events_csv, since) if events_csv else []
   354	    if ev:
   355	        etok = sum(e["tokens"] for e in ev)
   356	        ecost = sum(e["cost"] for e in ev)
   357	        L.append(f"  ACCOUNT SPEND:    {len(ev)} events, {etok:,} tokens"
   358	                 + (f", ${ecost:,.2f} billed" if ecost else " (all within included limits)"))
   359	        if added:
   360	            L += ["", f"  >>> COST PER ACCEPTED LINE: {etok/added:,.0f} tokens <<<"]
   361	        else:
   362	            L += ["", "  >>> COST PER ACCEPTED LINE: UNDEFINED — real spend, NO accepted",
   363	                  "      output in this repo. The failed-work multiplier."]
   364	
   365	        lanes = {}
   366	        for e in ev:
   367	            d = lanes.setdefault(e["lane"], [0, 0])
   368	            d[0] += 1
   369	            d[1] += e["tokens"]
   370	        L += ["", "  BY LANE (this is what the seat ledger cannot see):"]
   371	        for lane, (n, t) in sorted(lanes.items(), key=lambda x: -x[1][1]):
   372	            gov = "guarded" if lane == "interactive" else "VENDOR-SIDE, ungoverned here"
   373	            L.append(f"    {lane:14} {n:>5} events  {t:>13,} tok  {t/etok*100:>5.1f}%   {gov}")
   374	
   375	        fast = [e for e in ev if any(s in e["model"] for s in FAST_SURCHARGE)]
   376	        if fast:
   377	            ft = sum(e["tokens"] for e in fast)
   378	            L += ["", f"  ⚠ SURCHARGED FAST TIERS: {ft:,} tok ({ft/etok*100:.1f}% of spend)",
   379	                  "    Fast tiers measured 3.6x-5.5x their non-fast twins. Same work,",
   380	                  "    same models, a fraction of the bill if the default is changed."]
   381	        mx = [e for e in ev if e["max"]]
   382	        if mx:
   383	            L.append(f"  ⚠ MAX MODE: {sum(e['tokens'] for e in mx):,} tok on top of the above")
   384	
   385	        top = sorted({e["model"] for e in ev},
   386	                     key=lambda m: -sum(e["tokens"] for e in ev if e["model"] == m))[:5]
   387	        L += ["", "  TOP MODELS:"]
   388	        for m in top:
   389	            t = sum(e["tokens"] for e in ev if e["model"] == m)
   390	            L.append(f"    {m:32} {t:>13,}  {t/etok*100:>5.1f}%")
   391	    else:
   392	        L.append(f"  SEAT LEDGER ONLY:  {calls} calls, {toks:,} tokens "
   393	                 f"({len(hist)} guarded leases)")
   394	        if added and toks:
   395	            L += ["", f"  >>> COST PER ACCEPTED LINE: {toks/added:,.0f} tokens (MCP lane only) <<<"]
   396	        L += ["", "  NO VENDOR EXPORT SUPPLIED — this counts only what the MCP seats",
   397	              "  dispatched. On 2026-08-24 that was 3% of real account spend. Download",
   398	              "  the per-event CSV (vendor usage page -> Export CSV) and pass --events,",
   399	              "  or the number below is your own corner of the bill, not the bill."]
   400	
   401	    L += ["", "  Note: git output is local time, vendor events are UTC — a boundary day",
   402	          "  can straddle. Widen --days before drawing a conclusion from one day."]
   403	    return 0, "\n".join(L)
   404	
   405	
   406	# ---------------------------------------------------------------- cli
   407	def main():
   408	    try:
   409	        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
   410	    except Exception:
   411	        pass
   412	    ap = argparse.ArgumentParser(description=__doc__,
   413	                                 formatter_class=argparse.RawDescriptionHelpFormatter)
   414	    sub = ap.add_subparsers(dest="cmd")
   415	
   416	    p = sub.add_parser("preflight"); p.add_argument("repo")
   417	    p.add_argument("--model"); p.add_argument("--max-mode", action="store_true")
   418	    p.add_argument("--effort"); p.add_argument("--speed")
   419	
   420	    p = sub.add_parser("reserve"); p.add_argument("job")
   421	    p.add_argument("-t", "--est-pct", type=float, required=True,
   422	                   help="estimated share of the MONTH'S allowance, in percent")
   423	    p.add_argument("-n", "--note", default="")
   424	
   425	    p = sub.add_parser("release"); p.add_argument("job")
   426	    p.add_argument("-t", "--actual-pct", type=float)
   427	    p.add_argument("-l", "--lines", type=int, help="accepted lines this job produced")
   428	
   429	    sub.add_parser("status")
   430	    p = sub.add_parser("yield"); p.add_argument("repo"); p.add_argument("--days", type=int, default=7)
   431	    p.add_argument("--events", help="Cursor per-event usage CSV (vendor usage page -> Export CSV). "
   432	                                    "Omit to auto-discover the newest one.")
   433	    p.add_argument("--no-auto", action="store_true", help="do not auto-discover an export")
   434	
   435	    a = ap.parse_args()
   436	
   437	    if a.cmd == "preflight":
   438	        flags = {"maxmode": a.max_mode, "effort": a.effort, "speed": a.speed}
   439	        rc, problems, notes = preflight(a.repo, a.model, flags)
   440	        for n in notes:
   441	            print(f"  ok   {n}")
   442	        for pr in problems:
   443	            print(f"  STOP {pr}")
   444	        print("\nPREFLIGHT: " + ("REFUSED — fix the above before dispatching."
   445	                                 if rc else "clear."))
   446	        return rc
   447	
   448	    if a.cmd == "reserve":
   449	        ok, msg = reserve(a.job, a.est_pct, a.note)
   450	        print(("  " if ok else "  REFUSED — ") + msg)
   451	        return 0 if ok else 1
   452	
   453	    if a.cmd == "release":
   454	        ok, msg = release(a.job, a.actual_pct, a.lines)
   455	        print("  " + msg)
   456	        return 0 if ok else 1
   457	
   458	    if a.cmd == "status":
   459	        with Lock():
   460	            d = _load(); dropped = _expire(d); _save(d)
   461	        jobs = d.get("jobs", {})
   462	        print(f"RESERVATIONS  ({STORE})\n")
   463	        if not jobs:
   464	            print("  no open leases.")
   465	        for k, v in sorted(jobs.items()):
   466	            print(f"  {k:24} {v['est_pct']:>5}%  until {v['expires'][11:16]}  {v.get('note','')}")
   467	        print(f"\n  {len(jobs)}/{MAX_CONCURRENT} leases, "
   468	              f"{sum(v['est_pct'] for v in jobs.values()):.1f}% committed "
   469	              f"(ceiling {MAX_OUTSTANDING_PCT}%)")
   470	        if dropped:
   471	            print(f"  reclaimed expired: {', '.join(dropped)}")
   472	        return 0
   473	
   474	    if a.cmd == "yield":
   475	        csvp = a.events or (None if a.no_auto else find_events_csv())
   476	        if csvp and not a.events:
   477	            print(f"  (auto-discovered export: {csvp})\n")
   478	        rc, out = yield_report(a.repo, a.days, csvp)
   479	        print(out)
   480	        return rc
   481	
   482	    ap.print_help()
   483	    return 2
   484	
   485	
   486	if __name__ == "__main__":
   487	    sys.exit(main() or 0)
```

## ===== allowance.py =====
```python
     1	#!/usr/bin/env python3
     2	"""allowance — the record a metered seat checks before it spends.
     3	
     4	    python allowance.py                       # show what is granted
     5	    python allowance.py grant cursor 10/week --days 30
     6	    python allowance.py grant cursor 25/week --forever
     7	    python allowance.py revoke cursor
     8	    python allowance.py check cursor          # exit 0 if a call is permitted
     9	
    10	THE COUNCIL SEAT LAW (SPINE v2.5) gates SPENDING, not vendor class. Any seat may
    11	sit on a council; a seat that CAN spend needs a recorded allowance first — asked
    12	once, carrying a bound, and by default expiring, because a yes given once at
    13	midnight should not silently govern next year.
    14	
    15	The record lives on the operator's own machine, never in the method's repo, so
    16	nobody inherits another shop's permission. Delete it and every metered seat goes
    17	back to asking.
    18	"""
    19	import datetime
    20	import io
    21	import json
    22	import os
    23	import sys
    24	
    25	HOME = os.path.expanduser("~")
    26	STORE = os.environ.get(
    27	    "WMW_ALLOWANCE_FILE",
    28	    os.path.join(HOME, ".anderson-method", "allowances.json"))
    29	
    30	DEFAULT_BOUND = "10/week"
    31	DEFAULT_DAYS = 30          # a grant expires unless made permanent, on purpose
    32	
    33	WINDOWS = {"day": 1, "week": 7, "month": 30}
    34	
    35	def _load():
    36	    try:
    37	        return json.load(io.open(STORE, encoding="utf-8"))
    38	    except (OSError, json.JSONDecodeError):
    39	        return {}
    40	
    41	def _save(d):
    42	    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    43	    with io.open(STORE, "w", encoding="utf-8", newline="") as f:
    44	        json.dump(d, f, indent=2)
    45	
    46	def _parse_bound(text):
    47	    """'10/week' -> (10, 'week'). Raises ValueError on anything else."""
    48	    n, _, window = text.partition("/")
    49	    window = (window or "week").strip().lower().rstrip("s")
    50	    if window not in WINDOWS:
    51	        raise ValueError(f"window must be day, week or month — got {window!r}")
    52	    return int(n), window
    53	
    54	def grant(seat, bound=DEFAULT_BOUND, days=DEFAULT_DAYS, forever=False):
    55	    calls, window = _parse_bound(bound)
    56	    d = _load()
    57	    now = datetime.datetime.now()
    58	    d[seat] = {
    59	        "calls": calls,
    60	        "window": window,
    61	        "granted": now.isoformat(timespec="seconds"),
    62	        "expires": None if forever else (now + datetime.timedelta(days=days)).isoformat(timespec="seconds"),
    63	    }
    64	    _save(d)
    65	    return d[seat]
    66	
    67	def revoke(seat):
    68	    d = _load()
    69	    existed = d.pop(seat, None) is not None
    70	    _save(d)
    71	    return existed
    72	
    73	def status(seat):
    74	    """Returns (permitted, reason). A seat with no grant is NOT permitted."""
    75	    g = _load().get(seat)
    76	    if not g:
    77	        return False, ("no allowance recorded — this seat may not spend. Ask the operator, "
    78	                       f"then: python allowance.py grant {seat} {DEFAULT_BOUND}")
    79	    exp = g.get("expires")
    80	    if exp:
    81	        try:
    82	            if datetime.datetime.fromisoformat(exp) < datetime.datetime.now():
    83	                return False, (f"the allowance expired on {exp[:10]} — grants expire on purpose. "
    84	                               f"Re-ask the operator, then re-grant.")
    85	        except ValueError:
    86	            return False, "allowance has an unreadable expiry; re-grant it"
    87	    return True, f"{g['calls']} calls per {g['window']}" + (
    88	        "" if not exp else f", until {exp[:10]}")
    89	
    90	def main():
    91	    a = sys.argv[1:]
    92	    try:
    93	        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    94	    except Exception:
    95	        pass
    96	
    97	    if not a or a[0] == "show":
    98	        d = _load()
    99	        print(f"ALLOWANCES  ({STORE})\n")
   100	        if not d:
   101	            print("  none recorded — every metered seat will ask before it spends.")
   102	            return
   103	        for seat in sorted(d):
   104	            ok, why = status(seat)
   105	            print(f"  {'OK  ' if ok else 'STOP'}  {seat:12} {why}")
   106	        return
   107	
   108	    cmd = a[0]
   109	    if cmd == "grant":
   110	        if len(a) < 2:
   111	            print("usage: allowance.py grant <seat> [N/window] [--days N | --forever]"); return 2
   112	        seat = a[1]
   113	        bound = a[2] if len(a) > 2 and not a[2].startswith("--") else DEFAULT_BOUND
   114	        forever = "--forever" in a
   115	        days = DEFAULT_DAYS
   116	        if "--days" in a:
   117	            days = int(a[a.index("--days") + 1])
   118	        g = grant(seat, bound, days, forever)
   119	        when = "never expires" if g["expires"] is None else f"expires {g['expires'][:10]}"
   120	        print(f"granted: {seat} may spend {g['calls']} calls per {g['window']} ({when})")
   121	        return
   122	
   123	    if cmd == "revoke":
   124	        if len(a) < 2:
   125	            print("usage: allowance.py revoke <seat>"); return 2
   126	        print(f"revoked: {a[1]}" if revoke(a[1]) else f"no allowance was recorded for {a[1]}")
   127	        return
   128	
   129	    if cmd == "check":
   130	        if len(a) < 2:
   131	            print("usage: allowance.py check <seat>"); return 2
   132	        ok, why = status(a[1])
   133	        print(("PERMITTED — " if ok else "REFUSED — ") + why)
   134	        return 0 if ok else 1
   135	
   136	    print(__doc__)
   137	    return 2
   138	
   139	if __name__ == "__main__":
   140	    sys.exit(main() or 0)
```

## ===== armcheck.py =====
```python
     1	import json, subprocess, sys, os, glob, io, shutil
     2	sys.stdout.reconfigure(encoding="utf-8", errors="replace")
     3	SEATS = r"C:\Sync\Projects\andersons-dispatch-deck\mcp-seats"
     4	PLAYPEN = r"C:\Sync\_playpen\cursor"
     5	RESV = os.path.join(os.path.expanduser("~"), ".anderson-method", "reservations.json")
     6	
     7	def seat(server):
     8	    p = subprocess.Popen([sys.executable, os.path.join(SEATS, server)],
     9	                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    10	                         text=True, encoding="utf-8", bufsize=1)
    11	    def rpc(m):
    12	        p.stdin.write(json.dumps(m)+"\n"); p.stdin.flush()
    13	        if "id" in m: return json.loads(p.stdout.readline())
    14	    return p, rpc
    15	
    16	results = []
    17	def check(label, ok, detail=""):
    18	    results.append((label, ok, detail))
    19	    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    20	
    21	print("=== 1. all three seats start and list tools ===")
    22	for srv, want in (("wmw_grok_mcp.py", ["grok","grok-reply"]),
    23	                  ("wmw_gemini_mcp.py", ["gemini","gemini-reply"]),
    24	                  ("wmw_cursor_mcp.py", ["cursor","cursor-reply"])):
    25	    p, rpc = seat(srv)
    26	    r = rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    27	    v = r["result"]["serverInfo"]
    28	    t = [x["name"] for x in rpc({"jsonrpc":"2.0","id":2,"method":"tools/list"})["result"]["tools"]]
    29	    check(f"{srv:22} v{v['version']}", t == want, ",".join(t))
    30	    p.stdin.close(); p.wait(timeout=10)
    31	
    32	print("\n=== 2. the guards that cost money or safety ===")
    33	p, rpc = seat("wmw_cursor_mcp.py")
    34	rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    35	def cur(args):
    36	    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":args}})["result"]
    37	check("credit model refused without spend_credits", cur({"prompt":"x","model":"kimi-k3-high"})["isError"])
    38	check("auto/UNKNOWN refused even WITH spend_credits", cur({"prompt":"x","model":"auto","spend_credits":True})["isError"])
    39	check("model id with metacharacters refused", cur({"prompt":"x","model":"bad;id&whoami"})["isError"])
    40	check("write-capable with no cwd refused", cur({"prompt":"x","always_approve":True})["isError"])
    41	sysroot = os.environ.get("SystemRoot", r"C:\Windows")
    42	check("write-capable in System32 refused", cur({"prompt":"x","always_approve":True,"cwd":os.path.join(sysroot,"System32")})["isError"])
    43	check("YOLO on a non-allowlisted model refused",
    44	      "WRITE REFUSED" in cur({"prompt":"x","model":"gpt-5.3-codex","always_approve":True,"cwd":PLAYPEN,"spend_credits":True})["content"][0]["text"])
    45	
    46	# --- the guard, wired 2026-08-24 (council). Regression for the burn incident. ---
    47	_empty = os.path.join(PLAYPEN, "_armcheck_emptyrepo")
    48	os.makedirs(_empty, exist_ok=True)
    49	subprocess.run(["git","-C",_empty,"init","-q"], capture_output=True)
    50	check("build dispatch at an EMPTY repo refused (preflight)",
    51	      "PREFLIGHT REFUSED" in cur({"prompt":"build it","always_approve":True,"cwd":_empty,
    52	                                  "model":"composer-2.5"})["content"][0]["text"])
    53	shutil.rmtree(_empty, ignore_errors=True)
    54	check("no lease left behind after a refused dispatch",
    55	      not (json.load(io.open(RESV, encoding="utf-8")).get("jobs") if os.path.exists(RESV) else {}))
    56	p.stdin.close(); p.wait(timeout=10)
    57	
    58	p, rpc = seat("wmw_grok_mcp.py")
    59	rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    60	def gk(tool,args):
    61	    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":tool,"arguments":args}})["result"]
    62	check("grok: crafted sessionId cannot smuggle flags", gk("grok-reply",{"sessionId":"--always-approve","prompt":"x"})["isError"])
    63	check("grok: reply escalating with no cwd refused", gk("grok-reply",{"sessionId":"01a02b9c-384b-72d0-9c6f-f5ab60147aba","prompt":"x","always_approve":True})["isError"])
    64	p.stdin.close(); p.wait(timeout=10)
    65	
    66	print("\n=== 3. meters readable ===")
    67	r = subprocess.run([sys.executable, os.path.join(SEATS,"read-meters.py"), "--json"],
    68	                   capture_output=True, text=True, encoding="utf-8", timeout=120)
    69	try:
    70	    d = json.loads(r.stdout)
    71	    check("grok meter readable", d.get("grok",{}).get("weekly_percent_used") is not None,
    72	          f"{d.get('grok',{}).get('weekly_percent_used')}%")
    73	    check("cursor meter readable", d.get("cursor",{}).get("cursor_models_percent_used") is not None,
    74	          f"{d.get('cursor',{}).get('cursor_models_percent_used')}%")
    75	except Exception as e:
    76	    check("meters readable", False, str(e))
    77	
    78	print("\n=== 4. playpen intact, no stray spill files ===")
    79	check("playpen exists", os.path.isdir(PLAYPEN))
    80	spill = glob.glob(os.path.join(PLAYPEN,"prompts","*"))
    81	check("no leftover prompt handoffs", not spill, f"{len(spill)} found")
    82	
    83	bad = [l for l,ok,_ in results if not ok]
    84	print(f"\n{'='*46}\n{len(results)-len(bad)}/{len(results)} PASS" + (f"  — FAILED: {bad}" if bad else "  — ALL ARMED"))
```

## ===== read-meters.py =====
```python
     1	#!/usr/bin/env python3
     2	"""read-meters — what is actually left in the tanks.
     3	
     4	    python read-meters.py            # both vendors
     5	    python read-meters.py --grok     # xAI weekly pool only
     6	    python read-meters.py --cursor   # Cursor's two pools only
     7	    python read-meters.py --json     # machine-readable, for before/after diffs
     8	
     9	WHY THIS EXISTS. Neither vendor publishes the SIZE of an included pool, and
    10	neither one's API will tell you: both return only a PERCENTAGE USED, never an
    11	absolute cap. That is architectural, not an oversight — you cannot learn a pool's
    12	size by inspecting traffic. The only way to size one is to burn a known amount of
    13	work and watch the percentage move. This tool reads the percentage so that
    14	measurement is possible; `bench-burn.py` reports what a burn cost.
    15	
    16	Endpoints (found 2026-08-23; both undocumented, both may change without notice):
    17	  xAI     GET  https://cli-chat-proxy.grok.com/v1/billing?format=credits
    18	          auth: the OIDC bearer token inside ~/.grok/auth.json
    19	          gives: weekly pool percent, itemised by product (Build / Chat / Imagine)
    20	  Cursor  POST https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage
    21	          auth: accessToken from %APPDATA%\\Cursor\\auth.json, Connect-RPC headers
    22	          gives: autoPercentUsed  = the INCLUDED "Cursor Models" pool
    23	                 apiPercentUsed   = the metered "Other Models" credit pool
    24	                 bonusSpend       = free usage granted on top of what you paid for
    25	
    26	Read-only. Nothing here spends anything or changes any account.
    27	"""
    28	import datetime
    29	import io
    30	import json
    31	import os
    32	import sys
    33	import time
    34	import urllib.request
    35	
    36	TIMEOUT = 45
    37	
    38	def _get(url, headers, data=None):
    39	    req = urllib.request.Request(url, data=data, headers=headers)
    40	    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
    41	        return json.load(r)
    42	
    43	def _as_epoch(v):
    44	    """expires_at may be a unix number or an ISO-8601 string; accept either."""
    45	    if v is None:
    46	        return None
    47	    try:
    48	        return float(v)
    49	    except (TypeError, ValueError):
    50	        pass
    51	    try:
    52	        t = str(v).replace("Z", "+00:00")
    53	        # trim sub-second precision beyond microseconds, which fromisoformat rejects
    54	        if "." in t:
    55	            head, _, tail = t.partition(".")
    56	            frac = "".join(ch for ch in tail if ch.isdigit())[:6]
    57	            rest = tail[len(frac):].lstrip("0123456789")
    58	            t = f"{head}.{frac}{rest}"
    59	        return datetime.datetime.fromisoformat(t).timestamp()
    60	    except (TypeError, ValueError):
    61	        return None
    62	
    63	def _grok_token(auth):
    64	    """Pull the access token and its expiry out of the CLI's auth file.
    65	
    66	    The file is keyed by issuer+client id, with the token under 'key' and a unix
    67	    'expires_at' beside it. These are short-lived (about an hour); the CLI itself
    68	    refreshes on use, so an expired token means 'run a grok command', not 'broken'.
    69	    """
    70	    for node in auth.values():
    71	        if isinstance(node, dict) and isinstance(node.get("key"), str):
    72	            return node.get("key"), node.get("expires_at")
    73	    # fall back to any JWT-shaped string, in case the layout changes
    74	    def walk(o):
    75	        if isinstance(o, dict):
    76	            for v in o.values():
    77	                if isinstance(v, str) and v.count(".") == 2 and len(v) > 100:
    78	                    return v
    79	                r = walk(v)
    80	                if r:
    81	                    return r
    82	        elif isinstance(o, list):
    83	            for v in o:
    84	                r = walk(v)
    85	                if r:
    86	                    return r
    87	        return None
    88	    return walk(auth), None
    89	
    90	def read_grok():
    91	    path = os.path.expanduser(r"~\.grok\auth.json")
    92	    if not os.path.exists(path):
    93	        return {"error": "no ~/.grok/auth.json — is the Grok CLI logged in?"}
    94	    tok, expires_at = _grok_token(json.load(io.open(path, encoding="utf-8")))
    95	    if not tok:
    96	        return {"error": "no bearer token found in ~/.grok/auth.json"}
    97	    exp_ts = _as_epoch(expires_at)
    98	    if exp_ts and exp_ts < time.time():
    99	        age = int(time.time() - exp_ts)
   100	        return {"error": (f"the CLI's access token expired {age // 60} min ago. It refreshes itself "
   101	                          f"on use — run any grok command (e.g. `grok -p hi`) and read again.")}
   102	    try:
   103	        d = _get("https://cli-chat-proxy.grok.com/v1/billing?format=credits",
   104	                 {"Authorization": "Bearer " + tok, "User-Agent": "grok-cli"})
   105	    except Exception as e:
   106	        return {"error": f"grok billing request failed: {e}"}
   107	    c = d.get("config", d)
   108	    return {
   109	        "weekly_percent_used": c.get("creditUsagePercent"),
   110	        "by_product": {p.get("product"): p.get("usagePercent")
   111	                       for p in c.get("productUsage", [])},
   112	        "period_start": str(c.get("billingPeriodStart"))[:19],
   113	        "period_end": str(c.get("billingPeriodEnd"))[:19],
   114	        "prepaid_balance": (c.get("prepaidBalance") or {}).get("val"),
   115	        "on_demand_cap": (c.get("onDemandCap") or {}).get("val"),
   116	    }
   117	
   118	def read_cursor():
   119	    path = os.path.expandvars(r"%APPDATA%\Cursor\auth.json")
   120	    if not os.path.exists(path):
   121	        return {"error": "no %APPDATA%/Cursor/auth.json — sign in to the Cursor app once"}
   122	    tok = json.load(io.open(path, encoding="utf-8")).get("accessToken")
   123	    if not tok:
   124	        return {"error": "no accessToken in Cursor auth.json"}
   125	    try:
   126	        d = _get("https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage",
   127	                 {"Authorization": "Bearer " + tok,
   128	                  "Content-Type": "application/json",
   129	                  "Connect-Protocol-Version": "1"},
   130	                 data=b"{}")
   131	    except Exception as e:
   132	        return {"error": f"cursor usage request failed: {e}"}
   133	    pu = d.get("planUsage", {}) or {}
   134	    def ms(v):
   135	        try:
   136	            return datetime.datetime.fromtimestamp(int(v) / 1000).strftime("%Y-%m-%d")
   137	        except (TypeError, ValueError):
   138	            return str(v)
   139	    return {
   140	        "cursor_models_percent_used": pu.get("autoPercentUsed"),   # the INCLUDED pool
   141	        "other_models_percent_used": pu.get("apiPercentUsed"),     # the metered pool
   142	        "total_percent_used": pu.get("totalPercentUsed"),
   143	        "included_spend_usd": (pu.get("includedSpend") or 0) / 100,
   144	        "bonus_spend_usd": (pu.get("bonusSpend") or 0) / 100,
   145	        "total_spend_usd": (pu.get("totalSpend") or 0) / 100,
   146	        "cycle_start": ms(d.get("billingCycleStart")),
   147	        "cycle_end": ms(d.get("billingCycleEnd")),
   148	        "display_message": d.get("displayMessage"),
   149	    }
   150	
   151	def main():
   152	    args = sys.argv[1:]
   153	    want_grok = "--cursor" not in args
   154	    want_cursor = "--grok" not in args
   155	    out = {"read_at": datetime.datetime.now().isoformat(timespec="seconds")}
   156	    if want_grok:
   157	        out["grok"] = read_grok()
   158	    if want_cursor:
   159	        out["cursor"] = read_cursor()
   160	
   161	    if "--json" in args:
   162	        print(json.dumps(out, indent=2))
   163	        return
   164	
   165	    try:
   166	        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
   167	    except Exception:
   168	        pass
   169	    print(f"METERS — {out['read_at']}\n")
   170	    g = out.get("grok")
   171	    if g:
   172	        if g.get("error"):
   173	            print(f"  xAI / Grok    : {g['error']}")
   174	        else:
   175	            print(f"  xAI / Grok    weekly pool {g['weekly_percent_used']}% used"
   176	                  f"   (resets {g['period_end'][:10]})")
   177	            for prod, pct in (g.get("by_product") or {}).items():
   178	                print(f"                    {prod:14} {pct}%")
   179	            print("                    ONE tank: Build, Chat and Imagine all drain it")
   180	    c = out.get("cursor")
   181	    if c:
   182	        print()
   183	        if c.get("error"):
   184	            print(f"  Cursor        : {c['error']}")
   185	        else:
   186	            print(f"  Cursor        cycle {c['cycle_start']} -> {c['cycle_end']}")
   187	            print(f"                    Cursor Models (free)  {c['cursor_models_percent_used']}%"
   188	                  f"   <- Composer + Cursor Grok")
   189	            print(f"                    Other Models (credit) {c['other_models_percent_used']}%"
   190	                  f"   <- everything else")
   191	            print(f"                    spend: ${c['total_spend_usd']:.2f} total = "
   192	                  f"${c['included_spend_usd']:.2f} paid + ${c['bonus_spend_usd']:.2f} bonus")
   193	            if c.get("display_message"):
   194	                print(f"                    vendor says: {c['display_message']}")
   195	    print("\n  Neither vendor publishes a pool SIZE — only a percentage. To learn the size,")
   196	    print("  burn a known amount and watch the percentage move (see bench-burn.py).")
   197	
   198	if __name__ == "__main__":
   199	    main()
```

## YOUR LENS — THE EXPLOIT WRITER (🌙)
You have reviewed this shop's method twice today and found real flaws both times. Now go at the
CODE. Weight Q1 and Q2. For every finding, write the concrete attack: the exact prompt, model
id, session id, cwd or file contents an attacker supplies, and what they get. A finding you
cannot turn into a reproduction is a SUSPECTED finding and must be labelled as one.
