# Skill Benchmark: plexy-teach

**Model**: Junie general_purpose (gpt-6.1-sol)
**Date**: 2026-10-07
**Eval**: 11, recursive total (3 fresh runs per configuration)
**Scope**: forced-skill content pilot; identical artifact-only delivery constraints

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Reviewed rubric pass rate | 100.0% ± 0.0 | 100.0% ± 0.0 | +0.0 pp |
| Lesson text words | 1150.7 ± 63.7 | 1154.3 ± 66.5 | -3.7 |
| Headings | 8.0 ± 2.6 | 11.7 ± 1.2 | -3.7 |
| HTML characters | 11847.7 ± 786.2 | 25633.0 ± 6006.8 | -13785.3 |
| Script blocks | 0.0 ± 0.0 | 1.0 ± 0.0 | -1.0 |
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

- All six artifacts satisfy all seven frozen recursion-content expectations: 21/21 checks per configuration.
    - No rubric pass-rate improvement was detected on this prompt; the baseline was already substantively good.
    - This is an assistant-reviewed artifact result, not evidence that learners actually gained the capability.
- The consistent difference is artifact machinery, not prose compression.
    - With skill: all three lessons use static traces, native answer reveals, and no JavaScript.
    - Without skill: all three add bespoke call-frame steppers, numeric or multiple-choice checking, and JavaScript.
    - With-skill worked examples all use `[2, [3, 4]]`, three leaves and one child call.
    - Baselines begin with four or five leaves and two nested child calls; still small, valid teaching examples.
    - Text length is nearly identical; heading counts and HTML size are lower with the skill.
- All six displayed recursive functions passed nine inputs each: 54 successful input/output checks.
    - These include empty lists, nested empty lists, deeper nesting, continuation after child return, and negative values.
    - Arithmetic and return-flow explanations were also inspected directly; the original artifacts were not repaired.
- Every artifact has a title, language attribute, main landmark, and no detected required external dependencies.
    - That is static evidence only, not a passed accessibility, offline-rendering, or print test.
    - Baseline run 1 asserts that the lesson works offline without a performed browser check.
    - With-skill run 1 explicitly says to open answer reveals before printing; automatic print inclusion is unverified.
- This rubric does not prohibit a simulator when its content remains small and faithful.
    - The observed preference for simple presentation should not be turned into a retroactive baseline failure.
    - Normal routing, state continuity, exports, source verification, and rendered accessibility need separate scenarios.
- The result supports a narrow conclusion: on this model and prompt, the skill reduced incidental UI machinery
  while preserving substantive teaching, but did not improve the already-saturated content pass rate.
