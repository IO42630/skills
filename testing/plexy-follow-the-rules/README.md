# plexy-follow-the-rules smoke benchmark

- Mirrors the robot/markdown pilot: one task, three independent runs with the skill and three without it.
- Tests a native Python account action against supplied project guidelines and a selected external reference.
- The explicit whitespace-preservation request deliberately overrides the project's normal name stripping.
- Six deterministic assertions check conventions, reference naming, real behavior, errors, and scope.
- Saved executor outputs are never rewritten to make them pass.
- The target skill is unchanged; this is behavioral testing, not automatic trigger testing or skill optimization.

## Reproduce grading and reports

```bash
python3 -B -m unittest discover -s testing/plexy-follow-the-rules -p test_grade_runs.py -v
python3 -B testing/plexy-follow-the-rules/grade_runs.py
python3 -B testing/plexy-follow-the-rules/generate_report.py
open testing/plexy-follow-the-rules/iteration-1/review.html
```

- Python 3.9 or newer; no third-party dependencies.
- The 12 grader tests include valid controls and intentionally incorrect implementations.
- Grading reruns each saved implementation in a separate process with the real fixture repository.
- The report reuses skill-creator aggregation and its standard static viewer.
- The viewer exposes outputs, formal grades, benchmark results, and downloadable review feedback.
- The reproduction commands regrade saved outputs; they do not launch fresh model runs.

## Interpretation

- Result: 100% with skill and 100% without skill; zero observed pass-rate variance or improvement.
- This narrowly scoped task is already solved by the shared instructions plus explicit project guidance.
- Passing both configurations does not establish that the skill is ineffective on harder tasks.
- Conflict clarification, incompatible dependencies, and less explicit style evidence need separate evaluations.
- `iteration-1/execution.json` records the model, run handles, self-reported input reads, and protocol deviations.
- One with-skill executor additionally read skill-creator guidance; its run is retained and disclosed.
- A fixture annotation compatibility adjustment was made after execution, before grading, on Python 3.9.
- Unavailable timing and token measurements are null, not fabricated zeros or character-count proxies.
- The robot/markdown pilots used a different executor; do not interpret this as a controlled cross-skill ranking.