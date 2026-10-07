# Skill Benchmark: plexy-java

- Model: `gpt-6.1-sol`, Junie general-purpose subagents.
- One frozen customer-directory prompt; 5 independent runs per variant.
- Skill and existing robot/markdown artifacts were not modified.

## Summary

| Metric | With Skill | Without Skill | Delta |
|---|---|---|---|
| Assertion pass rate | 93.3% ± 3.7% | 58.3% ± 0.0% | +35.0% |
| Compiles | 5/5 | 5/5 | — |
| Core behavior | 5/5 | 5/5 | — |
| Null-map rejection | 5/5 | 5/5 | — |
| IOException propagation | 5/5 | 5/5 | — |
| Generation time / tokens | unavailable | unavailable | unavailable |

## Per-run results

| Run | With Skill | Without Skill |
|---|---|---|
| 1 | 11/12 | 7/12 |
| 2 | 11/12 | 7/12 |
| 3 | 11/12 | 7/12 |
| 4 | 12/12 | 7/12 |
| 5 | 11/12 | 7/12 |

## Per-assertion results

| Assertion | With Skill | Without Skill |
|---|---|---|
| The complete candidate compiles for Java 17 with the real declared dependencies. | 5/5 | 5/5 |
| Lookup, mutable customer fields, sorted displays, UTF-8 CSV loading, and supplied-map updates work. | 5/5 | 5/5 |
| Imports are explicit and grouped java/javax, third-party, then project-internal. | 5/5 | 0/5 |
| Customer uses Lombok @Data and @Builder instead of handwritten accessors or constructors. | 1/5 | 0/5 |
| Obvious local initializers use var rather than redundant explicit types. | 5/5 | 0/5 |
| Java sources compile without raw-type warnings. | 5/5 | 5/5 |
| Missing-file IOException reaches the caller rather than being swallowed. | 5/5 | 5/5 |
| findById returns typed Optional<Customer>, empty for absence and populated for presence. | 5/5 | 5/5 |
| The constructor rejects a null map and uses Objects.requireNonNull for that parameter. | 5/5 | 5/5 |
| The existing Maven dependency declarations are preserved without additions or duplicates. | 5/5 | 5/5 |
| Chained method-call dots start on new lines. | 5/5 | 0/5 |
| Calls with multiple arguments put each argument and the closing parenthesis on separate lines. | 5/5 | 0/5 |

## Observations and limitations

- Imports are explicit and grouped java/javax, third-party, then project-internal. With skill 5/5; without skill 0/5.
- Customer uses Lombok @Data and @Builder instead of handwritten accessors or constructors. With skill 1/5; without skill 0/5.
- Obvious local initializers use var rather than redundant explicit types. With skill 5/5; without skill 0/5.
- Chained method-call dots start on new lines. With skill 5/5; without skill 0/5.
- Calls with multiple arguments put each argument and the closing parenthesis on separate lines. With skill 5/5; without skill 0/5.
- 7 assertions pass in all 10 runs; these check correctness/control conditions rather than distinguish the skill.
- The frozen Lombok probe demands @Data and @Builder without handwritten DTO accessors or constructors. The task never explicitly requests a builder API; an annotation-specific failure need not mean failure to remove boilerplate.
- In the original cohort, with-skill runs 2 and 3 combine @RequiredArgsConstructor with scoped lombok.config to generate Objects.requireNonNull; run 1 retains a manual service constructor. Constructor bytecode and null-input execution verify the resulting guard.
- Time, token counts, and executor-wide tool/error counts were not exposed; null means unavailable, not zero. No efficiency claim is supported.
- One task with 5 repeats per variant is exploratory, not evidence of statistical significance or broad Java coverage.
- Only generated artifacts were tested. All agents were explicitly told not to build; evaluator success does not prove agent-side verification.
- The skill was explicitly loaded, not auto-triggered. Baseline agents were instructed not to read skills; they shared the repository and inherited agent instructions, so filesystem isolation was not enforced.

## Diagnostic variance

| Metric | With Skill (mean ± SD) | Without Skill (mean ± SD) |
|---|---|---|
| java_lines | 74.2 ± 3.3 | 95.6 ± 9.7 |
| max_line_length | 80.8 ± 1.9 | 101.2 ± 7.2 |
| var_initializers | 3.0 ± 1.0 | 0.0 ± 0.0 |
| raw_type_warnings | 0.0 ± 0.0 | 0.0 ± 0.0 |
| chain_layout_violations | 0.0 ± 0.0 | 2.0 ± 0.0 |
| argument_layout_violations | 0.0 ± 0.0 | 13.8 ± 1.5 |

- Line length is diagnostic only: the skill specifies no numeric limit.
- Style checks are targeted lexical probes, not a general-purpose Java parser.
- `@Slf4j` and generated service constructors are observed, not required by this DTO-focused Lombok check.
- Source dependency declarations are checked; the Maven lifecycle itself was not executed.
