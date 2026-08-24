#!/usr/bin/env python3
"""bench-burn — read the Cursor bench spend ledger and say what it cost.

    python bench-burn.py              # this month
    python bench-burn.py --all        # everything
    python bench-burn.py --days 7     # last 7 days

Tokens are NOT dollars. Cursor's usage dashboard is the ground truth; this is the
honest cross-check against it — run both, compare, and you learn your real rate
instead of projecting one.
"""
import datetime
import io
import json
import os
import sys
from collections import defaultdict

LEDGER = os.environ.get(
    "WMW_CURSOR_LEDGER",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bench-spend.jsonl"))

def load(since=None):
    if not os.path.exists(LEDGER):
        return []
    rows = []
    for line in io.open(LEDGER, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since and r.get("ts", "") < since:
            continue
        rows.append(r)
    return rows

def main():
    args = sys.argv[1:]
    now = datetime.datetime.now()
    if "--all" in args:
        since, label = None, "all time"
    elif "--days" in args:
        n = int(args[args.index("--days") + 1])
        since = (now - datetime.timedelta(days=n)).isoformat(timespec="seconds")
        label = f"last {n} days"
    else:
        since = now.replace(day=1, hour=0, minute=0, second=0).isoformat(timespec="seconds")
        label = f"{now:%B %Y} so far"

    rows = load(since)
    if not rows:
        print(f"No bench calls recorded ({label}). Ledger: {LEDGER}")
        return

    billable = [r for r in rows if r.get("billable")]
    free = [r for r in rows if not r.get("billable")]
    surcharged = [r for r in rows if r.get("surcharged")]

    def toks(rs, k):
        return sum(r.get(k) or 0 for r in rs)

    print(f"CURSOR BENCH BURN — {label}")
    print(f"  ledger: {LEDGER}\n")
    print(f"  free calls (included pool):  {len(free):4}   "
          f"{toks(free,'in'):>9,} in / {toks(free,'out'):>7,} out")
    print(f"  BILLABLE calls (credits):    {len(billable):4}   "
          f"{toks(billable,'in'):>9,} in / {toks(billable,'out'):>7,} out")
    if surcharged:
        print(f"  ...of which FAST-surcharged: {len(surcharged):4}   "
              f"(2-6x rate — check these were deliberate)")

    if billable:
        print("\n  BILLABLE breakdown by model:")
        by = defaultdict(lambda: [0, 0, 0])
        for r in billable:
            e = by[(r.get("model"), r.get("lineage"))]
            e[0] += 1
            e[1] += r.get("in") or 0
            e[2] += r.get("out") or 0
        for (model, lin), (n, i, o) in sorted(by.items(), key=lambda kv: -kv[1][2]):
            print(f"    {model:32} {lin:10} {n:3} calls  {i:>9,} in / {o:>7,} out")
        print("\n  Compare these against cursor.com's usage dashboard for real dollars.")
    else:
        print("\n  No credits spent. Everything ran on the included pool.")

    writes = [r for r in rows if r.get("write_capable")]
    if writes:
        print(f"\n  write-capable calls: {len(writes)} (these ran with --yolo)")

if __name__ == "__main__":
    main()
