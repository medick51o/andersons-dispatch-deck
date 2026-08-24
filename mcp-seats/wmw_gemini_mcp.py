#!/usr/bin/env python3
"""wmw-gemini — MCP stdio server wrapping the Antigravity CLI (Google seat). v1.3

Persistent Gemini/Antigravity seat for Claude Code, sibling of wmw-grok:
  gemini(prompt, ...)              start a new conversation -> reply + conversationId
  gemini-reply(conversationId, ..) continue that conversation with full context

v1.1 (2026-08-22, council findings): honest error detection, strict UTF-8 stdio,
argument validation, per-request exception boundary, prompt-length guard (the
CLI takes the prompt as an argv argument; Windows caps a command line at 32K
chars — oversized prompts get a clean error, not a crash), and the reply footer
reports the effective model/brain (`brain: UNREPORTED` when the CLI's JSON
does not say — so an independence preflight can fail closed instead of assuming
green = Gemini). v1.2: UUID-validated conversation ids + no-leading-dash argv guard (a crafted id
could otherwise smuggle CLI flags), --conversation= equals form, absolute-path-first
exe lookup, stdin closed. Install/registration: see README.md in this folder.
Requires Python 3.10+ on PATH.

v1.4: the read-only path now pins `--mode plan` explicitly instead of
inheriting whatever the machine's settings happen to allow.

Bakes in the two headless croak-fixes: --print-timeout 60m (the CLI default of
5 minutes killed long tasks) and --dangerously-skip-permissions behind
`always_approve` (headless runs can never click a permission prompt).

Transport: newline-delimited JSON-RPC 2.0 over stdio. Stdlib only.
Known limitation (documented, queued): requests are handled one at a time; a
long-running call blocks the loop and cancellation is not supported.
"""
import json
import os
import shutil
import subprocess
import sys

PRINT_TIMEOUT = "60m"
PROC_TIMEOUT_S = 3900
MAX_ARGV_PROMPT = 25000
MAX_REPLY_CHARS = 400_000  # chars; Windows command-line hard cap is 32767 for the whole line

def _utf8_stdio():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def find_agy():
    # Known install path FIRST (substitute-binary defence); PATH is the fallback.
    home = os.path.expanduser("~")
    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    for cand in (
        os.path.join(local, "agy", "bin", "agy.exe"),        # Windows
        os.path.join(home, ".antigravity", "bin", "agy"),    # macOS / Linux
        os.path.join(home, ".local", "bin", "agy"),
        os.path.join(home, "agy", "bin", "agy"),
    ):
        if os.path.isfile(cand):
            return cand
    return shutil.which("agy")

_UUID_RE = __import__("re").compile(r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z")

def _safe_id(value, label):
    """Session ids are argv values: a leading '-' would be reparsed as a CLI flag."""
    if not isinstance(value, str) or not _UUID_RE.match(value):
        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
    return value

def _safe_argv(value, label):
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip() or value.lstrip().startswith("-"):
        raise ValueError(f"'{label}' must be a non-empty string that does not start with '-'")
    return value

def _extract_json(raw):
    dec = json.JSONDecoder()
    idx = raw.find("{")
    while idx != -1:
        try:
            obj, _ = dec.raw_decode(raw[idx:])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
        idx = raw.find("{", idx + 1)
    return None

def run_gemini(prompt, conversation_id=None, cwd=None, model=None, always_approve=False):
    exe = find_agy()
    if not exe:
        return True, "Antigravity CLI not found (PATH or %LOCALAPPDATA%\\agy\\bin\\agy.exe)."
    if cwd and not os.path.isdir(cwd):
        return True, f"cwd is not a directory: {cwd}"
    if len(prompt) > MAX_ARGV_PROMPT:
        return True, (f"prompt is {len(prompt)} chars; this seat's CLI takes the prompt on the "
                      f"command line and Windows caps that at ~32K. Keep prompts under "
                      f"{MAX_ARGV_PROMPT} chars — write long material to a file and (with "
                      f"always_approve: true) ask Gemini to read the file instead.")
    cmd = [exe]
    if conversation_id:
        cmd += [f"--conversation={conversation_id}"]
    if model:
        cmd += ["--model", model]
    if always_approve:
        cmd += ["--dangerously-skip-permissions"]
    else:
        # Read-only used to mean "we simply omit the skip-permissions flag", i.e. we
        # trusted whatever the machine's own settings allowed. Both Grok seats flagged
        # that independently on 2026-08-23. Pin the CLI's own planning mode instead, so
        # the restraint is ours and explicit rather than inherited from a config file.
        cmd += ["--mode", "plan"]
    cmd += ["-p", prompt, "--output-format", "json", "--print-timeout", PRINT_TIMEOUT]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=PROC_TIMEOUT_S, cwd=cwd or None,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return True, f"Antigravity timed out after {PROC_TIMEOUT_S}s"
    except OSError as e:
        return True, f"could not launch agy: {e}"
    raw = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    data = _extract_json(raw)
    if data is None:
        return True, (f"agy exited {proc.returncode} with no parseable JSON.\n"
                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
    text = data.get("response")
    cid = data.get("conversation_id")
    status = data.get("status", "unknown")
    if proc.returncode != 0 or status != "SUCCESS" or not isinstance(cid, str) or not cid:
        return True, (f"agy run failed (exit {proc.returncode}, status {status}, "
                      f"conversationId={cid!r}).\ntext: {str(text)[:1000]}\nstderr: {err[:1000]}")
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    if len(text) > MAX_REPLY_CHARS:
        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-gemini] ...truncated at {MAX_REPLY_CHARS} chars]"
    # Effective model/brain: agy can rent non-Gemini brains (the Overflow Valve), and an
    # independence preflight must be able to fail closed when the brain is unknown.
    # NEVER promote the REQUESTED model into the brain slot: the CLI can rent a non-Gemini
    # brain, and a preflight must be able to fail closed. Only the CLI's own JSON counts.
    reported = data.get("model") or data.get("model_name")
    brain = reported if isinstance(reported, str) and reported else (
        f"UNREPORTED (requested: {model})" if model else "UNREPORTED")
    footer = (f"\n\n---\n[wmw-gemini] conversationId: {cid} · status: {status}"
              f" · brain: {brain} · turns: {data.get('num_turns', '?')}")
    return False, text + footer

