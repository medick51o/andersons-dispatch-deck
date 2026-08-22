# COUNCIL BRIEF — ROUND 2 (verification pass) — 2026-08-22

You are ONE seat on a four-vendor council. You are blind to the other seats. Round 1 reviewed this
same work and returned: REWORK (Codex), SHIP-WITH-FIXES (Grok, Gemini, Claude). The builder then
applied fixes. **Your job is to verify the FIXED state, not to re-litigate round 1.**

## What was claimed fixed

WRAPPERS (mcp-seats/*.py, now v1.2):
1. Large prompts crashed the Windows command line (32K limit) -> Grok now sends the prompt via
   --prompt-file; Gemini rejects >25K prompts with a clean error instead of crashing.
2. A crafted sessionId could smuggle CLI flags into the resumed session (e.g. sessionId
   "--always-approve"), because the CLI's --resume takes an OPTIONAL value -> ids must now match a
   UUID; no argv value (cwd/model) may start with "-"; resume uses the equals form (--resume=<id>).
3. "Read-only default" was only a doc claim -> when always_approve is false the Grok wrapper now
   passes real argv: --sandbox read-only --disable-web-search --no-subagents --no-memory.
4. PATH was searched before the known install path (substitute-binary risk) -> absolute install
   path is now preferred, PATH is the fallback; stdin is closed (DEVNULL).
5. Errors could look like success -> nonzero exit / error JSON / missing session id now return
   isError; UTF-8 stdio forced; per-request exception boundary so one bad request cannot kill the
   server; JSON extracted with raw_decode instead of first-brace.
6. Gemini's footer now reports the effective brain (UNREPORTED when unknown) so a rented
   non-Gemini brain cannot silently pass as an independent Gemini vote.

DOCTRINE:
7. SPINE existed in three divergent copies, two sharing a version string -> SPINE v2.0 is now the
   single canon, byte-identical in all six locations; it gained THE NOTATION v4.0 (owner of the
   emoji marks) and THE TRANSPORT LAW (persistent seats).
8. The transport laws were unowned and drifting across six files -> SPINE owns them; tier files
   (Deck SKILL, CREW v1.2) now render and cite rather than restate.
9. "Fresh call = blind seat" read as sufficient for independence -> now stated everywhere as
   necessary-but-not-sufficient (a reviewer also needs a different effective-model vendor, or to be
   human-launched).
10. Install was worded as mandatory -> now opt-in per vendor, offer-never-install, with a documented
    one-command removal, a declared Python prereq, and a documented one-request-at-a-time limitation.

## Your job

1. VERIFY each claimed fix against the actual current files. State PASS / FAIL / UNVERIFIED per item
   you check, with the evidence you used.
2. REGRESSION HUNT: did the fixes break anything or introduce new problems? (e.g. does UUID
   validation reject legitimate ids from either CLI? does the read-only argv break normal research
   calls? did the SPINE re-sync drop or contradict any pre-existing law?)
3. Anything still genuinely dangerous on a PUBLIC repo that strangers install from.

## Deliverable

Numbered findings, most severe first: severity (CRITICAL/MAJOR/MINOR/NIT) - file+location - what -
why it matters - concrete fix. Then a verification table of the 10 items. Then a verdict line:
SHIP / SHIP-WITH-FIXES / REWORK, one sentence, signed with your model name. No padding; "none found"
is a valid section.


===== FILE: mcp-seats/wmw_grok_mcp.py =====

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


===== FILE: mcp-seats/wmw_gemini_mcp.py =====

#!/usr/bin/env python3
"""wmw-gemini — MCP stdio server wrapping the Antigravity CLI (Google seat). v1.1

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
MAX_ARGV_PROMPT = 25000  # chars; Windows command-line hard cap is 32767 for the whole line

def _utf8_stdio():
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def find_agy():
    # Known install path FIRST (substitute-binary defence); PATH is the fallback.
    local = os.environ.get("LOCALAPPDATA", os.path.expanduser(r"~\AppData\Local"))
    cand = os.path.join(local, "agy", "bin", "agy.exe")
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
    # Effective model/brain: agy can rent non-Gemini brains (the Overflow Valve), and an
    # independence preflight must be able to fail closed when the brain is unknown.
    brain = data.get("model") or data.get("model_name") or (model if model else "UNREPORTED")
    footer = (f"\n\n---\n[wmw-gemini] conversationId: {cid} · status: {status}"
              f" · brain: {brain} · turns: {data.get('num_turns', '?')}")
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
                "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts this turn."},
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
            return run_gemini(
                _req_str(args, "prompt"), cwd=_safe_argv(_opt_str(args, "cwd"), "cwd"),
                model=_safe_argv(_opt_str(args, "model"), "model"),
                always_approve=_opt_bool(args, "always_approve"),
            )
        if name == "gemini-reply":
            return run_gemini(
                _req_str(args, "prompt"),
                conversation_id=_safe_id(args.get("conversationId"), "conversationId"),
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
                "serverInfo": {"name": "wmw-gemini", "version": "1.2.0"},
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


===== FILE: mcp-seats/README.md =====

# mcp-seats — persistent vendor seats for the method

*The method's models are crew, not vending machines. This folder rigs every vendor CLI into
Claude Code as a **persistent MCP seat**: the orchestrator starts a conversation with a seat,
gets a session id back, and can continue that exact conversation later with full context. No
more amnesia one-shots where the seat forgets everything between dispatches. Everything rides
the subscriptions you already pay — no API keys, no per-token bills.*

## What you get

| Seat | Server name | Start tool | Continue tool |
|---|---|---|---|
| Codex (OpenAI) | `codex` | `codex` | `codex-reply` + conversationId |
| Grok (xAI) | `grok` | `grok` | `grok-reply` + sessionId |
| Gemini (Google, via Antigravity) | `gemini` | `gemini` | `gemini-reply` + conversationId |

Server names are yours to choose at registration — this shop prefixes them with its machine name
(`wmw-grok`), you don't have to.

## Install

**Prereqs:** **Python 3.10+ on PATH** (`python --version` — the wrappers are stdlib-only, but
the registration commands invoke `python`; register the interpreter's full path if yours differs),
plus each vendor's CLI installed and logged in to your subscription. Verify before wiring:
`codex --version` · `grok --version` · `agy --version` (Antigravity). Wire only the seats you have —
the method degrades loud, not silent, when a vendor is missing.

**1 · Codex — one command** (its MCP server mode is built in):

```
claude mcp add --scope user codex -- codex mcp-server
```

(Windows: use `codex.cmd` if plain `codex` isn't found.)

**2 · Grok** — uses the bundled wrapper `wmw_grok_mcp.py` (stdlib-only Python, no dependencies):

```
claude mcp add --scope user grok -- python <path-to-this-folder>\wmw_grok_mcp.py
```

**3 · Gemini / Antigravity** — bundled wrapper `wmw_gemini_mcp.py`:

```
claude mcp add --scope user gemini -- python <path-to-this-folder>\wmw_gemini_mcp.py
```

**4 · Restart Claude Code.** New MCP tools only appear in fresh sessions. Then check
`claude mcp list` shows every seat `✔ Connected`.

## Opt-in, and clean removal

Vendors are suggestions — the method never requires you to own all four, and nothing here should
be installed on someone's machine unasked. The right flow is consent-first: the orchestrator
notices a CLI is present and OFFERS the upgrade ("you have Gemini — want a persistent seat
instead of blind one-shots?"). What registration actually does: adds one entry to your Claude
Code user config, nothing more — no PATH changes, no services, no edits to the vendor CLI's own
setup. Undo any seat with `claude mcp remove --scope user <name>`. The wrapper scripts are plain
stdlib Python you can read in two minutes.

## Acceptance test (run it before trusting a seat)

The codeword test, per seat: call the start tool with *"My codeword is REDHAWK. Reply with exactly:
STORED"*, take the session id from the reply footer, call the continue tool asking *"What is my
codeword?"* **PASS = the codeword comes back.** That proves real persistence, not a fresh session
wearing the same name.

## Why the wrappers exist (and what they quietly fix)

Codex ships an MCP server; Grok Build and Antigravity don't — but both have headless modes and
session resume, so a ~150-line stdlib wrapper closes the gap. The wrappers also bake in two fixes
for the classic "the seat croaked mid-task" failures of headless dispatching:

- **60-minute timeout** — Antigravity's headless default is 5 minutes; any longer task died mid-thought.
- **`always_approve` switch** — a headless run can never click a tool-permission prompt; without
  this flag a build task stalls on an unanswerable prompt until the timeout executes it. Pass
  `always_approve: true` on build tickets (with `cwd` pointed at the repo); omit it for read-only
  research and review work.

Adapting a wrapper to a NEW vendor CLI: only three parts change — the exe finder, the command-line
flags (headless flag, resume flag, JSON output flag), and the output parsing. The MCP plumbing at
the bottom never changes.

## Transport doctrine (the method's laws, applied to these tools)

- **Fresh call = blind seat.** A new start-tool call remembers nothing from any other session —
  exactly what council and review seats require. Reviewers are ALWAYS fresh calls; never brief a
  reviewer through a session that saw the build. Fresh is necessary, not sufficient — an
  independent review also needs a different effective-model vendor than the build (or a
  human-launched fresh seat); fresh-Codex reviewing Codex-built work is a self-check, not a review.
- **Reply-chain = the same seat continuing.** Use the continue tool for follow-ups inside one
  seat's owned lane. A reply-chained session stays in its owning-seat lineage forever — it can
  never become the independent reviewer of work its thread touched.
- Raw one-shots (`grok -p`, `codex exec`, `agy -p`) remain legal fallback transport; the
  persistent seats are the default.

## Known limitation (queued for v2)

Each wrapper handles one request at a time: a long-running seat call blocks that server's loop
(other seats are separate processes and unaffected), and in-flight calls cannot be cancelled
mid-run — the CLI keeps running until it finishes or times out. Fine for dispatch-and-wait
orchestration; not yet a concurrent job queue.


===== FILE: SETUP.md =====

# ADD — Setup: bring the arsenal online

Anderson's Dispatch Deck runs from **Claude Code** (the home CLI). The other three
vendors are separate CLIs you install and log into once; then Claude dispatches to them
headlessly. This is the install + auth + gotcha guide, plus a reachability probe so the
orchestrator knows what's actually online.

> Platform note: paths/commands below are Windows (the reference rig). Adapt for macOS/Linux.

---

## 0. Claude Code (the conductor) — already your home base
This is the CLI you're reading this in. It's the orchestrator; everything else hangs off
it. Nothing to install for ADD itself beyond dropping the `/dispatch` skill in
`~/.claude/skills/dispatch/`.

## 1. Codex (OpenAI) — the precise builder + sharpest reviewer
- **Install:** the OpenAI Codex CLI (npm or the official installer).
- **Auth:** log in with a ChatGPT/OpenAI plan (separate plan → its usage does NOT touch
  your Claude/Anthropic meter).
- **Dispatch pattern:** `codex exec --sandbox danger-full-access --skip-git-repo-check "<prompt>" < /dev/null`
- **GOTCHAS (learned the hard way):**
  - **Store/MSIX PowerShell kills it.** If your PowerShell is the Microsoft-Store (MSIX)
    build, Codex can't spawn a shell (CreateProcessAsUserW err 5). Fix: install real
    PowerShell from the **GitHub MSI** (not winget — winget reinstalls the MSIX), via
    elevated msiexec.
  - **OS-sandbox ACL bug** on some boxes → use the `--sandbox danger-full-access` lane
    (the working one). Add a `Bash(codex*)` allow-rule for hands-free dispatch.
  - **Always close stdin** headless (`< /dev/null`), or it hangs.
  - One clean goal per ticket — it refuses messy multi-fix tickets.

## 2. Grok (xAI) — the artist
- **Install:** the Grok CLI (lands at e.g. `C:\Users\<you>\.grok\bin\grok.exe`).
- **Auth:** log in with a **Super Grok / X Premium+** subscription (OIDC, no API key;
  token in `~/.grok/auth.json`).
- **Dispatch pattern:** `"<full path>\grok.exe" --prompt-file <file> --always-approve < /dev/null`
  (or `-p "<prompt>"`).
- **GOTCHAS:**
  - **Not on the tool-shell PATH** even when it's on your normal PATH — always use the
    FULL path when dispatching from an automation shell.
  - UI/art surface only ("reskins, doesn't rewire"). Require a trail-log entry per job.
  - Allow-rule for hands-free: `Bash("C:\Users\<you>\.grok\bin\grok.exe"*)`.

## 3. Gemini / Antigravity (Google) — the value powerhouse + image gen
- **Install:** `irm https://antigravity.google/cli/install.ps1 | iex` → `agy` at
  `C:\Users\<you>\AppData\Local\agy\bin\agy.exe`.
- **Auth:** log in with a **Google AI Pro** subscription. Do NOT chase the free "Login
  with Google" individuals OAuth — Google retired it (IneligibleTierError); Antigravity is
  the living path. *(Pricing/promos change over time — that's a current detail, not a
  requirement of the method. ADD treats every vendor as optional; use what you have.)*
- **Dispatch pattern:** `"<...>\agy.exe" -p "<prompt>" --model "Gemini 3.5 Flash (High)"`
  - Models under the sub: Gemini 3.5 Flash (Low/Med/High) · Gemini 3.1 Pro (Low/High) ·
    Claude Sonnet 4.6 · Claude Opus 4.6 · GPT-OSS 120B.
  - **Image gen (Nano Banana):** ask it to generate an image — runs on the SUB (no card
    needed); output lands in `~/.gemini/antigravity-cli/brain/<uuid>/*.jpg`.
- **GOTCHAS:**
  - Headless `-p` auto-denies external TOOL use (but writes to its brain dir + makes
    images fine). For code review, embed the code in the prompt.
  - The free AI-Studio KEY path 429s on images (no billing) — the SUB path does not.
  - ExecutionPolicy can block npm `.ps1` shims → `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## 4. Persistent seats (MCP) — wire the crew so it REMEMBERS

One-shot dispatches gave every seat amnesia: each call started from zero. The method now rigs
each vendor CLI into Claude Code as a **persistent MCP seat** — the orchestrator starts a
conversation with a seat, gets a session id back, and continues that exact conversation later
with full context. Same subscriptions, no API keys. **Opt-in, per vendor:** wire only the seats
you actually have and want — vendors are suggestions, and a missing one just isn't in the pool
(the method degrades loud, never demands a purchase). The orchestrator should OFFER this wiring
when it spots a CLI ("you have Gemini — want it persistent instead of amnesia one-shots?"), not
install it unasked. Registration is user-scope only, touches nothing else in your setup, and one
`claude mcp remove <name>` undoes it. Once a seat is wired, persistent is its default transport.

Full instructions, the wrapper scripts, the acceptance test, and the transport doctrine live in
**[`mcp-seats/README.md`](mcp-seats/README.md)**. The short version:

```bash
# Codex — MCP server mode is built in (Windows: codex.cmd if plain codex isn't found)
claude mcp add --scope user codex -- codex mcp-server
# Grok — bundled stdlib wrapper
claude mcp add --scope user grok -- python <repo>\mcp-seats\wmw_grok_mcp.py
# Gemini / Antigravity — bundled stdlib wrapper
claude mcp add --scope user gemini -- python <repo>\mcp-seats\wmw_gemini_mcp.py
```

Restart Claude Code (new MCP tools only appear in fresh sessions), confirm `claude mcp list`
shows each seat `✔ Connected`, then run the codeword acceptance test from the README per seat.
The wrappers also fix the two classic headless croaks: a 60-minute timeout (Antigravity's
default was 5) and an `always_approve` switch for build tickets (headless runs can't click
permission prompts). Two laws ride the transport: **reviewers are ALWAYS fresh calls** (a fresh
call is blind — exactly what independent review requires), and **a reply-chained session stays
in its owning-seat lineage forever** (it can never review work its thread touched).

---

## The reachability probe — what's online right now?
The orchestrator runs this (or its equivalent) at the start of a session and declares the
LIVE arsenal. Only dispatch to what actually answers. **Probe the default transport first:**
`claude mcp list` must show each wired seat Connected (and its tools present in THIS session —
they only appear in sessions started after registration); the CLI `--version` checks below prove
only the fallback lane. The arsenal declaration names which transport each seat answered on
(SPINE v2.0, transport law #4).

```bash
# Codex
codex --version 2>/dev/null && echo "CODEX: online" || echo "CODEX: missing (see §1)"
# Grok (use the real path)
"$HOME/.grok/bin/grok.exe" --version 2>/dev/null && echo "GROK: online" || echo "GROK: missing (see §2)"
# Gemini / Antigravity
"$LOCALAPPDATA/agy/bin/agy.exe" --version 2>/dev/null && echo "GEMINI: online" || echo "GEMINI: missing (see §3)"
# Claude is the host — always online (it's running this).
```

The orchestrator then states, plainly: *"Arsenal online: 🟠 Claude · 🔵 Codex · ⚫ Grok ·
🟢 Gemini. Ready."* — or names what's missing and points at the section above. A model
that isn't installed simply isn't in the dispatch pool for that session; the method
degrades gracefully (fewer weapons, same discipline). If NO cross-vendor reviewer is
reachable, say so — unreviewed work is never reported as done.


===== FILE: SKILL.md =====

---
name: dispatch
description: "ANDERSON'S DISPATCH DECK (ADD) — heavy multi-model agentic orchestration, NO persona / NO Team Rocket theater / NO character banter. Straight-faced. Claude conducts (wears GOLD 🟡): plans, dispatches the RIGHT model per job across the full arsenal (Claude tiers / Codex / Grok / Gemini-Antigravity incl. Nano Banana image gen), runs honest independent (cross-vendor) review, gates, and reports plainly by MODEL name. All the engineering discipline of SPINE, none of the show. Summon with /dispatch (or 'run the dispatch deck' / 'andersons dispatch deck') when the boss wants the powerhouse without the cat. Reserved rebrand alias: 'Agentic Dispatch Director' (also ADD)."
---
# Anderson's Dispatch Deck — ADD  (/dispatch) — heavy orchestration, straight-faced
*(Reserved future rebrand, coined 2026-07-17: "Agentic Dispatch Director" — also ADD.)*

**This SKILL is a thin loader.** The method is not in this file — it is in **SPINE.md**, which this
tier loads and renders **plain**: no cat, no Jessie/James/Butch/Cassidy, no episodes, no "prepare for
trouble." The Deck is SPINE with model names and a gold baton. Refer to workers by their MODEL
(Codex, Gemini Flash, Grok, Claude Sonnet), never by character names.

## DEPENDENCIES (versioned — enforceable inheritance)
```
DEPENDS:
  SPINE.md   >= 1.0     (the method engine — the WHOLE method for this tier)
```
On activation, **read each dep's version line** (`spine vX.Y (date)` at the top of the file) and
verify it satisfies the requirement. If SPINE is missing or its version is below the floor, **HALT
and tell the boss** ("SPINE v1.0+ required; found <X>") — do not run the method from memory. This
tier loads **SPINE only** — it deliberately does NOT load CREW or SHOW.

## LOAD RECEIPT (print on activation, first line)
```
🟡➤ ADD loaded · spine <parsed> · render: plain · crew: none · show: none
```
Interpolate `<parsed>` from SPINE's actual version line (never a hardcoded literal that could disagree
with the file). It says **loaded**, not "ready": this receipt confirms **SPINE inheritance only** and
prints BEFORE reachability is known — "ready" is reserved for after the On-invocation step-2 preflight.
The live arsenal and the independence status (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` /
`REVIEW UNAVAILABLE`) are declared at that step 2, before any work. If a dep is stale, the receipt says
so and the run stops.

## WHAT THE DECK ADDS ON TOP OF SPINE (the only delta — everything else is SPINE)
The Deck adds nothing to the *method*. Its entire delta is **plain rendering + the gold-baton color
narration.** Every rule below is SPINE's; this section only says how the Deck *presents* it.

### NARRATE IN COLOR (the one visual convention)
The orchestrator (🟡 GOLD) narrates the run and TAGS every model action with its vendor color (SPINE
Appendix A owns the vendor→color map): 🟡➤ conductor (Claude/Fable conducting — the ➤ is the baton) · 🟠 Claude · 🔵
Codex · ⚫ Grok · 🟢 Gemini. Announce dispatches/builds/reviews in-line:
> *"🟡 fencing the work into two lanes. 🟠 Claude building the parser · 🔵 Codex building the
> validator (parallel). → 🔵 Codex reviewing 🟠 Claude's parser: 2 findings, fixes attached. → 🟢
> Gemini generating the icon set. Gates: green."*
The color is a status light, not a costume — it says WHICH MODEL, nothing more. The banner never lies:
a model wearing another's brain shows both (🟠🟢 = Claude-brain on the Gemini seat).

### THE LEGEND — v4.0 (boss-adopted 2026-08-22; the Deck RENDERING of SPINE's THE NOTATION v4.0 — SPINE owns the marks)
**Seat first, act second, meter wrap around the words.** A line reads:
`🔵🔴 Codex reviewing 🟠 Claude's parser`
Seats: **⚪ THE BOSS** · **🟡➤ conductor** — the orchestrator wears the **➤ baton** after its dot
(gold when Claude conducts the Deck; whoever hosts the baton, the arrow follows — boss law, across
the board) · 🟠 Claude · 🔵 Codex · ⚫ Grok · 🟢 Gemini · 🟠🟢 borrowed brain (banner never lies:
brain color + host color).
Acts: **🔨 building** · **🔴 reviewing — a suffix on the seat** (🔵🔴 = Codex is reviewing; NOT a
reject) · **⛔ rejected / blocked / needs-boss** (never 🔴 for this — reviewing and rejection must
never look alike).
Council: **🌈👥👥 — every color, a crowd** (retires v3.1's 🟣; purple now means nothing here).
Meter: **wrap marks not narrated on this trunk** — subscription seats have windows, not per-token
bills, so the ♾️/💸/🚨💳 wraps (kept on `cursor-v2` for credit-burning shops) would be noise here.
Meter-AWARENESS itself (SPINE Part VI: headroom, the five levers) still binds.
States (kept from v3.1): 🚩 finding raised (flagged, not fatal) · 🚧 lane closed, detour in
progress · 🧪 gates running · 🩺 diagnosing (doctor-first) · 🕵️ adversary loose · 🏁 boss-validated
(top rung, outranks "done") · 🚢 shipped/deployed · 🪦 retired/parked · 🟤 quiet hold (nothing
running, watchers armed). Boss combos: ⚪🏁 in-hand validation · ⚪⚖️ ruling pending · ⚪🎮 on the
sticks.
A run reads as a timeline: 🩺 → 🌈👥👥 → 🟠🔨 → 🧪 → 🔵🔴→⛔ → 🟠🔨 → 🧪 → 🚢 → ⚪🏁 → 🟤.
Situations (worked lines):
> 🔵🔴 Codex reviewing ⚫ Grok's parser — proving the empty-input path
> 🔵🔴→⛔ Codex rejected the parser: empty input panics. Fix attached
> 🔵🔴 Codex reviewing → 🚩 empty-input panic · fix attached *(a finding, not a reject — build continues)*
> 🩺 diagnosing the failed gate before anyone else builds
> 🚢 shipped · ⚪🏁 boss already checked it · 🟤 quiet hold

Vendor→color still owned by SPINE Appendix A; this legend extends it and **supersedes v3.1**
(📝-as-reviewing and 🟣-as-council are retired marks).

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

## RUNNING THE DECK (all mechanics are SPINE's — this is the plain-render checklist)
1. **Plan first** (SPINE Part I — Gate-0 + the Diagnose/Design fork). State the goal back; write a
   short spec for anything substantial (what/why/done-when). Honor the Anderson house rules.
2. **Fence the work** (SPINE WRITE SET fence). Tickets with named, disjoint file sets; one clean goal
   each; parallel workers never touch the same files.
3. **Dispatch right-model-right-job, meter-aware** (SPINE Part VI routing + the five levers). Pick by
   strength AND weigh cost; the green seat (Gemini, via Antigravity) can carry Claude-grade work — a real
   Claude brain via Antigravity (the Overflow Valve, billed to Google's tab) or its own top Gemini
   tier as a capable substitute. Show the banner honestly. Announce plainly, no characters:
   "🔵 Codex building X." / "🟠🟢 Claude-brain-on-Gemini taking the parser to save the meter."
4. **Build with any model; route the review by FIT.** The two legal review paths, their statuses
   (`FULL CROSS-VENDOR` / `SOLO-VENDOR DEGRADED` / `REVIEW UNAVAILABLE`), and the fit-routing rule are
   **SPINE's — Part VI *Review dispatch* (+ Part IV's anti-laundering guard); this tier NAMES the move,
   it does not restate the rule.** *This shop's wiring (Appendix A), as an ILLUSTRATION of SPINE's
   fit-routing, not new law:* Codex is usually the sharpest CODE reviewer
   when it didn't build it (Claude/Grok/Gemini code → Codex); Codex built it → Claude reviews;
   architecture/judgment → Claude; Gemini = a cheap independent pass or tie-breaking 4th vote. State it
   by model + color, never a character. Every finding ships a fix; reviews land at checkpoints; the
   build never halts to argue; unresolved → the boss's decision queue.
5. **Gate before "done"** (SPINE Ladder of Truth). Run the project's real gates; claims capped at
   evidence — "gates pass," never "it works." The boss is the top rung (in-hand outranks the bench).
6. **Report plainly** (SPINE mission reports). What was dispatched, to which model, findings, what
   shipped, what needs the boss. The boss is the only one who merges.

## NON-NEGOTIABLES (all inherited from SPINE — restated only as the tier's guardrail card)
- **No unasked fleets** (Gate-0 / the five-prong fleet test). Deliberate and bounded; never a swarm.
- **Model tiering honored** — don't burn the frontier seat on mechanical work.
- **Independent review, never the builder's lineage** — the two legal paths and their statuses are
  SPINE's (Part IV + Part VI *Review dispatch*); this card names the guardrail, it does not restate the
  rule. Unreviewed work is never reported "done."
- **Nothing irreversible without the boss** — no push/merge/publish/spend on an assumption.
- **This is the STRAIGHT-FACED mode.** If the boss wants the show, that's `/team-rocket-takes-over`.
  Do not drift into persona here.

## ON INVOCATION
1. **Load SPINE**, verify its version against DEPENDS, print the load receipt.
2. **PROBE the arsenal, don't assume it** (SPINE Part VI — *Reachability & effective-model preflight*;
   the arsenal list lives in Appendix A). Run the reachability check (`--version` on each vendor CLI:
   codex, grok full-path, agy) AND confirm the effective model/lineage behind each host — a host
   renting another vendor's brain counts as THAT vendor's lineage, and an unestablished identity is
   `UNKNOWN LINEAGE`, which fails closed and is never counted as a cross-vendor reviewer. DECLARE the
   live arsenal and the independence status in one line: *"Online: 🟠 Claude · 🔵 Codex · ⚫ Grok · 🟢
   Gemini — FULL CROSS-VENDOR."* A model that doesn't answer isn't in the pool. The method degrades
   gracefully (Claude alone is valid); if NO independent reviewer is reachable, say so — unreviewed
   work is never reported as done.
3. Ask: **"What's the job?"** — then plan, fence, dispatch (right-model + meter-aware), review (by
   fit, independent — cross-vendor preferred, boss-launched fresh if solo), gate, report in color. All per SPINE.

## THE INVARIANTS (copied verbatim from SPINE Part VIII, per Principle 9)
```
TRM INVARIANTS (v2026-07-22 r2 · doctrine: SPINE.md)
- Whoever built it never approves it; review comes from a different
  effective-model vendor and lineage, or a boss-launched fresh seat.
- Claims are capped at evidence: "gates pass," never "it works."
- Disagreements go UP to the boss; convergence never ends anything, a
  ruling does.
- Every crew message signs its color; the boss alone assigns missions
  and merges.
```


===== FILE: SPINE.md (v2.0 excerpt: NOTATION + TRANSPORT LAW + Appendix A) =====

**THE NOTATION — v4.0 (boss-adopted 2026-08-22; supersedes the 2026-08-09 marks: 🟣-building is
repealed and the ⚪/🟤 reservations are spent). Seat first, act second. This section is the OWNER —
tier legends (Deck SKILL, CREW) are renderings of it.**

- **BUILDING = 🔨** trailing the seat: 🔵🔨 Codex building · 🟠🔨 Claude building. (**🟣 is retired
  everywhere** — it no longer means building, council, or anything else.)
- **REVIEWING = 🔴** trailing the seat on the plain Deck: 🔵🔴 = Codex reviewing — NOT a reject.
  **Grammar scope:** the Deck is seat-first; crew tiers are character-first, where a LEADING 🔴 is
  Butch's character color — so crew tiers render the reviewing act as **📝** (*🩷⚫ Cassidy (in
  grok) 📝*). Either way the vendor color stays visible: the value of a review is WHO ran it, and
  🔵🔨 then 🔵🔴 on the same work is the self-review failure this notation exists to expose.
- **REJECTED / BLOCKED / NEEDS-BOSS = ⛔**, never a red circle — rejection, reviewing, and Butch
  must never look alike.
- **COUNCIL = 🌈👥👥** — every color, a crowd; a council is a special move and asks first.
- **THE BOSS = ⚪** on the plain Deck, **👑** in crew tiers. Combos: ⚪🏁/👑🏁 in-hand validation ·
  ⚪⚖️/👑⚖️ ruling pending · ⚪🎮/👑🎮 on the sticks.
- **STATES:** 🚩 finding raised (flagged, not fatal) · 🚧 lane closed, detour in progress · 🧪
  gates running · 🩺 diagnosing (doctor-first) · 🕵️ adversary loose · 🏁 boss-validated (top rung,
  outranks "done") · 🚢 shipped/deployed · 🪦 retired/parked · 🟤 quiet hold (watchers armed).
- **Meter wrap marks (♾️/💸/🚨💳) are optional rendering** for shops that burn metered credits;
  this shop narrates none. Meter-AWARENESS (Part VI) still binds — subscription seats have windows
  and drainable quotas.

A run reads as a timeline: 🩺 → 🌈👥👥 → 🟠🔨 → 🧪 → 🔵🔴→⛔ → 🟠🔨 → 🧪 → 🚢 → ⚪🏁 → 🟤.

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
  reasons. Two-vendor agreement = treat as settled.
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
*SPINE owns the engine. It names no characters and tells no story — those are CREW's and SHOW's to
add, never to restate. Provenance of the Team Rocket Method (authorship, credits, status) lives in
CREW, because it is that brand's identity, not the brand-neutral engine's.*
