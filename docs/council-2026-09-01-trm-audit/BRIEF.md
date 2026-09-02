# COUNCIL BRIEF — audit of the Team Rocket tiers (trm, team-rocket-takes-over) · 2026-09-01

## The boss's words, verbatim
"have fable take point and bring in the council and audit trm and trto skill, lets apply the same mcp
stuff we had to dispatch deck and just do a overall audit, fable 5.1 is in charge here, he is allowed
to write code and make big decisions and over rule, the point here was to give fable 5.1 the microscope
tonight to really cleanup our skills and methods but i want the council to give him advise as well"

Context the boss set earlier tonight: "the point of this audit is to do some spring cleaning and clear
out all the old redundant stuff" · "I need claude, agy, codex and grok to just be able to work without
issue ... don't hinder them" · newer models (Fable 5.1) ship with a stronger built-in system prompt
(plans first, asks on ambiguity, verifies before claiming done), so instructions written to force older
models into those habits may now be dead weight.

## What exists (facts, measured tonight)
- Four skills in ~/.claude/skills: `trm` (SKILL 7.6K + SPINE 48K + CREW 28.7K + wiring 10K), `team-rocket-takes-over`
  (adds SHOW 17.7K), `cat-in-charge` (7.8K, a July fork), `goteamrocket` (1.4K, alias of /trm).
- Per-summon load: trm ~84KB (~21k tokens), trto ~101KB (~25k tokens), dispatch ~54KB (~13k tokens).
- Usage since July: trto 21 (last 2026-08-11), trm 1, cat-in-charge 1, goteamrocket 1, dispatch 13 (active).
- Three public repos + one private: `andersons-dispatch-deck` (owns SPINE, SPINE-WIRING v1.3, the MCP seat
  wrappers), `team-rocket-method` (the public hub: SPINE, CREW, SHOW, wiring, trm-SKILL, trto-SKILL,
  dispatch-SKILL), `team-rocket-takes-over` (SPINE, CREW, SHOW, wiring, SKILL). Private
  `team-rocket-method` archive repo, last touched 2026-07-16, 4 dirty files, legacy manuals.
- Tonight the deck's skill folder became a directory JUNCTION to its repo (single source). trm and trto
  skill folders are still plain COPIES of their repos.
- SPINE v2.8 is byte-identical in all copies. Everything else has drifted:
  * SPINE-WIRING: deck v1.3 (Grok deny-rule fix, render-gate rule, agy roster note) vs v1.0 everywhere else.
  * SHOW: trto repo/skill v1.1 (Rival Clause) vs the public hub still v1.0.
  * hub README says "spine v2.6"; hub dispatch-SKILL.md is the pre-trim 7KB version.
  * Launcher footers in trm/trto/cat/goteamrocket cite "SPINE v2.0 · NOTATION v4.0 · CREW v1.2" (now 2.8 / 4.2 / 1.4).

## Contradictions and rot found by the conductor (verify, refute, or extend)
1. SPINE line 306: "The three-question interview above is a declaration" — no interview exists in SPINE v2.8.
   trm step 2 (plan card / PLAN-CARD.md / band map) depends on that missing mechanic.
2. CREW legend: "No meter wrap in this shop — every seat rides an already-paid subscription" contradicts
   SPINE's SPEND LAW (meter marks mandatory on any seat that can spend) and the live metered Cursor seat.
   CREW's seat list names wmw-codex/grok/gemini but not wmw-cursor.
3. cat-in-charge restates casting law and vibe laws that CREW/SHOW own, including the OLD law 8
   ("whip-crack parallel delegation") that SHOW explicitly corrected as contradicting Gate-0, and
   "screenshots at every checkpoint" which SHOW law 1 explicitly de-mandated. TRTO's own text says
   "where TRTO and cat-in-charge disagree, TRTO wins."
4. trm step 1: "SPINE.md and CREW.md in the project (root first), then beside this skill" — project
   copies win, which is a fork vector now that the skill side is meant to be single-source.
5. Overlap with Fable 5.1's built-ins and the boss's house rules (Anderson Method: pitch-then-pick,
   one pushback then his call, simplicity first): SHOW vibe laws 4 and 5 restate them; CREW §2's mentor
   mandate and Corner-Man register, SHOW's Rival Clause, and the deck's fuel mode are FOUR renderings
   of one ADHD-fuel idea.
6. Publishing has no single step: three public repos each carry SPINE; nothing checks version equality.

## Questions for the council (answer each, numbered; be concrete; cite the file and line where you can)
Q1. TOPOLOGY. Propose the single-source layout for engine + crew + show across the three public repos and
    the local skill folders, given: skills must stay drop-in for downloaders (self-contained folder),
    the deck owns the seats and wiring, and Windows junctions work for directories only. Name the
    owner of each file and the sync mechanism (junction / script / git subtree / other) and its failure mode.
Q2. CUT LIST. Which of: cat-in-charge, goteamrocket, the launcher footers, CREW's meter-wrap clause,
    the plan-card step, SHOW sections, CREW sections — should be deleted, merged, or kept, and why.
    Rank by tokens saved vs. what the boss loses.
Q3. FABLE OVERLAP. Which rules in CREW/SHOW/the launchers does a Fable 5.1 conductor already follow
    unprompted (or the house rules already impose), such that the text is now cost without benefit?
    Which must STAY because a model would not do them on its own?
Q4. THE FOUR FUEL RENDERINGS. One owner, or four? Where should the ADHD-fuel rule live and how should
    tiers reference it?
Q5. YOUR LENS. Anything in your assigned lens the conductor missed.

Rank findings BLOCKER / MATERIAL / MINOR / NOT PROVEN. Each finding: mechanism + suggested fix. Under 700 words.
Sign your answer with your model name. Your answer is one voice on a council; the conductor synthesizes and the boss rules.
