I'll start by reading the review packet in full and following it exactly.The packet was truncated — I'll read the rest and then walk the refusal paths against the actual files.The packet is complete. Next I’ll compare the live sources and the pre-refactor seats so I can judge whether any guard actually weakened.I’ll pull git history, the build spec, and the pre-merge `_safe_cwd` implementations so I can compare guards, not just the snapshot in the packet.Shell is blocked, so I’ll recover the pre-refactor guards from docs and the live seat files instead.The combine packet still has the pre-merge `_safe_cwd` bodies. I’ll extract those and compare them line-by-line with the shared core.I have the pre-merge `_safe_cwd` bodies and the live adapters. Walking every refusal path against that union now.

**Verdict: the write-path union is sound. Vendor flags were not genericised. The move does not weaken a previously closed refusal. One new load-path was added to make a copied Cursor adapter import `seat_core`, and that is the only merge-introduced defect worth acting on.**

I compared the live files to the pre-merge wrappers in `docs/council-combine/pkt-gemini.md`. I did not re-run `armcheck --deep`.

---

## 1. Did any guard weaken in the move?

**No confirmed weakening of the write-path denylist.** `safe_write_cwd()` is the union, and on every closed check it is as strong as the strongest pre-merge seat, or stronger.

Write-capable refusal walk (`seat_core.py`):

| # | Path | Result |
|---|---|---|
| 1 | `write_capable` and `cwd is None` | refuse (`135–137`) |
| 2 | resolved cwd is not a directory | refuse (`139–141`) |
| 3 | `_within(real, exception)` for adapter exceptions | **allow and return** (`143–146`) — Cursor playpen only |
| 4 | cwd is that volume’s root (`Path(real).anchor`) | refuse (`148–151`) |
| 5 | inside `SystemRoot` / `windir` / `ProgramFiles` / `ProgramFiles(x86)` / `ProgramData` | refuse, containment (`153–158`) |
| 6 | at or inside `APPDATA` / `LOCALAPPDATA` | refuse, containment (`162–166`) |
| 7 | at or inside `expanduser("~")` or `USERPROFILE` | refuse, **subtree** (`168–175`) |
| 8 | any path component in `_CREDENTIAL_SEGMENTS` (casefold) | refuse (`177–180`) |
| 9 | else | return canonical `real` |

Read-only (`write_capable=False`) still does **not** apply 1–8; it only realpaths (`133–134`). That matches all three pre-merge seats and the spec: *“Read-only calls do not acquire generic vendor policy here.”*

Per-check vs pre-merge:

