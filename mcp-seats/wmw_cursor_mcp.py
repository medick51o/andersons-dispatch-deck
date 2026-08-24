#!/usr/bin/env python3
"""wmw-cursor — MCP stdio server wrapping the Cursor Agent CLI. v2.0

A persistent seat on the Cursor model pool:
  cursor(prompt, ...)          start a new conversation -> reply + sessionId
  cursor-reply(sessionId, ...) continue that conversation with full context

⚠ THE ONE METERED SEAT. Every other seat in this shop rides a flat subscription
at $0 marginal. This one draws Cursor's pools, and there are TWO of them:

  ♾️ INCLUDED  "Cursor Models" — composer-*, cursor-grok-*. Cursor's own models,
               generous included usage on a Pro plan. The pool you vibe-code with.
  💸 CREDITS   "Other Models" — claude-*, gpt-*, gemini-*, kimi-*, glm-*, billed
               at API prices (~$20/month included, then pay-as-you-go).
  ⚠️ UNKNOWN   Anything unrecognised, incl. `auto`. Refused unconditionally.

"Fast" tiers are a surcharge, not a convenience: Composer 2.5 goes $0.5/$2.5 ->
$3/$15 per million (6x output); Cursor Grok 4.6 doubles. Their own louder class.

THE PLAYPEN. Cursor gets a directory of its own to work in, so scratch files,
prompt handoffs and temp work never land in a real project and never block a
run. Everything the seat needs to write, it writes there. Override with
WMW_CURSOR_PLAYPEN.

SECURITY (v2.0 — after a live command-injection reproduction on this machine):
The Windows Cursor CLI is a .cmd shim that forwards its arguments to PowerShell,
so a prompt containing shell metacharacters could execute host commands. Proven,
not theoretical: a crafted prompt wrote a file. Therefore NO caller-controlled
string is ever placed on the command line. Prompts are always spilled to a file
in the playpen and referenced by a generated ASCII pointer; model ids must match
a strict identifier pattern; session ids must be UUIDs; cwd is passed to the OS
as a working directory, never as an argument.

Read-only is REAL and canary-verified: without always_approve the CLI runs with
`--mode ask`, its own read-only mode. (v1.0 used `--trust` alone, which
AUTHORISES a workspace rather than restricting it, and a "read-only" call wrote
a file straight through it.) `always_approve: true` passes --yolo and REQUIRES an
explicit cwd, which may not be a home, system or credential directory.

Requires Python 3.10+ and a logged-in Cursor CLI (`cursor-agent login`).
Known limitation: one request at a time; no cancellation mid-run.
"""
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CURSOR_TIMEOUT_S = 3600
MAX_REPLY_CHARS = 400_000
DEFAULT_MODEL = "composer-2.5"   # NON-fast on purpose: fast tiers are a surcharge

# ---------------------------------------------------------------------------
# THE COUNCIL LOCK (boss ruling 2026-08-23, revisitable).
# A COUNCIL runs on SUBSCRIPTION seats only — house Claude / Codex / Grok /
# Gemini. Never on the Cursor pool. One cheap Cursor review is fine; a fan-out of
# several metered seats answering the same brief is not, and that is exactly the
# shape that quietly drains a pool.
#
# Enforced, not merely written down: at most COUNCIL_LOCK_MAX billable calls in
# any COUNCIL_LOCK_WINDOW_S seconds. A normal review sails through; a 4-seat
# metered council trips the wire and is refused.
# Lift deliberately with WMW_CURSOR_COUNCIL_LOCK=off (and say so to the boss).
# ---------------------------------------------------------------------------
COUNCIL_LOCK_MAX = int(os.environ.get("WMW_CURSOR_COUNCIL_MAX", "2"))
COUNCIL_LOCK_WINDOW_S = int(os.environ.get("WMW_CURSOR_COUNCIL_WINDOW", "600"))
COUNCIL_LOCK_ON = os.environ.get("WMW_CURSOR_COUNCIL_LOCK", "on").lower() != "off"

# ---------------------------------------------------------------------------
# THE PLAYPEN — Cursor's own corner of the disk.
# ---------------------------------------------------------------------------
PLAYPEN = os.path.abspath(os.environ.get(
    "WMW_CURSOR_PLAYPEN", os.path.join("C:" + os.sep, "Sync", "_playpen", "cursor")))
