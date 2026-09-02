#!/usr/bin/env python3
"""Round-2 batch C — the contradiction repairs and the dead cross-references.

These are the findings worth more than the line count. Each one is a place where an
orchestrator reading SPINE could have done the wrong thing and been able to cite the
document for it.
"""
import io
import shutil

BASE = r"C:\Users\<you>\.claude\skills\team-rocket-takes-over\SPINE.md"
PROV = r"C:\Sync\Projects\andersons-dispatch-deck\SPINE-PROVENANCE.md"
TARGETS = [
    r"C:\Users\<you>\.claude\skills\trm\SPINE.md",
    r"C:\Users\<you>\.claude\skills\dispatch\SPINE.md",
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


# =====================================================================
# CONTRADICTION REPAIRS
# =====================================================================

# --- C1: "Reviews never stop the line" vs BLOCKER-now vs emergency brake.
# Found INDEPENDENTLY by Composer and Gemini. The two rules were never in
# conflict about REPORTING; they conflicted about who may STOP a lane. Name
# the axis and both survive intact.
sub("""- **Reviews never stop the line.** Builders build to the end of their lane; reviews land at the
  CHECKPOINT (lane/episode end), not mid-swing.""",
    """- **Reviews never stop the line — REPORTING and STOPPING are different acts.** A finding may be
  *filed* the moment it is found; what it may not do is halt a builder mid-swing. Non-blocking
  reviews land at the CHECKPOINT (lane/episode end). **Only two things stop a lane:** a BLOCKER
  (below) and the emergency brake (below) — and each halts the AFFECTED lane only, never the shop.""",
    "C1 review timing axis named (2-seat convergence)")

# --- C2: solo-vendor + autonomous = no legal review path exists.
# Gemini's catch. Part IV requires the review be boss-launched; a sleeping boss
# cannot launch one. The method was quietly demanding the impossible.
sub("""  `SOLO-VENDOR DEGRADED` (only a boss-launched fresh-context seat on the builder's own vendor is
  available) · `REVIEW UNAVAILABLE` (neither reachable). Every launcher runs this preflight, populates
  the cast map only from its result, and prints that status in its receipt.""",
    """  `SOLO-VENDOR DEGRADED` (only a boss-launched fresh-context seat on the builder's own vendor is
  available) · `REVIEW UNAVAILABLE` (neither reachable). Every launcher runs this preflight, populates
  the cast map only from its result, and prints that status in its receipt.
- **Solo vendor while the boss is asleep = `REVIEW UNAVAILABLE`, and say so.** The degraded path
  requires a *boss-launched* seat (Part IV); an orchestrator cannot launch its own reviewer and call
  it independent. So during the autonomous hours a solo-vendor shop has **no** legal review path.
  That is not a licence to self-approve: build, gate, and queue the work UNREVIEWED and labeled,
  for a reviewer the boss launches when he wakes.""",
    "C2 solo-vendor autonomous gap closed")

# --- C3: reachability preflight contradicted the Transport Law on what
# "online" means. Composer's catch: a --version probe would have counted a
# seat that has no live transport.
sub("""- **Fail CLOSED on the unknown.** If the effective identity behind a seat cannot be established, it is""",
    """- **Probe the TRANSPORT, not the binary** (THE TRANSPORT LAW owns this): a seat is online when its
  persistent seat answers in THIS session. A CLI `--version` proves only that the fallback lane
  exists — never enough on its own to count a seat present.
- **Fail CLOSED on the unknown.** If the effective identity behind a seat cannot be established, it is""",
    "C3 preflight probes transport, not binary")

# =====================================================================
# DEAD CROSS-REFERENCES  (pointers to things that do not exist)
# =====================================================================

# --- C4: "Meter-AWARENESS (Part VI)" names no heading anywhere. The rule it
# means is THE METER LAW, a top-level section. Flagged by Composer; verified.
sub("boss must never learn he spent from a footnote. Meter-AWARENESS (Part VI) binds on every seat:",
    "boss must never learn he spent from a footnote. THE METER LAW binds on every seat:",
    "C4 dead ref: Meter-AWARENESS -> THE METER LAW")

# --- C5: "the Anderson deck's shape.md rule" — no shape.md exists anywhere on
# this machine or in any of the three repos. Verified by filesystem search.
# State the rule inline instead of pointing at a file that was never written.
sub("""`episodes/YYYY-MM-DD-<slug>/` at the project root — collecting that run's artifacts: the shape
receipt (see the Anderson deck's shape.md rule), tickets as issued, worker reports/receipts, and""",
    """`episodes/YYYY-MM-DD-<slug>/` at the project root — collecting that run's artifacts: the shape
receipt (what was dispatched to whom, and why that shape), tickets as issued, worker reports, and""",
    "C5 dead ref: shape.md inlined")

# --- C6: the lineage playbook's real filename is MODEL-DISPATCH-GUIDE.md
# (verified present in every project scaffold); SPINE cited it lowercase.
sub("propose concrete routing tweaks to the playbook (`model-dispatch-guide.md`);",
    "propose concrete routing tweaks to the playbook (`MODEL-DISPATCH-GUIDE.md`);",
    "C6 dead ref: playbook filename casing")

# =====================================================================
# THE AMENDMENT SCAR -> provenance (both seats; ~13 lines, one real law)
# =====================================================================
SCAR = """**The amendment scar (kept, because a methodology that hides its own audit is not one).** A
four-seat evaluation fleet was told to break this protocol. The hole it found: every rule fixed
*who* reviews and none fixed *what the reviewer is handed* — a builder could pass a curated diff to
a genuinely independent reviewer, collect an honest "no findings," and hand the human a report that
reads exactly like rigor. **Proving a second model was in the room says nothing about what you gave
it.** Mechanisms 5 and 6 above are the fix, and the FIRST DRAFT of both was marked NOT DISCHARGED by
the reviewer: draft-5 derived write set and manifest from the same ticket (moved the curation hole,
didn't close it → hence three lists, one enumerated from the repo, with hashes); draft-6 would have
silently killed every real finding that can't be automated (→ hence "untestability is never
evidence"). **Both drafts read as rigorous; both were worse than the disease.** The general lesson
that governs all future amendments: *an invariant that leaves an artifact survives; one that exists
only as a habit dies at the first context compaction or deadline.* **When choosing between two ways
to write a rule, choose the one that leaves a trace.**"""

sub(SCAR,
    """**THE AMENDMENT LAW** (the scar that produced it is in SPINE-PROVENANCE.md). *An invariant that
leaves an artifact survives; one that exists only as a habit dies at the first context compaction or
deadline.* **When choosing between two ways to write a rule, choose the one that leaves a trace.**""",
    "C7 amendment scar -> provenance")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

# append the scar to provenance, verbatim
if "C7 amendment scar -> provenance" in applied:
    with io.open(PROV, "a", encoding="utf-8", newline="") as f:
        f.write("\n**The amendment scar** — kept, because a methodology that hides its own audit is\n"
                "not one. This is the origin of THE AMENDMENT LAW in Part V.\n\n")
        f.write(SCAR.replace("**The amendment scar (kept, because a methodology that hides its own "
                             "audit is not one).** A", "A"))
        f.write("\n")

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")
