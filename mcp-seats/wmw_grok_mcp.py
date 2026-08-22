#!/usr/bin/env python3
"""wmw-grok — MCP stdio server wrapping the Grok Build CLI.

Gives Claude Code a persistent Grok seat, mirroring wmw-codex:
  grok(prompt, ...)            start a new Grok conversation -> reply + sessionId
  grok-reply(sessionId, ...)   continue that conversation with full context

Transport: newline-delimited JSON-RPC 2.0 over stdio (MCP stdio transport).
No third-party dependencies. Registered via:
  claude mcp add --scope user wmw-grok -- python C:\\Sync\\Projects\\andersons-dispatch-deck\\wmw-grok\\wmw_grok_mcp.py
"""
import json
import os
import shutil
import subprocess
import sys

GROK_TIMEOUT_S = 3600  # builder jobs can run long; the CLI itself manages turns

def find_grok():
    exe = shutil.which("grok")
    if exe:
        return exe
    for cand in (
        os.path.expanduser(r"~\.grok\bin\grok.exe"),
        os.path.expanduser(r"~\.grok\bin\grok"),
    ):
        if os.path.exists(cand):
            return cand
    return None

def run_grok(prompt, session_id=None, cwd=None, model=None, always_approve=False):
    exe = find_grok()
    if not exe:
        return True, "grok CLI not found on PATH or in ~/.grok/bin — is Grok Build installed?"
    cmd = [exe]
    if session_id:
        cmd += ["--resume", session_id]
    if model:
        cmd += ["-m", model]
    if cwd:
        cmd += ["--cwd", cwd]
    if always_approve:
        cmd += ["--always-approve"]
    cmd += ["-p", prompt, "--output-format", "json"]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=GROK_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return True, f"grok timed out after {GROK_TIMEOUT_S}s"
    raw = (proc.stdout or "").strip()
    # The CLI may print startup noise before the JSON object; find its start.
    idx = raw.find("{")
    if idx == -1:
        err = (proc.stderr or "").strip()
        return True, f"grok exited {proc.returncode} with no JSON output.\nstdout: {raw[:2000]}\nstderr: {err[:2000]}"
    try:
        data = json.loads(raw[idx:])
    except json.JSONDecodeError as e:
        return True, f"could not parse grok JSON output ({e}).\nraw: {raw[:2000]}"
    text = data.get("text", "")
    sid = data.get("sessionId", "unknown")
    usage = data.get("modelUsage", {})
    model_used = next(iter(usage), "unknown-model")
    footer = f"\n\n---\n[wmw-grok] sessionId: {sid} · model: {model_used} · turns: {data.get('num_turns', '?')}"
    if proc.returncode != 0:
        footer += f" · exit: {proc.returncode}"
    return False, text + footer

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

def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "wmw-grok", "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name == "grok":
            is_err, text = run_grok(
                args.get("prompt", ""), cwd=args.get("cwd"), model=args.get("model"),
                always_approve=bool(args.get("always_approve")),
            )
        elif name == "grok-reply":
            is_err, text = run_grok(
                args.get("prompt", ""), session_id=args.get("sessionId"),
                always_approve=bool(args.get("always_approve")),
            )
        else:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"unknown tool: {name}"}}
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
    if mid is not None:
        return {"jsonrpc": "2.0", "id": mid,
                "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None  # notification — no response

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
