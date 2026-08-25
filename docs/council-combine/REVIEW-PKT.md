# REVIEW TICKET — the transport merge, built by Codex (OpenAI)

You are the INDEPENDENT REVIEWER. A different vendor built this; you did not.

## What was built
Three MCP seat wrappers had duplicated JSON-RPC, validation and path-safety code. That
duplication had a proven cost: a security fix applied to one seat never travelled to its
siblings, and the Gemini seat carried bugs the others had fixed months earlier.

The common machinery moved to a new `seat_core.py`; each wrapper became a thin adapter.
1472 lines -> 972. armcheck 26/26 including the deep attack canaries.

## YOUR JOB — this is a SECURITY review, not a style review
1. **Did any guard weaken in the move?** Walk every refusal path. The canonical
   `safe_write_cwd()` is supposed to be the UNION of what the three seats learned:
   symlink resolution, explicit-cwd requirement, root banned exactly, system/APPDATA/
   LOCALAPPDATA banned WITH subtrees case-insensitively, credential segments banned,
   Cursor's playpen allowed as a declared exception. Is any of that weaker than what the
   individual seats had?
2. **Did vendor-specific enforcement get genericised?** Grok's deny rules and
   `--disallowed-tools Agent`, Gemini's `--mode plan`, Cursor's `--mode ask` vs `--yolo`
   and `--approve-mcps` ONLY on the write path. A normalized INPUT is fine; a generic
   IMPLEMENTATION is a finding.
3. **What does the shared core now make possible that was impossible before?** One defect
   in seat_core reaches all three seats at once. Name the worst realistic case.
4. **Anything the builder left behind** — dead imports, orphaned constants, a fallback that
   masks a real failure. This shop found today that deletion leaves debris invisible to
   whoever did the deleting.

Quote exact line anchors. Distinguish CONFIRMED from SUSPECTED. Say plainly if it is sound.
Do not write any file. Report only.

---

# THE CODE AS BUILT

