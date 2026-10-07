# Skill Benchmark: plexy-teach

**Model**: Junie general_purpose (gpt-6.1-sol)
**Date**: 2026-10-07
**Eval**: 11, recursive total (3 fresh runs per configuration)
**Scope**: forced-skill content pilot; identical artifact-only delivery constraints

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Reviewed rubric pass rate | 100.0% ± 0.0 | 100.0% ± 0.0 | +0.0 pp |
| Lesson text words | 1220.0 ± 13.5 | 1330.3 ± 165.1 | -110.3 |
| Headings | 8.3 ± 0.6 | 7.0 ± 1.7 | +1.3 |
| HTML characters | 12182.7 ± 508.5 | 15166.7 ± 2264.6 | -2984.0 |
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
    - There is no rubric pass-rate improvement over either iteration 2 or iteration 3.
    - This is explicit non-blinded assistant review, not evidence of learner mastery or an observed ten-minute completion.
- Neither variant uses JavaScript in this round, matching iteration 3 rather than iteration 2's baseline steppers.
    - All lessons use static traces and native answer reveals.
    - Baseline run 3 adds static call-frame boxes and a sixth short section; these faithfully explain the same taught calls.
    - No retroactive failure is assigned for presentation choices that the frozen rubric permits.
- With-skill HTML is 19.7% smaller and lesson text 8.3% shorter on average.
    - All three with-skill worked inputs are [2, [3, 4]], with three leaves and one child call.
    - Baselines use four or five leaves and two child calls.
    - With-skill run 1 explicitly separates child_total assignment from addition; both forms pass the same function checks.
    - With-skill artifacts suggest delayed retrieval; baselines focus on immediate prediction, reconstruction, and diagnosis.
    - Shorter artifacts are a descriptive metric, not proof of stronger teaching or lower runtime cost.
- All six recursive functions pass nine inputs each: 54 executable input/output checks.
    - The earlier first-definition assumption also selected baseline run 2's explicitly flat introductory function.
    - The extractor correction checks the recursive implementation without altering either introductory or recursive lesson code.
    - Baseline run 3's phrase "at any depth" is qualified by its explicit recursion-depth limitation.
    - Worked arithmetic and feedback explanations were also inspected directly; no artifacts were edited after generation.
- All six have language attributes, semantic structure, and no detected required external dependencies.
    - Static evidence is not a passed accessibility, browser, offline-opening, or print check.
    - `review.html` includes this round's outputs and grades with iteration 3's outputs as previous context.
- Across all three completed rounds there are nine lessons per configuration, still on one frozen prompt.
    - All seven expectations remain saturated for both variants; no broad skill-quality or statistical-significance claim follows.
    - The consistent observed difference is smaller with-skill HTML, not universal JavaScript removal.
    - Research, normal routing, persistent workspace behavior, timing, tokens, and actual learner outcomes remain untested or unavailable.
