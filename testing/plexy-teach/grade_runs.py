#!/usr/bin/env python3
"""Combine explicit content reviews with static HTML metrics; never infer teaching quality from keywords."""

import argparse
import json
import re
import statistics
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITERATION = ROOT / "iteration-2"
EVAL_DIR = ITERATION / "eval-11-recursive-total"
CONFIGS = ["with_skill", "without_skill"]
RUNS = [1, 2, 3]


class LessonParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.tags = []
        self.text = []
        self.language = None
        self.dependencies = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attributes = dict(attrs)
        if tag in ["style", "script"]:
            self.hidden += 1
        if tag == "html":
            self.language = attributes.get("lang")
        if tag in ["script", "img", "source", "iframe", "audio", "video", "object", "embed"]:
            for key in ["src", "srcset", "data", "poster"]:
                if attributes.get(key):
                    self.dependencies.append(attributes[key])
        if tag == "link" and "stylesheet" in attributes.get("rel", "").split():
            self.dependencies.append(attributes.get("href", ""))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ["style", "script"]:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)


def analyze(html):
    parser = LessonParser()
    parser.feed(html)
    parser.close()
    words = re.findall(r"[A-Za-z0-9']+", " ".join(parser.text))
    dependencies = parser.dependencies + re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", html, re.IGNORECASE)
    dependencies += re.findall(r"@import\s+['\"]([^'\"]+)", html, re.IGNORECASE)
    required = [value for value in dependencies if not value.startswith(("data:", "#"))]
    return {
        "word_count": len(words),
        "html_chars": len(html),
        "heading_count": sum(parser.tags.count(f"h{number}") for number in range(1, 7)),
        "code_blocks": parser.tags.count("pre"),
        "scripts": parser.tags.count("script"),
        "answer_reveals": parser.tags.count("details"),
        "has_semantic_structure": all(tag in parser.tags for tag in ["html", "title", "main", "h1"]),
        "has_language": bool(parser.language),
        "required_dependencies": required,
        "static_self_contained": not required,
    }


def grade(html, expectations, review=None):
    checks = []
    if review is not None:
        checks = review.get("expectations", [])
        if len(checks) != len(expectations):
            raise ValueError("Review must address every frozen expectation exactly once.")
        for expected, check in zip(expectations, checks):
            if check.get("text") != expected:
                raise ValueError("Review differs from the frozen expectation order or text.")
            if (check.get("passed") is not None and not isinstance(check.get("passed"), bool)) or not isinstance(check.get("evidence"), str):
                raise ValueError("Each reviewed expectation needs a boolean/null result and evidence.")
            if not check["evidence"].strip():
                raise ValueError("Review evidence must not be empty.")
    if html is None:
        checks = [{"text": text, "passed": False, "evidence": "HTML artifact is missing."} for text in expectations]
        metrics = None
    else:
        metrics = analyze(html)
        if review is None:
            checks = [{"text": text, "passed": None, "evidence": "Content review not performed."} for text in expectations]
    passed = sum(check["passed"] is True for check in checks)
    failed = sum(check["passed"] is False for check in checks)
    unverified = sum(check["passed"] is None for check in checks)
    return {
        "expectations": checks,
        "summary": {
            "passed": passed,
            "failed": failed,
            "unverified": unverified,
            "total": len(checks),
            "pass_rate": passed / len(checks) if checks and not unverified else None,
        },
        "metrics": metrics,
        "review_method": "Explicit artifact inspection by the parent assistant; not a blind or independent judge.",
        "unavailable_checks": ["Browser rendering", "Keyboard interaction", "JavaScript-disabled rendering", "Print preview", "Narrow-screen layout", "Source research", "Skill routing", "Persistent workspace workflow"],
    }


def distribution(values):
    available = [value for value in values if value is not None]
    return {
        "mean": statistics.mean(available) if available else None,
        "stddev": statistics.stdev(available) if len(available) > 1 else (0.0 if available else None),
        "values": values,
    }


