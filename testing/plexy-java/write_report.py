#!/usr/bin/env python3
"""Prepare review metadata or summarize all paired graded runs without invented metrics."""

import argparse
import hashlib
import json
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from grade_runs import run_numbers

ROOT = Path(__file__).resolve().parent
ITERATION = ROOT / "iteration-1"
EVAL_DIR = ITERATION / "eval-0-customer-directory"
CONFIGS = ["with_skill", "without_skill"]


def stats(values):
    return {"mean": statistics.mean(values), "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values), "max": max(values)}


def prepare_metadata():
    metadata = (EVAL_DIR / "eval_metadata.json").read_text()
    numbers = run_numbers(EVAL_DIR)
    for config in CONFIGS:
        for number in numbers:
            run = EVAL_DIR / config / f"run-{number}"
            if not (run / "outputs").is_dir():
                raise FileNotFoundError(run)
            (run / "eval_metadata.json").write_text(metadata)


def write_report():
    numbers = run_numbers(EVAL_DIR)
    count = len(numbers)
    runs = []
    gradings = {config: [] for config in CONFIGS}
    for config in CONFIGS:
        for number in numbers:
            run = EVAL_DIR / config / f"run-{number}"
            grading = json.loads((run / "grading.json").read_text())
            gradings[config].append(grading)
            results = json.loads((run / "validation" / "results.json").read_text())
            runs.append({"eval_id": 0, "eval_name": "customer-directory", "configuration": config,
                         "run_number": number, "result": {**grading["summary"], "time_seconds": None,
                         "tokens": None, "tool_calls": None, "errors": None},
                         "validation": {name: result["exit_code"] for name, result in results.items()},
                         "expectations": grading["expectations"], "metrics": grading["metrics"], "notes": []})
    summary = {config: {"pass_rate": stats([grading["summary"]["pass_rate"] for grading in gradings[config]])}
               for config in CONFIGS}
    delta = summary["with_skill"]["pass_rate"]["mean"] - summary["without_skill"]["pass_rate"]["mean"]
    summary["delta"] = {"pass_rate": f"{delta:+.2f}"}
    notes = []
    for index, expectation in enumerate(gradings["with_skill"][0]["expectations"]):
        counts = [sum(grading["expectations"][index]["passed"] for grading in gradings[config]) for config in CONFIGS]
        if counts != [count, count]:
            notes.append(f"{expectation['text']} With skill {counts[0]}/{count}; without skill {counts[1]}/{count}.")
    common = [expectation["text"] for index, expectation in enumerate(gradings["with_skill"][0]["expectations"])
              if all(grading["expectations"][index]["passed"] for config in CONFIGS for grading in gradings[config])]
    notes.append(f"{len(common)} assertions pass in all {len(runs)} runs; these check correctness/control conditions rather than distinguish the skill.")
    notes.append("The frozen Lombok probe demands @Data and @Builder without handwritten DTO accessors or constructors. The task never explicitly requests a builder API; an annotation-specific failure need not mean failure to remove boilerplate.")
    notes.append("In the original cohort, with-skill runs 2 and 3 combine @RequiredArgsConstructor with scoped lombok.config to generate Objects.requireNonNull; run 1 retains a manual service constructor. Constructor bytecode and null-input execution verify the resulting guard.")
    notes.append("Time, token counts, and executor-wide tool/error counts were not exposed; null means unavailable, not zero. No efficiency claim is supported.")
    notes.append(f"One task with {count} repeats per variant is exploratory, not evidence of statistical significance or broad Java coverage.")
    notes.append("Only generated artifacts were tested. All agents were explicitly told not to build; evaluator success does not prove agent-side verification.")
    notes.append("The skill was explicitly loaded, not auto-triggered. Baseline agents were instructed not to read skills; they shared the repository and inherited agent instructions, so filesystem isolation was not enforced.")
    skill = ROOT.parents[1] / "plexy-java" / "SKILL.md"
    version = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
    benchmark = {
        "metadata": {"skill_name": "plexy-java", "skill_path": "plexy-java/SKILL.md",
                     "executor_model": "gpt-6.1-sol (Junie general-purpose subagents)", "analyzer_model": "gpt-6.1-sol",
                     "timestamp": datetime.now(timezone.utc).isoformat(), "evals_run": [0], "runs_per_configuration": count,
                     "generation_mode": "artifact-only, same inputs and 20-step budget per run",
                     "skill_sha256": hashlib.sha256(skill.read_bytes()).hexdigest(), "java_version": (version.stdout + version.stderr).strip()},
        "runs": runs, "run_summary": summary, "notes": notes,
    }
    inputs = sorted((ROOT / "fixtures" / "customer-directory").rglob("*.java")) + [ROOT / "fixtures" / "customer-directory" / "pom.xml"]
    evidence = inputs + [skill] + [path for path in ROOT.joinpath(".deps").iterdir() if path.suffix == ".jar"]
    evidence += [path for config in CONFIGS for number in numbers
                 for path in (EVAL_DIR / config / f"run-{number}" / "outputs").rglob("*") if path.is_file()]
    benchmark["artifact_sha256"] = {str(path.relative_to(ROOT.parents[1])): hashlib.sha256(path.read_bytes()).hexdigest()
                                    for path in sorted(evidence)}
    (ITERATION / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    lines = ["# Skill Benchmark: plexy-java", "", "- Model: `gpt-6.1-sol`, Junie general-purpose subagents.",
             f"- One frozen customer-directory prompt; {count} independent runs per variant.",
             "- Skill and existing robot/markdown artifacts were not modified.", "", "## Summary", "",
             "| Metric | With Skill | Without Skill | Delta |", "|---|---|---|---|"]
    values = [summary[config]["pass_rate"] for config in CONFIGS]
    lines.append(f"| Assertion pass rate | {values[0]['mean']:.1%} ± {values[0]['stddev']:.1%} | "
                 f"{values[1]['mean']:.1%} ± {values[1]['stddev']:.1%} | {delta:+.1%} |")
    for scenario, label in [("compile", "Compiles"), ("core", "Core behavior"), ("null", "Null-map rejection"), ("io", "IOException propagation")]:
        counts = [sum(run["validation"][scenario] == 0 for run in runs if run["configuration"] == config) for config in CONFIGS]
        lines.append(f"| {label} | {counts[0]}/{count} | {counts[1]}/{count} | — |")
    lines += ["| Generation time / tokens | unavailable | unavailable | unavailable |", "", "## Per-run results", "",
              "| Run | With Skill | Without Skill |", "|---|---|---|"]
    for number in numbers:
        results = [next(run["result"] for run in runs if run["configuration"] == config and run["run_number"] == number)
                   for config in CONFIGS]
        lines.append(f"| {number} | {results[0]['passed']}/{results[0]['total']} | {results[1]['passed']}/{results[1]['total']} |")
    lines += ["", "## Per-assertion results", "",
              "| Assertion | With Skill | Without Skill |", "|---|---|---|"]
    for index, expectation in enumerate(gradings["with_skill"][0]["expectations"]):
        counts = [sum(grading["expectations"][index]["passed"] for grading in gradings[config]) for config in CONFIGS]
        lines.append(f"| {expectation['text']} | {counts[0]}/{count} | {counts[1]}/{count} |")
    lines += ["", "## Observations and limitations", ""] + ["- " + note for note in notes]
    lines += ["", "## Diagnostic variance", "", "| Metric | With Skill (mean ± SD) | Without Skill (mean ± SD) |", "|---|---|---|"]
    for metric in gradings["with_skill"][0]["metrics"]:
        values = [stats([grading["metrics"][metric] for grading in gradings[config]]) for config in CONFIGS]
        lines.append(f"| {metric} | {values[0]['mean']:.1f} ± {values[0]['stddev']:.1f} | {values[1]['mean']:.1f} ± {values[1]['stddev']:.1f} |")
    lines += ["", "- Line length is diagnostic only: the skill specifies no numeric limit.",
              "- Style checks are targeted lexical probes, not a general-purpose Java parser.",
              "- `@Slf4j` and generated service constructors are observed, not required by this DTO-focused Lombok check.",
              "- Source dependency declarations are checked; the Maven lifecycle itself was not executed.", ""]
    (ITERATION / "benchmark.md").write_text("\n".join(lines))
    print(f"With skill {summary['with_skill']['pass_rate']['mean']:.1%}; without skill {summary['without_skill']['pass_rate']['mean']:.1%}; delta {delta:+.1%}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true", help="Prepare prompt metadata before opening ungraded outputs.")
    args = parser.parse_args()
    prepare_metadata()
    if not args.prepare_only:
        write_report()


if __name__ == "__main__":
    main()