### Testing quickstart and cheatsheet

- These evaluations compare agent behavior **with a skill** against a **without-skill baseline**.
    - Both configurations receive the same task.
    - Each output is scored against fixed assertions, not against the other output.
    - Aggregate results show whether explicitly supplying the skill changes those scores.
- Start with the saved reports; no new agent executions are needed to read them.
- Commands below assume the repository root as the working directory.

### What is tested against what?

| Suite            | Fixed task                                                  | Checks against each result                                                                                                                   | Saved runs         |
|------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| `plexy-robot`    | Explain a race condition and one standard prevention method | Robot prefix, ≤50 words, no listed filler, concurrency/fix keywords                                                                          | 3 with + 3 without |
| `plexy-markdown` | Explain Authentication, Authorization, and Accounting       | Topic coverage, ≤120-character lines with exemptions, no dash-chained bullets, ≥80% bullet content                                           | 3 with + 3 without |
| `plexy-do-less`  | Fix `timeout.py`: 1500 ms must become 1.5 seconds           | Correct conversion, preserved behavior, scoped edit, actual successful test execution, scoped investigation, ≤60-word reply without preamble | 5 with + 5 without |

- Task definitions live in each suite's `evals/evals.json`.
    - `prompt` is the task given to the agent.
    - `files` identifies starting fixtures, where present.
    - `expectations` lists the assertions used for grading.
- `grade_runs.py` implements the actual deterministic checks.
    - Editing assertion text alone does not implement a new check.
- For `plexy-do-less`, the loading contrast is recorded in runtime evidence.
    - `with_skill` reads `iteration-1/skill-snapshot/SKILL.md` before working.
    - `without_skill` is told not to load skills.
    - Both use the same Junie agent/model, tools, and budget with isolated starting files.
    - Shared governing instructions still apply to both configurations.
- The robot and Markdown artifacts record an external OpenCode/deepseek-flash executor.
    - Their exact skill-loading instructions and launch setup are not preserved here.
    - Do not compare their scores directly with the Junie do-less scores.

### Quickstart: inspect existing results

- Read the aggregate comparison for the suite you care about.
    - [Robot benchmark](plexy-robot/iteration-1/benchmark.md).
    - [Markdown benchmark](plexy-markdown/iteration-1/benchmark.md).
    - [Do-less benchmark](plexy-do-less/iteration-1/benchmark.md).
- Read [do-less analysis](plexy-do-less/iteration-1/analysis.md) for interpretation and caveats.
- Open the existing do-less review page on macOS.

```bash
open testing/plexy-do-less/iteration-1/review.html
```

- The review page has Outputs and Benchmark tabs.
    - Inspect individual outputs alongside their assertion grades.
    - Export reviewer feedback if you want to record a human judgment.
    - Keep exported feedback with the iteration; it does not automatically change grades or rerun agents.
- For robot and Markdown, inspect `outputs/` and `grading.json` directly.
    - Their suite directories do not contain a review-page launcher.

### Quickstart: regrade saved outputs

- Regrading evaluates the existing candidates; it **does not run fresh agents**.
- Graders need Python 3 and use the standard library.
- Robot and Markdown overwrite per-run `grading.json` files and print summaries.
    - They **do not refresh** the saved `benchmark.json` or `benchmark.md` reports.
    - A successful process exit does not mean every assertion passed; read the grades.

```bash
python3 -B testing/plexy-robot/grade_runs.py
python3 -B testing/plexy-markdown/grade_runs.py
```

- Do-less regrades every run listed in its manifest.
    - It reruns candidate acceptance tests and saves independent verification output.
    - It rewrites `grading.json`, `benchmark.json`, and `benchmark.md`.
    - Rebuild the HTML afterward to display the updated grades.

```bash
python3 -B testing/plexy-do-less/grade_runs.py
python3 -B testing/plexy-do-less/render_review.py
```

