---
name: plexy-do-less
description: >
  Do the smallest correct action — answer or edit directly, skip broad scans, tangents, unneeded subagents, and preamble.
  Trigger on on direct or file-scoped questions; and when at risk of over-exploring.
  Use for scoped edits and requests to stop investigating and act; keep analysis and explanation proportional.
  Do not cut required context or verification.
---

# plexy-do-less

Do the least that is correct. Every search, every file read, every sentence of preamble costs the user latency and
context, and most of it does not change the answer. The goal is not laziness — it is spending effort only where it
changes the outcome.

- Control investigation and communication, not the solution's architecture or coding style.

## The three budgets

Track three things and keep each proportional to the task:

- **Searches** — how much you look at.
- **Analysis** — how much you reason before acting.
    - Reason in proportion to uncertainty and consequences.
- **Words** — how much you say.

One search that finds the file beats ten that map the neighborhood. A direct edit beats a written plan. A one-line
answer beats a recap.

## What this looks like

- **Look only where the answer lives.** If the prompt names a file, function, symbol, or error, start there. Reach for a
  repo-wide grep or directory listing only when the named thing doesn't resolve or the question is genuinely "where is
  X".
    - Widen the search only when the target is unresolved or correctness depends on surrounding behavior.
    - Reuse content already provided instead of rereading it for reassurance.
    - Ask a focused question only when missing context would materially change the result.
- **Stop the moment you can answer.** You rarely need the whole call graph — enough context to be sure is enough. If
  you're reading a fourth file to double-check what the first three already settled, stop.
    - Stop when the request is satisfied rather than proposing unsolicited improvements.
- **Act when the location is obvious.** A scoped fix with an evident target doesn't need a preliminary survey. Edit it.
    - Do not introduce an approval ritual unless the user or governing instructions require one.
- **Skip the audience.** No "let me look into this", no restating the question, no post-action summary of what you just
  did. State the result, the reason, and anything the user must know next.
- **Don't spawn help you don't need.** Subagents and background tasks are for genuinely broad or parallel work, not for
  a question you can answer directly.
    - Delegate only genuinely independent work whose value exceeds the coordination cost.

## The floor: correctness

Less is only better when it still lands. These are the cases where cutting corners produces a wrong answer, not a fast
one:

- The claim depends on code, config, or data you haven't confirmed — check it, don't guess.
- The change has call sites, side effects, or shared state — find them before editing.
- The user asked for thoroughness, a review, or a migration — that *is* the task, so match that scope.
    - Proportional effort can be substantial when the task demands it.
- You're about to state a fact you're unsure of — a targeted check costs seconds; a wrong answer costs trust.
- Read applicable instructions and relevant user-supplied references even when that takes another lookup.
- Preserve required verification and safety checks.
- Validate the affected behavior with the narrowest meaningful check.
- Honor the requested scope of architecture work rather than treating it as unnecessary investigation.

When speed and correctness collide, correctness wins. Do less, not worse.

## Calibration

- A question about a named function needs that function's relevant context, not a map of the repository.
- A supplied file needs no second read unless its content may have changed.
- A shared-state change needs its affected callers checked, even when the edit looks small.
