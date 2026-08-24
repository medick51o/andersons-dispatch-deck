#!/usr/bin/env python3
"""wmw-grok — MCP stdio server wrapping the Grok Build CLI. v1.3

Gives Claude Code a persistent Grok seat:
  grok(prompt, ...)            start a new Grok conversation -> reply + sessionId
  grok-reply(sessionId, ...)   continue that conversation with full context

v1.1 (2026-08-22, council findings): prompt passed via --prompt-file (no Windows
32K command-line limit), honest error detection (nonzero exit / error JSON /
missing sessionId => isError), strict UTF-8 stdio, argument validation,
per-request exception boundary.
v1.4: read-only now also denies MCPTool/WebFetch/WebSearch and pins
--permission-mode default -- without those a "read-only" seat could call another
MCP seat and have IT write (reproduced live, then verified fixed).
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
MAX_REPLY_CHARS = 400_000   # cap what we hand back to the client

# Tools a read-only seat may never use. Deny rules bind on every platform; the CLI's
# --sandbox does not (Landlock/Seatbelt only, silently unenforced on Windows).
#
# MCPTool IS THE IMPORTANT ONE. Denying Write/Edit/Bash locks the front door and
# leaves every other door open: a "read-only" seat can call ANOTHER MCP server --
# including the sibling wmw-* seats -- and have it do the writing. Reproduced live
# 2026-08-23: a read-only Grok wrote a file through the Codex seat. Verified fixed
# by re-running that canary with MCPTool denied.
#
# NOTE: MultiEdit is NOT a recognised permission name in this CLI (unknown names
# are skipped with a warning); the real edit classes are Edit / Write /
# NotebookEdit. It is kept only as a harmless alias guard.
DENY_RULES = ("Write", "Edit", "MultiEdit", "NotebookEdit", "Bash",
              "MCPTool", "WebFetch", "WebSearch")

def _utf8_stdio():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def find_grok():
    # Known install path FIRST: a stray "grok" earlier on PATH would run with this user's
    # credentials. PATH is only the fallback.
    home = os.path.expanduser("~")
    for cand in (
        os.path.join(home, ".grok", "bin", "grok.exe"),   # Windows
        os.path.join(home, ".grok", "bin", "grok"),       # macOS / Linux
        os.path.join(home, ".local", "bin", "grok"),
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

def run_grok(prompt, session_id=None, cwd=None, model=None, always_approve=False,
             allow_web_search=False):
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
            # Read-only enforced by DENY RULES, not --sandbox: the CLI's sandbox is
            # Landlock/Seatbelt only and fails OPEN on Windows (council 2026-08-22 proved a
            # write succeeded under --sandbox read-only). Deny rules were verified to block it.
            for rule in DENY_RULES:
                cmd += ["--deny", rule]
            # The user's ~/.grok/config.toml may set permission_mode = "always-approve".
            # Deny rules still win for names they match, but everything NOT denied is
            # then auto-approved. Pin the mode explicitly so config cannot widen us.
            # --no-subagents does NOT stop a spawn: Grok proved it live on 2026-08-23 by
            # spawning a general-purpose child that ran to completion (it could not write,
            # because children inherit the deny rules, but it ran). `Agent` is not a valid
            # --deny class, so removing the tool outright is the only real kill switch.
            cmd += ["--disallowed-tools", "Agent"]
            cmd += ["--permission-mode", "default", "--no-subagents", "--no-memory"]
            if not allow_web_search:
                cmd += ["--disable-web-search"]
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
    if len(text) > MAX_REPLY_CHARS:
        text = text[:MAX_REPLY_CHARS] + f"\n\n[wmw-grok] ...truncated at {MAX_REPLY_CHARS} chars]"
    usage = data.get("modelUsage") or {}
    model_used = next(iter(usage), "unknown-model")
    footer = f"\n\n---\n[wmw-grok] sessionId: {sid} · model: {model_used} · turns: {data.get('num_turns', '?')}"
    return False, text + footer

def _safe_cwd(cwd, always_approve):
    """A write-capable seat may not be pointed at a home or system directory."""
    if not always_approve:
        return cwd
    if cwd is None:
        raise ValueError("always_approve requires an explicit cwd naming the project "
                         "directory the seat may write in")
    real = os.path.realpath(cwd)
    if not os.path.isdir(real):
        raise ValueError(f"cwd is not a directory: {cwd}")
    norm = lambda x: os.path.normcase(os.path.realpath(x))
    def within(child, parent):
        c, pa = norm(child), norm(parent)
        if c == pa:
            return True
        try:
            return os.path.commonpath([c, pa]) == pa
        except ValueError:      # different drives
            return False
    # Exact-root bans first (home and drive root are legitimate parents of projects).
    for r in (os.path.expanduser("~"), os.path.abspath(os.sep)):
        if norm(real) == norm(r):
            raise ValueError(f"refusing a write-capable session rooted at {real} — "
                             f"point cwd at a project directory")
    # System trees are banned by CONTAINMENT: an exact-match check let
    # C:\Windows\System32 through as a mere descendant. Found by Grok, 2026-08-23.
    for env in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"):
        v = os.environ.get(env)
        if v and within(real, v):
            raise ValueError(f"refusing a write-capable session inside a system directory "
                             f"({v}) — point cwd at a project directory")
    # Case-insensitive segment match: ".SSH" used to slip past a case-sensitive test.
    parts = [x.lower() for x in norm(real).split(os.sep)]
    for secret in (".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
                   ".config", ".azure", ".kube", ".gnupg"):
        if secret in parts:
            raise ValueError(f"refusing a write-capable session inside {secret}")
    return real   # return the CANONICAL path, so a symlink cannot be re-pointed after validation

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
            "full context, call grok-reply with that sessionId. DEFAULT IS READ-ONLY: file writes, "
            "edits and shell are denied, and web search is off unless allow_web_search is true. "
            "Set always_approve true ONLY for build tickets — it lets Grok write files and run "
            "commands under cwd. Use for build dispatches, research, and council seats."
        ),
        "annotations": {"destructiveHint": True, "openWorldHint": True},
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The task or message for Grok."},
                "cwd": {"type": "string", "description": "Working directory for the session (repo path for build work). Required when always_approve is true; must not be a home/system directory."},
                "model": {"type": "string", "description": "Optional Grok model ID override."},
                "always_approve": {"type": "boolean", "description": "DANGEROUS: auto-approve all of Grok's tool use, including file writes and shell commands under cwd. Required for build work; default false = deny-listed read-only."},
                "allow_web_search": {"type": "boolean", "description": "Allow web search/fetch on a read-only call (default false; ignored when always_approve is true)."},
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
                "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory."},
                "always_approve": {"type": "boolean", "description": "Auto-approve Grok's tool use this turn (file writes, shell). Requires cwd."},
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
            approve = _opt_bool(args, "always_approve")
            cwd = _safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve)
            return run_grok(
                _req_str(args, "prompt"), cwd=cwd,
                model=_safe_argv(_opt_str(args, "model"), "model"),
                always_approve=approve,
                allow_web_search=_opt_bool(args, "allow_web_search"),
            )
        if name == "grok-reply":
            # A reply may escalate a read-only thread to write-capable, so it must clear the
            # SAME cwd guard the start tool does. Without this, the legal sequence was:
            # grok(cwd=<somewhere sensitive>) read-only, then grok-reply(always_approve=true)
            # with no path check at all. Found by Grok, 2026-08-23.
            approve = _opt_bool(args, "always_approve")
            reply_cwd = _safe_cwd(_safe_argv(_opt_str(args, "cwd"), "cwd"), approve)
            return run_grok(
                _req_str(args, "prompt"),
                session_id=_safe_id(args.get("sessionId"), "sessionId"),
                cwd=reply_cwd,
                always_approve=approve,
                allow_web_search=_opt_bool(args, "allow_web_search"),
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
                "serverInfo": {"name": "wmw-grok", "version": "1.5.0"},
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
