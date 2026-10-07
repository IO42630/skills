#!/usr/bin/env python3
"""Run the installed skill-creator viewer with deferred annotations on Python 3.9."""

import __future__
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GENERATOR = ROOT.parent.parent / ".agents" / "skills" / "skill-creator" / "eval-viewer" / "generate_review.py"
ITERATION = ROOT / "iteration-1"


if __name__ == "__main__":
    sys.argv = [str(GENERATOR), str(ITERATION), "--skill-name", "plexy-do-less",
                "--benchmark", str(ITERATION / "benchmark.json"),
                "--static", str(ITERATION / "review.html")]
    code = compile(GENERATOR.read_text(), str(GENERATOR), "exec",
                   flags=__future__.annotations.compiler_flag)
    exec(code, {"__name__": "__main__", "__file__": str(GENERATOR)})