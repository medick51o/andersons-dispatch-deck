#!/usr/bin/env python3
"""calibrate-pool — size an unpublished usage pool by burning a known amount.

    python calibrate-pool.py --probe        # 1 call, check the meter's precision first
    python calibrate-pool.py --calls 6      # the real burn

The vendor publishes only a percentage. So: read the needle, push a KNOWN number of
tokens through, read the needle again. pool = tokens_spent / fraction_moved.

This spends real allowance on purpose. It runs the CHEAPEST included model (composer-2.5,
non-fast) so the measurement costs as little as possible, and it prints exactly what it
burned so the receipt is honest.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import time
import urllib.request

USAGE_URL = "https://api2.cursor.sh/aiserver.v1.DashboardService/GetCurrentPeriodUsage"
MODEL = "composer-2.5"          # cheapest measured row: 0.077% of pool per Mtok


def meter():
    """Raw, full-precision read. Returns (auto%, api%, totalSpend_cents)."""
    tok = json.load(io.open(os.path.expandvars(r"%APPDATA%\Cursor\auth.json"),
                            encoding="utf-8"))["accessToken"]
    req = urllib.request.Request(
        USAGE_URL, data=b"{}",
        headers={"Authorization": "Bearer " + tok,
                 "Content-Type": "application/json",
                 "Connect-Protocol-Version": "1"})
    d = json.load(urllib.request.urlopen(req, timeout=45))
    pu = d.get("planUsage", {}) or {}
    return (pu.get("autoPercentUsed") or 0.0,
            pu.get("apiPercentUsed") or 0.0,
            pu.get("totalSpend") or 0)


def find_cli():
    local = os.environ.get("LOCALAPPDATA", "")
    home = os.path.expanduser("~")
    for c in (os.path.join(local, "cursor-agent", "cursor-agent.cmd"),
              os.path.join(home, ".local", "bin", "cursor-agent"),
              os.path.join(home, ".cursor", "bin", "cursor-agent")):
        if os.path.exists(c):
            return c
    raise SystemExit("cursor-agent not found")


PLAYPEN = os.path.abspath(os.environ.get("WMW_CURSOR_PLAYPEN", r"C:\Sync\_playpen\cursor"))


def burn_once(cli, payload, n):
    """One call carrying real input volume.

    The payload cannot ride on argv — Windows caps the command line and a 68KB
    prompt trips WinError 206, the same trap the MCP wrapper spills to a file to
    avoid. So the text goes to a file and the model is told to read it; the read
    is what puts the tokens through. Each run gets a unique nonce so cache-reads
    do not silently make later calls cheaper than the first.
    """
    os.makedirs(PLAYPEN, exist_ok=True)
    f = os.path.join(PLAYPEN, f"burn-{n}-{n*7919}.txt")
    io.open(f, "w", encoding="utf-8", newline="").write(
        f"NONCE {n*7919}\n\n{payload}")
    prompt = (f"Read the file {f} in full. Then reply with only the word OK "
              f"and the nonce at its top. Do not summarize or analyze it.")
    p = subprocess.run([cli, "--model", MODEL, "--mode", "ask", "--trust",
                        "-p", prompt, "--output-format", "json"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=600)
    try:
        d = json.loads((p.stdout or "").strip())
    except Exception:
        return None
    u = d.get("usage") or {}
    return {k: u.get(k, 0) for k in
            ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calls", type=int, default=6)
    ap.add_argument("--probe", action="store_true", help="single call, precision check")
    a = ap.parse_args()
    calls = 1 if a.probe else a.calls

    cli = find_cli()
    # a big unique-ish payload so each call carries real input volume
    src = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "SPINE.md"), encoding="utf-8").read()

    a0, p0, s0 = meter()
    print(f"BEFORE   cursor-models {a0:.9f}%   other {p0:.9f}%   spend {s0}c")

    tot = {"inputTokens": 0, "outputTokens": 0,
           "cacheReadTokens": 0, "cacheWriteTokens": 0}
    for i in range(calls):
        u = burn_once(cli, src, i)
        if not u:
            print(f"  call {i+1}: FAILED (not counted)")
            continue
        for k in tot:
            tot[k] += u[k]
        print(f"  call {i+1}: in={u['inputTokens']:,} out={u['outputTokens']:,} "
              f"cacheR={u['cacheReadTokens']:,}")

    time.sleep(20)   # let the meter settle
    a1, p1, s1 = meter()
    print(f"AFTER    cursor-models {a1:.9f}%   other {p1:.9f}%   spend {s1}c")

    billable = tot["inputTokens"] + tot["outputTokens"] + tot["cacheReadTokens"]
    d_pct = a1 - a0
    d_spend = s1 - s0
    print(f"\nBURNED   {billable:,} tokens "
          f"(in {tot['inputTokens']:,} / out {tot['outputTokens']:,} / "
          f"cacheR {tot['cacheReadTokens']:,})")
    print(f"NEEDLE   moved {d_pct:.9f} percentage points; spend +{d_spend}c")

    if d_pct <= 0:
        print("\nNeedle did not move — burn more (raise --calls) or the meter lags.")
        return 1
    pool_tok = billable / (d_pct / 100.0)
    print(f"\n  POOL SIZE  ~{pool_tok/1e6:,.0f}M tokens/month  "
          f"(at composer-2.5 rates)")
    if d_spend > 0:
        print(f"  POOL VALUE ~${d_spend/100.0/(d_pct/100.0):,.0f}/month")
    print(f"  this burn cost {d_pct:.4f}% of the month's allowance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
