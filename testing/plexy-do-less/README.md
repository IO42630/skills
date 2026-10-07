# plexy-do-less evaluation

- Follow the existing `testing/plexy-robot` and `testing/plexy-markdown` format.
    - One fixed prompt, five fresh with-skill runs, five fresh without-skill runs.
    - The original three pairs are preserved; four more executions add two pairs.
    - Deterministic grading, per-run evidence, aggregate results, and a review page.
- Test a scoped code fix rather than judging brevity alone.
    - Check conversion, rejection behavior, caller behavior, scope, and requested verification.
    - Measure investigation calls and reply length separately from task completion.
- Keep the skill unchanged and freeze a copy in `iteration-1/skill-snapshot/SKILL.md`.
- Use the same Junie general-purpose agent, model, tools, and budget in both configurations.
    - With-skill agents explicitly read the snapshot; baselines are told not to load skills.
    - Each agent is pinned to its own `run-N/outputs` directory with identical starting files.
    - This measures explicit skill loading, not automatic triggering or fully isolated installations.
    - Inherited Junie instructions can already encourage concise, scoped work.
- Exclude skill loading and evidence-file writes from task-investigation measurements.
- Keep absent timing and token measurements unknown, not fabricated zeros.
- Treat one task with five repeats as a smoke test, not statistical evidence of general improvement.

## Reproduce

1. On a clean copy without `iteration-1`, run `python3 testing/plexy-do-less/prepare_runs.py`.
    - To add four executions without overwriting results, append two runs per configuration with
      `python3 testing/plexy-do-less/prepare_runs.py --additional-runs 2`.
    - Appending rejects changed skills, fixtures, or evaluation definitions.
2. Give each fresh agent the prompt from `evals/evals.json` and its own working directory.
    - Launch both configurations together, alternating their submission order between repeats.
    - Only with-skill agents read the frozen snapshot; neither configuration loads other skills.
    - Save `reply.txt`, verbatim test output with exit code, and actual execution evidence.
3. Collect tool-call records from the agent runtime, not an agent's retrospective claims.
    - `trace.json` records runtime actions, file paths, commands, and results in each run directory.
    - Preserve a readable `transcript.md` alongside it.
    - Use `collect_evidence.py SESSION_DIR --assignments iteration-1/additional_assignments.json`
      for the four additional runs; omit that option for the original recorded assignments.
4. Run `python3 testing/plexy-do-less/grade_runs.py`.
5. The grader aggregates results; generate the review page with the installed `skill-creator` script.
    - Run `python3 -B testing/plexy-do-less/render_review.py` for Python 3.9 compatibility.
    - Exact commands and findings are recorded in `iteration-1/analysis.md` after collection.

- The deliberately broken fixture should fail its tests before execution.
- Preparation refuses to overwrite existing results.
- Grading reruns the unchanged acceptance tests, but this does not prove agent-side test execution.
    - That assertion requires the recorded command and successful runtime result in `trace.json`.
- Read `iteration-1/benchmark.md` for the comparison and `iteration-1/review.html` for the outputs.