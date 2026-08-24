# Self-audit: how much of my own tank is left?

You are running as the operator's Grok Build CLI seat, on his subscription. He wants a REAL number for how
much usage his plan actually gives him, not a marketing adjective. Help him get it.

Investigate and report:

1. **Can you see your own usage/quota from here?** Check every avenue available to you:
   - any local state, config, cache or log under `~/.grok/` that records quota, weekly pool,
     percentage used, rate-limit headers, or reset time
   - whether any CLI subcommand or flag reports usage
   - whether an authenticated endpoint you can reach returns a quota/limits object
   - whether rate-limit headers come back on a normal request
   If you find a number, quote it exactly and say where it came from.

2. **What does `total_cost_usd` in your own JSON output actually mean?** Each of your headless runs
   reports one (today: $0.41 for a 21-turn deep code review, $0.14 for a 12-turn review, $0.23 for an
   11-turn web research task). Is that a real charge against a real balance, a notional
   API-equivalent price, or something else? Does it correspond to the weekly pool percentage that
   grok.com shows in its Usage tab?

3. **Where exactly should the operator look to see his remaining pool?** Name the exact page/tab/URL on
   grok.com or x.com, and describe what it displays (a percentage? a bar? a reset date?). Be
   specific enough that he can find it in two clicks.

4. **Design a burn test he can actually run.** He wants to convert "percentage of weekly pool" into
   "number of deep code reviews per week". Given that he can read his usage percentage before and
   after, and that a deep review costs about $0.41 by your own accounting, lay out the exact steps —
   what to record, what to run, what to record again, and the arithmetic that turns it into a real
   answer.

5. **What plan does this session appear to be on**, from anything you can actually observe? Do not
   guess. If you cannot tell, say so plainly.

Rules: report only what you can verify from real files, real commands, or real responses. Label
anything inferred. If an avenue is closed to you, say which and why. No invented numbers.