- HTML generation requires the installed helper at the following path.
    - `.agents/skills/skill-creator/eval-viewer/generate_review.py`.
    - `render_review.py` provides Python 3.9 annotation compatibility for that helper.
- None of these commands launches agents or revises a skill.

### Quickstart: add fresh do-less runs

- Preparation, agent execution, evidence collection, grading, and review are separate stages.
- There is no one-command agent launcher in these suites.
    - Robot and Markdown require arranging fresh executions and recording their outputs separately.
    - Their existing graders have hard-coded eval paths and three run numbers.

#### 1. Prepare isolated starting files

- Append two repeats **per configuration** to the current do-less iteration.
    - With five existing repeats, this creates `with_skill/run-6` and `run-7`, plus matching baseline directories.
    - Preparation copies fixtures; it does not execute the task.

```bash
python3 -B testing/plexy-do-less/prepare_runs.py --additional-runs 2
```

- For initial setup on a clean copy without `iteration-1`, omit `--additional-runs`.
    - Initial setup creates three runs per configuration, not five.
- Preparation refuses to overwrite existing run directories.
- Appending rejects changed skill content, fixtures, or eval metadata.
    - Changed inputs need a new iteration rather than mixing experiments.
    - The current scripts target `iteration-1`; they do not expose an iteration-selection option.

#### 2. Execute the task in fresh agents

- Use the task prompt from `plexy-do-less/evals/evals.json`, not the grading assertions.
- Pin its working directory and edit scope to its own `run-N/outputs/` directory.
    - Each directory starts with the same broken `timeout.py` and unchanged `test_timeout.py`.
    - Keep other candidates and grading material out of the agent's investigation.
- Instruct only the with-skill agents to read the frozen skill snapshot.
    - Tell baseline agents not to load skills.
    - Neither configuration should load other skills.
- Keep model, tools, budget, and surrounding instructions identical across configurations.
- Alternate configuration submission order between repeats.
- Ask each agent to preserve its evidence inside `outputs/`.
    - `reply.txt`: exact final user-facing response.
    - `test-output.txt`: verbatim requested test output with exit code.
- Record actual agent IDs and names for collection.
    - Do not use the old assignment map for newly launched agents.

#### 3. Collect execution evidence

- Create an assignment map for the fresh runs, using their actual identities.
    - Each entry maps an agent ID to `[agent_name, configuration, run_number]`.
    - For example, one entry for a newly created with-skill run could look like this.

```json
{
  "agent-8": ["do-less-with-6", "with_skill", 6]
}
```

- Include all fresh agents in the map; the example is not a complete four-run assignment.
- Collect evidence from the runtime session containing those executions.
    - Replace `SESSION_DIR` with that session directory.
    - Replace `ASSIGNMENTS_JSON` with the path to your assignment map.

```bash
python3 -B testing/plexy-do-less/collect_evidence.py SESSION_DIR --assignments ASSIGNMENTS_JSON
```

- The collector reads runtime events and copies readable transcripts.
    - It matches both agent ID and name to avoid mixing reused IDs.
    - `trace.json` retains the latest runtime block per step; wrapper calls are not counted twice.
    - It does not derive tool counts from the agent's own claims.
- Save a `timing.json` beside each run's `outputs/` directory before grading.
    - Use measured runtime data when available.
    - For unavailable measurements, preserve the existing explicit-null format.

```json
{
  "total_tokens": null,
  "duration_ms": null,
  "total_duration_seconds": null,
  "note": "Runtime did not expose timing or token usage."
}
```

#### 4. Grade and review

- Finish every newly prepared run before regrading; the grader expects complete evidence for all manifest runs.
- Run the do-less grading and HTML commands from the regrading quickstart.
- Read failed assertion evidence before interpreting aggregate differences.
- Keep old outputs and the frozen snapshot intact for comparison.

### Artifact cheatsheet

- Paths below are relative to `testing/<skill>/` unless noted.

