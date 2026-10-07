#!/usr/bin/env python3
"""Prepare isolated lesson-generation tasks for six fresh existing-agent sessions."""

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITERATION = ROOT / "iteration-2"
EVAL_DIR = ITERATION / "eval-11-recursive-total"
DELIVERY = (
    "Save the complete, self-contained HTML lesson as outputs/lesson.html. "
    "Only that artifact may be written for this content-only evaluation. "
    "Research and browser tools are unavailable. Do not claim to have researched sources, "
    "tested a browser, or observed learner answers. Do not ask follow-up questions; "
    "use the learner context in the request."
)


def main(iteration=ITERATION):
    if iteration.exists():
        raise RuntimeError(f"Refusing to overwrite an existing iteration: {iteration}")
    case = json.loads((ROOT / "evals/evals.json").read_text())["evals"][0]
    skill = (ROOT / "iteration-1/skill_snapshot.md").read_text()
    iteration.mkdir(exist_ok=True)
    (iteration / "skill_snapshot.md").write_text(skill)
    eval_dir = iteration / EVAL_DIR.name
    eval_dir.mkdir(exist_ok=True)
    metadata = {
        "eval_id": case["id"],
        "eval_name": "recursive-total",
        "date": date.today().isoformat(),
        "prompt": case["prompt"],
        "assertions": case["expectations"],
        "delivery_instructions": DELIVERY,
        "executor_model": "Junie general_purpose (gpt-6.1-sol)",
        "runs_per_configuration": 3,
        "skill_sha256": hashlib.sha256(skill.encode()).hexdigest(),
        "scope": "Forced-skill lesson content; no routing, research, workspace-state, or browser checks.",
        "isolation": "Fresh subagents; exclusive run directories; no other project files read.",
        "timing_and_tokens": "Unavailable from the generation interface; report null, not zero.",
    }
    (eval_dir / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    for config in ["with_skill", "without_skill"]:
        for number in [1, 2, 3]:
            run_dir = eval_dir / config / f"run-{number}"
            if run_dir.exists():
                raise RuntimeError(f"Refusing to overwrite an existing attempt: {run_dir}")
            (run_dir / "outputs").mkdir(parents=True)
            prompt = case["prompt"] + "\n\n" + DELIVERY
            if config == "with_skill":
                prompt = "Apply these teaching instructions:\n\n" + skill + "\n\nLearner request:\n" + prompt
            (run_dir / "prompt.txt").write_text(prompt + "\n")
    print(f"Prepared six tasks in {eval_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, choices=range(2, 1000), default=2)
    args = parser.parse_args()
    main(ROOT / f"iteration-{args.iteration}")