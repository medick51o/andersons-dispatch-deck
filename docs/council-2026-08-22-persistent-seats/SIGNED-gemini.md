# COUNCIL REVIEW — 🟢 Gemini (The Outsider Installer Lens)

**Reviewer:** 🟢 Gemini (`Gemini 3.6 Flash (High)`)  
**Focus:** Outsider Installation & Cross-Platform Usability (macOS/Linux/Windows, non-owner machine, zero prior setup, documentation quality).

---

## 1. Numbered Findings (Most Severe First)

### Finding 1
* **Severity:** CRITICAL
* **File + Location:** `mcp-seats/wmw_gemini_mcp.py` · lines 241–249 (`find_agy()`)
* **What is wrong:** `find_agy()` relies entirely on Windows-specific environment variables (`LOCALAPPDATA`) and `.exe` binary extensions when `agy` is not already on PATH:
  ```python
  local = os.environ.get("LOCALAPPDATA", os.path.expanduser(r"~\AppData\Local"))
  cand = os.path.join(local, "agy", "bin", "agy.exe")
  ```
* **Why it matters:** On macOS and Linux, `LOCALAPPDATA` does not exist, `AppData/Local` is invalid, and binaries do not end in `.exe`. If `agy` is installed in standard non-PATH user directories (such as `~/.local/bin/agy` or `~/.agy/bin/agy`), `find_agy()` returns `None`. Every call to `gemini` or `gemini-reply` will fail with `"Antigravity CLI not found"`.
* **Concrete suggested fix:** Update `find_agy()` to check POSIX fallback locations and extensionless binary names:
  ```python
  def find_agy():
      exe = shutil.which("agy")
      if exe:
          return exe
      candidates = [
          os.path.expanduser("~/.local/bin/agy"),
          os.path.expanduser("~/.agy/bin/agy"),
          "/usr/local/bin/agy",
      ]
      local = os.environ.get("LOCALAPPDATA")
      if local:
          candidates.insert(0, os.path.join(local, "agy", "bin", "agy.exe"))
      else:
          candidates.append(os.path.expanduser(r"~\AppData\Local\agy\bin\agy.exe"))
      for cand in candidates:
          if os.path.exists(cand):
              return cand
      return None
  ```

---

### Finding 2
* **Severity:** MAJOR
* **File + Location:** `SETUP.md` · lines 572–578 (The reachability probe)
* **What is wrong:** The automated reachability probe script hardcodes Windows environment variables and `.exe` extensions:
  ```bash
  "$HOME/.grok/bin/grok.exe" --version 2>/dev/null && echo "GROK: online" || ...
  "$LOCALAPPDATA/agy/bin/agy.exe" --version 2>/dev/null && echo "GEMINI: online" || ...
  ```
* **Why it matters:** On macOS/Linux, `$LOCALAPPDATA` is empty (resolving to `/agy/bin/agy.exe`) and the binaries are named `grok` and `agy` (no `.exe`). Running this reachability probe on a Mac or Linux machine reports Grok and Gemini as `missing` even when both are properly installed and logged in.
* **Concrete suggested fix:** Rewrite the reachability probe to check `command -v` first, then fallback paths per OS:
  ```bash
  # Grok
  (command -v grok >/dev/null 2>&1 || [ -f "$HOME/.grok/bin/grok" ] || [ -f "$HOME/.grok/bin/grok.exe" ]) && echo "GROK: online" || echo "GROK: missing (see §2)"
  # Gemini / Antigravity
  (command -v agy >/dev/null 2>&1 || [ -f "${LOCALAPPDATA:-$HOME/AppData/Local}/agy/bin/agy.exe" ] || [ -f "$HOME/.local/bin/agy" ] || [ -f "$HOME/.agy/bin/agy" ]) && echo "GEMINI: online" || echo "GEMINI: missing (see §3)"
  ```

---

