#!/usr/bin/env python3
"""Prepare isolated copies of the fixed timeout task; never overwrite runs."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "iteration-1" / "eval-0-scoped-timeout-fix"
SKILL = ROOT.parent.parent / "plexy-do-less" / "SKILL.md"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--additional-runs", type=int, default=0,
                        help="Append this many runs per configuration to an existing iteration.")
    args = parser.parse_args()
    if args.additional_runs < 0:
        parser.error("--additional-runs must be non-negative")
    if EVAL_DIR.exists() and not args.additional_runs:
        raise SystemExit(f"Refusing to overwrite {EVAL_DIR}")
    if args.additional_runs and not EVAL_DIR.exists():
        raise SystemExit("Prepare the initial iteration before appending runs")
    spec = json.loads((ROOT / "evals" / "evals.json").read_text())["evals"][0]
    metadata = {
        "eval_id": spec["id"],
        "eval_name": "scoped-timeout-fix",
        "prompt": spec["prompt"],
        "assertions": spec["expectations"],
    }
    snapshot = ROOT / "iteration-1" / "skill-snapshot" / "SKILL.md"
    fixtures = [source for source in (ROOT / "evals" / "fixtures").iterdir()
                if source.suffix == ".py"]
    hashes = {source.name: hashlib.sha256(source.read_bytes()).hexdigest() for source in fixtures}
    if args.additional_runs:
        manifest = json.loads((ROOT / "iteration-1" / "manifest.json").read_text())
        if (manifest["fixture_sha256"] != hashes
                or manifest["skill_sha256"] != hashlib.sha256(snapshot.read_bytes()).hexdigest()
                or manifest["skill_sha256"] != hashlib.sha256(SKILL.read_bytes()).hexdigest()
                or metadata != json.loads((EVAL_DIR / "eval_metadata.json").read_text())):
            raise SystemExit("Skill, fixtures, or evaluation changed; use a new iteration")
        first = manifest["runs_per_configuration"] + 1
        last = manifest["runs_per_configuration"] + args.additional_runs
    else:
        first, last = 1, 3
        manifest = {
            "skill_sha256": hashlib.sha256(SKILL.read_bytes()).hexdigest(),
            "fixture_sha256": hashes,
            "executor_model": "gpt-6.1-sol (Junie general-purpose subagent)",
            "baseline": "No explicitly loaded skill; inherited agent instructions remain identical.",
        }
    for config in ["with_skill", "without_skill"]:
        for run in range(first, last + 1):
            target = EVAL_DIR / config / f"run-{run}"
            if target.exists():
                raise SystemExit(f"Refusing to overwrite {target}")
    if not args.additional_runs:
        EVAL_DIR.mkdir(parents=True)
        snapshot.parent.mkdir()
        shutil.copyfile(SKILL, snapshot)
        (EVAL_DIR / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    for config in ["with_skill", "without_skill"]:
        for run in range(first, last + 1):
            output = EVAL_DIR / config / f"run-{run}" / "outputs"
            output.mkdir(parents=True)
            for source in fixtures:
                shutil.copyfile(source, output / source.name)
            (output.parent / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    manifest["runs_per_configuration"] = last
    (ROOT / "iteration-1" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Prepared {EVAL_DIR}: runs {first}-{last} for each configuration.")


if __name__ == "__main__":
    main()