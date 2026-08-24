#!/usr/bin/env python3
"""Round-2 batch D — the flaws Codex found in the v2.5 law written hours earlier.

Four of these are self-inflicted: the consent rewrite gated SPENDING, but three other
sections were still written against the OLD vendor-class test, and one clause of the new
law contradicted another clause of the same law. This is the builder-never-approves-own-work
rule paying for itself; the seat that caught them did not write them.
"""
import io
import shutil

BASE = r"C:\Users\andre\.claude\skills\team-rocket-takes-over\SPINE.md"
TARGETS = [
    r"C:\Users\andre\.claude\skills\trm\SPINE.md",
    r"C:\Users\andre\.claude\skills\dispatch\SPINE.md",
    r"C:\Sync\Projects\andersons-dispatch-deck\SPINE.md",
    r"C:\Sync\Projects\team-rocket-method-public\SPINE.md",
    r"C:\Sync\Projects\team-rocket-takes-over\SPINE.md",
]

s = io.open(BASE, encoding="utf-8").read()
before = s.count("\n")
applied, skipped = [], []


def sub(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        skipped.append(f"{label} (matched {n}x)")
        return
    s = s.replace(old, new)
    applied.append(label)


# --- D1: the new law contradicted itself. Clause 1 said a free seat needs no
# permission; clause 6 said convening consent is separate. An orchestrator could
# have read clause 1 as licence to convene a free council unasked -- exactly the
# self-authorized panel ruling 1 repealed this morning.
sub("1. **A seat that cannot spend needs no permission.** Free is free; convene it.",
    "1. **A seat that cannot spend needs no ALLOWANCE.** Free is free — but free is not consent to\n"
    "   convene: Gate-0's right-size rule still binds (clause 6).",
    "D1 free seat needs no allowance != needs no consent")

# --- D2: unknown cost cannot be waved through by an allowance. The Meter Law
# says unknown fails closed; the new law said "or an allowance covers it".
sub("   unmeasured (THE METER LAW). It may not sit until it can be read or an allowance covers it.",
    "   unmeasured (THE METER LAW). It may not sit until its spend can be READ. An allowance never\n"
    "   substitutes for a meter — a bound you cannot verify against is not a bound.",
    "D2 unknown cost cannot be waved through by allowance")

# --- D3: the council procedure dispatched to every REACHABLE vendor, which
# bypasses the eligibility gate the seat law just established.
sub("2. **Convene + assign lenses.** Dispatch to every reachable vendor, each handed a DISTINCT angle",
    "2. **Convene + assign lenses.** Dispatch to every reachable AND ELIGIBLE vendor (THE COUNCIL SEAT\n"
    "   LAW), each handed a DISTINCT angle",
    "D3 convene eligible, not merely reachable")

# --- D4: meter marks were keyed to vendor CLASS (reserve vs house) while the
# law now keys to SPENDING. A house seat with an API key attached would spend
# silently.
sub("""- **METER MARKS ARE MANDATORY ON RESERVE LINES (v4.1)** and absent everywhere else. Flat-rate house
  seats narrate no meter; a reserve seat narrates one on every line, computed from the model id,""",
    """- **METER MARKS ARE MANDATORY ON ANY LINE THAT CAN SPEND** (v4.1, rekeyed v2.5 from vendor class to
  spending, to match THE COUNCIL SEAT LAW). A genuinely flat-rate seat narrates no meter; **any seat
  that can bill — reserve or house — narrates one on every line**, computed from the model id,""",
    "D4 meter marks keyed to spending, not vendor class")

# --- D5: dead pointer -- no "Doctrine on review culture" exists.
sub("   it takes (bounded by the loop cap, Doctrine on review culture below).",
    "   it takes (bounded by Principle 8's loop cap and Part VII's review-culture caps).",
    "D5 dead ref: Doctrine on review culture")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")
