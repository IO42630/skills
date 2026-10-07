# Skill Benchmark: plexy-do-less

- One scoped bug-fix task; 5 runs per configuration.
- Model: `gpt-6.1-sol` through Junie general-purpose subagents.

| Metric | With skill | Without skill | Delta |
|---|---|---|---|
| Task completion | 100.0% ± 0.0 | 100.0% ± 0.0 | +0.0% |
| All assertions | 100.0% ± 0.0 | 100.0% ± 0.0 | +0.0% |
| Reply words | 40.6 ± 1.5 | 44.4 ± 5.7 | -3.8 |
| Investigation calls | 4.0 ± 0.0 | 4.0 ± 0.0 | +0.0 |
| Runtime actions | 8.4 ± 0.5 | 8.0 ± 0.0 | +0.4 |
| Test commands | 1.4 ± 0.5 | 2.0 ± 0.0 | -0.6 |
| Time / tokens | Not available | Not available | Not measured |

## Notes

- Completion is reported separately from efficiency/style; all four task requirements must pass.
- Tool counts include failed structure lookups; inherited Junie instructions require these lookups.
- Investigation counts exclude skill loading, required tests, edits, and evidence writes.
- Timing and tokens are unavailable; output characters are not reported as tokens.
- A single task and 5 repeats are a smoke test; no general or statistically significant claim.
- This tests explicitly loaded instructions, not automatic triggering or global skill isolation.
- Reply words: with skill 40.6 ± 1.5; without skill 44.4 ± 5.7.
- Investigation calls: with skill 4.0 ± 0.0; without skill 4.0 ± 0.0.