## ===== seat_core.py =====
```python
     1	#!/usr/bin/env python3
     2	"""Shared transport, validation, path safety, and process boundary for MCP seats."""
     3	
     4	from dataclasses import dataclass
     5	import json
     6	import os
     7	from pathlib import Path
     8	import re
     9	import shutil
    10	import subprocess
    11	import sys
    12	
    13	
    14	MAX_REPLY_CHARS = 400_000
    15	_UUID_RE = re.compile(
    16	    r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    17	    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
    18	)
    19	_MODEL_ID_RE = re.compile(r"\A[a-z0-9][a-z0-9._-]{0,63}\Z")
    20	_CREDENTIAL_SEGMENTS = {
    21	    ".ssh", ".aws", ".grok", ".gemini", ".claude", ".cursor",
    22	    ".config", ".azure", ".kube", ".gnupg",
    23	}
    24	
    25	def required_string(args, key):
    26	    value = args.get(key)
    27	    if not isinstance(value, str) or not value.strip():
    28	        raise ValueError(f"'{key}' must be a non-empty string")
    29	    return value
    30	
    31	
    32	def optional_string(args, key):
    33	    value = args.get(key)
    34	    if value is None:
    35	        return None
    36	    if not isinstance(value, str) or not value.strip():
    37	        raise ValueError(f"'{key}' must be a non-empty string when given")
    38	    return value
    39	
    40	
    41	def optional_boolean(args, key):
    42	    value = args.get(key)
    43	    if value is None:
    44	        return False
    45	    if isinstance(value, bool):
    46	        return value
    47	    if isinstance(value, str) and value.lower() in ("true", "false"):
    48	        return value.lower() == "true"
    49	    raise ValueError(f"'{key}' must be a boolean")
    50	
    51	
    52	def safe_uuid(value, label):
    53	    if not isinstance(value, str) or not _UUID_RE.match(value):
    54	        raise ValueError(f"'{label}' must be a UUID as returned in a prior reply footer")
    55	    return value
    56	
    57	
    58	def safe_argv_string(value, label):
    59	    """Validate an optional free-form string before placing it in argv."""
    60	    if value is None:
    61	        return None
    62	    if not isinstance(value, str) or not value.strip() or value.lstrip().startswith("-"):
    63	        raise ValueError(f"'{label}' must be a non-empty string that does not start with '-'")
    64	    return value
    65	
    66	
    67	def is_model_id(value):
    68	    return isinstance(value, str) and bool(_MODEL_ID_RE.match(value.strip().lower()))
    69	
    70	
    71	def safe_model_id(value, label="model"):
    72	    if value is None:
    73	        return None
    74	    if not is_model_id(value):
    75	        raise ValueError(f"'{label}' must be a plain model id such as 'composer-2.5' "
    76	                         "(letters, digits, dot, dash, underscore only)")
    77	    return value.strip().lower()
    78	
    79	
    80	def truncate_reply(value, seat, limit=MAX_REPLY_CHARS):
    81	    text = value if isinstance(value, str) else ("" if value is None else str(value))
    82	    if len(text) > limit:
    83	        return text[:limit] + f"\n\n[{seat}] ...truncated at {limit} chars]"
    84	    return text
    85	
    86	
    87	def discover_executable(candidates, path_name):
    88	    """Prefer adapter-declared absolute installs; use PATH only as a fallback."""
    89	    for candidate in candidates:
    90	        if candidate and os.path.isfile(candidate):
    91	            return candidate
    92	    return shutil.which(path_name)
    93	
    94	
    95	@dataclass(frozen=True)
    96	class ProcessFailure:
    97	    kind: str
    98	    detail: str
    99	
   100	
   101	def run_process(argv, timeout_s, cwd=None):
   102	    """The single subprocess timeout/launch boundary used by every seat."""
   103	    try:
   104	        proc = subprocess.run(
   105	            argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
   106	            timeout=timeout_s, cwd=cwd, stdin=subprocess.DEVNULL,
   107	        )
   108	        return proc, None
   109	    except subprocess.TimeoutExpired:
   110	        return None, ProcessFailure("timeout", f"timed out after {timeout_s}s")
   111	    except OSError as exc:
   112	        return None, ProcessFailure("launch", str(exc))
   113	
   114	
   115	def _normalized(path):
   116	    return os.path.normpath(os.path.realpath(path)).casefold()
   117	
   118	
   119	def _within(child, parent):
   120	    child_norm, parent_norm = _normalized(child), _normalized(parent)
   121	    try:
   122	        return os.path.commonpath([child_norm, parent_norm]) == parent_norm
   123	    except ValueError:  # different drives
   124	        return False
   125	
   126	
   127	def safe_write_cwd(cwd, write_capable, safe_exceptions=()):
   128	    """Return a resolved cwd after applying the union of all seat write guards.
   129	
   130	    Read-only calls do not acquire generic vendor policy here; they only receive a
   131	    normalized cwd. Vendor-specific read-only enforcement remains in each adapter.
   132	    """
   133	    if not write_capable:
   134	        return os.path.realpath(cwd) if cwd else None
   135	    if cwd is None:
   136	        raise ValueError("a write-capable session requires an explicit cwd naming the "
   137	                         "project directory the seat may write in")
   138	
   139	    real = os.path.realpath(cwd)
   140	    if not os.path.isdir(real):
   141	        raise ValueError(f"cwd is not a directory: {cwd}")
   142	
   143	    # Adapter-declared sandboxes (Cursor's playpen) are intentionally allowed.
   144	    for exception in safe_exceptions:
   145	        if exception and _within(real, exception):
   146	            return real
   147	
   148	    anchor = Path(real).anchor
   149	    if anchor and _normalized(real) == _normalized(anchor):
   150	        raise ValueError("refusing a write-capable session at the filesystem root — "
   151	                         "point cwd at a project directory")
   152	
   153	    for env_name in ("SystemRoot", "windir", "ProgramFiles", "ProgramFiles(x86)",
   154	                     "ProgramData"):
   155	        root = os.environ.get(env_name)
   156	        if root and _within(real, root):
   157	            raise ValueError("refusing a write-capable session inside a system directory "
   158	                             f"({root}) — point cwd at a project directory")
   159	
   160	    # These contain credentials and the installed CLIs. Containment is deliberate:
   161	    # equality-only checks once allowed APPDATA/System32 descendants.
   162	    for env_name in ("APPDATA", "LOCALAPPDATA"):
   163	        root = os.environ.get(env_name)
   164	        if root and _within(real, root):
   165	            raise ValueError(f"refusing a write-capable session at or inside {env_name} — "
   166	                             "credentials and the CLIs themselves live there")
   167	
   168	    # Gemini learned that a profile subtree, not just the profile root, is unsafe.
   169	    profile_roots = {os.path.expanduser("~")}
   170	    if os.environ.get("USERPROFILE"):
   171	        profile_roots.add(os.environ["USERPROFILE"])
   172	    for root in profile_roots:
   173	        if root and _within(real, root):
   174	            raise ValueError(f"refusing a write-capable session at or inside {root} — "
   175	                             "point cwd at a project directory")
   176	
   177	    parts = {part.casefold() for part in Path(real).parts}
   178	    for secret in _CREDENTIAL_SEGMENTS:
   179	        if secret in parts:
   180	            raise ValueError(f"refusing a write-capable session inside {secret}")
   181	    return real
   182	
   183	
   184	def configure_utf8_stdio():
   185	    for stream in (sys.stdin, sys.stdout):
   186	        try:
   187	            stream.reconfigure(encoding="utf-8", errors="replace")
   188	        except Exception:
   189	            pass
   190	
   191	
   192	def result_envelope(request_id, is_error, text):
   193	    return {
   194	        "jsonrpc": "2.0", "id": request_id,
   195	        "result": {"content": [{"type": "text", "text": text}], "isError": is_error},
   196	    }
   197	
   198	
   199	def error_envelope(request_id, code, message):
   200	    return {"jsonrpc": "2.0", "id": request_id,
   201	            "error": {"code": code, "message": message}}
   202	
   203	
   204	def dispatch(msg, server_name, version, tools, tool_call):
   205	    method, request_id = msg.get("method"), msg.get("id")
   206	    if method == "initialize":
   207	        params = msg.get("params", {})
   208	        return {
   209	            "jsonrpc": "2.0", "id": request_id,
   210	            "result": {
   211	                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
   212	                "capabilities": {"tools": {}},
   213	                "serverInfo": {"name": server_name, "version": version},
   214	            },
   215	        }
   216	    if method == "ping":
   217	        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
   218	    if method == "tools/list":
   219	        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}}
   220	    if method == "tools/call":
   221	        params = msg.get("params") or {}
   222	        name, args = params.get("name"), params.get("arguments") or {}
   223	        if not isinstance(args, dict):
   224	            result = (True, "arguments must be an object")
   225	        else:
   226	            try:
   227	                result = tool_call(name, args)
   228	            except ValueError as exc:
   229	                result = (True, f"invalid arguments: {exc}")
   230	        if result is None:
   231	            return error_envelope(request_id, -32602, f"unknown tool: {name}")
   232	        return result_envelope(request_id, *result)
   233	    if "id" in msg:
   234	        return error_envelope(request_id, -32601, f"method not found: {method}")
   235	    return None
   236	
   237	
   238	def serve(server_name, version, tools, tool_call, startup=None):
   239	    configure_utf8_stdio()
   240	    if startup:
   241	        startup()
   242	    for line in sys.stdin:
   243	        line = line.strip()
   244	        if not line:
   245	            continue
   246	        try:
   247	            msg = json.loads(line)
   248	        except json.JSONDecodeError:
   249	            response = error_envelope(None, -32700, "parse error")
   250	        else:
   251	            if not isinstance(msg, dict):
   252	                continue
   253	            try:
   254	                response = dispatch(msg, server_name, version, tools, tool_call)
   255	            except Exception as exc:  # one malformed request must not kill the seat
   256	                print(f"[{server_name}] internal error: {exc}", file=sys.stderr)
   257	                response = (error_envelope(msg.get("id"), -32603,
   258	                                           f"internal error: {exc}")
   259	                            if "id" in msg else None)
   260	        if response is not None:
   261	            sys.stdout.write(json.dumps(response) + "\n")
   262	            sys.stdout.flush()
```

