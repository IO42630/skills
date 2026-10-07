# Skill Benchmark: plexy-teach

**Model**: Junie general_purpose (gpt-6.1-sol)
**Date**: 2026-10-07
**Eval**: 11, recursive total (3 fresh runs per configuration)
**Scope**: forced-skill content pilot; identical artifact-only delivery constraints

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Reviewed rubric pass rate | 100.0% ± 0.0 | 100.0% ± 0.0 | +0.0 pp |
| Lesson text words | 1257.3 ± 39.5 | 1291.7 ± 118.4 | -34.3 |
| Headings | 8.3 ± 1.2 | 8.7 ± 1.2 | -0.3 |
| HTML characters | 12042.7 ± 318.3 | 14667.0 ± 575.5 | -2624.3 |
| Script blocks | 0.0 ± 0.0 | 0.0 ± 0.0 | +0.0 |
| Time / tokens | Unavailable | Unavailable | Unavailable |

## Notes

- Rubric decisions and concrete evidence are saved in each run's `content_review.json` and `grading.json`.
- Teaching quality is reviewed explicitly, not awarded for keyword matches, length, or heading count.
- Static structure/dependency metrics are not browser, accessibility, or pedagogical proof.
- Lesson text word counts exclude CSS/JavaScript but include code, controls, and collapsed answer explanations.
- Reviews are by the parent assistant with variant labels visible; not independent or blinded.
- Three runs of one prompt are exploratory, not evidence of statistical significance or broad skill quality.
- This model differs from the earlier robot/markdown model; compare variants within this pilot only.
- Iteration 1 is a preserved OpenCode startup timeout, not a completed comparison; see `README.md`.
- Timing and token data are unavailable, represented as null rather than fabricated zero measurements.

## Interpretation

- All six new artifacts satisfy all seven unchanged content expectations: 21/21 per configuration.
    - This repeats iteration 2's saturated pass rate; no content-rubric advantage was detected.
    - These are assistant artifact judgments, not measured learner gains or completion times.
- The earlier JavaScript difference did not repeat.
    - Both variants now use static traces and native answer reveals, with zero script blocks.
    - Baseline runs 2 and 3 include optional scratch textareas and explicitly say notes are not saved or graded.
    - Therefore removing bespoke JavaScript is not a stable demonstrated skill effect across rounds.
- With-skill HTML is 17.9% smaller on average, while lesson text is only 2.7% shorter.
    - With-skill examples have three or four leaves and one child call.
    - Baselines have four or five leaves and two nested child calls; all remain small enough for the rubric.
    - With-skill lessons include short delayed-recall suggestions; baselines emphasize immediate reconstruction.
    - These differences do not establish better learning, lower elapsed generation time, or reduced token cost.
- All six recursive functions pass nine inputs each: 54 executable input/output checks.
    - The extractor initially selected baseline run 2's introductory flat-list function.
    - That function is explicitly not the nested-list solution. Selection now requires a self-calling function.
    - Incomplete fill-in exercises are not executable implementations; exactly one complete recursive definition is required.
    - Regression tests cover a flat intro, incomplete exercise, missing recursive implementation, and ambiguous multiple implementations.
    - No generated lesson was repaired to improve its score.
- Static checks find language attributes, semantic structure, and no required external dependencies in all artifacts.
    - No browser, offline-rendering, keyboard, narrow-viewport, or printing result is claimed.
    - Rendered answer inclusion in print remains unverified for both variants.
- The seven expectations all pass both variants and therefore do not discriminate skill value on this prompt.
    - More repetitions improve our view of artifact variability, not topic coverage.
    - Timing/tokens remain unavailable; source research, routing, and durable workspace behavior are untested.
    - `review.html` provides the six outputs and grades for human feedback alongside iteration 2's outputs.
