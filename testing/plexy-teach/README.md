# plexy-teach Content Benchmark

- Mirrors the existing `testing/plexy-robot` and `testing/plexy-markdown` pilot structure.
    - One frozen prompt, three fresh runs with the skill, three without, saved outputs and per-run grading.
    - Uses existing teach case 11: a ten-minute recursive-total lesson for someone who knows loops and returns.
    - The other eleven teach scenarios are not run by this pilot.
- The original completed comparison is under `iteration-2/`; two unchanged repeats are under `iteration-3/` and `iteration-4/`.
    - Read `repeat-summary.md` for the comparison across all three completed rounds.
    - Each new round adds three fresh generations per variant: twelve new lessons, eighteen overall.
    - All variants score 100% on the same seven content checks; no pass-rate advantage is detected.
    - With-skill HTML is 17.9% and 19.7% smaller in the repeats, but neither new baseline uses JavaScript.
    - Each repeat has a standalone `review.html` with outputs, grades, benchmark, and previous-round outputs.
    - `benchmark.json` contains the machine-readable results.
    - `eval-11-recursive-total/` contains metadata and six independent run directories.
    - Each run saves its exact `prompt.txt`, `outputs/lesson.html`, content review, and grading.
    - `skill_snapshot.md` freezes the tested instructions; metadata records their SHA-256.
- Both variants use fresh Junie general-purpose generation sessions with the same current model.
    - With-skill prompts explicitly include the frozen skill; baseline prompts do not.
    - Both get identical artifact-only delivery constraints and the same learner request.
    - Generation sessions may read only their prompt and write only their lesson.
    - Generation sessions cannot read peer outputs, graders, expected answers, or other project instructions.
    - This is a forced-instruction content comparison, not a normal skill-routing test.
    - Common agent defaults still apply; this is not a guarantee of a completely skill-free runtime.

## Grading

- The seven expectations are frozen from `plexy-teach/evals/evals.json` before generation.
- Teaching quality requires explicit inspection of worked returns, arithmetic, feedback, scope, and prerequisites.
    - `content_review.json` records a boolean or null result and concrete evidence for every expectation.
    - The parent assistant reviews the artifacts with variant labels visible; reviews are not blinded or independent.
    - Missing reviews remain unverified; missing artifacts fail; altered or incomplete rubrics are rejected.
    - Word count, heading count, native answer reveals, and static HTML dependency checks are separate metrics.
    - Length and keyword matches never substitute for demonstrated reasoning.
    - Word counts exclude CSS/JavaScript but include code, controls, and collapsed answer explanations.
    - The displayed recursive Python functions are also executed against nine inputs each, including empty and nested lists.
        - Extraction restores line breaks for syntax-highlighted code; only restricted function operations are allowed.
        - It selects exactly one complete self-calling function, not the first introductory flat-list function.
        - Incomplete fill-in exercises are excluded; missing or ambiguous recursive implementations still fail.
        - These checks do not execute the JavaScript steppers or establish browser behavior.
- Regrade saved artifacts and regenerate both reports from the repository root:

```bash
python3 testing/plexy-teach/grade_runs.py
python3 testing/plexy-teach/grade_runs.py --iteration 3
python3 testing/plexy-teach/grade_runs.py --iteration 4
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s testing/plexy-teach -p 'test_*.py' -v
```

- `prepare_runs.py` prepares prompts for fresh existing-agent sessions; it does not launch a model.
    - The checked-in run directories already exist, so it refuses to overwrite them.
    - For another iteration, use `prepare_runs.py --iteration N` and `grade_runs.py --iteration N`.
    - Both default to iteration 2; preparation refuses to overwrite any existing iteration.
    - Dispatch each saved prompt to a fresh session restricted to that run's directory.
    - Keep the model and delivery constraints fixed; do not provide the grader or prior outputs.
    - Review all seven expectations for every resulting artifact before regenerating the comparison.
- `record_reviews.py` preserves the parent's explicit, line-referenced inspection decisions for iterations 3 and 4.
    - It materialized their `content_review.json` files; it is not an automatic evaluator for future generations.
    - It refuses to overwrite reviews or apply the decisions to an altered rubric.
- The review pages were produced by the standard skill-creator `eval-viewer/generate_review.py`.
    - Its Python 3.10+ annotations were postponed in memory for the installed Python 3.9; the bundled script was not modified.
    - Open either saved page and compare the Outputs and Benchmark tabs; HTML lessons are available as source/downloads.
    - Submit All Reviews downloads `feedback.json`; share it for a later feedback-driven iteration.

## Original Runner Attempt and Limits

- `iteration-1/` preserves the first, unsuccessful OpenCode attempt rather than hiding it.
    - `run_eval.py` used OpenCode `1.18.18`, a tool-free agent, and `opencode/deepseek-v4-flash-free`.
    - The first baseline attempt timed out after 240 seconds without any events or generated output.
    - A short diagnostic also stalled during startup; the free API endpoint reported the model unavailable.
    - The non-free endpoint required an API key, so it was not used.
    - No successful outputs or comparative scores are claimed for that iteration.
- The fallback model differs from the earlier robot/markdown model; compare variants within this pilot only.
- Research, skill routing, durable state, spaced-review workflow, and all browser checks are outside this pilot.
    - Inspectable inline HTML is not evidence of keyboard accessibility, print behavior, or rendered layout.
    - Timing and token counts for the fallback are unavailable and recorded as null, not zero.
    - Three repetitions of one prompt cannot establish statistical significance or general teaching quality.