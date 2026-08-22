I'll load the full council brief first, then review the shipped wrappers and docs on their own merits through the security lens.The brief is loaded. Next I’ll read the actual wrappers and docs in the repo so findings rest on the code, not just the packet.I’ll verify CLI flags, stdin handling, and a few likely overclaims against the real wrappers and docs.I’ll check the real CLI flags and stdin behavior next so I don’t overclaim.`--resume` plus a flag-shaped session id resumed this live session. Next I’ll confirm whether inherited stdin is folded into the prompt.## Findings

1. **CRITICAL** · `mcp-seats/wmw_grok_mcp.py` `run_grok()` (`--resume` + `sessionId`)  
   **What:** `sessionId` is copied onto the argv list with no shape check. Grok’s own help defines `--resume [<SESSION_ID>]` — the ID is optional. Clap then treats the next token starting with `-` as a **new flag**, not as the session id, and `--resume` with no value **resumes the most recent session**.  
   **Verified:** `grok --resume --disable-web-search -p "Reply with exactly: INJECT_TEST" --output-format json --max-turns 1` exited 0 and continued **this** Grok session (`sessionId` `01a02b88-b508-7c40-8faf-29ac8085ed1d`, ~82k input tokens of prior context). So `grok-reply(sessionId="--always-approve", prompt=...)` becomes `grok --resume --always-approve -p ...`: auto-approve **and** attach to whatever ran last (typically the builder). Same pattern for `--restore-code`, `--system-prompt-override`, `--sandbox`, `--cwd`, `--agent`.  
   **Why it matters:** One hostile tool argument turns a “review” into a YOLO continuation of the builder thread. That kills the anchoring law in code, not just in spirit. A malicious repo’s `CLAUDE.md` only has to tell the conductor to call `grok-reply` with that sessionId.  
   **Fix:** Reject any `sessionId` / `model` / `cwd` that is empty or starts with `-`. Require a UUID (Grok session ids are UUIDs). Pass `--resume=<uuid>` (equals form) so the value cannot be reparsed as a flag. Prefer `--session-id <uuid>` for a known id. On the Gemini sibling, reject `conversationId`/`model`/`cwd` with a leading `-` the same way.

