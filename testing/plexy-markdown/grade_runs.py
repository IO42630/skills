#!/usr/bin/env python3
"""Grade the plexy-markdown 3A benchmark runs with deterministic checks.

Writes grading.json into every run directory and prints a variance table.
Run from the repo root or anywhere: paths are resolved from this file.
"""

import json
import re
import statistics
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent / "iteration-1" / "eval-0-3as"
CONFIGS = ["with_skill", "without_skill"]
RUNS = [1, 2, 3]

BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
DASH_CHAIN_RE = re.compile(r"(?:\s[\u2014\u2013]\s)|(?:\s-\s)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
URL_ONLY_RE = re.compile(r"^\s*https?://\S+\s*$")


def analyze(text):
    lines = text.splitlines()
    in_fence = False
    in_frontmatter = False
    non_exempt = []
    content_lines = []
    bullets = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if i == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith("|") or stripped.startswith("[//]:") or stripped.startswith("<!--"):
            continue
        if URL_ONLY_RE.match(line):
            continue

        non_exempt.append((i, line))
        if HEADING_RE.match(line):
            continue
        content_lines.append((i, line))
        if BULLET_RE.match(line):
            bullets.append((i, line))

    long_lines = [(i, len(l)) for i, l in non_exempt if len(l) > 120]
    dash_chained = [
        (i, l) for i, l in bullets if DASH_CHAIN_RE.search(BULLET_RE.sub("", l, count=1))
    ]
    bullet_ratio = len(bullets) / len(content_lines) if content_lines else 0.0
    words = re.findall(r"[A-Za-z0-9']+", text)

    return {
        "word_count": len(words),
        "non_exempt_lines": len(non_exempt),
        "max_line_length": max((len(l) for _, l in non_exempt), default=0),
        "mean_line_length": round(
            statistics.mean([len(l) for _, l in non_exempt]), 1
        ) if non_exempt else 0.0,
        "long_lines": long_lines,
        "bullet_lines": len(bullets),
        "content_lines": len(content_lines),
        "bullet_ratio": round(bullet_ratio, 3),
        "dash_chained_bullets": dash_chained,
    }


def coverage_evidence(text):
    found = []
    for label, pattern in [
        ("Authentication", r"authenticat"),
        ("Authorization", r"authoriz"),
        ("Accounting/Auditing", r"accounting|auditing|accountability"),
    ]:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(label)
    return found


def grade(text):
    m = analyze(text)
    found = coverage_evidence(text)
    covered = len(found) == 3

    long_lines = m["long_lines"]
    if long_lines:
        sample_i, sample_len = sorted(long_lines, key=lambda t: -t[1])[0]
        evidence = (
            f"{len(long_lines)} line(s) exceed 120 chars; longest is line {sample_i} "
            f"at {sample_len} chars."
        )
    else:
        evidence = f"Longest non-exempt line is {m['max_line_length']} chars."

    dash = m["dash_chained_bullets"]
    if dash:
        sample_i, sample_line = dash[0]
        evidence = f"{len(dash)} dash-chained bullet(s); e.g. line {sample_i}: {sample_line.strip()[:90]}"
    else:
        evidence = "No bullets chain statements with an em-dash or hyphen."

    ratio = m["bullet_ratio"]
    structure_evidence = (
        f"{m['bullet_lines']}/{m['content_lines']} content lines are bullets "
        f"({ratio * 100:.0f}%)."
    )

    expectations = [
        {
            "text": "The document covers Authentication, Authorization, and Accounting.",
            "passed": covered,
            "evidence": "Found: " + ", ".join(found) + "." if found else "None of the three found.",
        },
        {
            "text": "Every non-exempt line is at most 120 characters.",
            "passed": not long_lines,
            "evidence": evidence,
        },
        {
            "text": "No bullet chains statements with an em-dash or hyphen.",
            "passed": not dash,
            "evidence": evidence,
        },
        {
            "text": "Bullets dominate: at least 80% of content lines are list items.",
            "passed": ratio >= 0.8,
            "evidence": structure_evidence,
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
        "metrics": {
            "word_count": m["word_count"],
            "max_line_length": m["max_line_length"],
            "mean_line_length": m["mean_line_length"],
            "bullet_ratio": m["bullet_ratio"],
            "long_lines": len(m["long_lines"]),
            "dash_chained_bullets": len(m["dash_chained_bullets"]),
        },
    }


def main():
    metrics_by_config = {c: [] for c in CONFIGS}

    for config in CONFIGS:
        for run in RUNS:
            out = EVAL_DIR / config / f"run-{run}" / "outputs" / "3A.md"
            if not out.exists():
                print(f"Missing: {out}")
                continue
            text = out.read_text()
            grading = grade(text)
            grading_path = out.parent.parent / "grading.json"
            grading_path.write_text(json.dumps(grading, indent=2) + "\n")
            metrics_by_config[config].append(grading["metrics"])
            print(
                f"{config}/run-{run}: pass_rate={grading['summary']['pass_rate']} "
                f"words={grading['metrics']['word_count']} "
                f"max_line={grading['metrics']['max_line_length']} "
                f"bullet_ratio={grading['metrics']['bullet_ratio']} "
                f"dash_chains={grading['metrics']['dash_chained_bullets']} "
                f"-> {grading_path.relative_to(EVAL_DIR.parent.parent.parent)}"
            )

    print("\n=== Style variance (mean ± stddev over 3 runs) ===")
    keys = ["word_count", "max_line_length", "mean_line_length", "bullet_ratio",
            "long_lines", "dash_chained_bullets"]
    header = f"{'metric':<22}" + "".join(f"{c:<28}" for c in CONFIGS)
    print(header)
    for key in keys:
        row = f"{key:<22}"
        for config in CONFIGS:
            values = [m[key] for m in metrics_by_config[config]]
            mean = statistics.mean(values)
            std = statistics.stdev(values) if len(values) > 1 else 0.0
            row += f"{mean:>8.1f} ± {std:<16.1f}"
        print(row)


if __name__ == "__main__":
    main()
