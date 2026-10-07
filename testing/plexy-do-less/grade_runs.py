#!/usr/bin/env python3
"""Grade the scoped timeout fix using behavior, source scope, and runtime evidence."""

import ast
import json
import re
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
ITERATION = ROOT / "iteration-1"
EVAL_DIR = ITERATION / "eval-0-scoped-timeout-fix"
CONFIGS = ["with_skill", "without_skill"]
TEST_COMMAND = "python3 -m unittest -v test_timeout.py"
PREAMBLE_RE = re.compile(r"^\s*(sure\b|certainly\b|of course\b|let me\b|i['’]ll\b|happy to\b)", re.I)
BEHAVIOR_CHECK = """
import json
import timeout

def rejects(function, value, message=False):
    try:
        function(value)
    except ValueError as error:
        return not message or str(error) == "timeout must be non-negative"
    return False

values = [0, 0.5, 1, 1500, 60000]
conversion = all(timeout.milliseconds_to_seconds(x) == x / 1000 for x in values)
negative = all(rejects(timeout.milliseconds_to_seconds, x, True) for x in [-1, -0.5])
caller = all(timeout.request_options(x) == {"timeout": x / 1000, "retries": 2} for x in values)
caller = caller and rejects(timeout.request_options, -1)
print(json.dumps({"conversion": conversion, "preserved": negative and caller}))
"""


def normalized_source(text):
    tree = ast.parse(text)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == "milliseconds_to_seconds")
    if not isinstance(function.body[-1], ast.Return):
        raise ValueError("Conversion return statement missing")
    function.body[-1].value = ast.Constant(value=None)
    return ast.dump(tree)


def successful_test(events):
    return any(
        event.get("kind") == "TerminalBlockUpdatedEvent"
        and TEST_COMMAND in event.get("command", "")
        and event.get("exitCode") == 0
        and re.search(r"^OK\s*$", event.get("output", ""), re.M)
        and "Ran 3 tests" in event.get("output", "")
        for event in events
    )


def investigation(steps, output):
    allowed = {output / name for name in ["timeout.py", "test_timeout.py"]}
    snapshot = ITERATION / "skill-snapshot" / "SKILL.md"
    calls = 0
    violations = []
    loaded = False
    for step in steps:
        event = step["event"]
        kind = event["kind"]
        if kind == "ViewFilesBlockUpdatedEvent":
            paths = [file["relativePath"] for file in event.get("files", [])]
            resolved = []
            for path in paths:
                candidate = Path(path)
                if not candidate.is_absolute():
                    candidate = (output if candidate.name == str(candidate) else REPO) / candidate
                resolved.append(candidate.resolve())
            if resolved == [snapshot.resolve()]:
                loaded = "unavailable" not in event.get("details", "").lower()
                continue
            calls += 1
            if not resolved or any(path not in allowed for path in resolved):
                violations.append(f"Read outside task files: {paths}")
        elif kind == "ToolBlockUpdatedEvent":
            calls += 1
            violations.append(f"Other investigation/delegation action: {step.get('label', '')}")
        elif kind == "TerminalBlockUpdatedEvent":
            command = event.get("command", "")
            if TEST_COMMAND not in command:
                calls += 1
                violations.append(f"Non-test terminal investigation: {command}")
    return calls, violations, loaded


