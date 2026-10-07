#!/usr/bin/env python3
"""Aggregate this pilot without turning unavailable runtime metrics into zeros."""

import hashlib
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

from grade_runs import CONFIGS, EVAL_DIR, ROOT, RUNS

ITERATION = EVAL_DIR.parent
SKILL = ROOT.parents[1] / "plexy-kiss" / "SKILL.md"


def stats(values):
    if not values:
        return None
    return {
        "mean": statistics.mean(values),
        "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def build_benchmark():
    runs = []
    for config in CONFIGS:
        for number in RUNS:
            directory = EVAL_DIR / config / f"run-{number}"
            grading = json.loads((directory / "grading.json").read_text())
            timing = json.loads((directory / "timing.json").read_text())
            runs.append({
                "eval_id": 0,
                "eval_name": "json-settings",
                "configuration": config,
                "run_number": number,
                "result": {
                    **grading["summary"],
                    "time_seconds": timing["total_duration_seconds"],
                    "tokens": timing["total_tokens"],
                },
                "expectations": grading["expectations"],
                "completion": grading["completion"],
                "metrics": grading.get("metrics", {}),
                "notes": [],
            })
    summary = {}
    for config in CONFIGS:
        selected = [run for run in runs if run["configuration"] == config]
        summary[config] = {
            key: stats([run["result"][key] for run in selected if run["result"][key] is not None])
            for key in ("pass_rate", "time_seconds", "tokens")
        }
        summary[config]["completion_rate"] = stats([int(run["completion"]["passed"]) for run in selected])
        summary[config]["source_lines"] = stats([run["metrics"]["source_lines"] for run in selected if "source_lines" in run["metrics"]])
    delta = summary["with_skill"]["pass_rate"]["mean"] - summary["without_skill"]["pass_rate"]["mean"]
    summary["delta"] = {"pass_rate": f"{delta:+.2f}", "time_seconds": None, "tokens": None}
    notes = [
        "Required completion is reported separately; a structural/style pass cannot cancel a correctness failure.",
        "Source length is descriptive, not a simplicity score; docstrings and annotations affect it.",
        "Timing and token counts were not exposed by the executor; null means unavailable, not zero.",
        f"One prompt with {len(RUNS)} repeats per configuration is a pilot, not evidence of general effectiveness or statistical significance.",
        "Both configurations used Junie general-purpose subagents (gpt-6.1-sol), unlike the earlier deepseek-flash reports; do not compare scores across models/tasks.",
        "Fresh subagent conversations and disjoint outputs were used, but the repository and inherited agent instructions were shared. Baselines were instructed not to consult skills; this is not fully isolated end-to-end skill-trigger testing.",
        "The AST check is a task-specific structural proxy, not a general ban on classes, dependencies, decorators, or asynchronous code.",
        "This case does not test justified interfaces, payment idempotency/security, or DRY across independent concepts.",
    ]
    if all(run["result"]["pass_rate"] == 1 for run in runs):
        checks = sum(run["result"]["total"] for run in runs)
        notes.insert(0, f"All assertions passed in all {len(runs)} runs ({checks}/{checks} checks). No assertion distinguishes skill-enabled from baseline behavior on this task; no observed benefit.")
    return {
        "metadata": {
            "skill_name": "plexy-kiss",
            "skill_path": "plexy-kiss/SKILL.md",
            "skill_sha256": hashlib.sha256(SKILL.read_bytes()).hexdigest(),
            "executor_model": "Junie general-purpose subagent (gpt-6.1-sol)",
            "analyzer_model": "gpt-6.1-sol",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": [0],
            "runs_per_configuration": len(RUNS),
        },
        "runs": runs,
        "run_summary": summary,
        "notes": notes,
    }


def markdown(benchmark):
    metadata = benchmark["metadata"]
    lines = [
        "# Skill Benchmark: plexy-kiss", "",
        f"**Model**: {metadata['executor_model']}",
        f"**Date**: {metadata['timestamp']}",
        f"**Evals**: 0 ({metadata['runs_per_configuration']} runs each per configuration)", "",
        "## Summary", "",
        "| Metric | With Skill | Without Skill | Delta |",
        "|--------|------------|---------------|-------|",
    ]
    summary = benchmark["run_summary"]
    for key, label, multiplier in (("pass_rate", "Pass rate", 100), ("completion_rate", "Required completion", 100), ("source_lines", "Source lines", 1)):
        cells = []
        for config in CONFIGS:
            value = summary[config][key]
            suffix = "%" if multiplier == 100 else ""
            cells.append(f"{value['mean'] * multiplier:.1f}{suffix} ± {value['stddev'] * multiplier:.1f}{suffix}" if value else "Unavailable")
        delta = summary["with_skill"][key]["mean"] - summary["without_skill"][key]["mean"] if all(summary[config][key] for config in CONFIGS) else None
        lines.append(f"| {label} | {' | '.join(cells)} | {delta * multiplier:+.1f} |" if delta is not None else f"| {label} | {' | '.join(cells)} | — |")
    lines.extend(["| Time | Unavailable | Unavailable | — |", "| Tokens | Unavailable | Unavailable | — |", "", "## Notes", ""])
    lines.extend(f"- {note}" for note in benchmark["notes"])
    return "\n".join(lines) + "\n"


def main():
    benchmark = build_benchmark()
    (ITERATION / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")
    (ITERATION / "benchmark.md").write_text(markdown(benchmark), encoding="utf-8")
    metadata = (EVAL_DIR / "eval_metadata.json").read_text(encoding="utf-8")
    for config in CONFIGS:
        for number in RUNS:
            (EVAL_DIR / config / f"run-{number}" / "eval_metadata.json").write_text(metadata, encoding="utf-8")
    print(f"Generated {ITERATION / 'benchmark.json'} and benchmark.md")


if __name__ == "__main__":
    main()