def main(iteration=ITERATION):
    eval_dir = iteration / EVAL_DIR.name
    metadata = json.loads((eval_dir / "eval_metadata.json").read_text())
    records = []
    for config in CONFIGS:
        for number in RUNS:
            run_dir = eval_dir / config / f"run-{number}"
            path = run_dir / "outputs/lesson.html"
            review_path = run_dir / "content_review.json"
            review = json.loads(review_path.read_text()) if review_path.exists() else None
            grading = grade(path.read_text() if path.exists() else None, metadata["assertions"], review)
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
            (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
            records.append({
                "eval_id": metadata["eval_id"],
                "eval_name": metadata["eval_name"],
                "configuration": config,
                "run_number": number,
                "result": grading["summary"],
                "metrics": grading["metrics"],
                "expectations": grading["expectations"],
                "time_seconds": None,
                "tokens": None,
            })
            print(f"{config}/run-{number}: {grading['summary']}")
    aggregates = {}
    for config in CONFIGS:
        selected = [record for record in records if record["configuration"] == config]
        aggregates[config] = {
            "pass_rate": distribution([record["result"]["pass_rate"] for record in selected]),
            "word_count": distribution([record["metrics"]["word_count"] if record["metrics"] else None for record in selected]),
            "heading_count": distribution([record["metrics"]["heading_count"] if record["metrics"] else None for record in selected]),
            "html_chars": distribution([record["metrics"]["html_chars"] if record["metrics"] else None for record in selected]),
            "scripts": distribution([record["metrics"]["scripts"] if record["metrics"] else None for record in selected]),
            "time_seconds": None,
            "tokens": None,
        }
    observations = iteration / "observations.md"
    notes = [line[2:] for line in observations.read_text().splitlines() if line.startswith("- ")] if observations.exists() else []
    benchmark = {"metadata": metadata, "runs": records, "run_summary": aggregates, "notes": notes}
    (iteration / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    lines = [
        "# Skill Benchmark: plexy-teach", "",
        f"**Model**: {metadata['executor_model']}",
        f"**Date**: {metadata['date']}",
        "**Eval**: 11, recursive total (3 fresh runs per configuration)",
        "**Scope**: forced-skill content pilot; identical artifact-only delivery constraints", "",
        "## Summary", "",
        "| Metric | With Skill | Without Skill | Delta |",
        "|--------|------------|---------------|-------|",
    ]
    for key, label in [("pass_rate", "Reviewed rubric pass rate"), ("word_count", "Lesson text words"), ("heading_count", "Headings"), ("html_chars", "HTML characters"), ("scripts", "Script blocks")]:
        left, right = (aggregates[config][key] for config in CONFIGS)
        if left["mean"] is None or right["mean"] is None or None in left["values"] + right["values"]:
            lines.append(f"| {label} | Unverified | Unverified | Unverified |")
        else:
            scale = 100 if key == "pass_rate" else 1
            suffix = "%" if key == "pass_rate" else ""
            delta_suffix = " pp" if key == "pass_rate" else ""
            lines.append(
                f"| {label} | {left['mean'] * scale:.1f}{suffix} ± {left['stddev'] * scale:.1f} | "
                f"{right['mean'] * scale:.1f}{suffix} ± {right['stddev'] * scale:.1f} | "
                f"{(left['mean'] - right['mean']) * scale:+.1f}{delta_suffix} |"
            )
    lines += [
        "| Time / tokens | Unavailable | Unavailable | Unavailable |", "",
        "## Notes", "",
        "- Rubric decisions and concrete evidence are saved in each run's `content_review.json` and `grading.json`.",
        "- Teaching quality is reviewed explicitly, not awarded for keyword matches, length, or heading count.",
        "- Static structure/dependency metrics are not browser, accessibility, or pedagogical proof.",
        "- Lesson text word counts exclude CSS/JavaScript but include code, controls, and collapsed answer explanations.",
        "- Reviews are by the parent assistant with variant labels visible; not independent or blinded.",
        "- Three runs of one prompt are exploratory, not evidence of statistical significance or broad skill quality.",
        "- This model differs from the earlier robot/markdown model; compare variants within this pilot only.",
        "- Iteration 1 is a preserved OpenCode startup timeout, not a completed comparison; see `README.md`.",
        "- Timing and token data are unavailable, represented as null rather than fabricated zero measurements.",
    ]
    if observations.exists():
        lines += ["", observations.read_text().strip()]
    (iteration / "benchmark.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, choices=range(2, 1000), default=2)
    args = parser.parse_args()
    main(ROOT / f"iteration-{args.iteration}")