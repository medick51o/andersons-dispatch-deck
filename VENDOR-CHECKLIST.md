# Vendor-side checklist — the guards no script can install

`dispatch-guard.py` governs dispatches that pass **through** it. The lanes that burned this
shop's allowance on 2026-08-21/22 do not. They execute on the vendor's infrastructure and obey
the vendor's settings, so they are closed **in the vendor's own dashboard, by a human, or not
at all.**

Codex put it plainly: *"a checklist, local hook, or dashboard alert is not a guard."* This page
is the short list of things that ARE.

---

## The correction that matters most

An earlier draft of this advice said: set on-demand spending to `$0` and the leak is sealed.
**That is wrong, and this shop's own billing page disproves it.**

During the burn window the dashboard read `On-Demand Usage: $0.00`. Thirteen cloud agents still
consumed 51.9M tokens and two-thirds of the month — **entirely inside the prepaid included
pool, with on-demand already at zero.**

> **A spend limit protects CASH. It does not protect the ALLOWANCE.**
> An agent can destroy the month's included pool without charging one extra dollar.

Set the limit anyway — it is free and it caps the tail risk of a runaway metered bill. Just do
not mistake it for the fix.

---

## Do these, in order

### 1. Cloud / background agents — disable the lane, or cap it

This is the lane that actually burned the month. Priority order:

- **Best:** turn cloud/background agents OFF entirely. Local MCP seats already cover the work,
  and they pass through the guard.
- **If kept:** never stack `maxMode` + `effort: xhigh` + `speed: fast`. That combination was
  measured at **5.5x** the cheapest included model. Twelve of thirteen agents carried all three.
- **If kept:** cap concurrent agents at 1–2. The incident was **thirteen launches**, not one bad
  model choice.
- Launch only against a repo with real tracked source. `dispatch-guard.py preflight <repo>`
  answers this in one second; eleven of thirteen agents were sent at a repo staged deliberately
  empty and produced zero lines.

### 2. On-demand spending — set the cash fuse

Dashboard → Spending. On-demand **off**, or on with a small hard limit. A cash backstop, not an
allowance guard (see above). Also disable any "auto-continue on-demand after the pool empties"
behavior: a single earlier *yes* can turn the next agent swarm into an uncapped metered bill.

### 3. Model defaults — the IDE and the cloud launcher keep their own

`~/.cursor/cli-config.json` was correctly pinned to `composer-2.5` with fast off for the entire
incident. **Cloud agents never read it.** Every surface keeps its own model selection:

| Surface | Reads the local config? |
|---|---|
| MCP seats (this rig) | yes — and is guarded |
| Cursor CLI, run by hand | yes |
| Cursor IDE chat / agent mode | **no** |
| Cloud / background agents | **no** |
| Web dashboard launcher | **no** |
| Mobile app | **no** |
| Bugbot on pull requests | **no** |

Set the cheap default **in each surface you actually use**, and treat any surface you do not
use as one to sign out of.

### 4. Sessions and credentials

Revoking a local config revokes nothing that already exists elsewhere. Review active sessions
and sign out anything stale: old devices, copied browser sessions, mobile, any container / WSL /
SSH host holding credentials. Each is its own enforcement domain.

### 5. Team seats — if one is ever added

Turn on "only admins can edit usage settings." Otherwise any member can lift the cap, and every
local meter stays green while the shared pool drains.

---

## Weekly, five minutes

```bash
python mcp-seats/read-meters.py                    # where the needle is
python mcp-seats/dispatch-guard.py status          # stale leases?
python mcp-seats/dispatch-guard.py yield <repo>    # cost per ACCEPTED change
```

Watch the **ratio**, not the balance. The subsidy will creep — 13x to 8x to 4x — rather than
cliff, and Composer's warning is the one to remember: *"the bankruptcy is slow and looks like
'the vendor got worse', not 'the architecture failed.'"*

Two numbers decide the architecture:

- **`bonusSpend` ratio below ~3x** → the arbitrage is over. Warm the metered API lane before
  that, not after.
- **Cost per accepted change trending up** → the shop is buying cheap nothing, which is the
  failure the meter cannot see. It is the only number here the vendor will never report for you.
