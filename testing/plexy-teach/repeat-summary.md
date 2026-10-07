# plexy-teach: Two Additional Testing Rounds

- Repeated the original six-artifact comparison twice, without changing the learner prompt, delivery constraints, skill snapshot, model, or seven content expectations.
    - Iteration 3: three fresh with-skill lessons and three fresh baselines.
    - Iteration 4: another three of each, with the pair launch order reversed.
    - All twelve new lessons were generated in isolated sessions; none was edited after generation to improve a score.
    - Skill snapshot SHA-256 remains `74b460e150af6c7d6f46982eb47fba039ca6d837e2bf75c29407c281e1bd8e92`.

## Results

| Completed round | With-skill rubric | Baseline rubric | With-skill mean words | Baseline mean words | With-skill mean HTML characters | Baseline mean HTML characters | Script blocks, with / baseline |
|-----------------|-------------------|-----------------|-----------------------|---------------------|--------------------------------|-------------------------------|--------------------------------|
| 2, original pilot | 21/21 | 21/21 | 1150.7 | 1154.3 | 11847.7 | 25633.0 | 0 / 3 |
| 3, first repeat | 21/21 | 21/21 | 1257.3 | 1291.7 | 12042.7 | 14667.0 | 0 / 0 |
| 4, second repeat | 21/21 | 21/21 | 1220.0 | 1330.3 | 12182.7 | 15166.7 | 0 / 0 |

- All 84 new expectation judgments pass; across the three completed rounds each variant has 63/63.
    - There is still no detected content-rubric advantage: this one prompt saturates the criteria for both variants.
- With-skill HTML is 17.9% smaller in iteration 3 and 19.7% smaller in iteration 4.
    - Text is only 2.7% and 8.3% shorter respectively; HTML size is not a direct measure of teaching quality.
    - With-skill worked inputs consistently use fewer leaves/child calls and include delayed-retrieval suggestions.
- The original baseline's JavaScript steppers did not repeat in either new round.
    - All new lessons use static explanations and native answer reveals.
    - Thus the earlier JavaScript-removal result is not a robust effect demonstrated across all rounds.

## Verification

- Seventeen tests pass, including input/skill/rubric consistency and overwriting safeguards.
- Eighteen recursive functions pass nine inputs each: 162 successful checks, including 108 for the new lessons.
    - Empty lists, nested empty lists, deeper returns, continuation after child return, and negative values are covered.
    - Two baseline lessons exposed a test-harness assumption: their first function was an explicitly flat-list bridge.
    - The extractor now selects exactly one complete self-calling function; regression tests cover flat intros, incomplete exercises, missing implementations, and ambiguous candidates.
    - Original generated artifacts and the seven frozen teaching expectations were not weakened or repaired.
- Worked return arithmetic, feedback, prerequisites, and ten-minute core scope were also inspected directly.
    - Reviews are by the parent assistant with variant labels visible, not independent or blinded.
    - Ten-minute fit is an artifact judgment, not a measured learner completion time.

## Reports and Human Review

- [First-repeat report](iteration-3/benchmark.md) · [review page](iteration-3/review.html).
- [Second-repeat report](iteration-4/benchmark.md) · [review page](iteration-4/review.html).
- Each round retains metadata, exact prompts, lessons, per-expectation evidence, machine-readable grades, and generation-session handles.
    - The standard review pages include previous-round outputs and allow feedback downloads.
- This remains a one-prompt, forced-instruction content experiment on `gpt-6.1-sol`.
    - Browser behavior, normal routing, source research, persistent workspace workflow, and learner outcomes are untested.
    - Timing and token counts are unavailable and stay null; no significance or cross-model superiority is claimed.