### Finding 3
* **Severity:** MAJOR
* **File + Location:** `mcp-seats/README.md` (lines 425, 431) & `SETUP.md` (lines 553, 555)
* **What is wrong:** Registration instructions use backslash relative paths and plain `python`:
  ```bash
  claude mcp add --scope user grok -- python <path-to-this-folder>\wmw_grok_mcp.py
  ```
  1. `claude mcp add --scope user` writes to global `~/.claude.json`. If a relative path or unexpanded placeholder is passed, running `claude` from any other directory fails to locate the Python script.
  2. Windows backslashes (`\`) cause shell syntax errors in POSIX shells (bash/zsh).
  3. On macOS and many Linux distros, `python` is not aliased to Python 3 (`python3`).
* **Why it matters:** Copy-pasting these commands on macOS/Linux causes immediate shell syntax errors or `file not found` errors when Claude Code launches the MCP server.
* **Concrete suggested fix:** Provide OS-specific copy-paste blocks using absolute path expansion (`$(pwd)` / `$((Get-Item .).FullName)`) and `python3`:
  ```bash
  # macOS / Linux (Bash/Zsh):
  claude mcp add --scope user grok -- python3 "$(pwd)/mcp-seats/wmw_grok_mcp.py"
  claude mcp add --scope user gemini -- python3 "$(pwd)/mcp-seats/wmw_gemini_mcp.py"

  # Windows (PowerShell):
  claude mcp add --scope user grok -- python "$((Get-Item .).FullName)\mcp-seats\wmw_grok_mcp.py"
  claude mcp add --scope user gemini -- python "$((Get-Item .).FullName)\mcp-seats\wmw_gemini_mcp.py"
  ```

---

### Finding 4
* **Severity:** MAJOR
* **File + Location:** `mcp-seats/wmw_grok_mcp.py` · line 92 (`run_grok`) & tool schemas (lines 141–152)
* **What is wrong:** Working directory handling is incomplete in `wmw_grok_mcp.py`:
  1. `subprocess.run` in `wmw_grok_mcp.py` does not pass `cwd=cwd or None` (unlike `wmw_gemini_mcp.py` line 265). It only appends `["--cwd", cwd]` to arguments if `cwd` is supplied on the initial `grok` call.
  2. Neither `grok-reply` nor `gemini-reply` input schemas accept a `cwd` argument.
* **Why it matters:** When `grok` or `grok-reply` is executed, the underlying process runs in whatever directory the MCP server process was started in (typically `~`). If `grok` relies on process CWD or if a reply turn requires working directory context, operations outside home directory will break.
* **Concrete suggested fix:**
  1. Pass `cwd=cwd or None` to `subprocess.run` in `wmw_grok_mcp.py`:
     ```python
     proc = subprocess.run(
         cmd, capture_output=True, text=True, encoding="utf-8",
         errors="replace", timeout=GROK_TIMEOUT_S, cwd=cwd or None,
     )
     ```
  2. Add optional `cwd` property to `grok-reply` and `gemini-reply` input schemas.

---

### Finding 5
* **Severity:** MAJOR
* **File + Location:** `SETUP.md` · §3 line 519 (Antigravity installation)
* **What is wrong:** Installation instructions for Antigravity (`gemini`) in `SETUP.md` provide only a Windows PowerShell snippet:
  `irm https://antigravity.google/cli/install.ps1 | iex`
* **Why it matters:** A stranger on macOS or Linux trying to follow `SETUP.md` step 3 will hit `command not found: irm` in bash/zsh.
* **Concrete suggested fix:** Include the macOS/Linux install command alongside PowerShell:
  ```markdown
  - **Install:**
    - Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 | iex`
    - macOS / Linux (Bash/Zsh): `curl -fsSL https://antigravity.google/cli/install.sh | bash`
  ```

---

### Finding 6
* **Severity:** MINOR
* **File + Location:** `mcp-seats/README.md`, `SETUP.md` §4, `SKILL.md`, `CREW.md`, and wrapper headers
* **What is wrong:** Inconsistent server naming across documentation and code:
  * `README.md` & `SETUP.md` instruct strangers to register names `codex`, `grok`, and `gemini`.
  * `SKILL.md` (line 856 / 670) and `CREW.md` (line 856) state: `Ours: wmw-codex · wmw-grok · wmw-gemini`.
  * `serverInfo.name` in both Python wrappers returns `wmw-grok` and `wmw-gemini`.
* **Why it matters:** A first-time reader cannot tell whether the standard registration is `grok` or `wmw-grok`, nor why `SKILL.md` refers to `wmw-codex` when Codex MCP mode registers as `codex`.
* **Concrete suggested fix:** Standardize registration names across all files. Explicitly note in `README.md` that server names (e.g., `grok` vs `wmw-grok`) set the tool prefix in Claude Code, and align `SKILL.md`/`CREW.md` references.

---

### Finding 7
* **Severity:** MINOR
* **File + Location:** `mcp-seats/wmw_grok_mcp.py` (line 55) & `mcp-seats/wmw_gemini_mcp.py` (line 230)
* **What is wrong:** File docstrings contain hardcoded local paths referencing a non-existent `wmw-grok` directory:
  `python C:\Sync\Projects\andersons-dispatch-deck\wmw-grok\wmw_grok_mcp.py`
* **Why it matters:** Strangers attempting to copy registration commands directly from the header comments will hit non-existent path errors.
* **Concrete suggested fix:** Replace hardcoded paths in docstrings with generic placeholder examples:
  `claude mcp add --scope user wmw-grok -- python /path/to/mcp-seats/wmw_grok_mcp.py`

---

### Finding 8
* **Severity:** NIT
* **File + Location:** `mcp-seats/wmw_grok_mcp.py` (lines 99–106) & `mcp-seats/wmw_gemini_mcp.py` (lines 272–279)
* **What is wrong:** JSON output parsing locates the first `{` via `idx = raw.find("{")` and parses `raw[idx:]`. If stdout contains trailing text after the JSON object (or if `text`/`response` is `null`), `json.loads` throws `JSONDecodeError` ("Extra data") or string concatenation raises `TypeError`.
* **Why it matters:** Any trailing logs or `null` JSON fields will crash tool execution.
* **Concrete suggested fix:** Slice up to `raw.rfind("}") + 1`, and use `(data.get("text") or "")` / `(data.get("response") or "")` for safe string concatenation.

---

## 2. Verification

* **Verified:**
  1. Python MCP stdio protocol implementation (`initialize`, `ping`, `tools/list`, `tools/call`, notification handling, JSON-RPC format) in `wmw_grok_mcp.py` and `wmw_gemini_mcp.py`.
  2. Doctrine and legend consistency across `SKILL.md` (v4.0 legend rules, persistent seat doctrine) and `CREW.md`.
  3. Timeout and permission flag handling (`--print-timeout 60m`, `--dangerously-skip-permissions`, `--always-approve`).
* **Could Not Verify:**
  1. Execution of `grok` CLI binary or `codex mcp-server` on a native macOS/Linux target machine without the respective vendor CLIs installed.

---

## 3. Verdict

**SHIP-WITH-FIXES**  
The persistent MCP seat architecture is sound and well-crafted, but cross-platform path resolution in `find_agy()`, the reachability probe script, and shell registration instructions must be fixed so non-Windows strangers can install successfully.

— **Gemini 3.6 Flash (High)**
