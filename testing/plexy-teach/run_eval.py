#!/usr/bin/env python3
"""Run a six-output, tool-free content comparison using the existing OpenCode CLI."""

import argparse
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
ITERATION = ROOT / "iteration-1"
EVAL_DIR = ITERATION / "eval-11-recursive-total"
MODEL = "opencode/deepseek-v4-flash-free"
DELIVERY = (
    "Return the complete HTML lesson in your final response, without Markdown fences or commentary. "
    "File, research, and browser tools are unavailable in this content-only evaluation. "
    "Do not claim to have researched sources, saved files, tested a browser, or observed learner answers. "
    "Do not ask follow-up questions; use the learner context in the request."
)


def prepare():
    ITERATION.mkdir(parents=True, exist_ok=True)
    eval_path = ROOT / "evals" / "evals.json"
    if not eval_path.exists():
        source = json.loads((REPO / "plexy-teach/evals/evals.json").read_text())
        case = next(case for case in source["evals"] if case["id"] == 11)
        eval_path.parent.mkdir(parents=True, exist_ok=True)
        eval_path.write_text(json.dumps({"skill_name": "plexy-teach", "evals": [case]}, indent=2) + "\n")
    case = json.loads(eval_path.read_text())["evals"][0]
    snapshot = ITERATION / "skill_snapshot.md"
    if not snapshot.exists():
        snapshot.write_text((REPO / "plexy-teach/SKILL.md").read_text())
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    metadata = {
        "eval_id": case["id"],
        "eval_name": "recursive-total",
        "prompt": case["prompt"],
        "assertions": case["expectations"],
        "delivery_instructions": DELIVERY,
        "executor_model": MODEL,
        "runs_per_configuration": 3,
        "skill_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        "scope": "Forced-skill, tool-free lesson content only; not routing or workspace workflow.",
    }
    (EVAL_DIR / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return case, snapshot.read_text()


def run(config, number, case, skill):
    run_dir = EVAL_DIR / config / f"run-{number}"
    if run_dir.exists():
        raise RuntimeError(f"Refusing to overwrite an existing attempt: {run_dir}")
    outputs = run_dir / "outputs"
    outputs.mkdir(parents=True)
    prompt = case["prompt"] + "\n\n" + DELIVERY
    if config == "with_skill":
        prompt = "Apply these teaching instructions:\n\n" + skill + "\n\nLearner request:\n" + prompt
    (run_dir / "prompt.txt").write_text(prompt + "\n")
    # An explicitly tool-free agent prevents loading other skills or reading benchmark criteria.
    agent = {
        "description": "Isolated lesson-content benchmark",
        "mode": "primary",
        "prompt": "Respond to the user's request. " + DELIVERY,
        "tools": {"*": False},
        "permission": {"*": "deny"},
    }
    env = os.environ.copy()
    env.update({
        "OPENCODE_CONFIG_CONTENT": json.dumps({
            "agent": {"lesson-benchmark": agent},
            "instructions": [],
            "share": "disabled",
            "autoupdate": False,
            "snapshot": False,
        }),
        "OPENCODE_DISABLE_CLAUDE_CODE": "true",
        "OPENCODE_DISABLE_AUTOUPDATE": "true",
    })
    command = [
        "opencode", "run", "--pure", "--agent", "lesson-benchmark", "--model", MODEL,
        "--format", "json", "--dir", str(outputs), prompt,
    ]
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    with (run_dir / "events.jsonl").open("w") as stdout, (run_dir / "stderr.txt").open("w") as stderr:
        try:
            result = subprocess.run(command, env=env, stdout=stdout, stderr=stderr, timeout=240)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            exit_code = 124
    events = []
    for line in (run_dir / "events.jsonl").read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    texts = [event["part"]["text"] for event in events if event.get("type") == "text"]
    response = "\n".join(texts).strip()
    (outputs / "reply.txt").write_text(response + "\n")
    # Keep the original response; only unwrap fences for the inspectable artifact.
    html = response
    if html.startswith("```") and html.endswith("```"):
        html = html.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    if html.lower().startswith(("<!doctype html", "<html")):
        (outputs / "lesson.html").write_text(html + "\n")
    finishes = [event["part"] for event in events if event.get("type") == "step_finish"]
    tokens = [part["tokens"] for part in finishes if "tokens" in part]
    errors = [event for event in events if event.get("type") == "error"]
    tool_calls = sum(event.get("type") == "tool_use" for event in events)
    execution = {
        "model": MODEL,
        "agent": "lesson-benchmark",
        "started_at": started,
        "duration_seconds": round(time.monotonic() - start, 3),
        "exit_code": exit_code,
        "tokens": tokens or None,
        "tool_calls": tool_calls,
        "errors": errors,
        "successful_generation": exit_code == 0 and not errors and (outputs / "lesson.html").exists(),
    }
    (run_dir / "execution.json").write_text(json.dumps(execution, indent=2) + "\n")
    print(f"{config}/run-{number}: success={execution['successful_generation']} time={execution['duration_seconds']}s", flush=True)
    if not execution["successful_generation"]:
        raise RuntimeError(f"Generation failed; inspect {run_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration", choices=["with_skill", "without_skill"])
    parser.add_argument("--run", type=int, choices=[1, 2, 3])
    args = parser.parse_args()
    if bool(args.configuration) != bool(args.run):
        parser.error("Supply both --configuration and --run, or neither for all six attempts.")
    case, skill = prepare()
    if args.configuration:
        run(args.configuration, args.run, case, skill)
    else:
        for number in [1, 2, 3]:
            order = ["without_skill", "with_skill"] if number % 2 else ["with_skill", "without_skill"]
            for config in order:
                run(config, number, case, skill)


if __name__ == "__main__":
    main()