PROMPTS_DIR = os.path.join(PLAYPEN, "prompts")
SPEND_LEDGER = os.environ.get("WMW_CURSOR_LEDGER", os.path.join(PLAYPEN, "bench-spend.jsonl"))

def _ensure_playpen():
    """Create the playpen on demand. Never let this break a call."""
    for d in (PLAYPEN, PROMPTS_DIR, os.path.join(PLAYPEN, "scratch")):
        try:
            os.makedirs(d, exist_ok=True)
        except OSError:
            return False
    readme = os.path.join(PLAYPEN, "README.md")
    if not os.path.exists(readme):
        try:
            with io.open(readme, "w", encoding="utf-8", newline="") as f:
                f.write(
                    "# Cursor's playpen\n\n"
                    "Scratch space for the `wmw-cursor` MCP seat. The seat writes prompt\n"
                    "handoffs (`prompts/`), scratch work (`scratch/`) and its spend ledger\n"
                    "here so none of that lands in a real project.\n\n"
                    "Safe to delete when nothing is running; it is recreated on demand.\n")
        except OSError:
            pass
    return True

# ---------------------------------------------------------------------------
# METER CLASSES (verified against Cursor's published pricing, 2026-08-23)
# ---------------------------------------------------------------------------
INCLUDED_PREFIXES = ("composer-", "cursor-grok-")
CREDIT_PREFIXES = ("claude-", "gpt-", "gemini-", "kimi-", "glm-")

# ---------------------------------------------------------------------------
# THE YOLO ALLOWLIST (boss ruling 2026-08-23).
# Only these families may run write-capable (--yolo). They are the two FREE,
# trusted seats: Composer and Cursor Grok. Everything else in the pool -- the
# Codex/Gemini/Claude mirrors, Kimi, GLM -- may read and advise, never write or
# execute, however the call is phrased.
#
# The boss's stated path: open cursor-codex and cursor-gemini next if this works
# out; Kimi and other foreign-lab models are explicitly NOT candidates today.
# Widening this tuple is the whole change -- keep it a deliberate, visible act.
# ---------------------------------------------------------------------------
YOLO_ALLOWLIST = ("composer-", "cursor-grok-")

def yolo_allowed(model_id):
    return (model_id or "").strip().lower().startswith(YOLO_ALLOWLIST)

# A model id may only ever be a plain identifier. Anything else cannot reach argv.
_MODEL_RE = re.compile(r"\A[a-z0-9][a-z0-9._-]{0,63}\Z")
_UUID_RE = re.compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                      r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")

def meter_class(model_id):
    m = (model_id or "").strip().lower()
    if not m or m == "auto" or not _MODEL_RE.match(m):
        return "UNKNOWN"
    fast = m.endswith("-fast")
    if m.startswith(INCLUDED_PREFIXES):
        return "INCLUDED-FAST" if fast else "INCLUDED"
    if m.startswith(CREDIT_PREFIXES):
        return "CREDITS-FAST" if fast else "CREDITS"
    return "UNKNOWN"

METER_MARK = {"INCLUDED": "♾️", "INCLUDED-FAST": "♾️💸",
              "CREDITS": "💸", "CREDITS-FAST": "🚨💳", "UNKNOWN": "⚠️"}

# THE CURSOR BANNER. The arrow is a CURSOR — its birthplace; the conductor's 🟡➤
# baton is the borrowed cousin. Every line this seat produces flies 🟣➤.
CURSOR_BANNER = "🟣➤"

BLOODLINE_MARK = {
    "Moonshot": "🌙",   # Kimi — Moonshot AI, literally the moon
    "Zhipu": "🔷",      # GLM
    "Cursor": "🎼",     # Composer — a composer writes the score
    "Anthropic": "🟠", "OpenAI": "🔵", "xAI": "⚫", "Google": "🟢",
    "UNKNOWN": "❓",
}

def _lineage(model_id):
    m = (model_id or "").lower()
    for pre, vendor in (("claude-", "Anthropic"), ("gpt-", "OpenAI"),
                        ("cursor-grok-", "xAI"), ("gemini-", "Google"),
                        ("kimi-", "Moonshot"), ("glm-", "Zhipu"),
                        ("composer-", "Cursor")):
        if m.startswith(pre):
            return vendor
    return "UNKNOWN"

