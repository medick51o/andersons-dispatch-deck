#!/usr/bin/env python3
"""Round-2 batch F — ceremony, preambles and worked examples that carry no rule.

Judgment applied: two Codex proposals were REFUSED and are recorded at the bottom, because
the passage carried a nuance the compression would have destroyed. A council advises.
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
applied, skipped, moved = [], [], []


def sub(old, new, label, prov=None):
    global s
    n = s.count(old)
    if n != 1:
        skipped.append(f"{label} (matched {n}x)")
        return
    s = s.replace(old, new)
    applied.append(label)
    if prov:
        moved.append(prov)


# --- F1: Part I throat-clearing; the four headings follow immediately ---
sub("""
Everything downstream is these four. Learn them first; the rest is mechanism.
""", "", "F1 Part I preamble")

# --- F2: Doctrine 1 origin story -> provenance ---
sub("""The day this was tuned, the shop took a "why won't my controller work" mess all the way to a
council-reviewed, self-verifying feature. Five gates, in order — the house default for anything gnarly:""",
    "Five gates, in order — the house default for anything gnarly:",
    "F2 Doctrine 1 origin story -> provenance",
    '**The 5-gate pipeline.** Tuned on the day the shop took a "why won\'t my controller work" mess '
    "all the way to a council-reviewed, self-verifying feature.")

# --- F3: loop-cap motivation. The three caps above are unambiguous. ---
sub("""   (Autonomous hours). Then the judge decides. Prevents perfectionist spirals that burn resources
   chasing diminishing returns.""",
    "   (Autonomous hours). Then the judge decides.",
    "F3 loop-cap motivation")

# --- F4: the review-coverage scar -> provenance. The rule above it ("Cut
# builds, cut fan-outs, cut orchestration. Never cut the channel.") is complete. ---
sub("""orchestration. Never cut the channel.** *(A prior draft said "review only the risky diffs to save
money" — that is not a budget setting, it is instructions to stop running the method. The reviewer
caught it; the scar stays.)*""",
    "orchestration. Never cut the channel.**",
    "F4 review-coverage scar -> provenance",
    '**Never cut the channel.** A prior draft said "review only the risky diffs to save money" — that '
    "is not a budget setting, it is instructions to stop running the method. The reviewer caught it.")

# --- F5: "When NOT to convene" restates Gate-0 + Doctrine 5 (Composer + Codex).
# The worked examples are the only distinctive content, so they stay -- compressed. ---
sub("""**When NOT to convene — the guardrail, not the fine print.** A trivial ask — *"rewrite this email,"
"did I send the PO out," a quick fix, a plain question* — is handled by the orchestrator alone (or a
single seat), **NEVER a council.** The orchestrator does not *oops* into a token-eating dream team for
a two-line task. Gate-0 and Doctrine 5 bind absolutely here: no genuine need for N independent
perspectives → no council. Breadth is not rigor; fan-outs cost multiples, not increments. The default
for small work is one seat doing it, quietly.""",
    """**When NOT to convene.** Gate-0 and Doctrine 5 bind absolutely: no genuine need for N independent
perspectives → **no council.** A trivial ask — *"rewrite this email," "did I send the PO out," a quick
fix, a plain question* — is handled by one seat, quietly. The orchestrator does not *oops* into a
token-eating dream team for a two-line task.""",
    "F5 when-not-to-convene compressed")

# --- F6: the notation timeline example. Every glyph in it is defined above. ---
sub("""A run reads as a timeline: 🩺 → 🌈👥👥 → 🟠🔨 → 🧪 → 🔵🔴→⛔ → 🟠🔨 → 🧪 → 🚢 → ⚪🏁 → 🟤.
""", "", "F6 notation timeline example")

# --- F7: closing ownership echo; lines 7-16 already assign SPINE/CREW/SHOW. ---
sub("""*SPINE owns the engine. It names no characters and tells no story — those are CREW's and SHOW's to
add, never to restate. Provenance of the Team Rocket Method (authorship, credits, status) lives in
CREW, because it is that brand's identity, not the brand-neutral engine's.*""",
    """*SPINE owns the engine; the Team Rocket Method's provenance lives in CREW, because it is that
brand's identity, not the brand-neutral engine's.*""",
    "F7 closing ownership echo")

io.open(BASE, "w", encoding="utf-8", newline="").write(s)
for t in TARGETS:
    shutil.copyfile(BASE, t)

if moved:
    with io.open(PROV, "a", encoding="utf-8", newline="") as f:
        for m in moved:
            f.write("\n" + m + "\n")

print("APPLIED:")
for a in applied:
    print("  +", a)
if skipped:
    print("SKIPPED (anchor did not match — left alone rather than guessed):")
    for k in skipped:
        print("  !", k)

print("""
REFUSED (council advised, orchestrator declined — recorded on purpose):
  - Codex CUT 4 'Ambiguity explanation' -> "Send it up."
    The sentence it deletes ("a model that resolves ambiguity has quietly seated itself
    as the requirements author") is the ONLY statement of WHY, and ruling 3 this morning
    turned that reasoning into scoped law. Compressing it would have left the scoped
    exception pointing at nothing.
  - Codex CUT 16 'Adjudication preamble' -> NOTHING.
    "Models agree by default; agreement is the cheapest thing in the room" is the premise
    the whole of Part V rests on, and ruling 4 this morning rewrote a clause to match it.
    It is a load-bearing claim, not throat-clearing.""")
print(f"\nlines {before} -> {s.count(chr(10))}   (net {s.count(chr(10)) - before})")
