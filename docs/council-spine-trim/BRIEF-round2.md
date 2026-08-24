# COUNCIL BRIEF — SPINE v2.5 · SECOND PASS

You are one seat on a multi-vendor council. Other seats are reading the same document
independently and are not told what you say. Do not try to guess their answers.

## What SPINE is

SPINE.md is the method engine for a one-person AI-orchestration shop. It is **loaded into
context on every single summon** of three skills, so every line costs tokens forever. It is
law, not documentation: an orchestrator reads it and is bound by it.

## The job

Find text that can be **deleted or compressed without losing a single rule, condition,
number, or nuance.**

The bar is strict. A passage stays if it is the ONLY place its rule is stated, or if it
carries a condition, an exception, or a number that appears nowhere else. Restatements,
re-explanations, motivational framing, and "as we said above" echoes are fair game.

Look especially for:
- **The same rule stated in three places** because it felt important each time.
- **Explanation of WHY a rule exists**, where the rule itself is already unambiguous.
- **Examples that teach nothing the rule did not already say.**
- **Ceremony** — preambles, transitions, section throat-clearing.
- **Compression** — a paragraph whose whole content is one sentence.

## Second job: contradictions and dead references

This document was just amended (v2.5). Amendments are where contradictions get born.
Report anything where:
- Two passages tell an orchestrator to do **different things** in the same situation.
- A cross-reference points at a section name, part number, or file that **does not exist**
  in this document. (Check the pointer text against the actual headings.)
- A rule was rewritten in one place but its **older phrasing survives** somewhere else.

Contradictions are worth more than line count. Report them even if they cost lines to fix.

## Output format — strict

For every finding:

```
[CUT n]  <short name>   (~N lines)
ANCHOR:  <the first 8-15 words of the passage, copied EXACTLY, character for character>
WHY:     <what makes this safe to remove — name where the surviving statement lives>
REPLACE: <the replacement text, or the word NOTHING if it is a pure deletion>
```

For contradictions:

```
[CONTRA n]  <short name>
WHERE:      <exact quoted phrase from each side>
CONFLICT:   <what an orchestrator would do differently depending on which it read>
FIX:        <your recommendation>
```

End with one line: `TOTAL: ~N lines cuttable, M contradictions`.

**The anchors must be copied exactly from the text.** They are used to find the passage
mechanically. An approximate anchor is a useless finding.

## Hard constraints

- Do not propose reorganizing the document. Cuts and compressions only.
- Do not propose making the language "punchier" at the cost of precision. This is law.
- If you believe a section should stay in full, say so — a defended section is a real finding.
- Do not write any file. Report only.
