# TOP-TO-BOTTOM ADVERSARIAL AUDIT — 🔵 Codex, deep pass

A guest seat spent today writing working exploits against this harness and found ten real
defects, every one confirmed in source. **All of them are now fixed.** You are being brought in
because you are the sharpest code reviewer in this shop and you did not write any of it.

**Your job is not to re-find what it found. Your job is to find what it MISSED, and to check
whether the fixes are actually correct.** A fix that closes one path and opens another is worth
more to know about than a fresh medium-severity finding.

## What it found, and what was done (verify these are genuinely closed)

1. **`time` never imported** while `run_cursor` called `time.time()` — the reservation guard was
   DEAD CODE that raised NameError on every guarded write dispatch. Fix: import time, plus a
   canary that performs a real guarded dispatch. *(The reason it survived: two green tests, and
   neither ever reached the line. Look for more of that shape.)*
2. **Spend ledger lived in the playpen** — the one directory a write-capable session may always
   write. Delete it and the council lock silently unlocks. Fix: moved to `~/.anderson-method/`.
3. **The granted window was never enforced.** `allowance.py` records "N per window"; the seat
   read only the count and policed a hardcoded 600s, so "10/week" ran ~1000x looser than
   written. Fix: the seat now reads `window_seconds()`.
4. **APPDATA / LOCALAPPDATA unprotected** — a write-capable session could root where this rig's
   credentials and the vendor CLIs live. Fix: containment ban on both.
5. **`_guard()` failed OPEN** — any load error returned None and the caller's truthiness test
   skipped preflight AND reservation silently. Fix: returns the exception; a write-capable
   dispatch is refused when the guard cannot load.
6. **`reserve` accepted a negative claim**, passing the upper cap and SUBTRACTING from
   outstanding — manufacturing headroom. Fix: positive claims only.
7. **`release` checked no ownership** — any caller could free any lease, so two cheap
   reservations DoS the operator's own rig for the TTL. Fix: leases carry an owner token.
8. **Unbounded JSON-RPC frame** — memory exhaustion primitive. Fix: 8MB cap.
9. **Lock reclaimed on age alone** — a slow-but-living holder had its lock stolen, so two
   processes both believed they held it. Fix: verify the recorded PID is dead; fail closed when
   it cannot be determined.
10. Earlier the same day, on other seats: `gemini-reply` accepted **no cwd at all** while
    passing `always_approve` through; Gemini's `_safe_cwd` compared by equality so
    `C:\Windows\System32` was legal under a banned `C:\Windows`; the Cursor seat passed
    `--approve-mcps` even on the read-only path.

## What it flagged as SUSPECTED and never proved — settle these

- **The pointer string on argv is checked only with `.isascii()`.** `&`, `;`, `|`, `$` and
  backtick are all ASCII. The pointer is *generated*, not caller-supplied — but trace whether
  any caller-influenced value reaches it (the playpen path comes from an env var).
- **The timeout kills the `.cmd` shim, not the agent grandchild.** On Windows the grandchild
  plausibly survives, keeps spending, and its lease is released as if the work had stopped.
- **`--approve-mcps` still fires on the yolo path**, auto-approving `~/.cursor/mcp.json` — and
  possibly a project-level `<cwd>\.cursor\mcp.json` that a write-capable agent could create.

## Also in scope — nothing here has been audited by anyone

