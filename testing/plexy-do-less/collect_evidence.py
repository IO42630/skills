#!/usr/bin/env python3
"""Copy completed-run evidence from Junie's runtime, without editing session history."""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "iteration-1" / "eval-0-scoped-timeout-fix"
ASSIGNMENTS = {
    "agent-4": ("do-less-with-1", "with_skill", 1),
    "agent-6": ("do-less-with-2", "with_skill", 2),
    "agent-2": ("do-less-with-3", "with_skill", 3),
    "agent-3": ("do-less-without-1", "without_skill", 1),
    "agent-7": ("do-less-without-2", "without_skill", 2),
    "agent-5": ("do-less-without-3", "without_skill", 3),
}
BLOCKS = {
    "ToolBlockUpdatedEvent",
    "ViewFilesBlockUpdatedEvent",
    "TerminalBlockUpdatedEvent",
    "FileChangesBlockUpdatedEvent",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_dir", type=Path)
    parser.add_argument("--assignments", type=Path,
                        help="JSON mapping agent IDs to [name, configuration, run number].")
    args = parser.parse_args()
    assignments = json.loads(args.assignments.read_text()) if args.assignments else ASSIGNMENTS
    session = args.session_dir.expanduser()
    steps = {agent: {} for agent in assignments}
    with (session / "events.jsonl").open() as events:
        for line in events:
            event = json.loads(line).get("event", {}).get("agentEvent", {})
            agent = event.get("agent", {}).get("id")
            if agent not in steps or event.get("kind") not in BLOCKS:
                continue
            if event.get("agent", {}).get("name") != assignments[agent][0]:
                continue
            step = steps[agent].setdefault(event["stepId"], {})
            if event["kind"] == "ToolBlockUpdatedEvent":
                step["label"] = event.get("text", "")
            step["event"] = {k: v for k, v in event.items() if k != "agent"}
    spec = json.loads((ROOT / "evals" / "evals.json").read_text())["evals"][0]
    metadata = {
        "eval_id": spec["id"],
        "eval_name": "scoped-timeout-fix",
        "prompt": spec["prompt"],
        "assertions": spec["expectations"],
    }
    (EVAL_DIR / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    for agent, (name, config, number) in assignments.items():
        run = EVAL_DIR / config / f"run-{number}"
        if not (run / "outputs" / "reply.txt").is_file():
            raise SystemExit(f"Run is incomplete: {run}")
        source = session / "subagents" / f"{agent}-{name}-transcript.md"
        shutil.copyfile(source, run / "transcript.md")
        trace = {
            "agent": agent,
            "agent_name": name,
            "source": f"{session.name}/events.jsonl",
            "method": "Match agent ID and name; latest runtime block per stepId; "
                      "wrapper calls are not counted separately.",
            "steps": list(steps[agent].values()),
        }
        (run / "trace.json").write_text(json.dumps(trace, indent=2) + "\n")
        (run / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(f"{config}/run-{number}: {len(trace['steps'])} runtime actions captured")


if __name__ == "__main__":
    main()