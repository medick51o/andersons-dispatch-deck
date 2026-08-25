# TOP-TO-BOTTOM ADVERSARIAL AUDIT — 🔵 Codex, deep pass

A guest seat spent today writing working exploits against this harness and found ten real
defects, every one confirmed in source. **All of them are now fixed.** You are being brought in
because you are the sharpest code reviewer in this shop and you did not write any of it.

**Your job is not to re-find what it found. Your job is to find what it MISSED, and to check
whether the fixes are actually correct.** A fix that closes one path and opens another is worth
more to know about than a fresh medium-severity finding.

## What it found, and what was done (verify these are genuinely closed)

1. **`time` never imported** while `run_cursor` called `time.time()` — the reservation guard was
   DEAD CODE that raised NameError on every guarded write dispatch. Fix: import time, plus a
   canary that performs a real guarded dispatch. *(The reason it survived: two green tests, and
   neither ever reached the line. Look for more of that shape.)*
2. **Spend ledger lived in the playpen** — the one directory a write-capable session may always
   write. Delete it and the council lock silently unlocks. Fix: moved to `~/.anderson-method/`.
3. **The granted window was never enforced.** `allowance.py` records "N per window"; the seat
   read only the count and policed a hardcoded 600s, so "10/week" ran ~1000x looser than
   written. Fix: the seat now reads `window_seconds()`.
4. **APPDATA / LOCALAPPDATA unprotected** — a write-capable session could root where this rig's
   credentials and the vendor CLIs live. Fix: containment ban on both.
5. **`_guard()` failed OPEN** — any load error returned None and the caller's truthiness test
   skipped preflight AND reservation silently. Fix: returns the exception; a write-capable
   dispatch is refused when the guard cannot load.
6. **`reserve` accepted a negative claim**, passing the upper cap and SUBTRACTING from
   outstanding — manufacturing headroom. Fix: positive claims only.
7. **`release` checked no ownership** — any caller could free any lease, so two cheap
   reservations DoS the operator's own rig for the TTL. Fix: leases carry an owner token.
8. **Unbounded JSON-RPC frame** — memory exhaustion primitive. Fix: 8MB cap.
9. **Lock reclaimed on age alone** — a slow-but-living holder had its lock stolen, so two
   processes both believed they held it. Fix: verify the recorded PID is dead; fail closed when
   it cannot be determined.
10. Earlier the same day, on other seats: `gemini-reply` accepted **no cwd at all** while
    passing `always_approve` through; Gemini's `_safe_cwd` compared by equality so
    `C:\Windows\System32` was legal under a banned `C:\Windows`; the Cursor seat passed
    `--approve-mcps` even on the read-only path.

## What it flagged as SUSPECTED and never proved — settle these

- **The pointer string on argv is checked only with `.isascii()`.** `&`, `;`, `|`, `$` and
  backtick are all ASCII. The pointer is *generated*, not caller-supplied — but trace whether
  any caller-influenced value reaches it (the playpen path comes from an env var).
- **The timeout kills the `.cmd` shim, not the agent grandchild.** On Windows the grandchild
  plausibly survives, keeps spending, and its lease is released as if the work had stopped.
- **`--approve-mcps` still fires on the yolo path**, auto-approving `~/.cursor/mcp.json` — and
  possibly a project-level `<cwd>\.cursor\mcp.json` that a write-capable agent could create.

## Also in scope — nothing here has been audited by anyone

`dispatch-guard.py` in full, including code added *after* the exploit pass read it:
`load_events`, `find_events_csv` (it globs the user's Downloads and reads arbitrary CSV),
`yield_report`, and the new owner-token logic. `armcheck.py` itself — it was rewritten twice
today and now runs in two modes. And `calibrate-pool.py`, which nobody has looked at at all.

## The question underneath all of it

The named adversary is **a steered LLM holding the operator's shell**. The guest seat's verdict
was that as a security boundary this harness is **false assurance** — that adversary can rewrite
the allowance store, the ledger, the lock, the guard and the arm test. The counter-argument is
that these guards exist to stop *accidents and drift*, which is what actually happened (an
unattended fleet burned two-thirds of a month in two days), not a determined attacker.

**Rule on that.** If the guest seat is right, say what SHOULD exist instead, concretely, for a
one-person shop that cannot run a separate privileged process. If the guards are worth keeping,
say which ones actually earn their place and which are decoration that should be deleted.

## Rules
- Quote the exact function or line. Distinguish CONFIRMED (you traced the failing path) from
  SUSPECTED. An unanchored finding is unusable.
- Rank by what an attacker or a careless operator actually achieves.
- **Attack the fixes, not just the original code.** Fixes written in a hurry are where the next
  bug lives, and all ten landed today.
- Say what is well built. A review with no positives is not credible.
- Do not write any file. Report only.

## Output
```
VERDICT (3 sentences)
ARE THE TEN FIXES CORRECT?   — each: HOLDS / INCOMPLETE / INTRODUCED A NEW BUG
WHAT THE EXPLOIT PASS MISSED — ranked, CONFIRMED vs SUSPECTED
THE THREE SUSPECTED ITEMS    — settle each one
UNAUDITED CODE               — findings in dispatch-guard/armcheck/calibrate-pool
RULING: FALSE ASSURANCE, OR WORTH KEEPING? — and what should exist instead
WHAT IS WELL BUILT
CONFIDENCE + what would change your mind
```
