# COUNCIL BRIEF — trim SPINE without losing a single load-bearing idea

You are ONE seat on a five-vendor council. You are blind to the other seats. Review on the merits.

## The file

`SPINE.md` in this repository — **920 lines, ~70,000 characters.** It is the method engine for a
multi-model AI dev shop. Every tier that inherits it (three of them) loads the WHOLE FILE on every
single invocation. So every wasted line costs tokens forever, on every summon, for every user.

It has grown by accretion: v1.0 through v2.4, each adding law without anyone going back to compress.

## The exact job

**Make it leaner without losing information.** That constraint is strict and it is the whole point:

- **DO** find text saying the same thing twice in different words, anywhere in the file.
- **DO** find verbose passages that could say the identical thing in half the words.
- **DO** find worked examples, restatements or asides that carry no rule a reader could not infer.
- **DO** find laws stated in one section and re-stated in another (the file's own Principle 9 says
  one owner per fact — check whether it obeys itself).
- **DO** find scaffolding that has outlived its purpose: superseded notes, changelog entries that no
  longer teach anything, transitional wording from a version nobody runs.

- **DO NOT** propose removing a law, a guardrail, a named test, or a distinction that changes
  behaviour. If a passage is long *because the idea is subtle*, leave it long and say so.
- **DO NOT** propose "tighten the prose" as a finding without showing the replacement text.
- **DO NOT** trade clarity for brevity. A rule that gets misread is worse than a rule that is wordy.

## What a good finding looks like

> **Lines 412–431 and 688–701 both define the review-independence test.** The second is a restatement
> with no added condition. Cut the second, replace with a one-line pointer to the first.
> **Saves ~18 lines. Loses nothing.**

Every finding needs: the location, what is redundant or bloated, the **replacement text or pointer**,
the **lines saved**, and an explicit statement of **what is lost** (ideally "nothing").

## Deliverable

1. Findings ordered by **lines saved, largest first**.
2. A total: how many lines you believe can be cut, and what percentage of the file that is.
3. A short **"do not touch" list** — passages that look verbose but are load-bearing, so the next
   person to try this does not cut them by mistake.
4. Sign with your model name.

Be honest if the answer is "this file is already tight." Padding a report with weak trims to look
useful is the failure mode here.

## YOUR LENS — ⚫ Grok: the adversary. Hunt the passages nobody would miss. Which sections are ceremony rather than law? Which rules are unenforceable as written (no test, no artifact, no consequence) and therefore cost tokens without changing behaviour? Be willing to say a beloved section is decoration. Read SPINE.md from the repo root.
