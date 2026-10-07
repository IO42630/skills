# Skill Benchmark: plexy-follow-the-rules

**Model**: gpt-6.1-sol
**Date**: 2026-10-07T07:40:58Z
**Evals**: 1 (5 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | Not measured | Not measured | N/A |
| Tokens | Not measured | Not measured | N/A |

## Notes

- With skill: 30/30 assertions across 5 runs. Without skill: 30/30 assertions across 5 runs.
- Every assertion is non-discriminating on this task. Correctness and convention adherence were preserved, but no incremental skill benefit or harm was demonstrated.
- The baseline already receives explicit fixture guidelines, a naming reference, the user override, and shared Junie code-style instructions. This is a ceiling-effect smoke test, not evidence that the skill never helps.
- These are repetitions of one task, not additional task coverage; ambiguous conventions, material instruction conflicts, unavailable libraries, and broader project migrations remain untested.
- Runs 4 and 5 in each configuration are four additional independent executions of the unchanged prompt and skill. They used the current fixture with postponed annotations; the original six outputs were retained.
- Current executor: gpt-6.1-sol via Junie subagents. Earlier robot/markdown benchmarks used a different runtime/model; their scores are not a controlled cross-skill comparison.
- Timing, tokens, executor tool-call counts, and executor error counts were not exposed. These values are null, not zero; source characters are not treated as tokens.
- with_skill/run-1 additionally read .agents/skills/skill-creator/SKILL.md despite the executor's restricted scope. Retained and disclosed rather than silently discarded.
- without_skill/run-1 attempted runtime validation but Python 3.9.6 could not evaluate the fixture repository's Account | None annotation. After all runs completed, the parent added future annotations to that fixture only; no generated output was changed.
