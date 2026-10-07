# plexy-java evaluation

- Same comparison shape as `testing/plexy-robot` and `testing/plexy-markdown`.
    - One fixed task, three independent with-skill runs, three independent baselines.
    - Same model, fixture, instructions, tools, and 20-step budget; only skill access differs.
- Task: refactor a Java 17 customer directory without losing its existing behavior.
- Results: `iteration-1/benchmark.md`, `benchmark.json`, and `review.html`.
- Each run retains its candidate sources, execution notes, grading evidence, and actual validation commands/results.
- The production skill and the earlier evaluations are unchanged.

## Recheck saved candidates

- Requirements: Python 3.9+, JDK 17+, and HTTPS access to Maven Central.
    - Maven is not required or used.
    - The first check downloads real Lombok 1.18.48 and SLF4J API 2.0.17 into ignored `.deps/`.
    - Maven Central's published SHA-1 checksums verify downloads; the report also records artifact SHA-256 hashes.
- From the repository root:

```bash
python3 -m unittest discover -s testing/plexy-java/checks -v
python3 testing/plexy-java/grade_runs.py --check-fixture
python3 testing/plexy-java/grade_runs.py
python3 testing/plexy-java/write_report.py
```

- The fixture check must compile and pass core behavior while reproducing accepted null maps and swallowed I/O errors.
- A grader command completing successfully means all candidates were scored, not that all expectations passed.
- `validation/results.json` contains subprocess exit codes, output, and constructor bytecode.
    - Bytecode validates `Objects.requireNonNull` even when Lombok generates the constructor.
- The grader does not repair candidate code or change its acceptance criteria to make it pass.

## Repeat generation

- Use a fresh iteration and fresh independent agent conversations.
- Read the frozen prompt in `evals/evals.json` and supply the three listed fixture files read-only.
    - File paths are relative to this evaluation directory, not the production skill directory.
- For each of three repeats, launch both variants together.
    - With skill: read `plexy-java/SKILL.md` before executing the task.
    - Baseline: read no skill files and do not reveal skill-specific assertions.
- Give each agent exclusive write access to its own `outputs/` and `execution.md`.
    - Preserve `pom.xml`, the source directory layout, and any needed `lombok.config`.
    - Do not disclose checks, reference solutions, other candidates, or reports.
- Agents generate artifacts only; compilation and grading happen separately after all six runs finish.
- Save actual timing/token notifications if exposed; otherwise mark them unavailable, never zero.
- The scripts currently target `iteration-1`; change the iteration constants before grading a new saved iteration.

## Review and boundaries

- Open `iteration-1/review.html` to inspect all six outputs and the comparison.
    - The page was generated with skill-creator's official `eval-viewer/generate_review.py`, not custom HTML.
    - Feedback from a static page downloads as `feedback.json`; it is not automatically written into this directory.
- Explicit loading tests adherence, not whether the skill's description triggers automatically.
- Baselines were instructed not to read skills but shared the repository and inherited general agent instructions.
    - This is not a filesystem-isolated or instruction-free baseline.
- The old robot/markdown runs used a different model, so compare variants within this Java test, not across skills.
- One task with three repeats is exploratory; it does not establish significance or comprehensive Java coverage.
- The prompt explicitly requests robust input/error handling, so those checks may pass without the skill too.
- The Lombok check targets DTO boilerplate; it does not require an otherwise unused logger.
- Its frozen `@Builder` requirement is stricter than removing boilerplate; all with-skill runs use `@Data` instead.
    - The failed assertion remains scored, with that evaluation weakness called out rather than relaxing the check.
- The style checker targets these sources, not every valid Java syntax form.
- Timing/token data is unavailable; no efficiency conclusions can be drawn.
- The local summarizer follows skill-creator's report schema but omits unavailable summary metrics.
    - This avoids substituting output characters for tokens or treating missing timing as zero.
- No automatic skill changes are made from the benchmark results.