def grade_run(run, assertions):
    output = run / "outputs"
    steps = json.loads((run / "trace.json").read_text())["steps"]
    events = [step["event"] for step in steps]
    behavior = subprocess.run([sys.executable, "-B", "-c", BEHAVIOR_CHECK], cwd=output,
                              capture_output=True, text=True, timeout=10)
    checked = json.loads(behavior.stdout) if behavior.returncode == 0 else {}
    acceptance = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_timeout.py"],
                                cwd=output, capture_output=True, text=True, timeout=10)
    (run / "verification.txt").write_text(acceptance.stdout + acceptance.stderr
                                         + f"\nExit code: {acceptance.returncode}\n")
    original = ROOT / "evals" / "fixtures"
    try:
        scoped = normalized_source((output / "timeout.py").read_text()) == normalized_source(
            (original / "timeout.py").read_text())
    except (SyntaxError, ValueError, StopIteration):
        scoped = False
    scoped = scoped and (output / "test_timeout.py").read_bytes() == (original / "test_timeout.py").read_bytes()
    scoped = scoped and {p.name for p in output.iterdir() if p.suffix == ".py"} == {
        "timeout.py", "test_timeout.py"}
    calls, violations, loaded = investigation(steps, output)
    reply = (output / "reply.txt").read_text()
    words = len(re.findall(r"\b[\w'’]+\b", reply))
    verdicts = [
        (checked.get("conversion", False), f"Behavioral probes: {checked}; exit={behavior.returncode}."),
        (checked.get("preserved", False), "Negative values and caller checked by behavioral probes."),
        (scoped, "AST comparison ignores only the conversion expression; tests compared byte-for-byte."),
        (successful_test(events), "Recorded terminal command, exit code, test count, and OK required."),
        (not violations, f"{calls} task investigation calls; violations: {violations}."),
        (0 < words <= 60 and not PREAMBLE_RE.search(reply), f"{words} words; reply begins {reply[:70]!r}."),
    ]
    expected_loaded = run.parent.name == "with_skill"
    if loaded != expected_loaded:
        raise ValueError(f"Skill-loading contrast not confirmed for {run}")
    expectations = [dict(text=text, passed=bool(passed), evidence=evidence)
                    for text, (passed, evidence) in zip(assertions, verdicts)]
    passed = sum(item["passed"] for item in expectations)
    completed = all(item["passed"] for item in expectations[:4]) and acceptance.returncode == 0
    metrics = {
        "word_count": words,
        "investigation_calls": calls,
        "recorded_runtime_actions": len(steps),
        "test_commands": sum(event["kind"] == "TerminalBlockUpdatedEvent" for event in events),
        "skill_loading": "confirmed" if loaded else "not_loaded",
        "task_completed": completed,
    }
    grading = {
        "expectations": expectations,
        "summary": dict(passed=passed, failed=len(expectations) - passed,
                        total=len(expectations), pass_rate=passed / len(expectations)),
        "execution_metrics": {"total_tool_calls": len(steps), "output_chars": len(reply)},
        "timing": json.loads((run / "timing.json").read_text()),
        "metrics": metrics,
        "eval_feedback": {
            "overall": "One obvious bug cannot establish behavior on migrations or shared-state changes; "
                       "scope and word-limit assertions are calibrated to this task only."
        },
    }
    (run / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
    print(f"{run.parent.name}/{run.name}: {passed}/{len(expectations)}; complete={completed}; "
          f"investigation={calls}; words={words}")
    return grading


def stats(values):
    return dict(mean=statistics.mean(values), stddev=statistics.stdev(values),
                min=min(values), max=max(values))


def main():
    spec = json.loads((ROOT / "evals" / "evals.json").read_text())["evals"][0]
    count = json.loads((ITERATION / "manifest.json").read_text())["runs_per_configuration"]
    runs = []
    summary = {}
    for config in CONFIGS:
        grades = []
        for number in range(1, count + 1):
            grading = grade_run(EVAL_DIR / config / f"run-{number}", spec["expectations"])
            grades.append(grading)
            runs.append({
                "eval_id": 0, "eval_name": "scoped-timeout-fix", "configuration": config,
                "run_number": number,
                "result": {**grading["summary"], "time_seconds": None, "tokens": None,
                           "tool_calls": grading["execution_metrics"]["total_tool_calls"]},
                "expectations": grading["expectations"], "metrics": grading["metrics"], "notes": [],
            })
        summary[config] = {"pass_rate": stats([g["summary"]["pass_rate"] for g in grades]),
                           "time_seconds": None, "tokens": None}
        for name in ["word_count", "investigation_calls", "recorded_runtime_actions", "test_commands"]:
            summary[config][name] = stats([g["metrics"][name] for g in grades])
        summary[config]["completion_rate"] = stats([int(g["metrics"]["task_completed"]) for g in grades])
    delta = summary["with_skill"]["pass_rate"]["mean"] - summary["without_skill"]["pass_rate"]["mean"]
    summary["delta"] = {"pass_rate": f"{delta:+.2f}", "time_seconds": None, "tokens": None}
    notes = [
        "Completion is reported separately from efficiency/style; all four task requirements must pass.",
        "Tool counts include failed structure lookups; inherited Junie instructions require these lookups.",
        "Investigation counts exclude skill loading, required tests, edits, and evidence writes.",
        "Timing and tokens are unavailable; output characters are not reported as tokens.",
        f"A single task and {count} repeats are a smoke test; no general or statistically significant claim.",
        "This tests explicitly loaded instructions, not automatic triggering or global skill isolation.",
    ]
    for name, label in [("word_count", "Reply words"), ("investigation_calls", "Investigation calls")]:
        a, b = summary["with_skill"][name], summary["without_skill"][name]
        notes.append(f"{label}: with skill {a['mean']:.1f} ± {a['stddev']:.1f}; "
                     f"without skill {b['mean']:.1f} ± {b['stddev']:.1f}.")
    benchmark = {
        "metadata": {"skill_name": "plexy-do-less", "executor_model": "gpt-6.1-sol (Junie)",
                     "timestamp": datetime.now(timezone.utc).isoformat(), "evals_run": [0],
                     "runs_per_configuration": count},
        "runs": runs, "run_summary": summary, "notes": notes,
    }
    (ITERATION / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    rows = ["# Skill Benchmark: plexy-do-less", "", f"- One scoped bug-fix task; {count} runs per configuration.",
            "- Model: `gpt-6.1-sol` through Junie general-purpose subagents.", "",
            "| Metric | With skill | Without skill | Delta |", "|---|---|---|---|"]
    for name, label in [("completion_rate", "Task completion"), ("pass_rate", "All assertions"),
                        ("word_count", "Reply words"), ("investigation_calls", "Investigation calls"),
                        ("recorded_runtime_actions", "Runtime actions"), ("test_commands", "Test commands")]:
        a, b = summary["with_skill"][name], summary["without_skill"][name]
        factor = 100 if name.endswith("rate") else 1
        suffix = "%" if factor == 100 else ""
        rows.append(f"| {label} | {a['mean'] * factor:.1f}{suffix} ± {a['stddev'] * factor:.1f} | "
                    f"{b['mean'] * factor:.1f}{suffix} ± {b['stddev'] * factor:.1f} | "
                    f"{(a['mean'] - b['mean']) * factor:+.1f}{suffix} |")
    rows.extend(["| Time / tokens | Not available | Not available | Not measured |", "", "## Notes", ""])
    rows.extend(f"- {note}" for note in notes)
    (ITERATION / "benchmark.md").write_text("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()