def _log_spend(model, lineage, klass, usage, sid, ok, write_capable):
    """One append-only row per LAUNCHED call, success or not. Never breaks a call."""
    try:
        _ensure_playpen()
        row = {
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "model": model, "lineage": lineage, "meter": klass,
            "billable": bool(klass and klass.startswith("CREDITS")),
            "surcharged": bool(klass and klass.endswith("FAST")),
            "in": (usage or {}).get("inputTokens"),
            "out": (usage or {}).get("outputTokens"),
            "cache_read": (usage or {}).get("cacheReadTokens"),
            "session": sid, "ok": ok, "write_capable": write_capable,
        }
        with io.open(SPEND_LEDGER, "a", encoding="utf-8", newline="") as f:
            f.write(json.dumps(row) + "\n")
    except Exception as e:
        print(f"[wmw-cursor] spend-ledger write failed: {e}", file=sys.stderr)

def _recent_billable(window_s):
    """How many billable calls landed in the last window_s seconds, per the ledger."""
    if not os.path.exists(SPEND_LEDGER):
        return 0
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=window_s)
    n = 0
    try:
        for line in io.open(SPEND_LEDGER, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not r.get("billable"):
                continue
            try:
                ts = datetime.datetime.fromisoformat(r.get("ts", ""))
            except ValueError:
                continue
            if ts >= cutoff:
                n += 1
    except OSError:
        return 0
    return n

def _utf8_stdio():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def find_cursor_agent():
    # Known install path first (substitute-binary defence); PATH is the fallback.
    home = os.path.expanduser("~")
    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    for cand in (
        os.path.join(local, "cursor-agent", "cursor-agent.cmd"),   # Windows
        os.path.join(home, ".local", "bin", "cursor-agent"),       # macOS / Linux
        os.path.join(home, ".cursor", "bin", "cursor-agent"),
    ):
        if os.path.isfile(cand):
            return cand
    return shutil.which("cursor-agent")

def _safe_id(value, label):
    if not isinstance(value, str) or not _UUID_RE.match(value):
        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
    return value

def _safe_model(value):
    if value is None:
        return None
    if not isinstance(value, str) or not _MODEL_RE.match(value.strip().lower()):
        raise ValueError("'model' must be a plain model id such as 'composer-2.5' "
                         "(letters, digits, dot, dash, underscore only)")
    return value.strip().lower()

def _norm(path):
    return os.path.normcase(os.path.realpath(path))

def _is_within(child, parent):
    """True when child == parent or sits underneath it. Symlink-resolved, case-folded."""
    c, p = _norm(child), _norm(parent)
    if c == p:
        return True
    try:
        return os.path.commonpath([c, p]) == p
    except ValueError:      # different drives
        return False

def _safe_cwd(cwd, always_approve):
    """A write-capable seat needs an explicit cwd, and it may not be a sensitive one.

    Returns the CANONICAL path, so a symlink cannot be validated and then
    dereferenced somewhere else afterwards.
    """
    if not always_approve:
        return os.path.realpath(cwd) if cwd else None
    if cwd is None:
        raise ValueError("always_approve requires an explicit cwd naming the project "
                         "directory the seat may write in (the playpen is a fine choice: "
                         + PLAYPEN + ")")
    real = os.path.realpath(cwd)
    if not os.path.isdir(real):
        raise ValueError(f"cwd is not a directory: {cwd}")
    # The playpen is always allowed — that is its whole purpose.
    if _is_within(real, PLAYPEN):
        return real
    roots = [os.path.expanduser("~"), os.path.abspath(os.sep)]
    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)",
                "ProgramData", "USERPROFILE"):
        v = os.environ.get(env)
        if v:
            roots.append(v)
    for r in roots:
        if _norm(real) == _norm(r):
            raise ValueError(f"refusing a write-capable session rooted at {real} — "
                             f"point cwd at a project directory or the playpen")
    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
        v = os.environ.get(env)
        if v and _is_within(real, v):
            raise ValueError(f"refusing a write-capable session inside a system directory "
                             f"({v}) — point cwd at a project directory or the playpen")
    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
                   ".config", ".azure", ".kube", ".gnupg"):
        parts = [p.lower() for p in _norm(real).split(os.sep)]
        if secret in parts:
            raise ValueError(f"refusing a write-capable session inside {secret}")
    return real

def _extract_json(raw):
    """Last complete result object wins — the CLI streams status lines first."""
    dec = json.JSONDecoder()
    found = None
    idx = raw.find("{")
    while idx != -1:
        try:
            obj, _ = dec.raw_decode(raw[idx:])
            if isinstance(obj, dict) and obj.get("type") == "result":
                found = obj
            elif isinstance(obj, dict) and found is None:
                found = obj
        except json.JSONDecodeError:
            pass
        idx = raw.find("{", idx + 1)
    return found