| Artifact                                  | What it records                                                     | Producer                             |
|-------------------------------------------|---------------------------------------------------------------------|--------------------------------------|
| `evals/evals.json`                        | Task prompt, expected output, assertion descriptions                | Evaluation author                    |
| `evals/fixtures/`                         | Broken starting code and acceptance tests; do-less only             | Evaluation author                    |
| `iteration-1/skill-snapshot/SKILL.md`     | Exact tested skill copy; do-less only                               | Preparation                          |
| `iteration-1/manifest.json`               | Skill/fixture hashes, executor, repeat count; do-less only          | Preparation                          |
| `eval_metadata.json`                      | Eval identity, prompt, assertions                                   | Setup or collection                  |
| `run-N/outputs/`                          | Candidate result: `reply.txt`, `3A.md`, or edited code and evidence | Task agent                           |
| `run-N/trace.json`, `run-N/transcript.md` | Runtime actions and readable execution history; do-less only        | Evidence collector                   |
| `run-N/timing.json`                       | Timing/token availability; do-less only                             | Runtime evidence recording           |
| `run-N/verification.txt`                  | Independent post-run acceptance-test output; do-less only           | Grader                               |
| `run-N/grading.json`                      | Per-assertion pass/fail, evidence, summary, metrics                 | Grader                               |
| `iteration-1/benchmark.json`              | Machine-readable aggregate comparison                               | Recorded aggregation; do-less grader |
| `iteration-1/benchmark.md`                | Human-readable comparison                                           | Recorded report; do-less grader      |
| `iteration-1/analysis.md`                 | Interpretation and limitations; do-less only                        | Evaluation reviewer                  |
| `iteration-1/review.html`                 | Static output/benchmark review; do-less only                        | Review renderer                      |

- Run directories are nested under `iteration-1/eval-0-<task>/<configuration>/`.
    - Task directory names are `race`, `3as`, and `scoped-timeout-fix` after the `eval-0-` prefix.
    - Configuration names are `with_skill` and `without_skill`.

### Reading the scores

- A run's `pass_rate` is **passed assertions / total assertions**.
    - Three passes out of four means 75%, not a fully successful run.
- Aggregate pass rate is the mean of the per-run assertion rates.
    - `±` reports sample standard deviation across repeats, not a confidence interval.
    - Delta is with-skill minus without-skill.
- Do-less reports task completion separately from style and efficiency.
    - Completion requires the first four assertions plus successful independent acceptance tests.
    - Investigation scope and reply style remain separate assertions.
- Do-less investigation counts exclude skill loading, edits, requested tests, and evidence writes.
    - Failed structure lookups still count as investigation calls.
    - Total runtime actions are a different metric from investigation calls.
- Successful grader-side tests do not prove the agent ran the requested command.
    - Do-less requires a recorded successful terminal result in `trace.json` for that assertion.
- Timing and token usage are unavailable in the recorded experiments.
    - Null or placeholder zeros do not mean free or instantaneous execution.
    - Output characters are not token measurements.
    - The current do-less aggregate keeps time and tokens null even if a run's timing file is populated later.

### Limits to keep in mind

- These are single-task smoke tests with a few repeats, not broad reliability benchmarks.
- The style graders use heuristics rather than semantic evaluation.
    - Robot keyword coverage does not prove a correct explanation.
    - Markdown checks do not fully enforce one statement per bullet or correct nesting.
    - Markdown's current width-check evidence text is overwritten by dash-check evidence.
        - Its width verdict remains correct; inspect the recorded line-length metrics.
- Do-less measures explicit skill loading, not automatic triggering or globally isolated skill installations.
- Shorter replies or fewer calls are only useful if task completion is preserved.

### Optional: check the do-less harness itself

- These unit tests validate the preparation, collection, and grading code, not new skill behavior.

```bash
python3 -B -m unittest discover -s testing/plexy-do-less -p 'test_*.py' -v
```