## ===== wmw_grok_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-grok — MCP stdio adapter for the Grok Build CLI."""
     3	import json
     4	import os
     5	import tempfile
     6	
     7	import seat_core as core
     8	
     9	GROK_TIMEOUT_S = 3600
    10	DENY_RULES = ("Write", "Edit", "MultiEdit", "NotebookEdit", "Bash",
    11	              "MCPTool", "WebFetch", "WebSearch")
    12	
    13	
    14	def find_grok():
    15	    home = os.path.expanduser("~")
    16	    return core.discover_executable((
    17	        os.path.join(home, ".grok", "bin", "grok.exe"),
    18	        os.path.join(home, ".grok", "bin", "grok"),
    19	        os.path.join(home, ".local", "bin", "grok"),
    20	    ), "grok")
    21	
    22	
    23	def _extract_json(raw):
    24	    """First complete object wins; Grok may print a banner before its JSON."""
    25	    decoder, index = json.JSONDecoder(), raw.find("{")
    26	    while index != -1:
    27	        try:
    28	            value, _ = decoder.raw_decode(raw[index:])
    29	            if isinstance(value, dict):
    30	                return value
    31	        except json.JSONDecodeError:
    32	            pass
    33	        index = raw.find("{", index + 1)
    34	    return None
    35	
    36	
    37	def run_grok(prompt, session_id=None, cwd=None, model=None, always_approve=False,
    38	             allow_web_search=False):
    39	    exe = find_grok()
    40	    if not exe:
    41	        return True, "grok CLI not found on PATH or in ~/.grok/bin — is Grok Build installed?"
    42	    if cwd and not os.path.isdir(cwd):
    43	        return True, f"cwd is not a directory: {cwd}"
    44	
    45	    prompt_path = None
    46	    try:
    47	        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md",
    48	                                         delete=False) as handle:
    49	            handle.write(prompt)
    50	            prompt_path = handle.name
    51	
    52	        # Vendor policy stays explicit here. Grok's sandbox fails open on Windows;
    53	        # deny rules are the read-only boundary, including cross-seat MCP laundering.
    54	        command = [exe]
    55	        if session_id:
    56	            command += [f"--resume={session_id}"]
    57	        if model:
    58	            command += ["-m", model]
    59	        if cwd:
    60	            command += ["--cwd", cwd]
    61	        if always_approve:
    62	            command += ["--always-approve"]
    63	        else:
    64	            for rule in DENY_RULES:
    65	                command += ["--deny", rule]
    66	            command += ["--disallowed-tools", "Agent", "--permission-mode", "default",
    67	                        "--no-subagents", "--no-memory"]
    68	            if not allow_web_search:
    69	                command += ["--disable-web-search"]
    70	        command += ["--prompt-file", prompt_path, "--output-format", "json"]
    71	        proc, failure = core.run_process(command, GROK_TIMEOUT_S)
    72	    finally:
    73	        if prompt_path:
    74	            try:
    75	                os.unlink(prompt_path)
    76	            except OSError:
    77	                pass
    78	
    79	    if failure:
    80	        if failure.kind == "timeout":
    81	            return True, f"grok timed out after {GROK_TIMEOUT_S}s"
    82	        return True, f"could not launch grok: {failure.detail}"
    83	
    84	    raw, err = (proc.stdout or "").strip(), (proc.stderr or "").strip()
    85	    data = _extract_json(raw)
    86	    if data is None:
    87	        return True, (f"grok exited {proc.returncode} with no parseable JSON.\n"
    88	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
    89	    if data.get("type") == "error":
    90	        return True, f"grok error: {data.get('message', '(no message)')}\nstderr: {err[:1000]}"
    91	    text, session_id = data.get("text"), data.get("sessionId")
    92	    if proc.returncode != 0 or not isinstance(session_id, str) or not session_id:
    93	        return True, (f"grok run failed (exit {proc.returncode}, sessionId={session_id!r}).\n"
    94	                      f"text: {str(text)[:1000]}\nstderr: {err[:1000]}")
    95	    text = core.truncate_reply(text, "wmw-grok")
    96	    model_used = next(iter(data.get("modelUsage") or {}), "unknown-model")
    97	    return False, (text + f"\n\n---\n[wmw-grok] sessionId: {session_id} · "
    98	                    f"model: {model_used} · turns: {data.get('num_turns', '?')}")
    99	
   100	
   101	TOOLS = [
   102	    {
   103	        "name": "grok",
   104	        "description": (
   105	            "Start a NEW persistent conversation with Grok (Grok Build CLI, xAI subscription seat). "
   106	            "Returns Grok's reply plus a sessionId footer. To continue the same conversation with "
   107	            "full context, call grok-reply with that sessionId. DEFAULT IS READ-ONLY: file writes, "
   108	            "edits and shell are denied, and web search is off unless allow_web_search is true. "
   109	            "Set always_approve true ONLY for build tickets — it lets Grok write files and run "
   110	            "commands under cwd. Use for build dispatches, research, and council seats."
   111	        ),
   112	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   113	        "inputSchema": {"type": "object", "properties": {
   114	            "prompt": {"type": "string", "description": "The task or message for Grok."},
   115	            "cwd": {"type": "string", "description": "Working directory for the session (repo path for build work). Required when always_approve is true; must not be a home/system directory."},
   116	            "model": {"type": "string", "description": "Optional Grok model ID override."},
   117	            "always_approve": {"type": "boolean", "description": "DANGEROUS: auto-approve all of Grok's tool use, including file writes and shell commands under cwd. Required for build work; default false = deny-listed read-only."},
   118	            "allow_web_search": {"type": "boolean", "description": "Allow web search/fetch on a read-only call (default false; ignored when always_approve is true)."},
   119	        }, "required": ["prompt"]},
   120	    },
   121	    {
   122	        "name": "grok-reply",
   123	        "description": (
   124	            "Continue an existing Grok conversation by sessionId (from a prior grok call's footer). "
   125	            "Grok retains the full prior context of that session."
   126	        ),
   127	        "inputSchema": {"type": "object", "properties": {
   128	            "sessionId": {"type": "string", "description": "The sessionId returned by a previous grok/grok-reply call."},
   129	            "prompt": {"type": "string", "description": "The follow-up message."},
   130	            "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory."},
   131	            "always_approve": {"type": "boolean", "description": "Auto-approve Grok's tool use this turn (file writes, shell). Requires cwd."},
   132	        }, "required": ["sessionId", "prompt"]},
   133	    },
   134	]
   135	
   136	
   137	def _tool_call(name, args):
   138	    if name not in ("grok", "grok-reply"):
   139	        return None
   140	    approve = core.optional_boolean(args, "always_approve")
   141	    cwd = core.safe_write_cwd(
   142	        core.safe_argv_string(core.optional_string(args, "cwd"), "cwd"), approve)
   143	    return run_grok(
   144	        core.required_string(args, "prompt"),
   145	        session_id=(core.safe_uuid(args.get("sessionId"), "sessionId")
   146	                    if name == "grok-reply" else None),
   147	        cwd=cwd,
   148	        model=(core.safe_argv_string(core.optional_string(args, "model"), "model")
   149	               if name == "grok" else None),
   150	        always_approve=approve,
   151	        allow_web_search=core.optional_boolean(args, "allow_web_search"),
   152	    )
   153	
   154	
   155	def main():
   156	    core.serve("wmw-grok", "1.6.0", TOOLS, _tool_call)
   157	
   158	
   159	if __name__ == "__main__":
   160	    main()