def run_cursor(prompt, session_id=None, cwd=None, model=None, always_approve=False,
               spend_credits=False):
    exe = find_cursor_agent()
    if not exe:
        return True, ("Cursor CLI not found. Install it, then `cursor-agent login`. "
                      "(Windows: %LOCALAPPDATA%\\cursor-agent\\cursor-agent.cmd)")
    chosen = model or DEFAULT_MODEL
    klass = meter_class(chosen)

    # THE METER GUARD. UNKNOWN is refused unconditionally — spend_credits unlocks
    # only RECOGNISED third-party models, never an unidentified or auto-routed one.
    if klass == "UNKNOWN":
        return True, (
            f"{CURSOR_BANNER} ⚠️ REFUSED — '{chosen}' is not a recognised model id, or is "
            f"`auto` (which may route anywhere). Unknown lineage fails closed and cannot be "
            f"unlocked with spend_credits. Name an explicit model: composer-2.5 (free) or "
            f"cursor-grok-4.6-high (free); see BENCH-LEDGER.md for the metered ones.")
    if klass.startswith("CREDITS") and not spend_credits:
        return True, (
            f"{CURSOR_BANNER} 🚨 CREDIT GUARD — REFUSED BEFORE SPENDING\n\n"
            f"'{chosen}' is meter class {klass} ({_lineage(chosen)} lineage). It draws "
            f"Cursor's third-party CREDIT pool (~$20/month included, then pay-as-you-go at "
            f"API prices), not the included Cursor Models pool.\n\n"
            f"To spend credits deliberately, pass spend_credits: true. To stay free, use an "
            f"INCLUDED model: composer-2.5 (default) or cursor-grok-4.6-high.\n\n"
            f"'-fast' variants are a surcharge (Composer 2.5 costs 6x more output on Fast), "
            f"never a free speed-up.")

    if always_approve and not yolo_allowed(chosen):
        return True, (
            f"{CURSOR_BANNER} 🛑 WRITE REFUSED — '{chosen}' is not on the YOLO allowlist.\n\n"
            f"Only the free, trusted seats may run write-capable: composer-* and "
            f"cursor-grok-*. Every other pool model ({_lineage(chosen)} here) may read and "
            f"advise, never write or execute.\n\n"
            f"Boss ruling 2026-08-23. Re-run this as a read-only call (drop always_approve), "
            f"or hand the build to composer-2.5 / cursor-grok-4.6-high.")

    if klass.startswith("CREDITS") and COUNCIL_LOCK_ON:
        recent = _recent_billable(COUNCIL_LOCK_WINDOW_S)
        if recent >= COUNCIL_LOCK_MAX:
            return True, (
                f"{CURSOR_BANNER} 🛑 COUNCIL LOCK — REFUSED\n\n"
                f"{recent} billable Cursor calls already landed in the last "
                f"{COUNCIL_LOCK_WINDOW_S // 60} minutes, at the cap of {COUNCIL_LOCK_MAX}. "
                f"This looks like a COUNCIL fanning out onto metered seats.\n\n"
                f"Standing boss ruling (2026-08-23): a council runs on SUBSCRIPTION seats "
                f"only — house Claude, Codex, Grok, Gemini. Cursor-hosted models are not "
                f"council seats right now.\n\n"
                f"Free INCLUDED models (composer-2.5, cursor-grok-4.6-*) are unaffected. To "
                f"lift this deliberately set WMW_CURSOR_COUNCIL_LOCK=off — and say so to "
                f"the boss first."
            )

    _ensure_playpen()
    # No cwd? Work in the playpen — the seat always has somewhere legitimate to be.
    workdir = cwd or PLAYPEN
    if not os.path.isdir(workdir):
        return True, f"cwd is not a directory: {workdir}"

    # ---- PROMPT TRANSPORT --------------------------------------------------
    # NOTHING caller-controlled goes on the command line. The Windows CLI is a
    # .cmd shim forwarding to PowerShell; a crafted prompt CAN execute host
    # commands (reproduced 2026-08-23). The prompt always travels as a file in
    # the playpen; only a generated ASCII pointer is passed as an argument.
    spill_path = None
    try:
        fd, spill_path = tempfile.mkstemp(prefix="prompt_", suffix=".md", dir=PROMPTS_DIR)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(prompt)
        except OSError as e:
            return True, f"could not write the prompt handoff file: {e}"

        # ASCII ONLY, deliberately: this string is the single thing that reaches argv,
        # and the Windows .cmd shim mangles (or executes) anything exotic.
        pointer = ("Read the file at " + spill_path.replace("\\", "/") +
                   " which contains your full instructions. Follow them exactly and answer "
                   "them directly. Do not modify or delete that file; it is a scratch "
                   "handoff and is cleaned up automatically.")
        if not pointer.isascii():
            return True, ("the prompt handoff path contains non-ASCII characters; set "
                          "WMW_CURSOR_PLAYPEN to a plain ASCII path")

        cmd = [exe]
        if session_id:
            cmd += [f"--resume={session_id}"]
        cmd += ["--model", chosen]
        cmd += ["--yolo"] if always_approve else ["--mode", "ask", "--trust"]
        # Let the seat use the MCP servers configured in ~/.cursor/mcp.json, so a
        # Cursor seat gets the same workshop the house seats have. NOTE: this
        # auto-approves whatever is in that file — keep it to read-only tools, and
        # deliberately NOT the sibling wmw-* seats: a seat that can drive another
        # seat can escalate around its own read-only mode (proved on wmw-grok,
        # 2026-08-23, where a read-only Grok wrote a file via the Codex seat).
        cmd += ["--approve-mcps"]
        cmd += ["-p", pointer, "--output-format", "json"]

        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=CURSOR_TIMEOUT_S, cwd=workdir,
                stdin=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired:
            _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
            return True, f"cursor-agent timed out after {CURSOR_TIMEOUT_S}s"
        except OSError as e:
            return True, f"could not launch cursor-agent: {e}"
    finally:
        if spill_path:
            try:
                os.unlink(spill_path)
            except (FileNotFoundError, OSError):
                pass

    raw = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    data = _extract_json(raw)
    # Only a run that produced NO result can be a trust refusal. Checking raw text
    # first was a self-inflicted false positive: a model reviewing this very file
    # quoted the phrase back and the wrapper refused its own review.
    if data is None and ("Workspace Trust Required" in raw or "Workspace Trust Required" in err):
        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
        return True, (f"Cursor refused {workdir} as untrusted. Point cwd at a project "
                      f"directory you trust, or leave cwd unset to use the playpen.")
    if data is None:
        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
        return True, (f"cursor-agent exited {proc.returncode} with no parseable JSON.\n"
                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
    if data.get("is_error") or data.get("subtype") not in (None, "success"):
        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"),
                   data.get("session_id") or session_id, False, always_approve)
        return True, (f"cursor-agent reported an error: {str(data.get('result'))[:1500]}\n"
                      f"stderr: {err[:800]}")
    text = data.get("result")
    sid = data.get("session_id")
    if proc.returncode != 0 or not isinstance(sid, str) or not sid:
        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"), sid or session_id,
                   False, always_approve)
        return True, (f"cursor-agent run failed (exit {proc.returncode}, session_id={sid!r}).\n"
                      f"result: {str(text)[:1000]}\nstderr: {err[:1000]}")
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    if len(text) > MAX_REPLY_CHARS:
        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-cursor] ...truncated at {MAX_REPLY_CHARS} chars]"

    usage = data.get("usage") or {}
    tok = (f"{usage.get('inputTokens', '?')} in / {usage.get('outputTokens', '?')} out"
           if usage else "usage unreported")
    mark = METER_MARK.get(klass, "⚠️")
    vendor = _lineage(chosen)
    blood = BLOODLINE_MARK.get(vendor, "❓")
    pool = ("Cursor Models pool — INCLUDED, no credits spent" if klass == "INCLUDED"
            else "Cursor Models pool — included, but a FAST-tier surcharge applies"
            if klass == "INCLUDED-FAST"
            else "third-party CREDIT pool — billed at API prices")
    _log_spend(chosen, vendor, klass, usage, sid, True, always_approve)
    money = ""
    if klass.startswith("CREDITS") or klass == "INCLUDED-FAST":
        money = (f"\n{CURSOR_BANNER} {mark} —— THIS CALL SPENT MONEY —— {mark} {CURSOR_BANNER}"
                 f"\n   {pool}")
    footer = (f"\n\n---\n{CURSOR_BANNER}{blood} [wmw-cursor] {mark} {vendor} · {chosen}"
              f"\n   sessionId: {sid} · meter: {klass} · {tok}{money}")
    return False, text + footer

