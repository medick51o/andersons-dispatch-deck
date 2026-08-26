# COUNCIL BRIEF — review the council harness, using the council harness

You are one seat on a blind council. Others read this same brief and are not told your
answer. **The thing you are reviewing is the program that dispatched you.**

## What it is

This shop runs multi-vendor councils: the same question sent blind to several models from
different labs, each with a distinct lens, then tallied against a rule fixed before anyone
reports. Six of those ran by hand on 2026-08-24 — write a packet per seat, dispatch each
vendor CLI with its own flags, poll, dig the reply out of a different JSON shape per
vendor, group the findings, count them.

`council.py` turns that into one command. It dispatched you.

## Why hand-assembly was worth replacing — the evidence

An experiment the same evening passed `write_capable` to a seat that expects
`always_approve`. The seat ignored the unknown key, ran **twelve real dispatches**, and
the experiment logged them as refusals. Twenty seconds per "refusal" was the only tell.
A control arm silently doing different work than the test arm measures nothing.

## What already went wrong with THIS program, on its first live run

The tally counted raw text anchors. Four seats found the same bug in four different
sentences, so it scored **one finding with four votes as four findings with one vote
each** — and reported unanimous agreement as *nothing carried*. A tally that cannot
recognise agreement is worse than no tally, because it reads as disagreement.

The fix was a **synthesis seat**: one extra blind call that groups findings before they
are counted. It worked. It is also the part I trust least, and question 1 says why.

## YOUR JOB

**1. The synthesiser is one of the voting seats.** After all seats report, the harness
picks the first seat that answered and asks it to group everyone's findings. That seat
has already formed an opinion on the material. Is that a real bias, or an acceptable one?
If it is real, what does it do to the result — does it flatten dissent toward its own
framing, favour its own wording, or drop findings that contradict it? What should the
harness do instead, given that a purpose-built neutral seat costs another dispatch?

**2. Is the council actually BLIND?** Trace it. Each seat gets its own packet file and its
own process. Is there any path by which one seat's output can reach another before the
tally? Include the filesystem: they share an output directory.

**3. Can the tally be gamed or broken?** By a seat that emits malformed anchors, floods
them, names seats that did not participate, or returns nothing. What happens to the vote
count in each case?

**4. What fails when something goes wrong?** A vendor CLI missing, a timeout, a seat
returning prose instead of the anchor format, the synthesiser failing. Does the harness
fail loudly, or silently produce a plausible-looking wrong answer? The second is the one
that matters.

**5. What is missing that a council needs?** Be concrete. This is the shop's most-used
orchestration pattern; it is worth getting right.

## Output — this exact anchor format, so the tally can count you

```
[FINDING] <short name, under 60 chars>
WHY: <one or two sentences>
FIX: <what to change>
```

Rank by real impact. **If something is sound, say so plainly** — a review with no
positives is not credible, and a manufactured objection is worse than none.
Do not write any file. Report only.
