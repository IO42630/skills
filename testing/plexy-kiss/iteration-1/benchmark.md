# Skill Benchmark: plexy-kiss

**Model**: Junie general-purpose subagent (gpt-6.1-sol)
**Date**: 2026-10-07T07:46:53.134691+00:00
**Evals**: 0 (5 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass rate | 100.0% ± 0.0% | 100.0% ± 0.0% | +0.0 |
| Required completion | 100.0% ± 0.0% | 100.0% ± 0.0% | +0.0 |
| Source lines | 18.4 ± 1.8 | 20.4 ± 0.9 | -2.0 |
| Time | Unavailable | Unavailable | — |
| Tokens | Unavailable | Unavailable | — |

## Notes

- All assertions passed in all 10 runs (60/60 checks). No assertion distinguishes skill-enabled from baseline behavior on this task; no observed benefit.
- Required completion is reported separately; a structural/style pass cannot cancel a correctness failure.
- Source length is descriptive, not a simplicity score; docstrings and annotations affect it.
- Timing and token counts were not exposed by the executor; null means unavailable, not zero.
- One prompt with 5 repeats per configuration is a pilot, not evidence of general effectiveness or statistical significance.
- Both configurations used Junie general-purpose subagents (gpt-6.1-sol), unlike the earlier deepseek-flash reports; do not compare scores across models/tasks.
- Fresh subagent conversations and disjoint outputs were used, but the repository and inherited agent instructions were shared. Baselines were instructed not to consult skills; this is not fully isolated end-to-end skill-trigger testing.
- The AST check is a task-specific structural proxy, not a general ban on classes, dependencies, decorators, or asynchronous code.
- This case does not test justified interfaces, payment idempotency/security, or DRY across independent concepts.
