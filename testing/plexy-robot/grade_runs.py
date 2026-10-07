#!/usr/bin/env python3
"""Grade the plexy-robot race-condition benchmark runs with deterministic checks.

Writes grading.json into every run directory and prints a variance table.
Run from the repo root or anywhere: paths are resolved from this file.
"""

import json
import re
import statistics
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent / "iteration-1" / "eval-0-race"
CONFIGS = ["with_skill", "without_skill"]
RUNS = [1, 2, 3]

PREFIX_RE = re.compile(r"^\s*\.\.\.\s")
FILLER_RE = re.compile(
    r"\b(sure|certainly|of course|just|really|basically|actually|happy to|great question)\b",
    re.IGNORECASE,
)
CONCURRENCY_RE = re.compile(
    r"\b(concurrent|concurrency|parallel|thread|process(?:es)?|simultaneous|interleav\w*)\b",
    re.IGNORECASE,
)
FIX_RE = re.compile(
    r"\b(lock|mutex|atomic|semaphore|synchroniz\w*|transaction)\b", re.IGNORECASE
)


def analyze(text):
    stripped = text.strip()
    words = re.findall(r"[A-Za-z0-9']+", text)
    filler_hits = sorted({m.group(0).lower() for m in FILLER_RE.finditer(text)})
    concurrency_hits = sorted({m.group(0).lower() for m in CONCURRENCY_RE.finditer(text)})
    fix_hits = sorted({m.group(0).lower() for m in FIX_RE.finditer(text)})
    return {
        "word_count": len(words),
        "has_prefix": bool(PREFIX_RE.match(stripped)),
        "filler_hits": filler_hits,
        "concurrency_hits": concurrency_hits,
        "fix_hits": fix_hits,
    }


def grade(text):
    m = analyze(text)

    prefix_evidence = "Reply starts with `... `." if m["has_prefix"] else (
        f"First characters: {text.strip()[:40]!r}"
    )

    terse_evidence = f"{m['word_count']} words."

    filler_evidence = (
        "Filler found: " + ", ".join(m["filler_hits"]) + "."
        if m["filler_hits"]
        else "No filler or pleasantry words found."
    )

    accurate = bool(m["concurrency_hits"]) and bool(m["fix_hits"])
    accuracy_evidence = (
        f"Concurrency terms: {', '.join(m['concurrency_hits']) or 'none'}; "
        f"fix terms: {', '.join(m['fix_hits']) or 'none'}."
    )

    expectations = [
        {
            "text": "The reply begins with literal `... ` (three dots and a space).",
            "passed": m["has_prefix"],
            "evidence": prefix_evidence,
        },
        {
            "text": "The reply is terse: at most 50 words.",
            "passed": m["word_count"] <= 50,
            "evidence": terse_evidence,
        },
        {
            "text": "The reply contains no filler or pleasantry words (sure, certainly, of course, just, really, basically, actually, happy to, great question).",
            "passed": not m["filler_hits"],
            "evidence": filler_evidence,
        },
        {
            "text": "The reply is accurate: it ties race conditions to concurrent/shared state and names a synchronization fix (lock, mutex, atomic, semaphore, transaction).",
            "passed": accurate,
            "evidence": accuracy_evidence,
        },
    ]

    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)
    return {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 2),
        },
        "execution_metrics": {
            "output_chars": len(text),
            "total_tool_calls": 0,
            "errors_encountered": 0,
        },
        "timing": {"total_duration_seconds": 0.0},
        "metrics": {"word_count": m["word_count"]},
    }


def main():
    metrics_by_config = {c: [] for c in CONFIGS}

    for config in CONFIGS:
        for run in RUNS:
            reply = EVAL_DIR / config / f"run-{run}" / "outputs" / "reply.txt"
            if not reply.exists():
                print(f"Missing: {reply}")
                continue
            text = reply.read_text()
            grading = grade(text)
            grading_path = reply.parent.parent / "grading.json"
            grading_path.write_text(json.dumps(grading, indent=2) + "\n")
            metrics_by_config[config].append(grading["metrics"])
            print(
                f"{config}/run-{run}: pass_rate={grading['summary']['pass_rate']} "
                f"words={grading['metrics']['word_count']} "
                f"prefix={grading['expectations'][0]['passed']} "
                f"filler={grading['expectations'][2]['passed']} "
                f"-> {grading_path.relative_to(EVAL_DIR.parent.parent.parent)}"
            )

    print("\n=== Reply length variance (mean +/- stddev over 3 runs) ===")
    for config in CONFIGS:
        values = [m["word_count"] for m in metrics_by_config[config]]
        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        print(f"{config:<16} words: {mean:.1f} +/- {std:.1f}  (runs: {values})")


if __name__ == "__main__":
    main()