```

## ===== wmw_gemini_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-gemini — MCP stdio adapter for the Antigravity CLI."""
     3	import json
     4	import os
     5	
     6	import seat_core as core
     7	
     8	PRINT_TIMEOUT = "60m"
     9	PROC_TIMEOUT_S = 3900
    10	MAX_ARGV_PROMPT = 25_000
    11	
    12	
    13	def find_agy():
    14	    home = os.path.expanduser("~")
    15	    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    16	    return core.discover_executable((
    17	        os.path.join(local, "agy", "bin", "agy.exe"),
    18	        os.path.join(home, ".antigravity", "bin", "agy"),
    19	        os.path.join(home, ".local", "bin", "agy"),
    20	        os.path.join(home, "agy", "bin", "agy"),
    21	    ), "agy")
    22	
    23	
    24	def _extract_json(raw):
    25	    decoder, index = json.JSONDecoder(), raw.find("{")
    26	    while index != -1:
    27	        try:
    28	            value, _ = decoder.raw_decode(raw[index:])
    29	            if isinstance(value, dict):
    30	                return value
    31	        except json.JSONDecodeError:
    32	            pass
    33	        index = raw.find("{", index + 1)
    34	    return None
    35	
    36	
    37	def run_gemini(prompt, conversation_id=None, cwd=None, model=None, always_approve=False):
    38	    exe = find_agy()
    39	    if not exe:
    40	        return True, "Antigravity CLI not found (PATH or %LOCALAPPDATA%\\agy\\bin\\agy.exe)."
    41	    if cwd and not os.path.isdir(cwd):
    42	        return True, f"cwd is not a directory: {cwd}"
    43	    if len(prompt) > MAX_ARGV_PROMPT:
    44	        return True, (f"prompt is {len(prompt)} chars; this seat's CLI takes the prompt on the "
    45	                      f"command line and Windows caps that at ~32K. Keep prompts under "
    46	                      f"{MAX_ARGV_PROMPT} chars — write long material to a file and (with "
    47	                      "always_approve: true) ask Gemini to read the file instead.")
    48	
    49	    # Antigravity's read-only boundary is its own plan mode. This must stay local:
    50	    # omitting the write flag alone would inherit potentially permissive user settings.
    51	    command = [exe]
    52	    if conversation_id:
    53	        command += [f"--conversation={conversation_id}"]
    54	    if model:
    55	        command += ["--model", model]
    56	    command += (["--dangerously-skip-permissions"] if always_approve
    57	                else ["--mode", "plan"])
    58	    command += ["-p", prompt, "--output-format", "json", "--print-timeout", PRINT_TIMEOUT]
    59	    proc, failure = core.run_process(command, PROC_TIMEOUT_S, cwd=cwd or None)
    60	    if failure:
    61	        if failure.kind == "timeout":
    62	            return True, f"Antigravity timed out after {PROC_TIMEOUT_S}s"
    63	        return True, f"could not launch agy: {failure.detail}"
    64	
    65	    raw, err = (proc.stdout or "").strip(), (proc.stderr or "").strip()
    66	    data = _extract_json(raw)
    67	    if data is None:
    68	        return True, (f"agy exited {proc.returncode} with no parseable JSON.\n"
    69	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
    70	    text, conversation_id = data.get("response"), data.get("conversation_id")
    71	    status = data.get("status", "unknown")
    72	    if (proc.returncode != 0 or status != "SUCCESS" or
    73	            not isinstance(conversation_id, str) or not conversation_id):
    74	        return True, (f"agy run failed (exit {proc.returncode}, status {status}, "
    75	                      f"conversationId={conversation_id!r}).\n"
    76	                      f"text: {str(text)[:1000]}\nstderr: {err[:1000]}")
    77	    text = core.truncate_reply(text, "wmw-gemini")
    78	
    79	    # Only the CLI-reported brain counts; requested model is never promoted to evidence.
    80	    reported = data.get("model") or data.get("model_name")
    81	    brain = reported if isinstance(reported, str) and reported else (
    82	        f"UNREPORTED (requested: {model})" if model else "UNREPORTED")
    83	    footer = (f"\n\n---\n[wmw-gemini] conversationId: {conversation_id} · status: {status}"
    84	              f" · brain: {brain} · turns: {data.get('num_turns', '?')}")
    85	    return False, text + footer
    86	
    87	
    88	TOOLS = [
    89	    {
    90	        "name": "gemini",
    91	        "description": (
    92	            "Start a NEW conversation with Gemini via the Antigravity CLI (Google "
    93	            "subscription seat). Returns the reply plus a conversationId footer (including the "
    94	            "effective brain — check it before counting this seat as an independent Gemini vote); "
    95	            "continue the same conversation with gemini-reply. Each fresh call is an independent, "
    96	            "blind session. Set always_approve true when Gemini must edit files or run commands "
    97	            "(headless permission prompts otherwise stall the run). Keep prompts under ~25K chars; "
    98	            "put long material in a file for Gemini to read."
    99	        ),
   100	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   101	        "inputSchema": {"type": "object", "properties": {
   102	            "prompt": {"type": "string", "description": "The task or message for Gemini."},
   103	            "cwd": {"type": "string", "description": "Working directory (repo path for build work)."},
   104	            "model": {"type": "string", "description": "Optional model override (agy models lists them; exact-match strings)."},
   105	            "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts. Required for build work; default false."},
   106	        }, "required": ["prompt"]},
   107	    },
   108	    {
   109	        "name": "gemini-reply",
   110	        "description": (
   111	            "Continue an existing Gemini/Antigravity conversation by conversationId (from a "
   112	            "prior gemini call's footer). Gemini retains the full prior context."
   113	        ),
   114	        "inputSchema": {"type": "object", "properties": {
   115	            "conversationId": {"type": "string", "description": "conversationId from a previous gemini/gemini-reply call."},
   116	            "prompt": {"type": "string", "description": "The follow-up message."},
   117	            "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true."},
   118	            "always_approve": {"type": "boolean", "description": "Skip tool-permission prompts this turn. Requires cwd."},
   119	        }, "required": ["conversationId", "prompt"]},
   120	    },
   121	]
   122	
   123	
   124	def _tool_call(name, args):
   125	    if name not in ("gemini", "gemini-reply"):
   126	        return None
   127	    approve = core.optional_boolean(args, "always_approve")
   128	    cwd = core.safe_write_cwd(
   129	        core.safe_argv_string(core.optional_string(args, "cwd"), "cwd"), approve)
   130	    return run_gemini(
   131	        core.required_string(args, "prompt"),
   132	        conversation_id=(core.safe_uuid(args.get("conversationId"), "conversationId")
   133	                         if name == "gemini-reply" else None),
   134	        cwd=cwd,
   135	        model=(core.safe_argv_string(core.optional_string(args, "model"), "model")
   136	               if name == "gemini" else None),
   137	        always_approve=approve,
   138	    )
   139	
   140	
   141	def main():
   142	    core.serve("wmw-gemini", "1.6.0", TOOLS, _tool_call)
   143	
   144	
   145	if __name__ == "__main__":
   146	    main()
```

