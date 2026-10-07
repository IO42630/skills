# plexy-kiss pilot

- Mirrors `testing/plexy-robot` and `testing/plexy-markdown`:
    - One frozen prompt.
    - Five fresh conversations with the skill and five without.
    - Repeats 4 and 5 add four executions to the original six-run pilot.
    - Saved candidate outputs, deterministic grades, and a comparison report.
- Uses Junie general-purpose subagents with `gpt-6.1-sol`, not the earlier reports' `deepseek-flash`.
- Tests a production-ready local JSON settings loader.
    - Keeps dictionary validation, Unicode/nested data, native diagnostics, and file cleanup.
    - Checks for unjustified framework structure in this specific task.
- Does not modify `plexy-kiss/SKILL.md` or repair evaluated candidates.

## Results

- Both configurations passed 30/30 assertions and completed 5/5 required tasks.
- The four additional executions passed 24/24 assertions.
- No observable improvement on this prompt; the baseline already uses a direct implementation.
- Source lengths: with skill 17/16/20/19/20 lines; without skill 20/20/20/22/20.
    - Differences are annotations and documentation, not a different algorithm.
- See `iteration-1/benchmark.md` and `iteration-1/benchmark.json`.
- Open `iteration-1/review.html` for the ten outputs and quantitative comparison.

## Repeat grading

- Python 3.9+ and the standard library are sufficient; no package installation is needed.
- These commands regrade existing outputs, not rerun model conversations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s testing/plexy-kiss -p test_grade_runs.py -v
PYTHONDONTWRITEBYTECODE=1 python3 testing/plexy-kiss/grade_runs.py
PYTHONDONTWRITEBYTECODE=1 python3 testing/plexy-kiss/report_runs.py
```

## Regenerate the review page

- Uses the installed `skill-creator` viewer; it is not a benchmark runtime dependency.
- On Python 3.10+, run:

```bash
python3 .agents/skills/skill-creator/eval-viewer/generate_review.py \
  testing/plexy-kiss/iteration-1 --skill-name plexy-kiss \
  --benchmark testing/plexy-kiss/iteration-1/benchmark.json \
  --static testing/plexy-kiss/iteration-1/review.html
```

- On Python 3.9, postpone the viewer's type annotations without editing its installed source:

```bash
python3 -c 'import __future__, sys; from pathlib import Path; p = Path(".agents/skills/skill-creator/eval-viewer/generate_review.py"); sys.argv[0] = str(p); exec(compile(p.read_text(), str(p), "exec", flags=__future__.annotations.compiler_flag), {"__name__": "__main__", "__file__": str(p)})' \
  testing/plexy-kiss/iteration-1 --skill-name plexy-kiss \
  --benchmark testing/plexy-kiss/iteration-1/benchmark.json \
  --static testing/plexy-kiss/iteration-1/review.html
```

## Limits

- Timing/token metrics are unavailable and recorded as `null`, never fabricated as zero.
- Fresh conversations and disjoint output directories share repository access and inherited agent instructions.
    - With-skill executors were told to read only `plexy-kiss/SKILL.md`; baselines were told to read no skills.
    - This measures instructed skill application, not automatic triggering or fully isolated skill installation.
- The structural assertion is a proxy for this local-file-only case, not a universal restriction on classes.
- One task with five repeats cannot establish general effectiveness or statistical significance.
- Justified interfaces, security-sensitive complexity, and precise `DRY` behavior remain untested.