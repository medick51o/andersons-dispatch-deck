#!/usr/bin/env python3
"""read-meters — what is actually left in the tanks.

    python read-meters.py            # both vendors
    python read-meters.py --grok     # xAI weekly pool only
    python read-meters.py --cursor   # Cursor's two pools only
    python read-meters.py --json     # machine-readable, for before/after diffs

WHY THIS EXISTS. Neither vendor publishes the SIZE of an included pool, and
neither one's API will tell you: both return only a PERCENTAGE USED, never an
absolute cap. That is architectural, not an oversight — you cannot learn a pool's
size by inspecting traffic. The only way to size one is to burn a known amount of
work and watch the percentage move. This tool reads the percentage so that
measurement is possible; `bench-burn.py` reports what a burn cost.

Endpoints (found 2026-08-23; both undocumented, both may change without notice):
  xAI     GET  https://cli-chat-proxy.grok.com/v1/billing?format=credits
          auth: the OIDC bearer token inside ~/.grok/auth.json
          gives: weekly pool percent, itemised by product (Build / Chat / Imagine)
  Cursor  POST https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage
          auth: accessToken from %APPDATA%\\Cursor\\auth.json, Connect-RPC headers
          gives: autoPercentUsed  = the INCLUDED "Cursor Models" pool
                 apiPercentUsed   = the metered "Other Models" credit pool
                 bonusSpend       = free usage granted on top of what you paid for

Read-only. Nothing here spends anything or changes any account.
"""
import datetime
import io
import json
import os
import sys
import urllib.request

TIMEOUT = 45

def _get(url, headers, data=None):
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)

def _find_jwt(o):
    """Walk an arbitrary structure for the first JWT-shaped string."""
    if isinstance(o, dict):
        for v in o.values():
            if isinstance(v, str) and v.count(".") == 2 and len(v) > 100:
                return v
            found = _find_jwt(v)
            if found:
                return found
    elif isinstance(o, list):
        for v in o:
            found = _find_jwt(v)
            if found:
                return found
    return None

def read_grok():
    path = os.path.expanduser(r"~\.grok\auth.json")
    if not os.path.exists(path):
        return {"error": "no ~/.grok/auth.json — is the Grok CLI logged in?"}
    tok = _find_jwt(json.load(io.open(path, encoding="utf-8")))
    if not tok:
        return {"error": "no bearer token found in ~/.grok/auth.json"}
    try:
        d = _get("https://cli-chat-proxy.grok.com/v1/billing?format=credits",
                 {"Authorization": "Bearer " + tok, "User-Agent": "grok-cli"})
    except Exception as e:
        return {"error": f"grok billing request failed: {e}"}
    c = d.get("config", d)
    return {
        "weekly_percent_used": c.get("creditUsagePercent"),
        "by_product": {p.get("product"): p.get("usagePercent")
                       for p in c.get("productUsage", [])},
        "period_start": str(c.get("billingPeriodStart"))[:19],
        "period_end": str(c.get("billingPeriodEnd"))[:19],
        "prepaid_balance": (c.get("prepaidBalance") or {}).get("val"),
        "on_demand_cap": (c.get("onDemandCap") or {}).get("val"),
    }

def read_cursor():
    path = os.path.expandvars(r"%APPDATA%\Cursor\auth.json")
    if not os.path.exists(path):
        return {"error": "no %APPDATA%/Cursor/auth.json — sign in to the Cursor app once"}
    tok = json.load(io.open(path, encoding="utf-8")).get("accessToken")
    if not tok:
        return {"error": "no accessToken in Cursor auth.json"}
    try:
        d = _get("https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage",
                 {"Authorization": "Bearer " + tok,
                  "Content-Type": "application/json",
                  "Connect-Protocol-Version": "1"},
                 data=b"{}")
    except Exception as e:
        return {"error": f"cursor usage request failed: {e}"}
    pu = d.get("planUsage", {}) or {}
    def ms(v):
        try:
            return datetime.datetime.fromtimestamp(int(v) / 1000).strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            return str(v)
    return {
        "cursor_models_percent_used": pu.get("autoPercentUsed"),   # the INCLUDED pool
        "other_models_percent_used": pu.get("apiPercentUsed"),     # the metered pool
        "total_percent_used": pu.get("totalPercentUsed"),
        "included_spend_usd": (pu.get("includedSpend") or 0) / 100,
        "bonus_spend_usd": (pu.get("bonusSpend") or 0) / 100,
        "total_spend_usd": (pu.get("totalSpend") or 0) / 100,
        "cycle_start": ms(d.get("billingCycleStart")),
        "cycle_end": ms(d.get("billingCycleEnd")),
        "display_message": d.get("displayMessage"),
    }

def main():
    args = sys.argv[1:]
    want_grok = "--cursor" not in args
    want_cursor = "--grok" not in args
    out = {"read_at": datetime.datetime.now().isoformat(timespec="seconds")}
    if want_grok:
        out["grok"] = read_grok()
    if want_cursor:
        out["cursor"] = read_cursor()

    if "--json" in args:
        print(json.dumps(out, indent=2))
        return

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(f"METERS — {out['read_at']}\n")
    g = out.get("grok")
    if g:
        if g.get("error"):
            print(f"  xAI / Grok    : {g['error']}")
        else:
            print(f"  xAI / Grok    weekly pool {g['weekly_percent_used']}% used"
                  f"   (resets {g['period_end'][:10]})")
            for prod, pct in (g.get("by_product") or {}).items():
                print(f"                    {prod:14} {pct}%")
            print("                    ONE tank: Build, Chat and Imagine all drain it")
    c = out.get("cursor")
    if c:
        print()
        if c.get("error"):
            print(f"  Cursor        : {c['error']}")
        else:
            print(f"  Cursor        cycle {c['cycle_start']} -> {c['cycle_end']}")
            print(f"                    Cursor Models (free)  {c['cursor_models_percent_used']}%"
                  f"   <- Composer + Cursor Grok")
            print(f"                    Other Models (credit) {c['other_models_percent_used']}%"
                  f"   <- everything else")
            print(f"                    spend: ${c['total_spend_usd']:.2f} total = "
                  f"${c['included_spend_usd']:.2f} paid + ${c['bonus_spend_usd']:.2f} bonus")
            if c.get("display_message"):
                print(f"                    vendor says: {c['display_message']}")
    print("\n  Neither vendor publishes a pool SIZE — only a percentage. To learn the size,")
    print("  burn a known amount and watch the percentage move (see bench-burn.py).")

if __name__ == "__main__":
    main()
