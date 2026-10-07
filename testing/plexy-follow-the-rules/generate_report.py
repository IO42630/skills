#!/usr/bin/env python3
"""Aggregate saved grades and generate the standard skill-creator static viewer."""

import __future__
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
ITERATION = ROOT / "iteration-1"
CREATOR = PROJECT / ".agents" / "skills" / "skill-creator"


def main():
    spec = importlib.util.spec_from_file_location("aggregate_benchmark", CREATOR / "scripts" / "aggregate_benchmark.py")
    aggregator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aggregator)
    benchmark = aggregator.generate_benchmark(ITERATION, "plexy-follow-the-rules", "plexy-follow-the-rules/SKILL.md")
    provenance = json.loads((ITERATION / "execution.json").read_text())
    benchmark["metadata"].update({
        "executor_model": provenance["executor_model"],
        "analyzer_model": provenance["executor_model"],
        "skill_sha256": hashlib.sha256((PROJECT / provenance["skill_path"]).read_bytes()).hexdigest(),
        "resource_metrics_available": False,
    })
    counts = {}
    for config in ["with_skill", "without_skill"]:
        runs = [run for run in benchmark["runs"] if run["configuration"] == config]
        counts[config] = {
            "runs": len(runs),
            "passed": sum(run["result"]["passed"] for run in runs),
            "total": sum(run["result"]["total"] for run in runs),
        }
    benchmark["metadata"]["runs_per_configuration"] = counts["with_skill"]["runs"]
    benchmark["notes"] = [
        f"With skill: {counts['with_skill']['passed']}/{counts['with_skill']['total']} assertions across "
        f"{counts['with_skill']['runs']} runs. Without skill: "
        f"{counts['without_skill']['passed']}/{counts['without_skill']['total']} assertions across "
        f"{counts['without_skill']['runs']} runs.",
        "Every assertion is non-discriminating on this task. Correctness and convention adherence were preserved, but no incremental skill benefit or harm was demonstrated.",
        "The baseline already receives explicit fixture guidelines, a naming reference, the user override, and shared Junie code-style instructions. This is a ceiling-effect smoke test, not evidence that the skill never helps.",
        "These are repetitions of one task, not additional task coverage; ambiguous conventions, material instruction conflicts, unavailable libraries, and broader project migrations remain untested.",
        "Runs 4 and 5 in each configuration are four additional independent executions of the unchanged prompt and skill. They used the current fixture with postponed annotations; the original six outputs were retained.",
        "Current executor: gpt-6.1-sol via Junie subagents. Earlier robot/markdown benchmarks used a different runtime/model; their scores are not a controlled cross-skill comparison.",
        "Timing, tokens, executor tool-call counts, and executor error counts were not exposed. These values are null, not zero; source characters are not treated as tokens.",
        *provenance["protocol_deviations"],
    ]
    markdown = aggregator.generate_markdown(benchmark)
    markdown = "\n".join(
        f"**Evals**: {len(benchmark['metadata']['evals_run'])} "
        f"({benchmark['metadata']['runs_per_configuration']} runs each per configuration)"
        if line.startswith("**Evals**:") else
        "| Time | Not measured | Not measured | N/A |" if line.startswith("| Time |") else
        "| Tokens | Not measured | Not measured | N/A |" if line.startswith("| Tokens |") else line
        for line in markdown.splitlines()
    )
    for config in ["with_skill", "without_skill"]:
        for metric in ["time_seconds", "tokens"]:
            benchmark["run_summary"][config][metric] = None
            benchmark["run_summary"]["delta"][metric] = None
    for run in benchmark["runs"]:
        run["eval_name"] = "native-account-action"
        for metric in ["time_seconds", "tokens", "tool_calls", "errors"]:
            run["result"][metric] = None
        run_dir = ITERATION / "eval-0-native-account-action" / run["configuration"] / f"run-{run['run_number']}"
        run["notes"] = ["See iteration-1/execution.json for self-reported execution provenance and deviations."]
        metadata = ITERATION / "eval-0-native-account-action" / "eval_metadata.json"
        (run_dir / "eval_metadata.json").write_text(metadata.read_text())
    (ITERATION / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    (ITERATION / "benchmark.md").write_text(markdown + "\n")
    print(markdown)

    viewer = CREATOR / "eval-viewer" / "generate_review.py"
    sys.argv = [str(viewer), str(ITERATION), "--skill-name", "plexy-follow-the-rules",
                "--benchmark", str(ITERATION / "benchmark.json"), "--static", str(ITERATION / "review.html")]
    # Postpone the upstream viewer's union annotations on the installed Python 3.9.
    code = compile(viewer.read_text(), str(viewer), "exec", flags=__future__.annotations.compiler_flag)
    exec(code, {"__name__": "__main__", "__file__": str(viewer)})


if __name__ == "__main__":
    main()