- **Symlink / canonical return.** Pre-merge Grok/Gemini returned the caller string on read-only and `real` on write; Cursor always returned `realpath`. Core now returns `realpath` on both (`133–134`, `181`). Not weaker.
- **Explicit cwd on write.** All three already raised; core still raises (`135–137`). Reply tools still go through the same helper (`wmw_grok_mcp.py 141–142`, `wmw_gemini_mcp.py 128–129`, `wmw_cursor_mcp.py 387`). The old `grok-reply` / `gemini-reply` escalation with no cwd stays closed.
- **Root.** Pre-merge used `abspath(os.sep)` — the *process* drive. Core uses `Path(real).anchor` (`148–151`), so `D:\` is refused even when the server is on `C:`. Stronger.
- **System trees.** Same env list, containment via `commonpath` (`119–124`, `153–158`). Same as Grok/Cursor; stronger than Gemini’s equality+startswith.
- **APPDATA / LOCALAPPDATA.** Cursor-only before (`pkt-gemini.md` Cursor L359–368). Now on every seat (`162–166`). Stronger for Grok and Gemini (covers redirected AppData that is not under the profile).
- **Profile.** Gemini banned the home **subtree**; Grok/Cursor banned home/USERPROFILE **exactly** so projects under the profile still worked. Core takes Gemini’s subtree ban and adds `USERPROFILE` (`168–175`). Stronger. On this box projects live under `C:\Sync\…`, so it is not a false-positive. A repo under `%USERPROFILE%\Documents` would now be refused on all three seats.
- **Playpen.** Still Cursor-only, passed in as `safe_exceptions=(PLAYPEN,)` (`wmw_cursor_mcp.py 387`), still short-circuits before the denylist (`143–146`). Same shape as pre-merge Cursor L342–343. Grok/Gemini pass no exceptions.
- **Credential segments.** Core has Cursor’s full ten-name set (`20–23`), compared casefold via `Path.parts` (`177–180`). Gemini was missing `.cursor` / `.azure` / `.kube` / `.gnupg` and matched case-sensitively by substring. Stronger for Gemini; equivalent for Grok/Cursor.

**CONFIRMED (not a weaken, a tightening):** Grok’s old comment said home is a legitimate *parent* of projects (pre-merge Grok `_safe_cwd` L194–198). That exact-root policy is gone. Write-capable Grok/Cursor may no longer sit under the profile. That is the spec’s union, not a bypass.

**SUSPECTED (nit, not a bypass):** Gemini’s old substring test (`os.sep + secret in real`) would also refuse `.ssh_backup` / `.cursor-tutor`. `Path.parts` only matches an exact component. The intended check is a directory named `.ssh`, not a prefix. Residual 8.3 / `\\?\` / junction TOCTOU is the same class as before; both sides still `realpath`.

Adapter refusals that are *not* in the core, and still fire:

- Grok read-only: `--deny` list including `MCPTool`, plus `--disallowed-tools Agent`, `--permission-mode default`, `--no-subagents`, `--no-memory`, optional `--disable-web-search` (`wmw_grok_mcp.py 10–11, 61–69`).
- Gemini read-only: `--mode plan`; write: `--dangerously-skip-permissions` (`wmw_gemini_mcp.py 49–57`).
- Cursor: meter/UNKNOWN, `spend_credits`, YOLO allowlist, allowance, council lock, guard fail-closed, preflight, ASCII spill pointer (`wmw_cursor_mcp.py 210–253, 255–279`).

`stdin=subprocess.DEVNULL` is in the shared launcher (`seat_core.py 106`). That is the confused-deputy fix (child must not eat MCP stdin). Preserved.

---

## 2. Did vendor-specific enforcement get genericised?

**No. CONFIRMED preserved.**

Normalized input is `always_approve` → `write_capable` for *path* policy only. CLI policy is still written out in each adapter:

- Grok: deny rules and `--disallowed-tools Agent` stay local (`wmw_grok_mcp.py 10–11, 61–67`).
- Gemini: `--mode plan` vs `--dangerously-skip-permissions` stay local (`wmw_gemini_mcp.py 49–57`).
- Cursor: `--mode ask --trust` vs `--yolo`, and `--approve-mcps` **only** on the write path (`wmw_cursor_mcp.py 276–279`).

Parsers stay split (Grok/Gemini first object, Cursor last `type==result`). Prompt transport stays split (Grok tempfile, Gemini argv + 25k cap, Cursor ASCII playpen spill). That matches BUILD-SPEC “KEEP APART.”

There is no generic `readonly=True` that picks flags.

---

## 3. What does the shared core now make possible that was impossible before?

**Worst realistic case (CONFIRMED, structural — not a current bypass):**

One defect in `safe_write_cwd()` is now a write-capable session on **all three** CLIs at once:

- Grok: `--always-approve` (deny list stripped)
- Gemini: `--dangerously-skip-permissions`
- Cursor: `--yolo` **and** `--approve-mcps`

Before, a containment miss had to be reproduced in three functions. The shop already paid that cost (Gemini missing Grok’s System32 containment; Gemini-reply missing the cwd requirement). The merge closes that class **and** inverts it: the next `_within` / `realpath` miss is a triple YOLO.

Next-worst shared knobs:

- `run_process()` (`101–112`) — drop `stdin=DEVNULL`, switch to `shell=True`, or mishandle timeout, and every seat inherits it. Timeout still uses `subprocess.run(..., timeout=)` with **no process-tree kill**. That gap existed per seat; it is now one function. A timed-out `--always-approve` / `--yolo` child can keep writing while the caller is told the call failed.
- `optional_boolean()` (`41–49`) — if missing/`"true"` handling ever flips, `always_approve` flips on every seat together.
- `discover_executable()` PATH fallback (`87–92`) — substitute-binary defence is still “known path first,” but a bad `isfile` check would load a PATH hijack for grok, agy, and cursor-agent.

armcheck still attacks *wrappers*, not `seat_core` directly. Grok never gets the System32 / home / APPDATA canaries (those are Cursor/Gemini only). After the merge that is mostly redundant **unless** the Grok wiring differs — and it does: Grok/Gemini run `safe_argv_string` on cwd, Cursor does not, and only Cursor passes `safe_exceptions`.

---

## 4. Anything the builder left behind

**CONFIRMED — Cursor `seat_core` import fallback (merge-introduced).** `wmw_cursor_mcp.py 10–15`:

```python
try:
    import seat_core as core
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.getcwd(), "mcp-seats"))
    import seat_core as core
