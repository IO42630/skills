# Skill Benchmark: plexy-robot

**Model**: opencode general subagent (deepseek-flash)
**Date**: 2026-10-07T06:34:51Z
**Evals**: 0 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 83% ± 14% | 42% ± 14% | +0.42 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Voice contract holds: 3/3 with-skill replies start with literal `... ` and contain zero filler words; baseline: 0/3 prefix, 1/3 contained filler.
- Skill compresses but does not enforce the 'ruthless' budget: with-skill replies ran 49/54/98 words (67+/-27) vs baseline 180-236 (203+/-29). Only 1/3 with-skill runs met the eval's aggressive <=50-word bar.
- Accuracy preserved everywhere: all 6 replies tie race conditions to concurrency/shared state and name a lock/mutex fix, so compression did not cost correctness.
- Same shape-vs-volume pattern as plexy-markdown: the skill fixes style features (prefix, filler, voice) but reply length stays model-chosen and variable.
- No timing or token data: this task runtime did not expose duration_ms/total_tokens, so both rows are 0.