## ===== wmw_cursor_mcp.py =====
```python
     1	#!/usr/bin/env python3
     2	"""wmw-cursor — MCP stdio adapter for the metered Cursor Agent model pool."""
     3	import datetime
     4	import io
     5	import json
     6	import os
     7	import sys
     8	import tempfile
     9	
    10	try:
    11	    import seat_core as core
    12	except ModuleNotFoundError:
    13	    # armcheck's fail-closed canary runs a copied adapter beside a broken guard.
    14	    sys.path.insert(0, os.path.join(os.getcwd(), "mcp-seats"))
    15	    import seat_core as core
    16	
    17	CURSOR_TIMEOUT_S = 3600
    18	DEFAULT_MODEL = "composer-2.5"
    19	COUNCIL_LOCK_MAX = int(os.environ.get("WMW_CURSOR_COUNCIL_MAX", "2"))
    20	COUNCIL_LOCK_WINDOW_S = int(os.environ.get("WMW_CURSOR_COUNCIL_WINDOW", "600"))
    21	COUNCIL_LOCK_ON = os.environ.get("WMW_CURSOR_COUNCIL_LOCK", "on").lower() != "off"
    22	PLAYPEN = os.path.abspath(os.environ.get(
    23	    "WMW_CURSOR_PLAYPEN", os.path.join("C:" + os.sep, "Sync", "_playpen", "cursor")))
    24	PROMPTS_DIR = os.path.join(PLAYPEN, "prompts")
    25	# Guard state must not live where the guarded write-capable agent can erase it.
    26	SPEND_LEDGER = os.environ.get(
    27	    "WMW_CURSOR_LEDGER",
    28	    os.path.join(os.path.expanduser("~"), ".anderson-method", "bench-spend.jsonl"))
    29	
    30	INCLUDED_PREFIXES = ("composer-", "cursor-grok-")
    31	CREDIT_PREFIXES = ("claude-", "gpt-", "gemini-", "kimi-", "glm-")
    32	YOLO_ALLOWLIST = ("composer-", "cursor-grok-")
    33	METER_MARK = {"INCLUDED": "♾️", "INCLUDED-FAST": "♾️💸",
    34	              "CREDITS": "💸", "CREDITS-FAST": "🚨💳", "UNKNOWN": "⚠️"}
    35	CURSOR_BANNER = "🟣➤"
    36	BLOODLINE_MARK = {
    37	    "Moonshot": "🌙", "Zhipu": "🔷", "Cursor": "🎼", "Anthropic": "🟠",
    38	    "OpenAI": "🔵", "xAI": "⚫", "Google": "🟢", "UNKNOWN": "❓",
    39	}
    40	
    41	
    42	def _ensure_playpen():
    43	    for directory in (PLAYPEN, PROMPTS_DIR, os.path.join(PLAYPEN, "scratch")):
    44	        try:
    45	            os.makedirs(directory, exist_ok=True)
    46	        except OSError:
    47	            return False
    48	    readme = os.path.join(PLAYPEN, "README.md")
    49	    if not os.path.exists(readme):
    50	        try:
    51	            with io.open(readme, "w", encoding="utf-8", newline="") as handle:
    52	                handle.write("# Cursor's playpen\n\nScratch space for the `wmw-cursor` MCP seat. The seat writes prompt\nhandoffs (`prompts/`), scratch work (`scratch/`) and its spend ledger\nhere so none of that lands in a real project.\n\nSafe to delete when nothing is running; it is recreated on demand.\n")
    53	        except OSError:
    54	            pass
    55	    return True
    56	
    57	
    58	def yolo_allowed(model_id):
    59	    return (model_id or "").strip().lower().startswith(YOLO_ALLOWLIST)
    60	
    61	
    62	def meter_class(model_id):
    63	    model = (model_id or "").strip().lower()
    64	    if not model or model == "auto" or not core.is_model_id(model):
    65	        return "UNKNOWN"
    66	    fast = model.endswith("-fast")
    67	    if model.startswith(INCLUDED_PREFIXES):
    68	        return "INCLUDED-FAST" if fast else "INCLUDED"
    69	    if model.startswith(CREDIT_PREFIXES):
    70	        return "CREDITS-FAST" if fast else "CREDITS"
    71	    return "UNKNOWN"
    72	
    73	
    74	def _lineage(model_id):
    75	    model = (model_id or "").lower()
    76	    for prefix, vendor in (("claude-", "Anthropic"), ("gpt-", "OpenAI"),
    77	                           ("cursor-grok-", "xAI"), ("gemini-", "Google"),
    78	                           ("kimi-", "Moonshot"), ("glm-", "Zhipu"),
    79	                           ("composer-", "Cursor")):
    80	        if model.startswith(prefix):
    81	            return vendor
    82	    return "UNKNOWN"
    83	
    84	
    85	def _log_spend(model, lineage, klass, usage, session_id, ok, write_capable):
    86	    """Append one observation per launched call; logging never breaks a call."""
    87	    try:
    88	        _ensure_playpen()
    89	        row = {
    90	            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
    91	            "model": model, "lineage": lineage, "meter": klass,
    92	            "billable": bool(klass and klass.startswith("CREDITS")),
    93	            "surcharged": bool(klass and klass.endswith("FAST")),
    94	            "in": (usage or {}).get("inputTokens"),
    95	            "out": (usage or {}).get("outputTokens"),
    96	            "cache_read": (usage or {}).get("cacheReadTokens"),
    97	            "session": session_id, "ok": ok, "write_capable": write_capable,
    98	        }
    99	        with io.open(SPEND_LEDGER, "a", encoding="utf-8", newline="") as handle:
   100	            handle.write(json.dumps(row) + "\n")
   101	    except Exception as exc:
   102	        print(f"[wmw-cursor] spend-ledger write failed: {exc}", file=sys.stderr)
   103	
   104	
   105	def _allowance(seat):
   106	    try:
   107	        import importlib.util
   108	        spec = importlib.util.spec_from_file_location(
   109	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   110	                                            "allowance.py"))
   111	        module = importlib.util.module_from_spec(spec)
   112	        spec.loader.exec_module(module)
   113	        return module.status(seat)
   114	    except Exception as exc:
   115	        return False, f"the allowance record could not be read ({exc}); failing closed"
   116	
   117	
   118	def _allowance_window_s(seat, fallback):
   119	    try:
   120	        import importlib.util
   121	        spec = importlib.util.spec_from_file_location(
   122	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   123	                                            "allowance.py"))
   124	        module = importlib.util.module_from_spec(spec)
   125	        spec.loader.exec_module(module)
   126	        return int(module.window_seconds(seat, fallback))
   127	    except Exception:
   128	        return fallback
   129	
   130	
   131	def _allowance_calls(seat, fallback):
   132	    try:
   133	        import importlib.util
   134	        spec = importlib.util.spec_from_file_location(
   135	            "_allowance_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   136	                                            "allowance.py"))
   137	        module = importlib.util.module_from_spec(spec)
   138	        spec.loader.exec_module(module)
   139	        return int((module._load().get(seat) or {}).get("calls", fallback))
   140	    except Exception:
   141	        return fallback
   142	
   143	
   144	def _guard():
   145	    try:
   146	        import importlib.util
   147	        spec = importlib.util.spec_from_file_location(
   148	            "_guard_mod", os.path.join(os.path.dirname(os.path.abspath(__file__)),
   149	                                        "dispatch-guard.py"))
   150	        module = importlib.util.module_from_spec(spec)
   151	        spec.loader.exec_module(module)
   152	        return module
   153	    except Exception as exc:
   154	        print(f"[wmw-cursor] dispatch-guard unavailable: {exc}", file=sys.stderr)
   155	        return exc  # write dispatches fail closed when the guard cannot load
   156	
   157	
   158	def _recent_billable(window_s):
   159	    if not os.path.exists(SPEND_LEDGER):
   160	        return 0
   161	    cutoff, count = datetime.datetime.now() - datetime.timedelta(seconds=window_s), 0
   162	    try:
   163	        for line in io.open(SPEND_LEDGER, encoding="utf-8"):
   164	            try:
   165	                row = json.loads(line)
   166	                timestamp = datetime.datetime.fromisoformat(row.get("ts", ""))
   167	            except (json.JSONDecodeError, ValueError):
   168	                continue
   169	            if row.get("billable") and timestamp >= cutoff:
   170	                count += 1
   171	    except OSError:
   172	        return 0
   173	    return count
   174	
   175	
   176	def find_cursor_agent():
   177	    home = os.path.expanduser("~")
   178	    local = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
   179	    return core.discover_executable((
   180	        os.path.join(local, "cursor-agent", "cursor-agent.cmd"),
   181	        os.path.join(home, ".local", "bin", "cursor-agent"),
   182	        os.path.join(home, ".cursor", "bin", "cursor-agent"),
   183	    ), "cursor-agent")
   184	
   185	
   186	def _extract_json(raw):
   187	    """Last complete result wins because Cursor streams status objects first."""
   188	    decoder, found, index = json.JSONDecoder(), None, raw.find("{")
   189	    while index != -1:
   190	        try:
   191	            value, _ = decoder.raw_decode(raw[index:])
   192	            if isinstance(value, dict) and value.get("type") == "result":
   193	                found = value
   194	            elif isinstance(value, dict) and found is None:
   195	                found = value
   196	        except json.JSONDecodeError:
   197	            pass
   198	        index = raw.find("{", index + 1)
   199	    return found
   200	
   201	
   202	def run_cursor(prompt, session_id=None, cwd=None, model=None, always_approve=False,
   203	               spend_credits=False):
   204	    exe = find_cursor_agent()
   205	    if not exe:
   206	        return True, ("Cursor CLI not found. Install it, then `cursor-agent login`. "
   207	                      "(Windows: %LOCALAPPDATA%\\cursor-agent\\cursor-agent.cmd)")
   208	    chosen, klass = model or DEFAULT_MODEL, meter_class(model or DEFAULT_MODEL)
   209	
   210	    if klass == "UNKNOWN":
   211	        return True, (f"{CURSOR_BANNER} ⚠️ REFUSED — '{chosen}' is not a recognised model id, "
   212	                      "or is `auto` (which may route anywhere). Unknown lineage fails closed "
   213	                      "and cannot be unlocked with spend_credits. Name an explicit model: "
   214	                      "composer-2.5 (free) or cursor-grok-4.6-high (free).")
   215	    if klass.startswith("CREDITS") and not spend_credits:
   216	        return True, (f"{CURSOR_BANNER} 🚨 CREDIT GUARD — REFUSED BEFORE SPENDING\n\n"
   217	                      f"'{chosen}' is meter class {klass} ({_lineage(chosen)} lineage). It "
   218	                      "draws Cursor's third-party CREDIT pool. Pass spend_credits: true "
   219	                      "deliberately, or use composer-2.5 / cursor-grok-4.6-high.")
   220	    if always_approve and not yolo_allowed(chosen):
   221	        return True, (f"{CURSOR_BANNER} 🛑 WRITE REFUSED — '{chosen}' is not on the YOLO "
   222	                      "allowlist. Only composer-* and cursor-grok-* may write or execute.")
   223	
   224	    if klass.startswith("CREDITS"):
   225	        ok, why = _allowance("cursor")
   226	        if not ok:
   227	            return True, (f"{CURSOR_BANNER} 🛑 NO ALLOWANCE — REFUSED BEFORE SPENDING\n\n"
   228	                          f"'{chosen}' bills the third-party credit pool, and {why}\n\n"
   229	                          "Free INCLUDED models are unaffected and need no allowance.")
   230	    if klass.startswith("CREDITS") and COUNCIL_LOCK_ON:
   231	        window = _allowance_window_s("cursor", COUNCIL_LOCK_WINDOW_S)
   232	        recent = _recent_billable(window)
   233	        if recent >= _allowance_calls("cursor", COUNCIL_LOCK_MAX):
   234	            return True, (f"{CURSOR_BANNER} 🛑 COUNCIL LOCK — REFUSED\n\n{recent} billable "
   235	                          f"Cursor calls already landed in the last {window // 60} minutes, "
   236	                          "at the operator's granted bound. Councils use subscription seats.")
   237	
   238	    _ensure_playpen()
   239	    workdir = cwd or PLAYPEN
   240	    if not os.path.isdir(workdir):
   241	        return True, f"cwd is not a directory: {workdir}"
   242	
   243	    guard = _guard()
   244	    if isinstance(guard, Exception) and always_approve:
   245	        return True, (f"{CURSOR_BANNER} 🛑 GUARD UNAVAILABLE — WRITE REFUSED\n\n"
   246	                      f"dispatch-guard could not be loaded ({guard}).\n\n"
   247	                      "A write-capable dispatch is refused while its guard is missing.")
   248	    if guard and not isinstance(guard, Exception) and always_approve and cwd:
   249	        rc, problems, _notes = guard.preflight(workdir, model=chosen)
   250	        if rc:
   251	            return True, (f"{CURSOR_BANNER} 🛑 PREFLIGHT REFUSED — dispatch would spend for "
   252	                          "nothing\n\n" + "\n".join(f"  • {p}" for p in problems) +
   253	                          "\n\nPoint the seat at a repo with real source, or run read-only.")
   254	
   255	    # The Windows CLI is a .cmd shim: no caller-controlled string may reach argv.
   256	    spill_path = None
   257	    try:
   258	        fd, spill_path = tempfile.mkstemp(prefix="prompt_", suffix=".md", dir=PROMPTS_DIR)
   259	        try:
   260	            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
   261	                handle.write(prompt)
   262	        except OSError as exc:
   263	            return True, f"could not write the prompt handoff file: {exc}"
   264	        pointer = ("Read the file at " + spill_path.replace("\\", "/") +
   265	                   " which contains your full instructions. Follow them exactly and answer "
   266	                   "them directly. Do not modify or delete that file; it is a scratch "
   267	                   "handoff and is cleaned up automatically.")
   268	        if not pointer.isascii():
   269	            return True, ("the prompt handoff path contains non-ASCII characters; set "
   270	                          "WMW_CURSOR_PLAYPEN to a plain ASCII path")
   271	
   272	        command = [exe]
   273	        if session_id:
   274	            command += [f"--resume={session_id}"]
   275	        command += ["--model", chosen]
   276	        command += ["--yolo"] if always_approve else ["--mode", "ask", "--trust"]
   277	        # Auto-approved MCPs are an escalation route and bind only after writes are enabled.
   278	        if always_approve:
   279	            command += ["--approve-mcps"]
   280	        command += ["-p", pointer, "--output-format", "json"]
   281	        proc, failure = core.run_process(command, CURSOR_TIMEOUT_S, cwd=workdir)
   282	    finally:
   283	        if spill_path:
   284	            try:
   285	                os.unlink(spill_path)
   286	            except (FileNotFoundError, OSError):
   287	                pass
   288	
   289	    if failure:
   290	        if failure.kind == "timeout":
   291	            _log_spend(chosen, _lineage(chosen), klass, None, session_id, False,
   292	                       always_approve)
   293	            return True, f"cursor-agent timed out after {CURSOR_TIMEOUT_S}s"
   294	        return True, f"could not launch cursor-agent: {failure.detail}"
   295	
   296	    raw, err = (proc.stdout or "").strip(), (proc.stderr or "").strip()
   297	    data = _extract_json(raw)
   298	    if data is None and ("Workspace Trust Required" in raw or
   299	                         "Workspace Trust Required" in err):
   300	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   301	        return True, (f"Cursor refused {workdir} as untrusted. Point cwd at a project "
   302	                      "directory you trust, or leave cwd unset to use the playpen.")
   303	    if data is None:
   304	        _log_spend(chosen, _lineage(chosen), klass, None, session_id, False, always_approve)
   305	        return True, (f"cursor-agent exited {proc.returncode} with no parseable JSON.\n"
   306	                      f"stdout: {raw[:2000]}\nstderr: {err[:2000]}")
   307	    if data.get("is_error") or data.get("subtype") not in (None, "success"):
   308	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"),
   309	                   data.get("session_id") or session_id, False, always_approve)
   310	        return True, (f"cursor-agent reported an error: {str(data.get('result'))[:1500]}\n"
   311	                      f"stderr: {err[:800]}")
   312	    text, returned_id = data.get("result"), data.get("session_id")
   313	    if proc.returncode != 0 or not isinstance(returned_id, str) or not returned_id:
   314	        _log_spend(chosen, _lineage(chosen), klass, data.get("usage"),
   315	                   returned_id or session_id, False, always_approve)
   316	        return True, (f"cursor-agent run failed (exit {proc.returncode}, "
   317	                      f"session_id={returned_id!r}).\nresult: {str(text)[:1000]}\n"
   318	                      f"stderr: {err[:1000]}")
   319	
   320	    text, usage = core.truncate_reply(text, "wmw-cursor"), data.get("usage") or {}
   321	    tokens = (f"{usage.get('inputTokens', '?')} in / {usage.get('outputTokens', '?')} out"
   322	              if usage else "usage unreported")
   323	    mark, vendor = METER_MARK.get(klass, "⚠️"), _lineage(chosen)
   324	    pool = ("Cursor Models pool — INCLUDED, no credits spent" if klass == "INCLUDED" else
   325	            "Cursor Models pool — included, but a FAST-tier surcharge applies"
   326	            if klass == "INCLUDED-FAST" else
   327	            "third-party CREDIT pool — billed at API prices")
   328	    _log_spend(chosen, vendor, klass, usage, returned_id, True, always_approve)
   329	    money = ((f"\n{CURSOR_BANNER} {mark} —— THIS CALL SPENT MONEY —— {mark} {CURSOR_BANNER}"
   330	              f"\n   {pool}") if klass.startswith("CREDITS") or
   331	             klass == "INCLUDED-FAST" else "")
   332	    footer = (f"\n\n---\n{CURSOR_BANNER}{BLOODLINE_MARK.get(vendor, '❓')} [wmw-cursor] "
   333	              f"{mark} {vendor} · {chosen}\n   sessionId: {returned_id} · meter: {klass} · "
   334	              f"{tokens}{money}")
   335	    return False, text + footer
   336	
   337	
   338	_MODEL_NOTE = ("Model id (default composer-2.5 — the free, non-fast door). Free/INCLUDED: "
   339	               "composer-2.5, cursor-grok-4.6-{low,medium,high,xhigh}, cursor-grok-4.5-*. "
   340	               "Metered/CREDITS (need spend_credits): claude-*, gpt-*, gemini-*, kimi-*, "
   341	               "glm-*. `auto` is refused. See BENCH-LEDGER.md; `cursor-agent models` lists all.")
   342	TOOLS = [
   343	    {
   344	        "name": "cursor",
   345	        "description": (
   346	            "Start a NEW persistent conversation on the CURSOR MODEL POOL (Composer 2.5 by "
   347	            "default; Cursor Grok, Codex, Kimi, GLM and other tiers via `model`). Returns the "
   348	            "reply plus a sessionId footer; continue it with cursor-reply. ⚠ THE ONE METERED "
   349	            "SEAT: composer-* and cursor-grok-* are INCLUDED (free); everything else bills "
   350	            "Cursor's credit pool and is refused unless spend_credits is true. DEFAULT IS "
   351	            "READ-ONLY (no code execution, no file writes). Set always_approve true only for "
   352	            "build tickets, and then cwd is REQUIRED. With no cwd the seat works in its own "
   353	            "playpen directory."
   354	        ),
   355	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   356	        "inputSchema": {"type": "object", "properties": {
   357	            "prompt": {"type": "string", "description": "The task or message."},
   358	            "cwd": {"type": "string", "description": "Working directory. REQUIRED when always_approve is true; must not be a home, system or credential directory. Omit to work in the playpen."},
   359	            "model": {"type": "string", "description": _MODEL_NOTE},
   360	            "always_approve": {"type": "boolean", "description": "DANGEROUS: pass --yolo so the agent may write files and run commands under cwd. Default false = read-only."},
   361	            "spend_credits": {"type": "boolean", "description": "Required to reach any THIRD-PARTY model (claude-/gpt-/gemini-/kimi-/glm-), billed at API prices against Cursor's credit pool. Ask the boss first."},
   362	        }, "required": ["prompt"]},
   363	    },
   364	    {
   365	        "name": "cursor-reply",
   366	        "description": (
   367	            "Continue an existing Cursor-pool conversation by sessionId (from a prior cursor "
   368	            "call's footer), with full prior context. Same meter rules apply."
   369	        ),
   370	        "annotations": {"destructiveHint": True, "openWorldHint": True},
   371	        "inputSchema": {"type": "object", "properties": {
   372	            "sessionId": {"type": "string", "description": "sessionId from a previous cursor/cursor-reply call."},
   373	            "prompt": {"type": "string", "description": "The follow-up message."},
   374	            "model": {"type": "string", "description": _MODEL_NOTE},
   375	            "cwd": {"type": "string", "description": "Working directory for this turn."},
   376	            "always_approve": {"type": "boolean", "description": "Pass --yolo for this turn (write-capable); requires cwd."},
   377	            "spend_credits": {"type": "boolean", "description": "Required to reach a third-party (credit-billed) model."},
   378	        }, "required": ["sessionId", "prompt"]},
   379	    },
   380	]
   381	
   382	
   383	def _tool_call(name, args):
   384	    if name not in ("cursor", "cursor-reply"):
   385	        return None
   386	    approve = core.optional_boolean(args, "always_approve")
   387	    cwd = core.safe_write_cwd(core.optional_string(args, "cwd"), approve, (PLAYPEN,))
   388	    return run_cursor(
   389	        core.required_string(args, "prompt"),
   390	        session_id=(core.safe_uuid(args.get("sessionId"), "sessionId")
   391	                    if name == "cursor-reply" else None),
   392	        cwd=cwd,
   393	        model=core.safe_model_id(core.optional_string(args, "model")),
   394	        always_approve=approve,
   395	        spend_credits=core.optional_boolean(args, "spend_credits"),
   396	    )
   397	
   398	
   399	def main():
   400	    core.serve("wmw-cursor", "2.7.0", TOOLS, _tool_call, startup=_ensure_playpen)
   401	
   402	
   403	if __name__ == "__main__":
   404	    main()
```