2. **CRITICAL** · `wmw_grok_mcp.py` + `wmw_gemini_mcp.py` tool schemas; `mcp-seats/README.md` “read-only”; `SKILL.md` “Research/review tickets: omit both (read-only default)”  
   **What:** `always_approve` is an LLM-controlled boolean. True maps to Grok `--always-approve` (“auto-approve **all** tool executions”) and to Gemini `--dangerously-skip-permissions`. `cwd` is any string — home, `C:\`, another repo, wherever. Nothing pins `--permission-mode`, `--sandbox`, `--tools` / `--disallowed-tools`, `--disable-web-search`, `--no-subagents`, or `--no-memory`. Install is `--scope user`, so the tools exist in **every** later project, including hostile ones.  
   This box’s `~/.grok/config.toml` already has `permission_mode = "always-approve"`. The wrapper never passes `--permission-mode`, so **omitting** the flag is “use CLI default,” not read-only. Grok still has web search unless `--disable-web-search` is set; `--always-approve` auto-allows off-allowlist domains (Grok README). `grok inspect --json` in this tree reported `projectTrusted: true` and loaded `~/.claude/Claude.md` plus user hooks.  
   **Why it matters:** Docs sell a safe default. The code is a confused deputy: one allowed MCP call bypasses Claude Code’s own per-tool prompts and yields a second agent with shell, writes, and network. Prompt injection from a public repo can set `always_approve: true` and `cwd: C:\Users\<you>` and exfil via web search (including `~/.grok/auth.json`; Grok’s sandbox write-protects `~/.grok/auth/`, not `auth.json`). The Gemini flag name in the schema (`always_approve`) undersells `--dangerously-skip-permissions`.  
   **Fix:**  
   - `always_approve=false`: pass explicit `--permission-mode plan` (or Grok `--sandbox read-only` where it actually binds), `--disable-web-search`, `--no-subagents`, `--no-memory`, and a write/shell denylist (`--disallowed-tools` / `--tools` read-only). Do **not** trust config.  
   - `always_approve=true`: require `cwd` to be an existing directory under an allowlist (workspace / explicit roots). Refuse `$HOME`, profile, `C:\`, Windows, `.ssh`, `.aws`, `.grok`.  
   - Mark MCP tools with `destructiveHint` / `openWorldHint`.  
   - README/SKILL: user-scope + YOLO is a loaded gun; say so. “Read-only default” only if the wrapper **sends** the hardening flags.

3. **MAJOR** · both wrappers `*-reply`; README / SKILL / CREW “two laws ride the transport”  
   **What:** Session ids are bearer tokens printed in a forgeable text footer. `grok-reply` / `gemini-reply` resume any id they are given. Nothing binds an id to a role, a cwd, or “this thread built, so it cannot review.” `grok-reply` also drops `cwd`/`model`; `gemini-reply` drops `cwd` (agy child’s cwd becomes the MCP server’s cwd — often the currently open project, not the original ticket).  
   **Why it matters:** The method’s load-bearing invariant is documented as a property of the transport. The transport is a dumb pipe. A prompt-injected conductor can `*-reply` the builder session and title it a review. Finding 1 makes that even cheaper (no real id needed).  
   **Fix:** Treat ids as secrets: structured MCP field, not a regex in model text; strip lookalike `[wmw-grok] sessionId:` lines from model output before appending the real footer. Refuse reply-as-review in the tool **description** is not enough — add a `purpose: review|build` argument and, for review, force a fresh start (`--no-memory`, no `--resume`). Persist cwd on the reply path.

4. **MAJOR** · `wmw_grok_mcp.py` lines 68–70 vs Gemini lines 71–73  
   **What:** After JSON parses, Grok **always** returns `isError=False`. Non-zero exit is a footer footnote. Gemini at least sets error on `status != SUCCESS` or non-zero exit.  
   **Why it matters:** A YOLO turn that failed mid-shell still looks successful to the conductor.  
   **Fix:** `isError = proc.returncode != 0` (and treat missing/invalid JSON as error, as now). Do not report `sessionId: unknown` as a usable resume token.

5. **MAJOR** · `find_grok()` / `find_agy()`; `SETUP.md` §2 gotcha  
   **What:** Both wrappers `shutil.which` first, then fall back to the well-known install path. SETUP.md already says Grok is “not on the tool-shell PATH” and to use the **full** path. `which("grok")` / `which("agy")` on Windows follows `PATHEXT` (`.exe/.cmd/.bat/.ps1`).  
   **Why it matters:** User-scope MCP inherits the user’s PATH. A project or earlier PATH entry named `grok`/`agy` (including an unrelated npm `grok`) is executed with this user’s `~/.grok/auth.json` / Antigravity creds. That is a straight substitute-binary.  
   **Fix:** Prefer the known absolute install path; only then PATH. `os.path.isfile`, refuse `.cmd/.bat/.ps1` unless it is the real installer shim. Do not search the workspace.

6. **MINOR** · docstrings in both `.py` files; README timeout copy  
   **What:** Registration examples point at `...\andersons-dispatch-deck\wmw-grok\wmw_*_mcp.py` (that folder is not the ship). That leaks this machine’s `C:\Sync\Projects\...` layout on a public repo. README: “stalls … until the timeout **executes** it” (Gemini header correctly says **kills**). “60-minute timeout” is attributed to “the wrappers”; only agy gets `--print-timeout 60m`. Grok is a 3600s `subprocess` cap and does not pass `--max-turns`.  
   **Why it matters:** Wrong path is a footgun. “Timeout executes it” can be read as auto-run-on-timeout. Strangers think Grok has the same CLI timeout as agy.  
   **Fix:** Point at `mcp-seats\`; genericize paths; say “kills”; split Grok vs Gemini timeout behavior; cap Grok with `--max-turns`.

7. **MINOR** · both `subprocess.run(...)` (no `stdin=`)  
   **What:** SETUP.md §1–2: close stdin headless or the CLI hangs. Wrappers inherit MCP stdio.  
   **Verified for Grok `-p`:** `stdin=DEVNULL` returned in ~6s; an open `PIPE` with no EOF also returned in ~6s; piped `SECRET_FROM_STDIN_XYZ` did **not** appear in `text`/`thought`. So I could **not** reproduce a Grok `-p` hang or stdin-to-prompt fold. agy documents `--input-format stream-json` as **reading NDJSON from stdin**; I did not run that.  
   **Fix:** `stdin=subprocess.DEVNULL` anyway. Cheap, matches your own one-shot doctrine, closes the agy stream-json footgun.

8. **NIT** · `bool(args.get("always_approve"))` in both handlers; JSON `raw.find("{")`; no MCP `annotations`  
   **What:** `bool("false")` is `True` if a client ever stringifies. First `{` in CLI noise can become the parsed object. Tools are not marked destructive.  
   **Fix:** `always_approve is True`; `json.JSONDecoder().raw_decode`; set hints.

**CRITICAL / MAJOR / MINOR / NIT:** as above. None empty.

## Verified

- Read `mcp-seats/wmw_grok_mcp.py`, `wmw_gemini_mcp.py`, `README.md`, `SETUP.md` §4, `SKILL.md` persistent-seats, CREW persistent-seats block.  
- `grok --help` / `agy --help`: `--always-approve`, optional `--resume [<SESSION_ID>]`, `--disable-web-search`, `--sandbox`, `--permission-mode`, `--dangerously-skip-permissions`, `--print-timeout` default 5m.  
- `~/.grok/config.toml`: `permission_mode = "always-approve"`.  
- **Resume injection** as in finding 1 (live).  
- Grok JSON matches the wrapper’s `text` / `sessionId` / `modelUsage` / `num_turns`.  
- Grok `-p` stdin hang/prompt-fold: **not** reproduced.  
- Did **not** run the Claude MCP handshake, the REDHAWK codeword test, agy `--conversation` injection, or a live write to prove config YOLO without the flag. Windows `--sandbox` accepted the flag; I did not prove it enforces FS (README only names Landlock/Seatbelt).

**SHIP-WITH-FIXES** — persistence as a thin MCP pipe is fine; do not leave a public `claude mcp add --scope user` wrapper on main until sessionId cannot inject flags and “read-only” is actual argv, not a comment.  
Grok 4.6