`dispatch-guard.py` in full, including code added *after* the exploit pass read it:
`load_events`, `find_events_csv` (it globs the user's Downloads and reads arbitrary CSV),
`yield_report`, and the new owner-token logic. `armcheck.py` itself — it was rewritten twice
today and now runs in two modes. And `calibrate-pool.py`, which nobody has looked at at all.

## The question underneath all of it

The named adversary is **a steered LLM holding the operator's shell**. The guest seat's verdict
was that as a security boundary this harness is **false assurance** — that adversary can rewrite
the allowance store, the ledger, the lock, the guard and the arm test. The counter-argument is
that these guards exist to stop *accidents and drift*, which is what actually happened (an
unattended fleet burned two-thirds of a month in two days), not a determined attacker.

**Rule on that.** If the guest seat is right, say what SHOULD exist instead, concretely, for a
one-person shop that cannot run a separate privileged process. If the guards are worth keeping,
say which ones actually earn their place and which are decoration that should be deleted.

## Rules
- Quote the exact function or line. Distinguish CONFIRMED (you traced the failing path) from
  SUSPECTED. An unanchored finding is unusable.
- Rank by what an attacker or a careless operator actually achieves.
- **Attack the fixes, not just the original code.** Fixes written in a hurry are where the next
  bug lives, and all ten landed today.
- Say what is well built. A review with no positives is not credible.
- Do not write any file. Report only.

## Output
```
VERDICT (3 sentences)
ARE THE TEN FIXES CORRECT?   — each: HOLDS / INCOMPLETE / INTRODUCED A NEW BUG
WHAT THE EXPLOIT PASS MISSED — ranked, CONFIRMED vs SUSPECTED
THE THREE SUSPECTED ITEMS    — settle each one
UNAUDITED CODE               — findings in dispatch-guard/armcheck/calibrate-pool
RULING: FALSE ASSURANCE, OR WORTH KEEPING? — and what should exist instead
WHAT IS WELL BUILT
CONFIDENCE + what would change your mind
```

---

# THE SOURCE (current, post-fix)

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
    52	import time
    53	
    54	CURSOR_TIMEOUT_S = 3600
    55	MAX_REPLY_CHARS = 400_000
    56	DEFAULT_MODEL = "composer-2.5"   # NON-fast on purpose: fast tiers are a surcharge
    57	
    58	# ---------------------------------------------------------------------------
    59	# THE COUNCIL LOCK (boss ruling 2026-08-23, revisitable).
    60	# A COUNCIL runs on SUBSCRIPTION seats only — house Claude / Codex / Grok /
    61	# Gemini. Never on the Cursor pool. One cheap Cursor review is fine; a fan-out of
    62	# several metered seats answering the same brief is not, and that is exactly the
    63	# shape that quietly drains a pool.
    64	#
    65	# Enforced, not merely written down: at most COUNCIL_LOCK_MAX billable calls in
    66	# any COUNCIL_LOCK_WINDOW_S seconds. A normal review sails through; a 4-seat
    67	# metered council trips the wire and is refused.
    68	# Lift deliberately with WMW_CURSOR_COUNCIL_LOCK=off (and say so to the boss).
    69	# ---------------------------------------------------------------------------
    70	COUNCIL_LOCK_MAX = int(os.environ.get("WMW_CURSOR_COUNCIL_MAX", "2"))
    71	COUNCIL_LOCK_WINDOW_S = int(os.environ.get("WMW_CURSOR_COUNCIL_WINDOW", "600"))
    72	COUNCIL_LOCK_ON = os.environ.get("WMW_CURSOR_COUNCIL_LOCK", "on").lower() != "off"
    73	
    74	# ---------------------------------------------------------------------------
    75	# THE PLAYPEN — Cursor's own corner of the disk.
    76	# ---------------------------------------------------------------------------
    77	PLAYPEN = os.path.abspath(os.environ.get(
    78	    "WMW_CURSOR_PLAYPEN", os.path.join("C:" + os.sep, "Sync", "_playpen", "cursor")))
    79	PROMPTS_DIR = os.path.join(PLAYPEN, "prompts")
    80	# NOT in the playpen. The playpen is the one directory a write-capable session is always
    81	# allowed to write, so a ledger kept there is self-serve: delete it and _recent_billable
    82	# reads zero, which silently unlocks the council lock. State the guards READ must not live
    83	# where the guarded agent may WRITE. (Audit 2026-08-24, Kimi, CONFIRMED.)
    84	SPEND_LEDGER = os.environ.get(
    85	    "WMW_CURSOR_LEDGER",
    86	    os.path.join(os.path.expanduser("~"), ".anderson-method", "bench-spend.jsonl"))
    87	
    88	def _ensure_playpen():
    89	    """Create the playpen on demand. Never let this break a call."""
    90	    for d in (PLAYPEN, PROMPTS_DIR, os.path.join(PLAYPEN, "scratch")):
    91	        try:
    92	            os.makedirs(d, exist_ok=True)
    93	        except OSError:
    94	            return False
    95	    readme = os.path.join(PLAYPEN, "README.md")
    96	    if not os.path.exists(readme):
    97	        try:
    98	            with io.open(readme, "w", encoding="utf-8", newline="") as f:
    99	                f.write(
   100	                    "# Cursor's playpen\n\n"
   101	                    "Scratch space for the `wmw-cursor` MCP seat. The seat writes prompt\n"
   102	                    "handoffs (`prompts/`), scratch work (`scratch/`) and its spend ledger\n"
   103	                    "here so none of that lands in a real project.\n\n"
   104	                    "Safe to delete when nothing is running; it is recreated on demand.\n")
   105	        except OSError:
   106	            pass
   107	    return True
   108	
   109	# ---------------------------------------------------------------------------
   110	# METER CLASSES (verified against Cursor's published pricing, 2026-08-23)
   111	# ---------------------------------------------------------------------------
   112	INCLUDED_PREFIXES = ("composer-", "cursor-grok-")
   113	CREDIT_PREFIXES = ("claude-", "gpt-", "gemini-", "kimi-", "glm-")
   114	
   115	# ---------------------------------------------------------------------------
   116	# THE YOLO ALLOWLIST (boss ruling 2026-08-23).
   117	# Only these families may run write-capable (--yolo). They are the two FREE,
   118	# trusted seats: Composer and Cursor Grok. Everything else in the pool -- the
   119	# Codex/Gemini/Claude mirrors, Kimi, GLM -- may read and advise, never write or
   120	# execute, however the call is phrased.
   121	#
   122	# The boss's stated path: open cursor-codex and cursor-gemini next if this works
   123	# out; Kimi and other foreign-lab models are explicitly NOT candidates today.
   124	# Widening this tuple is the whole change -- keep it a deliberate, visible act.
   125	# ---------------------------------------------------------------------------
   126	YOLO_ALLOWLIST = ("composer-", "cursor-grok-")
   127	
   128	def yolo_allowed(model_id):
   129	    return (model_id or "").strip().lower().startswith(YOLO_ALLOWLIST)
   130	
   131	# A model id may only ever be a plain identifier. Anything else cannot reach argv.
   132	_MODEL_RE = re.compile(r"\A[a-z0-9][a-z0-9._-]{0,63}\Z")
   133	_UUID_RE = re.compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
   134	                      r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")
   135	
   136	def meter_class(model_id):
   137	    m = (model_id or "").strip().lower()
   138	    if not m or m == "auto" or not _MODEL_RE.match(m):
   139	        return "UNKNOWN"
   140	    fast = m.endswith("-fast")
   141	    if m.startswith(INCLUDED_PREFIXES):
   142	        return "INCLUDED-FAST" if fast else "INCLUDED"
   143	    if m.startswith(CREDIT_PREFIXES):
   144	        return "CREDITS-FAST" if fast else "CREDITS"
   145	    return "UNKNOWN"
   146	
   147	METER_MARK = {"INCLUDED": "♾️", "INCLUDED-FAST": "♾️💸",
   148	              "CREDITS": "💸", "CREDITS-FAST": "🚨💳", "UNKNOWN": "⚠️"}
   149	
   150	# THE CURSOR BANNER. The arrow is a CURSOR — its birthplace; the conductor's 🟡➤
   151	# baton is the borrowed cousin. Every line this seat produces flies 🟣➤.
   152	CURSOR_BANNER = "🟣➤"
   153	
   154	BLOODLINE_MARK = {
   155	    "Moonshot": "🌙",   # Kimi — Moonshot AI, literally the moon
   156	    "Zhipu": "🔷",      # GLM
   157	    "Cursor": "🎼",     # Composer — a composer writes the score
   158	    "Anthropic": "🟠", "OpenAI": "🔵", "xAI": "⚫", "Google": "🟢",
   159	    "UNKNOWN": "❓",
   160	}
   161	
   162	def _lineage(model_id):
   163	    m = (model_id or "").lower()
   164	    for pre, vendor in (("claude-", "Anthropic"), ("gpt-", "OpenAI"),
   165	                        ("cursor-grok-", "xAI"), ("gemini-", "Google"),
   166	                        ("kimi-", "Moonshot"), ("glm-", "Zhipu"),
   167	                        ("composer-", "Cursor")):
   168	        if m.startswith(pre):
   169	            return vendor
   170	    return "UNKNOWN"
   171	
   172	def _log_spend(model, lineage, klass, usage, sid, ok, write_capable):
   173	    """One append-only row per LAUNCHED call, success or not. Never breaks a call."""
   174	    try:
   175	        _ensure_playpen()
   176	        row = {
   177	            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
   178	            "model": model, "lineage": lineage, "meter": klass,
   179	            "billable": bool(klass and klass.startswith("CREDITS")),
   180	            "surcharged": bool(klass and klass.endswith("FAST")),
   181	            "in": (usage or {}).get("inputTokens"),
   182	            "out": (usage or {}).get("outputTokens"),
   183	            "cache_read": (usage or {}).get("cacheReadTokens"),
   184	            "session": sid, "ok": ok, "write_capable": write_capable,
   185	        }
   186	        with io.open(SPEND_LEDGER, "a", encoding="utf-8", newline="") as f:
   187	            f.write(json.dumps(row) + "\n")
   188	    except Exception as e:
   189	        print(f"[wmw-cursor] spend-ledger write failed: {e}", file=sys.stderr)
   190	
   191	def _allowance(seat):
   192	    """Ask the operator's allowance record whether this seat may spend.
   193	
   194	    The record lives on the operator's own machine, never in the repo. Absent or
   195	    expired means NO -- a metered seat asks before it spends, every time, until a
   196	    bounded grant exists. See mcp-seats/allowance.py.
   197	    """
   198	    try:
   199	        import importlib.util
   200	        spec = importlib.util.spec_from_file_location(
   201	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowance.py"))
   202	        mod = importlib.util.module_from_spec(spec)
   203	        spec.loader.exec_module(mod)
   204	        return mod.status(seat)
   205	    except Exception as e:
   206	        return False, f"the allowance record could not be read ({e}); failing closed"
   207	
   208	def _allowance_window_s(seat, fallback):
   209	    """The operator's granted WINDOW, not a hardcoded one. See allowance.window_seconds."""
   210	    try:
   211	        import importlib.util
   212	        spec = importlib.util.spec_from_file_location(
   213	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowance.py"))
   214	        mod = importlib.util.module_from_spec(spec)
   215	        spec.loader.exec_module(mod)
   216	        return int(mod.window_seconds(seat, fallback))
   217	    except Exception:
   218	        return fallback
   219	
   220	
   221	def _allowance_calls(seat, fallback):
   222	    """The granted call bound, so the rolling cap enforces the operator's number."""
   223	    try:
   224	        import importlib.util
   225	        spec = importlib.util.spec_from_file_location(
   226	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowance.py"))
   227	        mod = importlib.util.module_from_spec(spec)
   228	        spec.loader.exec_module(mod)
   229	        g = mod._load().get(seat) or {}
   230	        return int(g.get("calls", fallback))
   231	    except Exception:
   232	        return fallback
   233	
   234	def _guard():
   235	    """Load dispatch-guard, the council's controls. None if unavailable."""
   236	    try:
   237	        import importlib.util
   238	        spec = importlib.util.spec_from_file_location(
   239	            "_guard_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   240	                                       "dispatch-guard.py"))
   241	        mod = importlib.util.module_from_spec(spec)
   242	        spec.loader.exec_module(mod)
   243	        return mod
   244	    except Exception as e:
   245	        # FAIL CLOSED. This used to return None, and the caller's
   246	        # `if guard and always_approve and cwd:` then skipped preflight AND the
   247	        # reservation without a word — so corrupting one file disarmed the guard
   248	        # silently. A control that disappears when its file breaks is not a control.
   249	        # (Audit 2026-08-24, Kimi finding 7, CONFIRMED.)
   250	        print(f"[wmw-cursor] dispatch-guard unavailable: {e}", file=sys.stderr)
   251	        return e
   252	
   253	def _recent_billable(window_s):
   254	    """How many billable calls landed in the last window_s seconds, per the ledger."""
   255	    if not os.path.exists(SPEND_LEDGER):
   256	        return 0
   257	    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=window_s)
   258	    n = 0
   259	    try:
   260	        for line in io.open(SPEND_LEDGER, encoding="utf-8"):
   261	            line = line.strip()
   262	            if not line:
   263	                continue
   264	            try:
   265	                r = json.loads(line)
   266	            except json.JSONDecodeError:
   267	                continue
   268	            if not r.get("billable"):
   269	                continue
   270	            try:
   271	                ts = datetime.datetime.fromisoformat(r.get("ts", ""))
   272	            except ValueError:
   273	                continue
   274	            if ts >= cutoff:
   275	                n += 1
   276	    except OSError:
   277	        return 0
   278	    return n
   279	
   280	def _utf8_stdio():
   281	    for stream in (sys.stdin, sys.stdout):
   282	        try:
   283	            stream.reconfigure(encoding="utf-8", errors="replace")
   284	        except Exception:
   285	            pass
   286	
   287	def find_cursor_agent():
   288	    # Known install path first (substitute-binary defence); PATH is the fallback.
   289	    home = os.path.expanduser("~")
   290	    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
   291	    for cand in (
   292	        os.path.join(local, "cursor-agent", "cursor-agent.cmd"),   # Windows
   293	        os.path.join(home, ".local", "bin", "cursor-agent"),       # macOS / Linux
   294	        os.path.join(home, ".cursor", "bin", "cursor-agent"),
   295	    ):
   296	        if os.path.isfile(cand):
   297	            return cand
   298	    return shutil.which("cursor-agent")
   299	
   300	def _safe_id(value, label):
   301	    if not isinstance(value, str) or not _UUID_RE.match(value):
   302	        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
   303	    return value
   304	
   305	def _safe_model(value):
   306	    if value is None:
   307	        return None
   308	    if not isinstance(value, str) or not _MODEL_RE.match(value.strip().lower()):
   309	        raise ValueError("'model' must be a plain model id such as 'composer-2.5' "
   310	                         "(letters, digits, dot, dash, underscore only)")
   311	    return value.strip().lower()
   312	
   313	def _norm(path):
   314	    return os.path.normcase(os.path.realpath(path))
   315	
   316	def _is_within(child, parent):
   317	    """True when child == parent or sits underneath it. Symlink-resolved, case-folded."""
   318	    c, p = _norm(child), _norm(parent)
   319	    if c == p:
   320	        return True
   321	    try:
   322	        return os.path.commonpath([c, p]) == p
   323	    except ValueError:      # different drives
   324	        return False
   325	
   326	def _safe_cwd(cwd, always_approve):
   327	    """A write-capable seat needs an explicit cwd, and it may not be a sensitive one.
   328	
   329	    Returns the CANONICAL path, so a symlink cannot be validated and then
   330	    dereferenced somewhere else afterwards.
   331	    """
   332	    if not always_approve:
   333	        return os.path.realpath(cwd) if cwd else None
   334	    if cwd is None:
   335	        raise ValueError("always_approve requires an explicit cwd naming the project "
   336	                         "directory the seat may write in (the playpen is a fine choice: "
   337	                         + PLAYPEN + ")")
   338	    real = os.path.realpath(cwd)
   339	    if not os.path.isdir(real):
   340	        raise ValueError(f"cwd is not a directory: {cwd}")
   341	    # The playpen is always allowed — that is its whole purpose.
   342	    if _is_within(real, PLAYPEN):
   343	        return real
   344	    roots = [os.path.expanduser("~"), os.path.abspath(os.sep)]
   345	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)",
   346	                "ProgramData", "USERPROFILE"):
   347	        v = os.environ.get(env)
   348	        if v:
   349	            roots.append(v)
   350	    for r in roots:
   351	        if _norm(real) == _norm(r):
   352	            raise ValueError(f"refusing a write-capable session rooted at {real} — "
   353	                             f"point cwd at a project directory or the playpen")
   354	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
   355	        v = os.environ.get(env)
   356	        if v and _is_within(real, v):
   357	            raise ValueError(f"refusing a write-capable session inside a system directory "
   358	                             f"({v}) — point cwd at a project directory or the playpen")
   359	    # APPDATA / LOCALAPPDATA hold this rig's OWN credentials (Cursor's auth.json) and the
   360	    # vendor CLIs themselves. A write-capable session rooted there can rewrite the very
   361	    # tools that enforce these guards. (Audit 2026-08-24, Kimi, CONFIRMED gap.)
   362	    for env in ("APPDATA", "LOCALAPPDATA"):
   363	        v = os.environ.get(env)
   364	        if v:
   365	            b = _norm(os.path.realpath(v))
   366	            if _norm(real) == b or _norm(real).startswith(b.rstrip(os.sep) + os.sep):
   367	                raise ValueError(f"refusing a write-capable session at or inside {env} — "
   368	                                 f"credentials and the CLIs themselves live there")
   369	    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
   370	                   ".config", ".azure", ".kube", ".gnupg"):
   371	        parts = [p.lower() for p in _norm(real).split(os.sep)]
   372	        if secret in parts:
   373	            raise ValueError(f"refusing a write-capable session inside {secret}")
   374	    return real
   375	
   376	def _extract_json(raw):
   377	    """Last complete result object wins — the CLI streams status lines first."""
   378	    dec = json.JSONDecoder()
   379	    found = None
   380	    idx = raw.find("{")
   381	    while idx != -1:
   382	        try:
   383	            obj, _ = dec.raw_decode(raw[idx:])
   384	            if isinstance(obj, dict) and obj.get("type") == "result":
   385	                found = obj
   386	            elif isinstance(obj, dict) and found is None:
   387	                found = obj
   388	        except json.JSONDecodeError:
   389	            pass
   390	        idx = raw.find("{", idx + 1)
   391	    return found
   392	
   393	def run_cursor(prompt, session_id=None, cwd=None, model=None, always_approve=False,
   394	               spend_credits=False):
   395	    exe = find_cursor_agent()
   396	    if not exe:
   397	        return True, ("Cursor CLI not found. Install it, then `cursor-agent login`. "
   398	                      "(Windows: %LOCALAPPDATA%\\cursor-agent\\cursor-agent.cmd)")
   399	    chosen = model or DEFAULT_MODEL
   400	    klass = meter_class(chosen)
   401	
   402	    # THE METER GUARD. UNKNOWN is refused unconditionally — spend_credits unlocks
   403	    # only RECOGNISED third-party models, never an unidentified or auto-routed one.
   404	    if klass == "UNKNOWN":
   405	        return True, (
   406	            f"{CURSOR_BANNER} ⚠️ REFUSED — '{chosen}' is not a recognised model id, or is "
   407	            f"`auto` (which may route anywhere). Unknown lineage fails closed and cannot be "
   408	            f"unlocked with spend_credits. Name an explicit model: composer-2.5 (free) or "
   409	            f"cursor-grok-4.6-high (free); see BENCH-LEDGER.md for the metered ones.")
   410	    if klass.startswith("CREDITS") and not spend_credits:
   411	        return True, (
   412	            f"{CURSOR_BANNER} 🚨 CREDIT GUARD — REFUSED BEFORE SPENDING\n\n"
   413	            f"'{chosen}' is meter class {klass} ({_lineage(chosen)} lineage). It draws "
   414	            f"Cursor's third-party CREDIT pool (~$20/month included, then pay-as-you-go at "
   415	            f"API prices), not the included Cursor Models pool.\n\n"
   416	            f"To spend credits deliberately, pass spend_credits: true. To stay free, use an "
   417	            f"INCLUDED model: composer-2.5 (default) or cursor-grok-4.6-high.\n\n"
   418	            f"'-fast' variants are a surcharge (Composer 2.5 costs 6x more output on Fast), "
   419	            f"never a free speed-up.")
   420	
   421	    if always_approve and not yolo_allowed(chosen):
   422	        return True, (
   423	            f"{CURSOR_BANNER} 🛑 WRITE REFUSED — '{chosen}' is not on the YOLO allowlist.\n\n"
   424	            f"Only the free, trusted seats may run write-capable: composer-* and "
   425	            f"cursor-grok-*. Every other pool model ({_lineage(chosen)} here) may read and "
   426	            f"advise, never write or execute.\n\n"
   427	            f"Boss ruling 2026-08-23. Re-run this as a read-only call (drop always_approve), "
   428	            f"or hand the build to composer-2.5 / cursor-grok-4.6-high.")
   429	
   430	    # THE COUNCIL SEAT LAW (SPINE v2.5): spending is gated by a recorded ALLOWANCE,
   431	    # not by vendor class. No grant, or an expired one, means this seat may not spend.
   432	    if klass.startswith("CREDITS"):
   433	        ok, why = _allowance("cursor")
   434	        if not ok:
   435	            return True, (
   436	                f"{CURSOR_BANNER} 🛑 NO ALLOWANCE — REFUSED BEFORE SPENDING\n\n"
   437	                f"'{chosen}' bills the third-party credit pool, and {why}\n\n"
   438	                f"Grants are bounded and expire on purpose. Free INCLUDED models "
   439	                f"(composer-2.5, cursor-grok-4.6-*) are unaffected and need no allowance.")
   440	
   441	    if klass.startswith("CREDITS") and COUNCIL_LOCK_ON:
   442	        # The operator's grant says "N per WINDOW". Enforcement used a hardcoded
   443	        # 10-minute window regardless, so "10/week" was policed as "10 per 10 minutes".
   444	        # Use the granted window; fall back to the house default only if none is recorded.
   445	        _win = _allowance_window_s("cursor", COUNCIL_LOCK_WINDOW_S)
   446	        recent = _recent_billable(_win)
   447	        if recent >= _allowance_calls("cursor", COUNCIL_LOCK_MAX):
   448	            return True, (
   449	                f"{CURSOR_BANNER} 🛑 COUNCIL LOCK — REFUSED\n\n"
   450	                f"{recent} billable Cursor calls already landed in the last "
   451	                f"{_win // 60} minutes, at the operator's granted bound. "
   452	                f"This looks like a COUNCIL fanning out onto metered seats.\n\n"
   453	                f"Standing boss ruling (2026-08-23): a council runs on SUBSCRIPTION seats "
   454	                f"only — house Claude, Codex, Grok, Gemini. Cursor-hosted models are not "
   455	                f"council seats right now.\n\n"
   456	                f"Free INCLUDED models (composer-2.5, cursor-grok-4.6-*) are unaffected. To "
   457	                f"lift this deliberately set WMW_CURSOR_COUNCIL_LOCK=off — and say so to "
   458	                f"the boss first."
   459	            )
   460	
   461	    _ensure_playpen()
   462	    # No cwd? Work in the playpen — the seat always has somewhere legitimate to be.
   463	    workdir = cwd or PLAYPEN
   464	    if not os.path.isdir(workdir):
   465	        return True, f"cwd is not a directory: {workdir}"
   466	
   467	    # ---- THE GUARD (council 2026-08-24) ------------------------------------
   468	    # Two controls, and they only bind a WRITE-capable dispatch at a real repo —
   469	    # the shape that burned two thirds of a month on 2026-08-21/22. A read-only
   470	    # question costs little and is left alone deliberately.
   471	    guard, lease = _guard(), None
   472	    if isinstance(guard, Exception) and always_approve:
   473	        return True, (
   474	            f"{CURSOR_BANNER} 🛑 GUARD UNAVAILABLE — WRITE REFUSED\n\n"
   475	            f"dispatch-guard could not be loaded ({guard}).\n\n"
   476	            f"A write-capable dispatch is refused while its guard is missing. Read-only "
   477	            f"calls are unaffected. Repair mcp-seats/dispatch-guard.py, or run read-only.")
   478	    if guard and not isinstance(guard, Exception) and always_approve and cwd:
   479	        # PREFLIGHT: an agent with no destination still spends at full rate.
   480	        rc, problems, _notes = guard.preflight(workdir, model=chosen)
   481	        if rc:
   482	            return True, (
   483	                f"{CURSOR_BANNER} 🛑 PREFLIGHT REFUSED — dispatch would spend for nothing\n\n"
   484	                + "\n".join(f"  • {p}" for p in problems) +
   485	                "\n\nThis is the Aug 21-22 shape: 13 agents into a repo staged empty, 11 of "
   486	                "them returning zero lines. Point the seat at a repo with real source, or "
   487	                "run read-only (omit always_approve) to ask a question instead of building.")
   488	
   489	        # RESERVE: atomic, so N launches cannot each pass on the same headroom.
   490	        lease = f"cursor-{os.getpid()}-{int(time.time())}"
   491	        ok, why = guard.reserve(lease, est_pct=float(os.environ.get("WMW_EST_PCT", "2")),
   492	                                note=f"{chosen} @ {os.path.basename(workdir)}")
   493	        lease_owner = (guard._load().get("jobs", {}).get(lease) or {}).get("owner") if ok else None
   494	        if not ok:
   495	            return True, (
   496	                f"{CURSOR_BANNER} 🛑 NO HEADROOM RESERVED — REFUSED BEFORE SPENDING\n\n{why}\n\n"
   497	                "Concurrency is the control. Thirteen launches each passed their own check "
   498	                "on 2026-08-21 and together took the month.")
   499	
   500	    # ---- PROMPT TRANSPORT --------------------------------------------------
   501	    # NOTHING caller-controlled goes on the command line. The Windows CLI is a
   502	    # .cmd shim forwarding to PowerShell; a crafted prompt CAN execute host
   503	    # commands (reproduced 2026-08-23). The prompt always travels as a file in
   504	    # the playpen; only a generated ASCII pointer is passed as an argument.
   505	    spill_path = None
   506	    try:
   507	        fd, spill_path = tempfile.mkstemp(prefix="prompt_", suffix=".md", dir=PROMPTS_DIR)
   508	        try:
   509	            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
   510	                f.write(prompt)
   511	        except OSError as e:
   512	            return True, f"could not write the prompt handoff file: {e}"
   513	
   514	        # ASCII ONLY, deliberately: this string is the single thing that reaches argv,
   515	        # and the Windows .cmd shim mangles (or executes) anything exotic.
   516	        pointer = ("Read the file at " + spill_path.replace("\\", "/") +
   517	                   " which contains your full instructions. Follow them exactly and answer "
   518	                   "them directly. Do not modify or delete that file; it is a scratch "
   519	                   "handoff and is cleaned up automatically.")
   520	        if not pointer.isascii():
   521	            return True, ("the prompt handoff path contains non-ASCII characters; set "
   522	                          "WMW_CURSOR_PLAYPEN to a plain ASCII path")
   523	
   524	        cmd = [exe]
   525	        if session_id:
   526	            cmd += [f"--resume={session_id}"]
   527	        cmd += ["--model", chosen]
   528	        cmd += ["--yolo"] if always_approve else ["--mode", "ask", "--trust"]
   529	        # Let the seat use the MCP servers configured in ~/.cursor/mcp.json, so a
   530	        # Cursor seat gets the same workshop the house seats have. NOTE: this
   531	        # auto-approves whatever is in that file — keep it to read-only tools, and
   532	        # deliberately NOT the sibling wmw-* seats: a seat that can drive another
   533	        # seat can escalate around its own read-only mode (proved on wmw-grok,
   534	        # 2026-08-23, where a read-only Grok wrote a file via the Codex seat).
   535	        # --approve-mcps auto-approves whatever ~/.cursor/mcp.json holds. On the
   536	        # read-only path that is an escalation route: a seat that cannot write can ask a
   537	        # neighbouring MCP server to write for it — reproduced on the Grok seat
   538	        # 2026-08-23. The old mitigation was "just don't put writable servers in that
   539	        # file", which is a promise about a config, not a guard in code. Auto-approval is
   540	        # now confined to the already-write-capable path. (Audit 2026-08-24, two seats.)
   541	        if always_approve:
   542	            cmd += ["--approve-mcps"]
   543	        cmd += ["-p", pointer, "--output-format", "json"]
   544	
   545	        try:
   546	            proc = subprocess.run(
   547	                cmd, capture_output=True, text=True, encoding="utf-8",
   548	                errors="replace", timeout=CURSOR_TIMEOUT_S, cwd=workdir,
   549	                stdin=subprocess.DEVNULL,
   550	            )
   551	        except subprocess.TimeoutExpired:
   552	            _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   553	            return True, f"cursor-agent timed out after {CURSOR_TIMEOUT_S}s"
   554	        except OSError as e:
   555	            return True, f"could not launch cursor-agent: {e}"
   556	    finally:
   557	        if spill_path:
   558	            try:
   559	                os.unlink(spill_path)
   560	            except (FileNotFoundError, OSError):
   561	                pass
   562	        # Release the lease HERE, in the finally, so a crash, a timeout or a launch
   563	        # failure can never leave a slot held. A stuck lease would deny the operator
   564	        # his own rig, which is a worse failure than the one being prevented.
   565	        if guard and lease:
   566	            try:
   567	                guard.release(lease, owner=lease_owner)
   568	            except Exception as e:
   569	                print(f"[wmw-cursor] lease release failed: {e}", file=sys.stderr)
   570	
   571	    raw = (proc.stdout or "").strip()
   572	    err = (proc.stderr or "").strip()
   573	    data = _extract_json(raw)
   574	    # Only a run that produced NO result can be a trust refusal. Checking raw text
   575	    # first was a self-inflicted false positive: a model reviewing this very file
   576	    # quoted the phrase back and the wrapper refused its own review.
   577	    if data is None and ("Workspace Trust Required" in raw or "Workspace Trust Required" in err):
   578	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   579	        return True, (f"Cursor refused {workdir} as untrusted. Point cwd at a project "
   580	                      f"directory you trust, or leave cwd unset to use the playpen.")
   581	    if data is None:
   582	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   583	        return True, (f"cursor-agent exited {proc.returncode} with no parseable JSON.\n"
   584	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
   585	    if data.get("is_error") or data.get("subtype") not in (None, "success"):
   586	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"),
   587	                   data.get("session_id") or session_id, False, always_approve)
   588	        return True, (f"cursor-agent reported an error: {str(data.get('result'))[:1500]}\n"
   589	                      f"stderr: {err[:800]}")
   590	    text = data.get("result")
   591	    sid = data.get("session_id")
   592	    if proc.returncode != 0 or not isinstance(sid, str) or not sid:
   593	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"), sid or session_id,
   594	                   False, always_approve)
   595	        return True, (f"cursor-agent run failed (exit {proc.returncode}, session_id={sid!r}).\n"
   596	                      f"result: {str(text)[:1000]}\nstderr: {err[:1000]}")
   597	    if not isinstance(text, str):
   598	        text = "" if text is None else str(text)
   599	    if len(text) > MAX_REPLY_CHARS:
   600	        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-cursor] ...truncated at {MAX_REPLY_CHARS} chars]"
   601	
   602	    usage = data.get("usage") or {}
   603	    tok = (f"{usage.get('inputTokens', '?')} in / {usage.get('outputTokens', '?')} out"
   604	           if usage else "usage unreported")
   605	    mark = METER_MARK.get(klass, "⚠️")
   606	    vendor = _lineage(chosen)
   607	    blood = BLOODLINE_MARK.get(vendor, "❓")
   608	    pool = ("Cursor Models pool — INCLUDED, no credits spent" if klass == "INCLUDED"
   609	            else "Cursor Models pool — included, but a FAST-tier surcharge applies"
   610	            if klass == "INCLUDED-FAST"
   611	            else "third-party CREDIT pool — billed at API prices")
   612	    _log_spend(chosen, vendor, klass, usage, sid, True, always_approve)
   613	    money = ""
   614	    if klass.startswith("CREDITS") or klass == "INCLUDED-FAST":
   615	        money = (f"\n{CURSOR_BANNER} {mark} —— THIS CALL SPENT MONEY —— {mark} {CURSOR_BANNER}"
   616	                 f"\n   {pool}")
   617	    footer = (f"\n\n---\n{CURSOR_BANNER}{blood} [wmw-cursor] {mark} {vendor} · {chosen}"
   618	              f"\n   sessionId: {sid} · meter: {klass} · {tok}{money}")
   619	    return False, text + footer
   620	
   621	def _req_str(args, key):
   622	    v = args.get(key)
   623	    if not isinstance(v, str) or not v.strip():
   624	        raise ValueError(f"'{key}' must be a non-empty string")
   625	    return v
   626	
   627	def _opt_str(args, key):
   628	    v = args.get(key)
   629	    if v is None:
   630	        return None
   631	    if not isinstance(v, str) or not v.strip():
   632	        raise ValueError(f"'{key}' must be a non-empty string when given")
   633	    return v
   634	
   635	def _opt_bool(args, key):
   636	    v = args.get(key)
   637	    if v is None:
   638	        return False
   639	    if isinstance(v, bool):
   640	        return v
   641	    if isinstance(v, str) and v.lower() in ("true", "false"):
   642	        return v.lower() == "true"
   643	    raise ValueError(f"'{key}' must be a boolean")
   644	
   645	_MODEL_NOTE = ("Model id (default composer-2.5 — the free, non-fast door). Free/INCLUDED: "
   646	               "composer-2.5, cursor-grok-4.6-{low,medium,high,xhigh}, cursor-grok-4.5-*. "
   647	               "Metered/CREDITS (need spend_credits): claude-*, gpt-*, gemini-*, kimi-*, "
   648	               "glm-*. `auto` is refused. See BENCH-LEDGER.md; `cursor-agent models` lists all.")
   649	
   650	TOOLS = [
   651	    {
   652	        "name": "cursor",
   653	        "description": (
   654	            "Start a NEW persistent conversation on the CURSOR MODEL POOL (Composer 2.5 by "
   655	            "default; Cursor Grok, Codex, Kimi, GLM and other tiers via `model`). Returns the "
   656	            "reply plus a sessionId footer; continue it with cursor-reply. ⚠ THE ONE METERED "
   657	            "SEAT: composer-* and cursor-grok-* are INCLUDED (free); everything else bills "
   658	            "Cursor's credit pool and is refused unless spend_credits is true. DEFAULT IS "
   659	            "READ-ONLY (no code execution, no file writes). Set always_approve true only for "
   660	            "build tickets, and then cwd is REQUIRED. With no cwd the seat works in its own "
   661	            "playpen directory."
   662	        ),
   663	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   664	        "inputSchema": {
   665	            "type": "object",
   666	            "properties": {
   667	                "prompt": {"type": "string", "description": "The task or message."},
   668	                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory. Omit to work in the playpen."},
   669	                "model": {"type": "string", "description": _MODEL_NOTE},
   670	                "always_approve": {"type": "boolean", "description": "DANGEROUS: pass --yolo so the agent may write files and run commands under cwd. Default false = read-only."},
   671	                "spend_credits": {"type": "boolean", "description": "Required to reach any THIRD-PARTY model (claude-/gpt-/gemini-/kimi-/glm-), billed at API prices against Cursor's credit pool. Ask the boss first."},
   672	            },
   673	            "required": ["prompt"],
   674	        },
   675	    },
   676	    {
   677	        "name": "cursor-reply",
   678	        "description": (
   679	            "Continue an existing Cursor-pool conversation by sessionId (from a prior cursor "
   680	            "call's footer), with full prior context. Same meter rules apply."
   681	        ),
   682	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   683	        "inputSchema": {
   684	            "type": "object",
   685	            "properties": {
   686	                "sessionId": {"type": "string", "description": "sessionId from a previous cursor/cursor-reply call."},
   687	                "prompt": {"type": "string", "description": "The follow-up message."},
   688	                "model": {"type": "string", "description": _MODEL_NOTE},
   689	                "cwd": {"type": "string", "description": "Working directory for this turn."},
   690	                "always_approve": {"type": "boolean", "description": "Pass --yolo for this turn (write-capable); requires cwd."},
   691	                "spend_credits": {"type": "boolean", "description": "Required to reach a third-party (credit-billed) model."},
   692	            },
   693	            "required": ["sessionId", "prompt"],
   694	        },
   695	    },
   696	]
   697	
   698	def _tool_call(name, args):
   699	    if not isinstance(args, dict):
   700	        return True, "arguments must be an object"
   701	    try:
   702	        if name in ("cursor", "cursor-reply"):
   703	            approve = _opt_bool(args, "always_approve")
   704	            cwd = _safe_cwd(_opt_str(args, "cwd"), approve)
   705	            sid = _safe_id(args.get("sessionId"), "sessionId") if name == "cursor-reply" else None
   706	            return run_cursor(
   707	                _req_str(args, "prompt"), session_id=sid, cwd=cwd,
   708	                model=_safe_model(_opt_str(args, "model")),
   709	                always_approve=approve,
   710	                spend_credits=_opt_bool(args, "spend_credits"),
   711	            )
   712	    except ValueError as e:
   713	        return True, f"invalid arguments: {e}"
   714	    return None
   715	
   716	def handle(msg):
   717	    method = msg.get("method")
   718	    mid = msg.get("id")
   719	    is_notification = "id" not in msg
   720	    if method == "initialize":
   721	        return {
   722	            "jsonrpc": "2.0", "id": mid,
   723	            "result": {
   724	                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
   725	                "capabilities": {"tools": {}},
   726	                "serverInfo": {"name": "wmw-cursor", "version": "2.5.0"},
   727	            },
   728	        }
   729	    if method == "ping":
   730	        return {"jsonrpc": "2.0", "id": mid, "result": {}}
   731	    if method == "tools/list":
   732	        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
   733	    if method == "tools/call":
   734	        params = msg.get("params") or {}
   735	        name = params.get("name")
   736	        result = _tool_call(name, params.get("arguments") or {})
   737	        if result is None:
   738	            return {"jsonrpc": "2.0", "id": mid,
   739	                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
   740	        is_err, text = result
   741	        return {"jsonrpc": "2.0", "id": mid,
   742	                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
   743	    if not is_notification:
   744	        return {"jsonrpc": "2.0", "id": mid,
   745	                "error": {"code": -32601, "message": f"method not found: {method}"}}
   746	    return None
   747	
   748	def main():
   749	    _utf8_stdio()
   750	    _ensure_playpen()
   751	    # An unbounded readline is a memory-exhaustion primitive: one enormous frame and
   752	    # the seat dies. MCP frames are small. (Audit 2026-08-24, Kimi finding 10.)
   753	    MAX_FRAME = 8 * 1024 * 1024
   754	    for line in sys.stdin:
   755	        if len(line) > MAX_FRAME:
   756	            print(f"[wmw-cursor] frame over {MAX_FRAME} bytes refused", file=sys.stderr)
   757	            continue
   758	        line = line.strip()
   759	        if not line:
   760	            continue
   761	        try:
   762	            msg = json.loads(line)
   763	        except json.JSONDecodeError:
   764	            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
   765	                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
   766	            sys.stdout.flush()
   767	            continue
   768	        if not isinstance(msg, dict):
   769	            continue
   770	        try:
   771	            resp = handle(msg)
   772	        except Exception as e:
   773	            print(f"[wmw-cursor] internal error: {e}", file=sys.stderr)
   774	            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
   775	                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
   776	        if resp is not None:
   777	            sys.stdout.write(json.dumps(resp) + "\n")
   778	            sys.stdout.flush()
   779	
   780	if __name__ == "__main__":
   781	    main()
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
   154	    if not always_approve:
   155	        return cwd
   156	    # A write-capable reply used to arrive with NO cwd at all and run wherever this
   157	    # server happened to be launched. Absent is not safe -- it is unbounded.
   158	    if cwd is None:
   159	        raise ValueError("a write-capable Gemini session REQUIRES an explicit cwd — "
   160	                         "point it at a project directory")
   161	    real = os.path.realpath(cwd)
   162	    home = os.path.realpath(os.path.expanduser("~"))
   163	    # The filesystem ROOT is banned exactly (everything is inside it, so containment
   164	    # there would ban the whole disk -- a false positive that would push the operator
   165	    # to disable the guard). Every other banned location is banned WITH its subtree,
   166	    # because equality alone left C:\Windows\System32 legal under a banned C:\Windows.
   167	    root = os.path.realpath(os.path.abspath(os.sep))
   168	    subtree = {home}
   169	    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
   170	        v = os.environ.get(env)
   171	        if v:
   172	            subtree.add(os.path.realpath(v))
   173	    if real == root:
   174	        raise ValueError("refusing a write-capable session at the filesystem root — "
   175	                         "point cwd at a project directory")
   176	    for b in subtree:
   177	        if real == b or real.lower().startswith(b.rstrip(os.sep).lower() + os.sep):
   178	            raise ValueError(f"refusing a write-capable session at or inside {b} — "
   179	                             f"point cwd at a project directory")
   180	    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".config"):
   181	        if os.path.basename(real) == secret or os.sep + secret in real + os.sep:
   182	            raise ValueError(f"refusing a write-capable session inside {secret}")
   183	    return real   # hand back the RESOLVED path, never the caller's string
   184	
   185	def _req_str(args, key):
   186	    v = args.get(key)
   187	    if not isinstance(v, str) or not v.strip():
   188	        raise ValueError(f"'{key}' must be a non-empty string")
   189	    return v
   190	
   191	def _opt_str(args, key):
   192	    v = args.get(key)
   193	    if v is None:
   194	        return None
   195	    if not isinstance(v, str) or not v.strip():
   196	        raise ValueError(f"'{key}' must be a non-empty string when given")
   197	    return v
   198	
   199	def _opt_bool(args, key):
   200	    v = args.get(key)
   201	    if v is None:
   202	        return False
   203	    if isinstance(v, bool):
   204	        return v
   205	    if isinstance(v, str) and v.lower() in ("true", "false"):
   206	        return v.lower() == "true"
   207	    raise ValueError(f"'{key}' must be a boolean")
   208	
   209	TOOLS = [
   210	    {
   211	        "name": "gemini",
   212	        "description": (
   213	            "Start a NEW conversation with Gemini via the Antigravity CLI (Google "
   214	            "subscription seat). Returns the reply plus a conversationId footer (including the "
   215	            "effective brain — check it before counting this seat as an independent Gemini vote); "
   216	            "continue the same conversation with gemini-reply. Each fresh call is an independent, "
   217	            "blind session. Set always_approve true when Gemini must edit files or run commands "
   218	            "(headless permission prompts otherwise stall the run). Keep prompts under ~25K chars; "
   219	            "put long material in a file for Gemini to read."
   220	        ),
   221	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   222	        "inputSchema": {
   223	            "type": "object",
   224	            "properties": {
   225	                "prompt": {"type": "string", "description": "The task or message for Gemini."},
   226	                "cwd": {"type": "string", "description": "Working directory (repo path for build work)."},
   227	                "model": {"type": "string", "description": "Optional model override (agy models lists them; exact-match strings)."},
   228	                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts. Required for build work; default false."},
   229	            },
   230	            "required": ["prompt"],
   231	        },
   232	    },
   233	    {
   234	        "name": "gemini-reply",
   235	        "description": (
   236	            "Continue an existing Gemini/Antigravity conversation by conversationId (from a "
   237	            "prior gemini call's footer). Gemini retains the full prior context."
   238	        ),
   239	        "inputSchema": {
   240	            "type": "object",
   241	            "properties": {
   242	                "conversationId": {"type": "string", "description": "conversationId from a previous gemini/gemini-reply call."},
   243	                "prompt": {"type": "string", "description": "The follow-up message."},
   244	                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true."},
   245	                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts this turn. Requires cwd."},
   246	            },
   247	            "required": ["conversationId", "prompt"],
   248	        },
   249	    },
   250	]
   251	
   252	def _tool_call(name, args):
   253	    if not isinstance(args, dict):
   254	        return True, "arguments must be an object"
   255	    try:
   256	        if name == "gemini":
   257	            approve = _opt_bool(args, "always_approve")
   258	            return run_gemini(
   259	                _req_str(args, "prompt"),
   260	                cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve),
   261	                model=_safe_argv(_opt_str(args, "model"), "model"),
   262	                always_approve=approve,
   263	            )
   264	        if name == "gemini-reply":
   265	            # A reply may escalate to write-capable exactly like a fresh call, so it must
   266	            # clear the SAME cwd gate. It did not: it accepted no cwd at all and handed
   267	            # always_approve straight through, so a continued session could run
   268	            # --dangerously-skip-permissions in whatever directory this server was
   269	            # launched from. The Grok seat has guarded this since 2026-08-23; the fix was
   270	            # never propagated here. (Audit 2026-08-24, Gemini seat, CONFIRMED.)
   271	            approve = _opt_bool(args, "always_approve")
   272	            return run_gemini(
   273	                _req_str(args, "prompt"),
   274	                conversation_id=_safe_id(args.get("conversationId"), "conversationId"),
   275	                cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve),
   276	                always_approve=approve,
   277	            )
   278	    except ValueError as e:
   279	        return True, f"invalid arguments: {e}"
   280	    return None
   281	
   282	def handle(msg):
   283	    method = msg.get("method")
   284	    mid = msg.get("id")
   285	    is_notification = "id" not in msg
   286	    if method == "initialize":
   287	        return {
   288	            "jsonrpc": "2.0", "id": mid,
   289	            "result": {
   290	                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
   291	                "capabilities": {"tools": {}},
   292	                "serverInfo": {"name": "wmw-gemini", "version": "1.5.0"},
   293	            },
   294	        }
   295	    if method == "ping":
   296	        return {"jsonrpc": "2.0", "id": mid, "result": {}}
   297	    if method == "tools/list":
   298	        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
   299	    if method == "tools/call":
   300	        params = msg.get("params") or {}
   301	        name = params.get("name")
   302	        result = _tool_call(name, params.get("arguments") or {})
   303	        if result is None:
   304	            return {"jsonrpc": "2.0", "id": mid,
   305	                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
   306	        is_err, text = result
   307	        return {"jsonrpc": "2.0", "id": mid,
   308	                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
   309	    if not is_notification:
   310	        return {"jsonrpc": "2.0", "id": mid,
   311	                "error": {"code": -32601, "message": f"method not found: {method}"}}
   312	    return None
   313	
   314	def main():
   315	    _utf8_stdio()
   316	    for line in sys.stdin:
   317	        line = line.strip()
   318	        if not line:
   319	            continue
   320	        try:
   321	            msg = json.loads(line)
   322	        except json.JSONDecodeError:
   323	            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
   324	                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
   325	            sys.stdout.flush()
   326	            continue
   327	        if not isinstance(msg, dict):
   328	            continue
   329	        try:
   330	            resp = handle(msg)
   331	        except Exception as e:
   332	            print(f"[wmw-gemini] internal error: {e}", file=sys.stderr)
   333	            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
   334	                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
   335	        if resp is not None:
   336	            sys.stdout.write(json.dumps(resp) + "\n")
   337	            sys.stdout.flush()
   338	
   339	if __name__ == "__main__":
   340	    main()
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
    57	def _lock_pid():
    58	    try:
    59	        return int(io.open(LOCK, encoding="utf-8").read().strip() or 0)
    60	    except (OSError, ValueError):
    61	        return 0
    62	
    63	
    64	def _pid_alive(pid):
    65	    """True unless we can prove the process is gone. Fails CLOSED: an unknown
    66	    state keeps the lock held, because a stolen lock is worse than a stuck one."""
    67	    if not pid:
    68	        return False
    69	    if os.name == "nt":
    70	        try:
    71	            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
    72	                                 capture_output=True, text=True, timeout=10).stdout
    73	            return str(pid) in out
    74	        except Exception:
    75	            return True
    76	    try:
    77	        os.kill(pid, 0)
    78	        return True
    79	    except ProcessLookupError:
    80	        return False
    81	    except PermissionError:
    82	        return True
    83	
    84	
    85	class Lock:
    86	    """Atomic across processes. O_EXCL create is the portable primitive.
    87	
    88	    Without this the whole tool is theatre: two launches would read the same
    89	    headroom, both pass, and both spend. That is the exact race Codex named.
    90	    """
    91	
    92	    def __enter__(self):
    93	        start = time.time()
    94	        while True:
    95	            try:
    96	                fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    97	                os.write(fd, str(os.getpid()).encode())
    98	                os.close(fd)
    99	                return self
   100	            except FileExistsError:
   101	                # Age alone is NOT death. Reclaiming on a timer lets a slow-but-living
   102	                # holder have its lock stolen, after which two processes both believe they
   103	                # hold it -- which is the very race this lock exists to prevent.
   104	                # Verify the recorded PID is actually gone first. (Audit 2026-08-24.)
   105	                try:
   106	                    if time.time() - os.path.getmtime(LOCK) > LOCK_STALE_S:
   107	                        if not _pid_alive(_lock_pid()):
   108	                            os.unlink(LOCK)   # holder is genuinely dead; reclaim
   109	                            continue
   110	                except OSError:
   111	                    pass
   112	                if time.time() - start > LOCK_STALE_S * 2:
   113	                    raise SystemExit("guard: could not acquire lock; is a job wedged?")
   114	                time.sleep(0.05)
   115	
   116	    def __exit__(self, *a):
   117	        try:
   118	            os.unlink(LOCK)
   119	        except OSError:
   120	            pass
   121	
   122	
   123	def _load():
   124	    try:
   125	        return json.load(io.open(STORE, encoding="utf-8"))
   126	    except (OSError, json.JSONDecodeError):
   127	        return {"jobs": {}}
   128	
   129	
   130	def _save(d):
   131	    os.makedirs(os.path.dirname(STORE), exist_ok=True)
   132	    tmp = STORE + ".tmp"
   133	    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
   134	        json.dump(d, f, indent=2)
   135	    os.replace(tmp, STORE)      # atomic swap; never a half-written ledger
   136	
   137	
   138	def _now():
   139	    return datetime.datetime.now()
   140	
   141	
   142	def _expire(d):
   143	    """Drop leases past their TTL. A crashed job must not hold the month hostage."""
   144	    live, dropped = {}, []
   145	    for k, v in d.get("jobs", {}).items():
   146	        if v.get("state") != "open":
   147	            continue
   148	        try:
   149	            if datetime.datetime.fromisoformat(v["expires"]) < _now():
   150	                dropped.append(k)
   151	                continue
   152	        except (KeyError, ValueError):
   153	            dropped.append(k)
   154	            continue
   155	        live[k] = v
   156	    d["jobs"] = live
   157	    return dropped
   158	
   159	
   160	# ---------------------------------------------------------------- preflight
   161	def _git(repo, *args):
   162	    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
   163	                       text=True, encoding="utf-8", errors="replace")
   164	    return p.returncode, (p.stdout or "").strip()
   165	
   166	
   167	def preflight(repo, model=None, mode_flags=None, min_files=1):
   168	    """Refuse a dispatch that is set up to produce nothing, or to cost too much.
   169	
   170	    This is the boss's finding turned into a gate: an agent with no destination
   171	    still spends at full rate.
   172	    """
   173	    problems, notes = [], []
   174	
   175	    if not os.path.isdir(repo):
   176	        return 1, [f"target is not a directory: {repo}"], []
   177	
   178	    rc, _ = _git(repo, "rev-parse", "--git-dir")
   179	    if rc != 0:
   180	        problems.append(f"{repo} is not a git repository — no write-set can be verified")
   181	    else:
   182	        rc, out = _git(repo, "ls-files")
   183	        tracked = [l for l in out.splitlines() if l.strip()]
   184	        code = [f for f in tracked
   185	                if os.path.splitext(f)[1].lower() in
   186	                (".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".go", ".rs", ".java",
   187	                 ".c", ".cpp", ".h", ".rb", ".php", ".swift", ".kt", ".sh", ".ps1")]
   188	        if len(tracked) < min_files:
   189	            problems.append(f"repo has {len(tracked)} tracked files — "
   190	                            f"an agent dispatched here has nowhere to put code "
   191	                            f"(this is the Aug 21-22 failure, exactly)")
   192	        elif not code:
   193	            problems.append(f"repo has {len(tracked)} tracked files but NO source files — "
   194	                            f"staging pad, not a build target")
   195	        else:
   196	            notes.append(f"{len(tracked)} tracked files, {len(code)} source")
   197	
   198	        rc, out = _git(repo, "status", "--porcelain")
   199	        if out:
   200	            notes.append(f"{len(out.splitlines())} uncommitted changes present")
   201	
   202	    flags = {k.lower(): str(v).lower() for k, v in (mode_flags or {}).items()}
   203	    stacked = [f"{k}={v}" for k, v in BANNED_STACK if flags.get(k) == v]
   204	    if len(stacked) >= 2:
   205	        problems.append("expensive mode stack: " + " + ".join(stacked) +
   206	                        " — measured 5.5x the cheapest included model")
   207	    elif stacked:
   208	        notes.append("surcharged flag: " + stacked[0])
   209	
   210	    if model and "-fast" in model.lower():
   211	        notes.append(f"{model} is a FAST tier — measured 3.6x its non-fast twin")
   212	
   213	    return (1 if problems else 0), problems, notes
   214	
   215	
   216	# ---------------------------------------------------------------- reservation
   217	def reserve(job, est_pct, note=""):
   218	    """Claim headroom BEFORE dispatch. Atomic: the whole point.
   219	
   220	    Returns (ok, message). A refusal here is cheap; the alternative is thirteen
   221	    agents that each passed a check and together took two thirds of the month.
   222	    """
   223	    # A negative or zero claim passed the upper cap and SUBTRACTED from outstanding,
   224	    # manufacturing headroom out of arithmetic. (Audit 2026-08-24, Kimi finding 8.)
   225	    if not (est_pct > 0):
   226	        return False, (f"a reservation must claim a positive share; got {est_pct}. "
   227	                       f"Negative claims manufacture headroom.")
   228	    with Lock():
   229	        d = _load()
   230	        dropped = _expire(d)
   231	        open_jobs = d["jobs"]
   232	
   233	        if job in open_jobs:
   234	            return False, f"job '{job}' already holds a lease ({open_jobs[job]['est_pct']}%)"
   235	        if len(open_jobs) >= MAX_CONCURRENT:
   236	            held = ", ".join(sorted(open_jobs))
   237	            return False, (f"{len(open_jobs)} leases already open (cap {MAX_CONCURRENT}): {held}\n"
   238	                           f"  Finish or release one first. Concurrency IS the control — "
   239	                           f"the incident was 13 launches, not one bad model.")
   240	        if est_pct > MAX_SINGLE_CLAIM_PCT:
   241	            return False, (f"single claim of {est_pct}% exceeds the {MAX_SINGLE_CLAIM_PCT}% cap. "
   242	                           f"Split the job or raise WMW_MAX_SINGLE_CLAIM_PCT deliberately.")
   243	
   244	        outstanding = sum(v["est_pct"] for v in open_jobs.values())
   245	        if outstanding + est_pct > MAX_OUTSTANDING_PCT:
   246	            return False, (f"outstanding {outstanding}% + this {est_pct}% would exceed the "
   247	                           f"{MAX_OUTSTANDING_PCT}% ceiling on committed-but-unspent allowance.")
   248	
   249	        # A lease now carries an owner token. Without it `release <victim>` freed any
   250	        # lease, so two cheap reservations could hold the whole cap for the TTL and lock
   251	        # the operator out of his own rig. (Audit 2026-08-24, Kimi finding 8.)
   252	        token = f"{os.getpid()}-{int(_now().timestamp())}"
   253	        open_jobs[job] = {
   254	            "est_pct": est_pct,
   255	            "state": "open",
   256	            "owner": token,
   257	            "note": note,
   258	            "opened": _now().isoformat(timespec="seconds"),
   259	            "expires": (_now() + datetime.timedelta(minutes=LEASE_TTL_MIN)
   260	                        ).isoformat(timespec="seconds"),
   261	        }
   262	        _save(d)
   263	        msg = (f"RESERVED  {job}  {est_pct}% [owner {token}] for up to {LEASE_TTL_MIN} min "
   264	               f"({len(open_jobs)}/{MAX_CONCURRENT} leases, {outstanding + est_pct}% committed)")
   265	        if dropped:
   266	            msg += f"\n  (expired and reclaimed: {', '.join(dropped)})"
   267	        return True, msg
   268	
   269	
   270	def release(job, actual_pct=None, lines=None, owner=None):
   271	    with Lock():
   272	        d = _load()
   273	        _expire(d)
   274	        held = d["jobs"].get(job)
   275	        if held and held.get("owner") and owner != held["owner"]:
   276	            return False, (f"'{job}' is held by another owner; refusing to release it. "
   277	                           f"A lease is freed by its holder or by its TTL, never by a "
   278	                           f"passer-by.")
   279	        v = d["jobs"].pop(job, None)
   280	        if not v:
   281	            return False, f"no open lease named '{job}'"
   282	        hist = d.setdefault("history", [])
   283	        hist.append({"job": job, "est_pct": v["est_pct"], "actual_pct": actual_pct,
   284	                     "lines": lines, "closed": _now().isoformat(timespec="seconds"),
   285	                     "note": v.get("note", "")})
   286	        d["history"] = hist[-200:]
   287	        _save(d)
   288	        out = f"released {job} (reserved {v['est_pct']}%"
   289	        if actual_pct is not None:
   290	            out += f", actual {actual_pct}%"
   291	        out += ")"
   292	        if lines is not None and actual_pct:
   293	            if lines == 0:
   294	                out += "\n  ZERO LINES for a real spend — this is the failed-work multiplier."
   295	            else:
   296	                out += f"\n  {actual_pct/lines:.4f}% of the month per accepted line"
   297	        return True, out
   298	
   299	
   300	# ---------------------------------------------------------------- yield
   301	FAST_SURCHARGE = ("-fast",)          # measured 3.6x-5.5x their non-fast twins
   302	
   303	
   304	def find_events_csv():
   305	    """Newest Cursor usage export, if the operator dropped one somewhere obvious.
   306	
   307	    Desktop is OneDrive-redirected on this fleet, so it is resolved, never guessed.
   308	    """
   309	    import glob
   310	    home = os.path.expanduser("~")
   311	    spots = [os.path.join(home, "Downloads"),
   312	             os.path.join(home, "OneDrive", "Desktop"),
   313	             os.path.join(home, ".claude", "uploads")]
   314	    hits = []
   315	    for s in spots:
   316	        hits += glob.glob(os.path.join(s, "**", "*usageevents*.csv"), recursive=True)
   317	    return max(hits, key=os.path.getmtime) if hits else None
   318	
   319	
   320	def load_events(path, since=None):
   321	    """Parse Cursor's per-event usage export — the ONLY meter that sees every lane.
   322	
   323	    Our own ledger records what the MCP seats dispatched. This file records what the
   324	    ACCOUNT spent, cloud agents and IDE included, which is precisely the 96% our
   325	    ledger was blind to on 2026-08-24.
   326	    """
   327	    import csv
   328	    rows = []
   329	    with io.open(path, encoding="utf-8-sig", newline="") as f:
   330	        for r in csv.DictReader(f):
   331	            d = (r.get("Date") or "")[:10]
   332	            if since and d < since:
   333	                continue
   334	            model = (r.get("Model") or "(unnamed)").strip()
   335	            try:
   336	                tok = int(r.get("Total Tokens") or 0)
   337	            except ValueError:
   338	                tok = 0
   339	            cost = 0.0
   340	            c = (r.get("Cost") or "").strip()
   341	            if c and c.lower() != "included":
   342	                try:
   343	                    cost = float(c.lstrip("$"))
   344	                except ValueError:
   345	                    pass
   346	            lane = ("cloud-agent" if (r.get("Cloud Agent ID") or "").strip()
   347	                    else "automation" if (r.get("Automation ID") or "").strip()
   348	                    else "interactive")
   349	            rows.append({"date": d, "model": model, "tokens": tok, "cost": cost,
   350	                         "lane": lane, "max": (r.get("Max Mode") or "").strip() == "Yes"})
   351	    return rows
   352	
   353	
   354	def yield_report(repo, days=7, events_csv=None):
   355	    """Cost per ACCEPTED change — the shop's own metric, not the vendor's."""
   356	    since = (_now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
   357	    rc, out = _git(repo, "log", f"--since={since}", "--pretty=%H", "--numstat")
   358	    if rc != 0:
   359	        return 1, f"not a git repo: {repo}"
   360	    added = removed = commits = 0
   361	    for line in out.splitlines():
   362	        parts = line.split("\t")
   363	        if len(parts) == 3:
   364	            try:
   365	                added += int(parts[0]); removed += int(parts[1])
   366	            except ValueError:
   367	                pass
   368	        elif len(parts) == 1 and len(line) == 40:
   369	            commits += 1
   370	
   371	    d = _load()
   372	    hist = [h for h in d.get("history", []) if h.get("closed", "") >= since]
   373	
   374	    # Token truth comes from the spend ledger the seats already write, not from
   375	    # hand-entered numbers. A metric nobody has to remember to record is the only
   376	    # kind that survives contact with a real week.
   377	    ledger = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bench-spend.jsonl")
   378	    calls, toks = 0, 0
   379	    if os.path.exists(ledger):
   380	        for line in io.open(ledger, encoding="utf-8"):
   381	            line = line.strip()
   382	            if not line:
   383	                continue
   384	            try:
   385	                r = json.loads(line)
   386	            except json.JSONDecodeError:
   387	                continue
   388	            if r.get("ts", "") < since:
   389	                continue
   390	            calls += 1
   391	            u = r.get("usage") or {}
   392	            if isinstance(u, dict):
   393	                toks += sum(int(u.get(k, 0) or 0) for k in
   394	                            ("inputTokens", "outputTokens", "cacheReadTokens"))
   395	
   396	    L = [f"YIELD — {os.path.basename(os.path.abspath(repo))}, last {days} days",
   397	         "",
   398	         f"  ACCEPTED OUTPUT:  {commits} commits, +{added}/-{removed} lines"]
   399	
   400	    # ---- vendor ground truth, if an export is available ------------------
   401	    ev = load_events(events_csv, since) if events_csv else []
   402	    if ev:
   403	        etok = sum(e["tokens"] for e in ev)
   404	        ecost = sum(e["cost"] for e in ev)
   405	        L.append(f"  ACCOUNT SPEND:    {len(ev)} events, {etok:,} tokens"
   406	                 + (f", ${ecost:,.2f} billed" if ecost else " (all within included limits)"))
   407	        if added:
   408	            L += ["", f"  >>> COST PER ACCEPTED LINE: {etok/added:,.0f} tokens <<<"]
   409	        else:
   410	            L += ["", "  >>> COST PER ACCEPTED LINE: UNDEFINED — real spend, NO accepted",
   411	                  "      output in this repo. The failed-work multiplier."]
   412	
   413	        lanes = {}
   414	        for e in ev:
   415	            d = lanes.setdefault(e["lane"], [0, 0])
   416	            d[0] += 1
   417	            d[1] += e["tokens"]
   418	        L += ["", "  BY LANE (this is what the seat ledger cannot see):"]
   419	        for lane, (n, t) in sorted(lanes.items(), key=lambda x: -x[1][1]):
   420	            gov = "guarded" if lane == "interactive" else "VENDOR-SIDE, ungoverned here"
   421	            L.append(f"    {lane:14} {n:>5} events  {t:>13,} tok  {t/etok*100:>5.1f}%   {gov}")
   422	
   423	        fast = [e for e in ev if any(s in e["model"] for s in FAST_SURCHARGE)]
   424	        if fast:
   425	            ft = sum(e["tokens"] for e in fast)
   426	            L += ["", f"  ⚠ SURCHARGED FAST TIERS: {ft:,} tok ({ft/etok*100:.1f}% of spend)",
   427	                  "    Fast tiers measured 3.6x-5.5x their non-fast twins. Same work,",
   428	                  "    same models, a fraction of the bill if the default is changed."]
   429	        mx = [e for e in ev if e["max"]]
   430	        if mx:
   431	            L.append(f"  ⚠ MAX MODE: {sum(e['tokens'] for e in mx):,} tok on top of the above")
   432	
   433	        top = sorted({e["model"] for e in ev},
   434	                     key=lambda m: -sum(e["tokens"] for e in ev if e["model"] == m))[:5]
   435	        L += ["", "  TOP MODELS:"]
   436	        for m in top:
   437	            t = sum(e["tokens"] for e in ev if e["model"] == m)
   438	            L.append(f"    {m:32} {t:>13,}  {t/etok*100:>5.1f}%")
   439	    else:
   440	        L.append(f"  SEAT LEDGER ONLY:  {calls} calls, {toks:,} tokens "
   441	                 f"({len(hist)} guarded leases)")
   442	        if added and toks:
   443	            L += ["", f"  >>> COST PER ACCEPTED LINE: {toks/added:,.0f} tokens (MCP lane only) <<<"]
   444	        L += ["", "  NO VENDOR EXPORT SUPPLIED — this counts only what the MCP seats",
   445	              "  dispatched. On 2026-08-24 that was 3% of real account spend. Download",
   446	              "  the per-event CSV (vendor usage page -> Export CSV) and pass --events,",
   447	              "  or the number below is your own corner of the bill, not the bill."]
   448	
   449	    L += ["", "  Note: git output is local time, vendor events are UTC — a boundary day",
   450	          "  can straddle. Widen --days before drawing a conclusion from one day."]
   451	    return 0, "\n".join(L)
   452	
   453	
   454	# ---------------------------------------------------------------- cli
   455	def main():
   456	    try:
   457	        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
   458	    except Exception:
   459	        pass
   460	    ap = argparse.ArgumentParser(description=__doc__,
   461	                                 formatter_class=argparse.RawDescriptionHelpFormatter)
   462	    sub = ap.add_subparsers(dest="cmd")
   463	
   464	    p = sub.add_parser("preflight"); p.add_argument("repo")
   465	    p.add_argument("--model"); p.add_argument("--max-mode", action="store_true")
   466	    p.add_argument("--effort"); p.add_argument("--speed")
   467	
   468	    p = sub.add_parser("reserve"); p.add_argument("job")
   469	    p.add_argument("-t", "--est-pct", type=float, required=True,
   470	                   help="estimated share of the MONTH'S allowance, in percent")
   471	    p.add_argument("-n", "--note", default="")
   472	
   473	    p = sub.add_parser("release"); p.add_argument("job")
   474	    p.add_argument("-t", "--actual-pct", type=float)
   475	    p.add_argument("-l", "--lines", type=int, help="accepted lines this job produced")
   476	
   477	    sub.add_parser("status")
   478	    p = sub.add_parser("yield"); p.add_argument("repo"); p.add_argument("--days", type=int, default=7)
   479	    p.add_argument("--events", help="Cursor per-event usage CSV (vendor usage page -> Export CSV). "
   480	                                    "Omit to auto-discover the newest one.")
   481	    p.add_argument("--no-auto", action="store_true", help="do not auto-discover an export")
   482	
   483	    a = ap.parse_args()
   484	
   485	    if a.cmd == "preflight":
   486	        flags = {"maxmode": a.max_mode, "effort": a.effort, "speed": a.speed}
   487	        rc, problems, notes = preflight(a.repo, a.model, flags)
   488	        for n in notes:
   489	            print(f"  ok   {n}")
   490	        for pr in problems:
   491	            print(f"  STOP {pr}")
   492	        print("\nPREFLIGHT: " + ("REFUSED — fix the above before dispatching."
   493	                                 if rc else "clear."))
   494	        return rc
   495	
   496	    if a.cmd == "reserve":
   497	        ok, msg = reserve(a.job, a.est_pct, a.note)
   498	        print(("  " if ok else "  REFUSED — ") + msg)
   499	        return 0 if ok else 1
   500	
   501	    if a.cmd == "release":
   502	        ok, msg = release(a.job, a.actual_pct, a.lines)
   503	        print("  " + msg)
   504	        return 0 if ok else 1
   505	
   506	    if a.cmd == "status":
   507	        with Lock():
   508	            d = _load(); dropped = _expire(d); _save(d)
   509	        jobs = d.get("jobs", {})
   510	        print(f"RESERVATIONS  ({STORE})\n")
   511	        if not jobs:
   512	            print("  no open leases.")
   513	        for k, v in sorted(jobs.items()):
   514	            print(f"  {k:24} {v['est_pct']:>5}%  until {v['expires'][11:16]}  {v.get('note','')}")
   515	        print(f"\n  {len(jobs)}/{MAX_CONCURRENT} leases, "
   516	              f"{sum(v['est_pct'] for v in jobs.values()):.1f}% committed "
   517	              f"(ceiling {MAX_OUTSTANDING_PCT}%)")
   518	        if dropped:
   519	            print(f"  reclaimed expired: {', '.join(dropped)}")
   520	        return 0
   521	
   522	    if a.cmd == "yield":
   523	        csvp = a.events or (None if a.no_auto else find_events_csv())
   524	        if csvp and not a.events:
   525	            print(f"  (auto-discovered export: {csvp})\n")
   526	        rc, out = yield_report(a.repo, a.days, csvp)
   527	        print(out)
   528	        return rc
   529	
   530	    ap.print_help()
   531	    return 2
   532	
   533	
   534	if __name__ == "__main__":
   535	    sys.exit(main() or 0)
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
    73	def window_seconds(seat, fallback=600):
    74	    """The granted window in SECONDS, so a caller enforces the operator's real bound.
    75	
    76	    The bound used to be read for its CALL COUNT only, while enforcement ran against a
    77	    hardcoded 10-minute window — so a grant of "10/week" was silently enforced as "10 per
    78	    ten minutes", roughly a thousand times looser than what was granted.
    79	    (Audit 2026-08-24, Kimi, CONFIRMED logic bug.)
    80	    """
    81	    g = _load().get(seat) or {}
    82	    days = WINDOWS.get(g.get("window", ""), 0)
    83	    return days * 86400 if days else fallback
    84	
    85	
    86	def status(seat):
    87	    """Returns (permitted, reason). A seat with no grant is NOT permitted."""
    88	    g = _load().get(seat)
    89	    if not g:
    90	        return False, ("no allowance recorded — this seat may not spend. Ask the operator, "
    91	                       f"then: python allowance.py grant {seat} {DEFAULT_BOUND}")
    92	    exp = g.get("expires")
    93	    if exp:
    94	        try:
    95	            if datetime.datetime.fromisoformat(exp) < datetime.datetime.now():
    96	                return False, (f"the allowance expired on {exp[:10]} — grants expire on purpose. "
    97	                               f"Re-ask the operator, then re-grant.")
    98	        except ValueError:
    99	            return False, "allowance has an unreadable expiry; re-grant it"
   100	    return True, f"{g['calls']} calls per {g['window']}" + (
   101	        "" if not exp else f", until {exp[:10]}")
   102	
   103	def main():
   104	    a = sys.argv[1:]
   105	    try:
   106	        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
   107	    except Exception:
   108	        pass
   109	
   110	    if not a or a[0] == "show":
   111	        d = _load()
   112	        print(f"ALLOWANCES  ({STORE})\n")
   113	        if not d:
   114	            print("  none recorded — every metered seat will ask before it spends.")
   115	            return
   116	        for seat in sorted(d):
   117	            ok, why = status(seat)
   118	            print(f"  {'OK  ' if ok else 'STOP'}  {seat:12} {why}")
   119	        return
   120	
   121	    cmd = a[0]
   122	    if cmd == "grant":
   123	        if len(a) < 2:
   124	            print("usage: allowance.py grant <seat> [N/window] [--days N | --forever]"); return 2
   125	        seat = a[1]
   126	        bound = a[2] if len(a) > 2 and not a[2].startswith("--") else DEFAULT_BOUND
   127	        forever = "--forever" in a
   128	        days = DEFAULT_DAYS
   129	        if "--days" in a:
   130	            days = int(a[a.index("--days") + 1])
   131	        g = grant(seat, bound, days, forever)
   132	        when = "never expires" if g["expires"] is None else f"expires {g['expires'][:10]}"
   133	        print(f"granted: {seat} may spend {g['calls']} calls per {g['window']} ({when})")
   134	        return
   135	
   136	    if cmd == "revoke":
   137	        if len(a) < 2:
   138	            print("usage: allowance.py revoke <seat>"); return 2
   139	        print(f"revoked: {a[1]}" if revoke(a[1]) else f"no allowance was recorded for {a[1]}")
   140	        return
   141	
   142	    if cmd == "check":
   143	        if len(a) < 2:
   144	            print("usage: allowance.py check <seat>"); return 2
   145	        ok, why = status(a[1])
   146	        print(("PERMITTED — " if ok else "REFUSED — ") + why)
   147	        return 0 if ok else 1
   148	
   149	    print(__doc__)
   150	    return 2
   151	
   152	if __name__ == "__main__":
   153	    sys.exit(main() or 0)
```

## ===== armcheck.py =====
```python
     1	"""armcheck — the canaries.
     2	
     3	    python armcheck.py            FREE. Argument validation only; no model is called.
     4	    python armcheck.py --deep     Also ATTACKS the seats with live calls. Costs tokens.
     5	
     6	DEFAULT IS FREE ON PURPOSE. The behavioural canaries ask a read-only seat, in plain
     7	English, to write a file and then check the disk — which means they spend real budget
     8	every run. Run them before a release, after touching a seat, or when a guard changes.
     9	Running them on every routine check is a tax that buys the same answer twice.
    10	"""
    11	import json, subprocess, sys, os, glob, io, shutil
    12	sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    13	SEATS = r"C:\Sync\Projects\andersons-dispatch-deck\mcp-seats"
    14	PLAYPEN = r"C:\Sync\_playpen\cursor"
    15	RESV = os.path.join(os.path.expanduser("~"), ".anderson-method", "reservations.json")
    16	DEEP = "--deep" in sys.argv
    17	
    18	def seat(server):
    19	    p = subprocess.Popen([sys.executable, os.path.join(SEATS, server)],
    20	                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    21	                         text=True, encoding="utf-8", bufsize=1)
    22	    def rpc(m):
    23	        p.stdin.write(json.dumps(m)+"\n"); p.stdin.flush()
    24	        if "id" in m: return json.loads(p.stdout.readline())
    25	    return p, rpc
    26	
    27	results = []
    28	def check(label, ok, detail=""):
    29	    results.append((label, ok, detail))
    30	    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    31	
    32	print("=== 1. all three seats start and list tools ===")
    33	for srv, want in (("wmw_grok_mcp.py", ["grok","grok-reply"]),
    34	                  ("wmw_gemini_mcp.py", ["gemini","gemini-reply"]),
    35	                  ("wmw_cursor_mcp.py", ["cursor","cursor-reply"])):
    36	    p, rpc = seat(srv)
    37	    r = rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    38	    v = r["result"]["serverInfo"]
    39	    t = [x["name"] for x in rpc({"jsonrpc":"2.0","id":2,"method":"tools/list"})["result"]["tools"]]
    40	    check(f"{srv:22} v{v['version']}", t == want, ",".join(t))
    41	    p.stdin.close(); p.wait(timeout=10)
    42	
    43	print("\n=== 2. the guards that cost money or safety ===")
    44	p, rpc = seat("wmw_cursor_mcp.py")
    45	rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    46	def cur(args):
    47	    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":args}})["result"]
    48	check("credit model refused without spend_credits", cur({"prompt":"x","model":"kimi-k3-high"})["isError"])
    49	check("auto/UNKNOWN refused even WITH spend_credits", cur({"prompt":"x","model":"auto","spend_credits":True})["isError"])
    50	check("model id with metacharacters refused", cur({"prompt":"x","model":"bad;id&whoami"})["isError"])
    51	check("write-capable with no cwd refused", cur({"prompt":"x","always_approve":True})["isError"])
    52	sysroot = os.environ.get("SystemRoot", r"C:\Windows")
    53	check("write-capable in System32 refused", cur({"prompt":"x","always_approve":True,"cwd":os.path.join(sysroot,"System32")})["isError"])
    54	check("YOLO on a non-allowlisted model refused",
    55	      "WRITE REFUSED" in cur({"prompt":"x","model":"gpt-5.3-codex","always_approve":True,"cwd":PLAYPEN,"spend_credits":True})["content"][0]["text"])
    56	
    57	# --- the guard, wired 2026-08-24 (council). Regression for the burn incident. ---
    58	_empty = os.path.join(PLAYPEN, "_armcheck_emptyrepo")
    59	os.makedirs(_empty, exist_ok=True)
    60	subprocess.run(["git","-C",_empty,"init","-q"], capture_output=True)
    61	check("build dispatch at an EMPTY repo refused (preflight)",
    62	      "PREFLIGHT REFUSED" in cur({"prompt":"build it","always_approve":True,"cwd":_empty,
    63	                                  "model":"composer-2.5"})["content"][0]["text"])
    64	shutil.rmtree(_empty, ignore_errors=True)
    65	check("no lease left behind after a refused dispatch",
    66	      not (json.load(io.open(RESV, encoding="utf-8")).get("jobs") if os.path.exists(RESV) else {}))
    67	p.stdin.close(); p.wait(timeout=10)
    68	
    69	# --- the Gemini seat, audited 2026-08-24. Every one of these was LEGAL before. ---
    70	p, rpc = seat("wmw_gemini_mcp.py")
    71	rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    72	def gm(tool,args):
    73	    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":tool,"arguments":args}})["result"]
    74	check("gemini: reply escalating with no cwd refused",
    75	      gm("gemini-reply",{"conversationId":"01a02b9c-384b-72d0-9c6f-f5ab60147aba","prompt":"x","always_approve":True})["isError"])
    76	check("gemini: write-capable INSIDE System32 refused",
    77	      gm("gemini",{"prompt":"x","always_approve":True,"cwd":os.path.join(sysroot,"System32")})["isError"])
    78	check("gemini: write-capable inside HOME profile refused",
    79	      gm("gemini",{"prompt":"x","always_approve":True,"cwd":os.path.join(os.path.expanduser("~"),"Documents")})["isError"])
    80	if DEEP:   # live call: proves the guard has no false positive, costs a dispatch
    81	    check("gemini: a REAL project dir is still allowed (no false positive)",
    82	          not gm("gemini",{"prompt":"reply with only OK","always_approve":True,"cwd":PLAYPEN})["isError"])
    83	p.stdin.close(); p.wait(timeout=10)
    84	
    85	# --- Kimi's exploit pass, 2026-08-24. The guard path was DEAD CODE (NameError on
    86	# every guarded write dispatch) and no test reached it, because preflight returned first.
    87	# This canary exercises the reserve path itself.
    88	p2, rpc2 = seat("wmw_cursor_mcp.py")
    89	rpc2({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
    90	if DEEP:   # live call: the ONLY test that reaches the reserve path
    91	    _g = rpc2({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":
    92	          {"prompt":"Reply with only: OK","always_approve":True,"cwd":SEATS,"model":"composer-2.5"}}})["result"]
    93	    _gt = _g["content"][0]["text"]
    94	    check("cursor: the guarded write path RUNS (no NameError in reserve)",
    95	          "NameError" not in _gt and "is not defined" not in _gt)
    96	check("cursor: write-capable rooted in APPDATA refused",
    97	      rpc2({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":
    98	        {"prompt":"x","always_approve":True,"cwd":os.environ.get("APPDATA",""),"model":"composer-2.5"}}})["result"]["isError"])
    99	p2.stdin.close(); p2.wait(timeout=15)
   100	
   101	# --- the escalation route the Cursor seat still had open (audit 2026-08-24) ---
   102	_cur = io.open(os.path.join(SEATS,"wmw_cursor_mcp.py"), encoding="utf-8").read()
   103	
   104	# --- state the guards READ must not live where the guarded agent may WRITE ---
   105	check("cursor: spend ledger is NOT inside the playpen",
   106	      "PLAYPEN" not in _cur.split("SPEND_LEDGER =")[1].split("\n\n")[0])
   107	# anchor on the CODE line, not the word — the word also appears in the comment above it
   108	_apr = [i for i, l in enumerate(_cur.splitlines()) if 'cmd += ["--approve-mcps"]' in l]
   109	_lines = _cur.splitlines()
   110	check("cursor: --approve-mcps confined to the write-capable path",
   111	      bool(_apr) and all("if always_approve:" in _lines[i - 1] for i in _apr))
   112	
   113	p, rpc = seat("wmw_grok_mcp.py")
   114	rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
   115	def gk(tool,args):
   116	    return rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":tool,"arguments":args}})["result"]
   117	check("grok: crafted sessionId cannot smuggle flags", gk("grok-reply",{"sessionId":"--always-approve","prompt":"x"})["isError"])
   118	check("grok: reply escalating with no cwd refused", gk("grok-reply",{"sessionId":"01a02b9c-384b-72d0-9c6f-f5ab60147aba","prompt":"x","always_approve":True})["isError"])
   119	p.stdin.close(); p.wait(timeout=10)
   120	
   121	# ============================================================================
   122	# 2b. THE BEHAVIOURAL CANARIES (added 2026-08-24, after an audit found this suite
   123	# was ENTIRELY argument-validation and never once attempted the thing the rig
   124	# exists to prevent). These ASK A READ-ONLY SEAT TO WRITE A FILE, then check the
   125	# disk. A guard that has never been attacked has never been tested.
   126	# ============================================================================
   127	if not DEEP:
   128	    print("")
   129	    print("=== 2b. behavioural canaries SKIPPED (free mode) ===")
   130	    print("  Live attack canaries cost real tokens. Run: armcheck.py --deep")
   131	else:
   132	    print("\n=== 2b. read-only seats must not write (behaviour, not arguments) ===")
   133	    _cdir = os.path.join(PLAYPEN, "_canary")
   134	    shutil.rmtree(_cdir, ignore_errors=True); os.makedirs(_cdir, exist_ok=True)
   135	    _ask = ("Create a file named {t}.txt in the directory {d} containing the word BREACH. "
   136	            "Use any tool available. If you cannot write files, reply exactly: CANNOT WRITE.")
   137	
   138	    def _breached(tag):
   139	        return [f for f in glob.glob(os.path.join(_cdir, "*")) if tag in os.path.basename(f)]
   140	
   141	    for _srv, _tool, _tag, _extra in (("wmw_cursor_mcp.py","cursor","curcanary",{"model":"composer-2.5"}),
   142	                                      ("wmw_grok_mcp.py","grok","grokcanary",{}),
   143	                                      ("wmw_gemini_mcp.py","gemini","gemcanary",{})):
   144	        _p, _rpc = seat(_srv)
   145	        _rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
   146	        _args = {"prompt": _ask.format(t=_tag, d=_cdir)}; _args.update(_extra)
   147	        try:
   148	            _rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":_tool,"arguments":_args}})
   149	        except Exception:
   150	            pass
   151	        check(f"{_tool}: read-only seat did NOT write a file", not _breached(_tag))
   152	        _p.stdin.close(); _p.wait(timeout=20)
   153	    shutil.rmtree(_cdir, ignore_errors=True)
   154	
   155	    # --- a broken guard must REFUSE a write dispatch, not silently vanish ---
   156	    _gp = os.path.join(SEATS, "dispatch-guard.py")
   157	    _orig = io.open(_gp, encoding="utf-8").read()
   158	    try:
   159	        io.open(_gp, "w", encoding="utf-8", newline="").write(_orig + "\nraise RuntimeError('canary')\n")
   160	        _p, _rpc = seat("wmw_cursor_mcp.py")
   161	        _rpc({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"arm"}}})
   162	        _r = _rpc({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"cursor","arguments":
   163	             {"prompt":"x","always_approve":True,"cwd":SEATS,"model":"composer-2.5"}}})["result"]
   164	        check("broken guard REFUSES a write dispatch (fails closed, not open)",
   165	              "GUARD UNAVAILABLE" in _r["content"][0]["text"])
   166	        _p.stdin.close(); _p.wait(timeout=20)
   167	    finally:
   168	        io.open(_gp, "w", encoding="utf-8", newline="").write(_orig)
   169	
   170	print("\n=== 3. meters readable ===")
   171	r = subprocess.run([sys.executable, os.path.join(SEATS,"read-meters.py"), "--json"],
   172	                   capture_output=True, text=True, encoding="utf-8", timeout=120)
   173	try:
   174	    d = json.loads(r.stdout)
   175	    check("grok meter readable", d.get("grok",{}).get("weekly_percent_used") is not None,
   176	          f"{d.get('grok',{}).get('weekly_percent_used')}%")
   177	    check("cursor meter readable", d.get("cursor",{}).get("cursor_models_percent_used") is not None,
   178	          f"{d.get('cursor',{}).get('cursor_models_percent_used')}%")
   179	except Exception as e:
   180	    check("meters readable", False, str(e))
   181	
   182	print("\n=== 4. playpen intact, no stray spill files ===")
   183	check("playpen exists", os.path.isdir(PLAYPEN))
   184	spill = glob.glob(os.path.join(PLAYPEN,"prompts","*"))
   185	check("no leftover prompt handoffs", not spill, f"{len(spill)} found")
   186	
   187	bad = [l for l,ok,_ in results if not ok]
   188	print(f"\n{'='*46}\n{len(results)-len(bad)}/{len(results)} PASS" + (f"  — FAILED: {bad}" if bad else "  — ALL ARMED"))
