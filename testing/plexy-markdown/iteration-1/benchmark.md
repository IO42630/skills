# Skill Benchmark: plexy-markdown

**Model**: opencode general subagent (deepseek-flash)
**Date**: 2026-10-07T06:27:19Z
**Evals**: 0 (3 runs each per configuration)

## Summary

| Metric    | With Skill  | Without Skill | Delta |
|-----------|-------------|---------------|-------|
| Pass Rate | 100% ± 0%   | 25% ± 0%      | +0.75 |
| Time      | 0.0s ± 0.0s | 0.0s ± 0.0s   | +0.0s |
| Tokens    | 0 ± 0       | 0 ± 0         | +0    |

## Notes

- All 4 assertions passed in 3/3 with-skill runs; the baseline passed only content coverage (25%).
- Style variance collapses with the skill: max line length 72+/-10 chars vs 398+/-4 (baseline); long lines 0 vs 11.3+/-1.2; dash-chained bullets 0 vs 10+/-1; bullet ratio 1.0 vs 0.5.
- The skill controls shape, not volume: with-skill docs still ran 250-413 words (+/-83), so document length remains model-chosen.
- All 3 baseline runs were consistently prose-styled (~400-char lines), so the user's 45-word bullet baseline did not reproduce; that sample looks like an outlier rather than a style the skill must fix.
- No timing or token data: this task runtime did not expose duration_ms/total_tokens, so both rows are 0.