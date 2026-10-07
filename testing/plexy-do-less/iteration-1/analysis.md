# plexy-do-less smoke-test findings

- Repeat the robot/markdown format: one task, five fresh runs per configuration, deterministic grading.
- Preserve the original three pairs and append four executions: two with the skill and two baselines.
- Use a code-edit task because `plexy-do-less` controls investigation and action, not just response style.
- Keep `plexy-do-less/SKILL.md` unchanged; the tested snapshot and fixture hashes are in `manifest.json`.

## Results

- All ten runs passed all six assertions: 100% with the skill and 100% without it.
- All ten runs completed the task and ran the requested tests successfully.
    - Conversion works for zero, fractional milliseconds, and multiple positive values.
    - Negative-value rejection and the caller's timeout/retry behavior are preserved.
    - Only the conversion expression changed; supplied tests are byte-for-byte unchanged.
    - Agent-side command execution is confirmed by terminal records, not post-run verification alone.
- All runs used four investigation calls: two failed structure lookups and two successful file reads.
    - There were no broad repository surveys or helper subagents.
    - The unavailable structure capability and inherited lookup requirement affect both configurations.
- Replies were 41/41/41/42/38 words with the skill and 53/41/46/44/38 words without it.
    - Mean ± sample standard deviation: 40.6 ± 1.5 versus 44.4 ± 5.7 words.
    - Replies include evaluation-evidence bookkeeping, so this is not a pure user-task verbosity measure.
- With-skill runs invoked tests 2/1/1/2/1 times; baseline runs invoked tests 2/2/2/2/2 times.
    - Three with-skill runs skipped the pre-fix reproduction of this obvious divisor bug.
    - Every run still performed the requested final verification, passing all three test methods.
    - Mean test invocations: 1.4 with the skill versus 2.0 without it.
- Additional runs 4 and 5 passed 24/24 assertions in total and all requested tests.
    - Reply lengths: 42/38 words with the skill, 44/38 without it.
    - Both groups still used four investigation calls per run.
- All seven harness tests passed, including append safety and reused-agent-ID evidence isolation.
    - The isolation test reproduced mixed old/new events before the collector fix and passed afterward.
- No duration or token counts were supplied by the completion notifications.
    - Store these as unknown; do not substitute output characters or zero-valued measurements.

## Interpretation

- This smoke test finds no completion regression and no reduction in investigation.
- With-skill runs use slightly shorter replies and fewer test invocations on this obvious fix.
    - These differences do not establish a general efficiency improvement or justify skipping necessary reproduction.
- All assertions pass in both configurations, so this task has a ceiling effect.
    - It establishes basic compatibility with required verification, not a distinctive skill advantage.
- Governing Junie instructions already encourage scoped edits, proportional work, and concise replies.
- Explicit loading is verified, but automatic triggering and globally isolated skill installations are not tested.
- The earlier robot/markdown artifacts used a different executor; their scores are not directly comparable here.
- No skill revision is justified by this single task; broader/shared-state tasks would be a separate follow-up.

## Artifacts and commands

- `evals/evals.json`: fixed prompt, starting fixtures, and six acceptance assertions.
- `iteration-1/eval-0-scoped-timeout-fix/{with_skill,without_skill}/run-N/`:
    - `outputs/`: candidate code, unchanged tests, final reply, and captured agent-side test output.
    - `transcript.md` and `trace.json`: copied execution evidence from the completed runtime.
    - `grading.json` and `verification.txt`: deterministic grades and independent final-state verification.
    - `timing.json`: explicitly unavailable timing/token data.
- `benchmark.json` and `benchmark.md`: aggregate results with completion separate from style/efficiency.
- `additional_assignments.json`: fresh agent names, IDs, configurations, and run numbers for the four additions.
- `review.html`: standalone skill-creator review page with Outputs and Benchmark tabs.
    - Review the outputs and export feedback before deciding whether to change the skill.

```bash
python3 testing/plexy-do-less/prepare_runs.py
python3 -B testing/plexy-do-less/collect_evidence.py '~/.junie/sessions/session-261007-091331-8bj7'
python3 testing/plexy-do-less/prepare_runs.py --additional-runs 2
python3 -B testing/plexy-do-less/collect_evidence.py '~/.junie/sessions/session-261007-091331-8bj7' --assignments testing/plexy-do-less/iteration-1/additional_assignments.json
python3 -B -m unittest discover -s testing/plexy-do-less -p 'test_*.py' -v
python3 -B testing/plexy-do-less/grade_runs.py
python3 -B testing/plexy-do-less/render_review.py
```

- Initial preparation requires a clean copy; appending preserves existing runs and rejects changed inputs.
- The collector's agent assignments describe this recorded session; update them for fresh executions.
    - Evidence matches both agent ID and name because IDs were reused after session continuation.
- The deterministic grader aggregates in the viewer's schema, preserving unknown timing/token data.
    - The shared aggregation script instead substitutes zeros/output characters when measurements are absent.
- `render_review.py` invokes the installed `generate_review.py` without modifying it.
    - Deferred annotations avoid its Python 3.10 union-annotation error on the installed Python 3.9.