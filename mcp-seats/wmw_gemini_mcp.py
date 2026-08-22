#!/usr/bin/env python3
"""wmw-gemini — MCP stdio server wrapping the Antigravity CLI (Google seat).

Persistent Gemini/Antigravity seat for Claude Code, sibling of wmw-grok:
  gemini(prompt, ...)              start a new conversation -> reply + conversationId
  gemini-reply(conversationId, ..) continue that conversation with full context

Bakes in the two headless crash fixes discovered 2026-08-22:
  - --print-timeout raised from the 5m default (long tasks died mid-thought)
  - --dangerously-skip-permissions on always_approve (headless permission
    prompts can never be answered and stall until the timeout kills the run)

Transport: newline-delimited JSON-RPC 2.0 over stdio. Stdlib only.
Registered via:
  claude mcp add --scope user wmw-gemini -- python C:\\Sync\\Projects\\andersons-dispatch-deck\\wmw-grok\\wmw_gemini_mcp.py
"""
import json
import os
import shutil
import subprocess
import sys

PRINT_TIMEOUT = "60m"   # passed to agy --print-timeout
PROC_TIMEOUT_S = 3900   # subprocess guard, slightly above PRINT_TIMEOUT

def find_agy():
    exe = shutil.which("agy")
    if exe:
        return exe
    local = os.environ.get("LOCALAPPDATA", os.path.expanduser(r"~\AppData\Local"))
    cand = os.path.join(local, "agy", "bin", "agy.exe")
    if os.path.exists(cand):
        return cand
    return None

def run_gemini(prompt, conversation_id=None, cwd=None, model=None, always_approve=False):
    exe = find_agy()
    if not exe:
        return True, "Antigravity CLI not found (PATH or %LOCALAPPDATA%\\agy\\bin\\agy.exe)."
    cmd = [exe]
    if conversation_id:
        cmd += ["--conversation", conversation_id]
    if model:
        cmd += ["--model", model]
    if always_approve:
        cmd += ["--dangerously-skip-permissions"]
    cmd += ["-p", prompt, "--output-format", "json", "--print-timeout", PRINT_TIMEOUT]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=PROC_TIMEOUT_S, cwd=cwd or None,
        )
    except subprocess.TimeoutExpired:
        return True, f"Antigravity timed out after {PROC_TIMEOUT_S}s"
    except NotADirectoryError:
        return True, f"cwd is not a directory: {cwd}"
    raw = (proc.stdout or "").strip()
    idx = raw.find("{")
    if idx == -1:
        err = (proc.stderr or "").strip()
        return True, f"agy exited {proc.returncode} with no JSON output.\nstdout: {raw[:2000]}\nstderr: {err[:2000]}"
    try:
        data = json.loads(raw[idx:])
    except json.JSONDecodeError as e:
        return True, f"could not parse agy JSON output ({e}).\nraw: {raw[:2000]}"
    text = data.get("response", "")
    cid = data.get("conversation_id", "unknown")
    status = data.get("status", "unknown")
    footer = (f"\n\n---\n[wmw-gemini] conversationId: {cid} · status: {status}"
              f" · turns: {data.get('num_turns', '?')}")
    if proc.returncode != 0:
        footer += f" · exit: {proc.returncode}"
    return (status != "SUCCESS" or proc.returncode != 0), text + footer

TOOLS = [
    {
        "name": "gemini",
        "description": (
            "Start a NEW conversation with Gemini via the Antigravity CLI (Google "
            "subscription seat). Returns the reply plus a conversationId footer; continue "
            "the same conversation with gemini-reply. Each fresh call is an independent, "
            "blind session — correct for council/review seats. Set always_approve true when "
            "Gemini must edit files or run commands (headless permission prompts otherwise "
            "stall the run)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The task or message for Gemini."},
                "cwd": {"type": "string", "description": "Working directory (repo path for build work)."},
                "model": {"type": "string", "description": "Optional model override (agy models lists them)."},
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

def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "wmw-gemini", "version": "1.0.0"},
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
        if name == "gemini":
            is_err, text = run_gemini(
                args.get("prompt", ""), cwd=args.get("cwd"), model=args.get("model"),
                always_approve=bool(args.get("always_approve")),
            )
        elif name == "gemini-reply":
            is_err, text = run_gemini(
                args.get("prompt", ""), conversation_id=args.get("conversationId"),
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
    return None

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