```

This exists because armcheck copies the adapter **without** `seat_core` (and the builder was not allowed to edit armcheck). Before the split, `_safe_cwd` lived in the copied file, so the guard travelled with the copy. After the split, a missing adjacent `seat_core` is resolved from **`$CWD/mcp-seats/seat_core.py`**.

Production registration runs `mcp-seats/wmw_cursor_mcp.py`, so the first import succeeds and this branch is dead. It becomes live whenever the adapter is started from a copy, a temp dir, or a deleted `seat_core.py`. Grok/Gemini have **no** fallback: they fail closed. Cursor is the only seat that will load a planted core.

That is exactly “a fallback that masks a real failure.” It is the load path for the module that *is* the guard.

**CONFIRMED — lost load-bearing comments, not lost behavior.** Pre-merge Grok spelled out why `MCPTool` is the deny that matters (sibling-seat laundering, reproduced 2026-08-23). The list still includes `MCPTool` (`wmw_grok_mcp.py 10–11`); the rationale is now one line (`52–53`). Same for Gemini’s “do not omit the skip-permissions flag and trust machine settings” — shortened, still present (`49–50`).

**CONFIRMED — no dead imports / orphaned constants in the four files.** `_safe_cwd`, `_utf8_stdio`, `_opt_str`, local `MAX_REPLY_CHARS`, `shutil` in the adapters are gone. `isdir` checks in `run_grok` / `run_gemini` / `run_cursor` are not dead: they still cover the read-only path, which `safe_write_cwd` does not.

**Not merge debris (pre-existing, still true):**

- `grok-reply` / `gemini-reply` still lack `destructiveHint` / `openWorldHint` while the start tools have them.
- Grok `allow_web_search: true` still does not undo `--deny WebSearch` / `--deny WebFetch` (`10–11` vs `68–69`).
- Read-only sessions may still `cwd` at `.ssh` and read it; only write is denied.
- `WMW_CURSOR_PLAYPEN` is an unchecked allow-root (operator env). If it is set to `C:\Windows`, Cursor YOLO is allowed there. Same as pre-merge.

---

## Plainly

The merge did the security job it was asked to do. Path policy is the union (symlink-resolved, write requires cwd, root exact, system/APPDATA/LOCALAPPDATA containment, credential segments, Cursor playpen exception). Gemini’s profile-subtree lesson now applies to Grok and Cursor as well. Vendor read/write flags were not collapsed into a generic implementation.

Ship the core. The only merge-introduced fix I would require is the Cursor import: fail closed, or pin `seat_core` to a known directory next to the real adapters — do not search `$CWD`.