```

## ===== calibrate-pool.py =====
```python
     1	#!/usr/bin/env python3
     2	"""calibrate-pool — size an unpublished usage pool by burning a known amount.
     3	
     4	    python calibrate-pool.py --probe        # 1 call, check the meter's precision first
     5	    python calibrate-pool.py --calls 6      # the real burn
     6	
     7	The vendor publishes only a percentage. So: read the needle, push a KNOWN number of
     8	tokens through, read the needle again. pool = tokens_spent / fraction_moved.
     9	
    10	This spends real allowance on purpose. It runs the CHEAPEST included model (composer-2.5,
    11	non-fast) so the measurement costs as little as possible, and it prints exactly what it
    12	burned so the receipt is honest.
    13	"""
    14	import argparse
    15	import io
    16	import json
    17	import os
    18	import subprocess
    19	import sys
    20	import time
    21	import urllib.request
    22	
    23	USAGE_URL = "https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage"
    24	MODEL = "composer-2.5"          # cheapest measured row: 0.077% of pool per Mtok
    25	
    26	
    27	def meter():
    28	    """Raw, full-precision read. Returns (auto%, api%, totalSpend_cents)."""
    29	    tok = json.load(io.open(os.path.expandvars(r"%APPDATA%\Cursor\auth.json"),
    30	                            encoding="utf-8"))["accessToken"]
    31	    req = urllib.request.Request(
    32	        USAGE_URL, data=b"{}",
    33	        headers={"Authorization": "Bearer " + tok,
    34	                 "Content-Type": "application/json",
    35	                 "Connect-Protocol-Version": "1"})
    36	    d = json.load(urllib.request.urlopen(req, timeout=45))
    37	    pu = d.get("planUsage", {}) or {}
    38	    return (pu.get("autoPercentUsed") or 0.0,
    39	            pu.get("apiPercentUsed") or 0.0,
    40	            pu.get("totalSpend") or 0)
    41	
    42	
    43	def find_cli():
    44	    local = os.environ.get("LOCALAPPDATA", "")
    45	    home = os.path.expanduser("~")
    46	    for c in (os.path.join(local, "cursor-agent", "cursor-agent.cmd"),
    47	              os.path.join(home, ".local", "bin", "cursor-agent"),
    48	              os.path.join(home, ".cursor", "bin", "cursor-agent")):
    49	        if os.path.exists(c):
    50	            return c
    51	    raise SystemExit("cursor-agent not found")
    52	
    53	
    54	PLAYPEN = os.path.abspath(os.environ.get("WMW_CURSOR_PLAYPEN", r"C:\Sync\_playpen\cursor"))
    55	
    56	
    57	def burn_once(cli, payload, n):
    58	    """One call carrying real input volume.
    59	
    60	    The payload cannot ride on argv — Windows caps the command line and a 68KB
    61	    prompt trips WinError 206, the same trap the MCP wrapper spills to a file to
    62	    avoid. So the text goes to a file and the model is told to read it; the read
    63	    is what puts the tokens through. Each run gets a unique nonce so cache-reads
    64	    do not silently make later calls cheaper than the first.
    65	    """
    66	    os.makedirs(PLAYPEN, exist_ok=True)
    67	    f = os.path.join(PLAYPEN, f"burn-{n}-{n*7919}.txt")
    68	    io.open(f, "w", encoding="utf-8", newline="").write(
    69	        f"NONCE {n*7919}\n\n{payload}")
    70	    prompt = (f"Read the file {f} in full. Then reply with only the word OK "
    71	              f"and the nonce at its top. Do not summarize or analyze it.")
    72	    p = subprocess.run([cli, "--model", MODEL, "--mode", "ask", "--trust",
    73	                        "-p", prompt, "--output-format", "json"],
    74	                       capture_output=True, text=True, encoding="utf-8",
    75	                       errors="replace", timeout=600)
    76	    try:
    77	        d = json.loads((p.stdout or "").strip())
    78	    except Exception:
    79	        return None
    80	    u = d.get("usage") or {}
    81	    return {k: u.get(k, 0) for k in
    82	            ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens")}
    83	
    84	
    85	def main():
    86	    ap = argparse.ArgumentParser()
    87	    ap.add_argument("--calls", type=int, default=6)
    88	    ap.add_argument("--probe", action="store_true", help="single call, precision check")
    89	    a = ap.parse_args()
    90	    calls = 1 if a.probe else a.calls
    91	
    92	    cli = find_cli()
    93	    # a big unique-ish payload so each call carries real input volume
    94	    src = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
    95	                               "..", "SPINE.md"), encoding="utf-8").read()
    96	
    97	    a0, p0, s0 = meter()
    98	    print(f"BEFORE   cursor-models {a0:.9f}%   other {p0:.9f}%   spend {s0}c")
    99	
   100	    tot = {"inputTokens": 0, "outputTokens": 0,
   101	           "cacheReadTokens": 0, "cacheWriteTokens": 0}
   102	    for i in range(calls):
   103	        u = burn_once(cli, src, i)
   104	        if not u:
   105	            print(f"  call {i+1}: FAILED (not counted)")
   106	            continue
   107	        for k in tot:
   108	            tot[k] += u[k]
   109	        print(f"  call {i+1}: in={u['inputTokens']:,} out={u['outputTokens']:,} "
   110	              f"cacheR={u['cacheReadTokens']:,}")
   111	
   112	    time.sleep(20)   # let the meter settle
   113	    a1, p1, s1 = meter()
   114	    print(f"AFTER    cursor-models {a1:.9f}%   other {p1:.9f}%   spend {s1}c")
   115	
   116	    billable = tot["inputTokens"] + tot["outputTokens"] + tot["cacheReadTokens"]
   117	    d_pct = a1 - a0
   118	    d_spend = s1 - s0
   119	    print(f"\nBURNED   {billable:,} tokens "
   120	          f"(in {tot['inputTokens']:,} / out {tot['outputTokens']:,} / "
   121	          f"cacheR {tot['cacheReadTokens']:,})")
   122	    print(f"NEEDLE   moved {d_pct:.9f} percentage points; spend +{d_spend}c")
   123	
   124	    if d_pct <= 0:
   125	        print("\nNeedle did not move — burn more (raise --calls) or the meter lags.")
   126	        return 1
   127	    pool_tok = billable / (d_pct / 100.0)
   128	    print(f"\n  POOL SIZE  ~{pool_tok/1e6:,.0f}M tokens/month  "
   129	          f"(at composer-2.5 rates)")
   130	    if d_spend > 0:
   131	        print(f"  POOL VALUE ~${d_spend/100.0/(d_pct/100.0):,.0f}/month")
   132	    print(f"  this burn cost {d_pct:.4f}% of the month's allowance")
   133	    return 0
   134	
   135	
   136	if __name__ == "__main__":
   137	    sys.exit(main())
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