def _req_str(args, key):
    v = args.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"'{key}' must be a non-empty string")
    return v

def _opt_str(args, key):
    v = args.get(key)
    if v is None:
        return None
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"'{key}' must be a non-empty string when given")
    return v

def _opt_bool(args, key):
    v = args.get(key)
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.lower() in ("true", "false"):
        return v.lower() == "true"
    raise ValueError(f"'{key}' must be a boolean")

_MODEL_NOTE = ("Model id (default composer-2.5 — the free, non-fast door). Free/INCLUDED: "
               "composer-2.5, cursor-grok-4.6-{low,medium,high,xhigh}, cursor-grok-4.5-*. "
               "Metered/CREDITS (need spend_credits): claude-*, gpt-*, gemini-*, kimi-*, "
               "glm-*. `auto` is refused. See BENCH-LEDGER.md; `cursor-agent models` lists all.")

TOOLS = [
    {
        "name": "cursor",
        "description": (
            "Start a NEW persistent conversation on the CURSOR MODEL POOL (Composer 2.5 by "
            "default; Cursor Grok, Codex, Kimi, GLM and other tiers via `model`). Returns the "
            "reply plus a sessionId footer; continue it with cursor-reply. ⚠ THE ONE METERED "
            "SEAT: composer-* and cursor-grok-* are INCLUDED (free); everything else bills "
            "Cursor's credit pool and is refused unless spend_credits is true. DEFAULT IS "
            "READ-ONLY (no code execution, no file writes). Set always_approve true only for "
            "build tickets, and then cwd is REQUIRED. With no cwd the seat works in its own "
            "playpen directory."
        ),
        "annotations": {"destructiveHint": True, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The task or message."},
                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory. Omit to work in the playpen."},
                "model": {"type": "string", "description": _MODEL_NOTE},
                "always_approve": {"type": "boolean", "description": "DANGEROUS: pass --yolo so the agent may write files and run commands under cwd. Default false = read-only."},
                "spend_credits": {"type": "boolean", "description": "Required to reach any THIRD-PARTY model (claude-/gpt-/gemini-/kimi-/glm-), billed at API prices against Cursor's credit pool. Ask the boss first."},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "cursor-reply",
        "description": (
            "Continue an existing Cursor-pool conversation by sessionId (from a prior cursor "
            "call's footer), with full prior context. Same meter rules apply."
        ),
        "annotations": {"destructiveHint": True, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "properties": {
                "sessionId": {"type": "string", "description": "sessionId from a previous cursor/cursor-reply call."},
                "prompt": {"type": "string", "description": "The follow-up message."},
                "model": {"type": "string", "description": _MODEL_NOTE},
                "cwd": {"type": "string", "description": "Working directory for this turn."},
                "always_approve": {"type": "boolean", "description": "Pass --yolo for this turn (write-capable); requires cwd."},
                "spend_credits": {"type": "boolean", "description": "Required to reach a third-party (credit-billed) model."},
            },
            "required": ["sessionId", "prompt"],
        },
    },
]

def _tool_call(name, args):
    if not isinstance(args, dict):
        return True, "arguments must be an object"
    try:
        if name in ("cursor", "cursor-reply"):
            approve = _opt_bool(args, "always_approve")
            cwd = _safe_cwd(_opt_str(args, "cwd"), approve)
            sid = _safe_id(args.get("sessionId"), "sessionId") if name == "cursor-reply" else None
            return run_cursor(
                _req_str(args, "prompt"), session_id=sid, cwd=cwd,
                model=_safe_model(_opt_str(args, "model")),
                always_approve=approve,
                spend_credits=_opt_bool(args, "spend_credits"),
            )
    except ValueError as e:
        return True, f"invalid arguments: {e}"
    return None

def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    is_notification = "id" not in msg
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "wmw-cursor", "version": "2.1.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        result = _tool_call(name, params.get("arguments") or {})
        if result is None:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
        is_err, text = result
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
    if not is_notification:
        return {"jsonrpc": "2.0", "id": mid,
                "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None

def main():
    _utf8_stdio()
    _ensure_playpen()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
            sys.stdout.flush()
            continue
        if not isinstance(msg, dict):
            continue
        try:
            resp = handle(msg)
        except Exception as e:
            print(f"[wmw-cursor] internal error: {e}", file=sys.stderr)
            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
