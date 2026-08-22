#!/usr/bin/env python3
"""wmw-grok — MCP stdio server wrapping the Grok Build CLI. v1.1

Gives Claude Code a persistent Grok seat:
  grok(prompt, ...)            start a new Grok conversation -> reply + sessionId
  grok-reply(sessionId, ...)   continue that conversation with full context

v1.1 (2026-08-22, council findings): prompt passed via --prompt-file (no Windows
32K command-line limit), honest error detection (nonzero exit / error JSON /
missing sessionId => isError), strict UTF-8 stdio, argument validation,
per-request exception boundary.
v1.2: UUID-validated session ids + no-leading-dash argv guard (a crafted id could
otherwise smuggle CLI flags), --resume= equals form, real read-only argv when
always_approve is false, absolute-path-first exe lookup, stdin closed. Requires Python 3.10+ on PATH.

Transport: newline-delimited JSON-RPC 2.0 over stdio. Stdlib only.
Known limitation (documented, queued): requests are handled one at a time; a
long-running call blocks the loop and cancellation is not supported.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

GROK_TIMEOUT_S = 3600

def _utf8_stdio():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def find_grok():
    # Known install path FIRST: a stray "grok" earlier on PATH would run with this user's
    # credentials. PATH is only the fallback.
    for cand in (
        os.path.expanduser(r"~\.grok\bin\grok.exe"),
        os.path.expanduser(r"~\.grok\bin\grok"),
        os.path.expanduser("~/.grok/bin/grok"),
    ):
        if os.path.isfile(cand):
            return cand
    return shutil.which("grok")

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
    """Find the first complete JSON object in raw text (banner-noise tolerant)."""
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

def run_grok(prompt, session_id=None, cwd=None, model=None, always_approve=False):
    exe = find_grok()
    if not exe:
        return True, "grok CLI not found on PATH or in ~/.grok/bin — is Grok Build installed?"
    if cwd and not os.path.isdir(cwd):
        return True, f"cwd is not a directory: {cwd}"
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md",
                                         delete=False) as f:
            f.write(prompt)
            tmp = f.name
        cmd = [exe]
        if session_id:
            cmd += [f"--resume={session_id}"]
        if model:
            cmd += ["-m", model]
        if cwd:
            cmd += ["--cwd", cwd]
        if always_approve:
            cmd += ["--always-approve"]
        if not always_approve:
            # read-only means read-only in argv, not in a comment or a config default
            cmd += ["--sandbox", "read-only", "--disable-web-search", "--no-subagents", "--no-memory"]
        cmd += ["--prompt-file", tmp, "--output-format", "json"]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=GROK_TIMEOUT_S,
                stdin=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired:
            return True, f"grok timed out after {GROK_TIMEOUT_S}s"
        except OSError as e:
            return True, f"could not launch grok: {e}"
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    raw = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    data = _extract_json(raw)
    if data is None:
        return True, (f"grok exited {proc.returncode} with no parseable JSON.\n"
                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
    if data.get("type") == "error":
        return True, f"grok error: {data.get('message', '(no message)')}\nstderr: {err[:1000]}"
    text = data.get("text")
    sid = data.get("sessionId")
    if proc.returncode != 0 or not isinstance(sid, str) or not sid:
        return True, (f"grok run failed (exit {proc.returncode}, sessionId={sid!r}).\n"
                      f"text: {str(text)[:1000]}\nstderr: {err[:1000]}")
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    usage = data.get("modelUsage") or {}
    model_used = next(iter(usage), "unknown-model")
    footer = f"\n\n---\n[wmw-grok] sessionId: {sid} · model: {model_used} · turns: {data.get('num_turns', '?')}"
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

TOOLS = [
    {
        "name": "grok",
        "description": (
            "Start a NEW persistent conversation with Grok (Grok Build CLI, xAI subscription seat). "
            "Returns Grok's reply plus a sessionId footer. To continue the same conversation with "
            "full context, call grok-reply with that sessionId. Grok has web search and can read/"
            "edit files in cwd when always_approve is true. Use for build dispatches, research, "
            "and council seats."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The task or message for Grok."},
                "cwd": {"type": "string", "description": "Working directory for the session (repo path for build work)."},
                "model": {"type": "string", "description": "Optional Grok model ID override."},
                "always_approve": {"type": "boolean", "description": "Auto-approve Grok's tool use (file edits, commands). Required for build work; default false (read/research only)."},
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "grok-reply",
        "description": (
            "Continue an existing Grok conversation by sessionId (from a prior grok call's footer). "
            "Grok retains the full prior context of that session."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "sessionId": {"type": "string", "description": "The sessionId returned by a previous grok/grok-reply call."},
                "prompt": {"type": "string", "description": "The follow-up message."},
                "always_approve": {"type": "boolean", "description": "Auto-approve Grok's tool use this turn."},
            },
            "required": ["sessionId", "prompt"],
        },
    },
]

def _tool_call(name, args):
    if not isinstance(args, dict):
        return True, "arguments must be an object"
    try:
        if name == "grok":
            return run_grok(
                _req_str(args, "prompt"), cwd=_safe_argv(_opt_str(args, "cwd"), "cwd"),
                model=_safe_argv(_opt_str(args, "model"), "model"),
                always_approve=_opt_bool(args, "always_approve"),
            )
        if name == "grok-reply":
            return run_grok(
                _req_str(args, "prompt"),
                session_id=_safe_id(args.get("sessionId"), "sessionId"),
                always_approve=_opt_bool(args, "always_approve"),
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
                "serverInfo": {"name": "wmw-grok", "version": "1.2.0"},
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
    return None  # notification — no response

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
        except Exception as e:  # request boundary: never let one request kill the server
            print(f"[wmw-grok] internal error: {e}", file=sys.stderr)
            resp = {"jsonrpc": "2.0", "id": msg.get("id"),
                    "error": {"code": -32603, "message": f"internal error: {e}"}} if "id" in msg else None
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