def _safe_cwd(cwd, always_approve):
    """A write-capable seat may not be pointed at a home or system directory."""
    if not always_approve:
        return cwd
    # A write-capable reply used to arrive with NO cwd at all and run wherever this
    # server happened to be launched. Absent is not safe -- it is unbounded.
    if cwd is None:
        raise ValueError("a write-capable Gemini session REQUIRES an explicit cwd — "
                         "point it at a project directory")
    real = os.path.realpath(cwd)
    home = os.path.realpath(os.path.expanduser("~"))
    # The filesystem ROOT is banned exactly (everything is inside it, so containment
    # there would ban the whole disk -- a false positive that would push the operator
    # to disable the guard). Every other banned location is banned WITH its subtree,
    # because equality alone left C:\Windows\System32 legal under a banned C:\Windows.
    root = os.path.realpath(os.path.abspath(os.sep))
    subtree = {home}
    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
        v = os.environ.get(env)
        if v:
            subtree.add(os.path.realpath(v))
    if real == root:
        raise ValueError("refusing a write-capable session at the filesystem root — "
                         "point cwd at a project directory")
    for b in subtree:
        if real == b or real.lower().startswith(b.rstrip(os.sep).lower() + os.sep):
            raise ValueError(f"refusing a write-capable session at or inside {b} — "
                             f"point cwd at a project directory")
    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".config"):
        if os.path.basename(real) == secret or os.sep + secret in real + os.sep:
            raise ValueError(f"refusing a write-capable session inside {secret}")
    return real   # hand back the RESOLVED path, never the caller's string

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

TOOLS = [
    {
        "name": "gemini",
        "description": (
            "Start a NEW conversation with Gemini via the Antigravity CLI (Google "
            "subscription seat). Returns the reply plus a conversationId footer (including the "
            "effective brain — check it before counting this seat as an independent Gemini vote); "
            "continue the same conversation with gemini-reply. Each fresh call is an independent, "
            "blind session. Set always_approve true when Gemini must edit files or run commands "
            "(headless permission prompts otherwise stall the run). Keep prompts under ~25K chars; "
            "put long material in a file for Gemini to read."
        ),
        "annotations": {"destructiveHint": True, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The task or message for Gemini."},
                "cwd": {"type": "string", "description": "Working directory (repo path for build work)."},
                "model": {"type": "string", "description": "Optional model override (agy models lists them; exact-match strings)."},
                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts. Required for build work; default false."},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "gemini-reply",
        "description": (
            "Continue an existing Gemini/Antigravity conversation by conversationId (from a "
            "prior gemini call's footer). Gemini retains the full prior context."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "conversationId from a previous gemini/gemini-reply call."},
                "prompt": {"type": "string", "description": "The follow-up message."},
                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true."},
                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts this turn. Requires cwd."},
            },
            "required": ["conversationId", "prompt"],
        },
    },
]

def _tool_call(name, args):
    if not isinstance(args, dict):
        return True, "arguments must be an object"
    try:
        if name == "gemini":
            approve = _opt_bool(args, "always_approve")
            return run_gemini(
                _req_str(args, "prompt"),
                cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve),
                model=_safe_argv(_opt_str(args, "model"), "model"),
                always_approve=approve,
            )
        if name == "gemini-reply":
            # A reply may escalate to write-capable exactly like a fresh call, so it must
            # clear the SAME cwd gate. It did not: it accepted no cwd at all and handed
            # always_approve straight through, so a continued session could run
            # --dangerously-skip-permissions in whatever directory this server was
            # launched from. The Grok seat has guarded this since 2026-08-23; the fix was
            # never propagated here. (Audit 2026-08-24, Gemini seat, CONFIRMED.)
            approve = _opt_bool(args, "always_approve")
            return run_gemini(
                _req_str(args, "prompt"),
                conversation_id=_safe_id(args.get("conversationId"), "conversationId"),
                cwd=_safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve),
                always_approve=approve,
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
                "serverInfo": {"name": "wmw-gemini", "version": "1.5.0"},
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
            print(f"[wmw-gemini] internal error: {e}", file=sys.stderr)
            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
