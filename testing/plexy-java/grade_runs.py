#!/usr/bin/env python3
"""Compile, exercise, and grade all paired saved Java candidates.

Only Python's standard library and a JDK 17+ are required. Real Lombok/SLF4J
dependencies are cached locally; Maven is not needed. No candidate is modified.
"""

import argparse
import hashlib
import json
import os
import re
import statistics
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "iteration-1" / "eval-0-customer-directory"
CONFIGS = ["with_skill", "without_skill"]
EXPECTATIONS = [
    "The complete candidate compiles for Java 17 with the real declared dependencies.",
    "Lookup, mutable customer fields, sorted displays, UTF-8 CSV loading, and supplied-map updates work.",
    "Imports are explicit and grouped java/javax, third-party, then project-internal.",
    "Customer uses Lombok @Data and @Builder instead of handwritten accessors or constructors.",
    "Obvious local initializers use var rather than redundant explicit types.",
    "Java sources compile without raw-type warnings.",
    "Missing-file IOException reaches the caller rather than being swallowed.",
    "findById returns typed Optional<Customer>, empty for absence and populated for presence.",
    "The constructor rejects a null map and uses Objects.requireNonNull for that parameter.",
    "The existing Maven dependency declarations are preserved without additions or duplicates.",
    "Chained method-call dots start on new lines.",
    "Calls with multiple arguments put each argument and the closing parenthesis on separate lines.",
]

MASK_RE = re.compile(r'"""[\s\S]*?"""|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/')


def run_numbers(eval_dir=EVAL_DIR):
    numbers = {}
    for config in CONFIGS:
        numbers[config] = sorted(int(path.name[4:]) for path in (eval_dir / config).iterdir()
                                 if path.is_dir() and re.fullmatch(r"run-[1-9]\d*", path.name))
    if numbers[CONFIGS[0]] != numbers[CONFIGS[1]]:
        raise ValueError("Runs must be paired across configurations: " + str(numbers))
    if not numbers[CONFIGS[0]]:
        raise ValueError("No runs found in " + str(eval_dir))
    return numbers[CONFIGS[0]]


def mask_java(text):
    def replace(match):
        value = match.group()
        masked = "".join("\n" if char == "\n" else " " for char in value)
        return masked if value.startswith("/") else "S" + masked[1:]
    return MASK_RE.sub(replace, text)


def line_number(text, offset):
    return text.count("\n", 0, offset) + 1


def call_layout(text):
    code = mask_java(text)
    chains = []
    for match in re.finditer(r"\)(\s*)\.\s*[A-Za-z_]\w*\s*\(", code):
        dot = code.index(".", match.start())
        if "\n" not in match.group(1) or code[code.rfind("\n", 0, dot) + 1:dot].strip():
            chains.append(line_number(code, dot))

    calls = []
    violations = []
    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", code):
        if match.group(1) in {"if", "for", "while", "switch", "catch", "synchronized"}:
            continue
        if code[:match.start()].rstrip().endswith("@"):
            continue
        opening = code.index("(", match.start())
        stack = ["("]
        commas = []
        closing = None
        for index in range(opening + 1, len(code)):
            char = code[index]
            if char in "([{":
                stack.append(char)
            elif char in ")]}":
                stack.pop()
                if not stack:
                    closing = index
                    break
            elif char == "," and stack == ["("]:
                commas.append(index)
        if closing is None or not commas:
            continue
        tail = code[closing + 1:].lstrip()
        if tail.startswith("{") or tail.startswith("throws "):
            continue  # Method/constructor declarations are not calls.
        boundaries = [opening] + commas
        ends = commas + [closing]
        valid = all("\n" in code[start + 1:end][:len(code[start + 1:end]) - len(code[start + 1:end].lstrip())]
                    for start, end in zip(boundaries, ends))
        final_arg = code[commas[-1] + 1:closing]
        valid = valid and "\n" in final_arg[len(final_arg.rstrip()):]
        calls.append(line_number(code, opening))
        if not valid:
            violations.append(line_number(code, opening))
    return {"chain_violations": chains, "multi_argument_calls": calls, "argument_violations": violations}


def imports_ok(text):
    imports = re.findall(r"^\s*import\s+(?:static\s+)?([^;]+);", mask_java(text), re.MULTILINE)
    groups = [0 if name.startswith(("java.", "javax.")) else 2 if name.startswith("example.") else 1
              for name in imports]
    return not any("*" in name for name in imports) and groups == sorted(groups), imports


def dependency_declarations(path):
    tree = ET.parse(path)
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    result = []
    for dependency in tree.findall("./m:dependencies/m:dependency", ns):
        result.append(tuple(dependency.findtext("m:" + key, default="", namespaces=ns)
                            for key in ["groupId", "artifactId", "version", "scope", "classifier", "type"]))
    return sorted(result)


def fetch_dependencies():
    cache = ROOT / ".deps"
    cache.mkdir(exist_ok=True)
    paths = []
    for relative, filename in [
        ("org/projectlombok/lombok/1.18.48/lombok-1.18.48.jar", "lombok-1.18.48.jar"),
        ("org/slf4j/slf4j-api/2.0.17/slf4j-api-2.0.17.jar", "slf4j-api-2.0.17.jar"),
    ]:
        path = cache / filename
        url = "https://repo.maven.apache.org/maven2/" + relative
        with urllib.request.urlopen(url + ".sha1", timeout=30) as response:
            expected = response.read().decode().strip().split()[0]
        if not path.exists() or hashlib.sha1(path.read_bytes()).hexdigest() != expected:
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
            if hashlib.sha1(content).hexdigest() != expected:
                raise ValueError("Dependency checksum mismatch: " + filename)
            path.write_bytes(content)
        paths.append(path)
    return paths


def execute(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=60)
    return {"command": [str(value) for value in command], "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def validate(project, validation, dependencies):
    validation.mkdir(parents=True, exist_ok=True)
    classes = validation / "classes"
    classes.mkdir(exist_ok=True)
    classpath = os.pathsep.join(str(path) for path in dependencies)
    sources = sorted((project / "src" / "main" / "java").rglob("*.java"))
    compilation = execute(["javac", "--release", "17", "-Xlint:rawtypes", "-cp", classpath,
                           "-processorpath", str(dependencies[0]), "-d", str(classes),
                           *map(str, sources), str(ROOT / "checks" / "BehaviorCheck.java")], validation)
    results = {"compile": compilation}
    results["bytecode"] = execute(["javap", "-c", "-p", "-classpath", str(classes),
                                   "example.service.CustomerDirectory"], validation) \
        if compilation["exit_code"] == 0 else {"exit_code": None, "stdout": "", "stderr": "Not run: compilation failed."}
    for scenario in ["core", "null", "io", "optional"]:
        results[scenario] = execute(["java", "-Djava.io.tmpdir=" + str(validation), "-cp",
                                     str(classes) + os.pathsep + classpath, "BehaviorCheck", scenario], validation) \
            if compilation["exit_code"] == 0 else {"exit_code": None, "stdout": "", "stderr": "Not run: compilation failed."}
    (validation / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return results


def grade(project, results):
    sources = sorted((project / "src" / "main" / "java").rglob("*.java"))
    texts = {str(path.relative_to(project)): path.read_text() for path in sources}
    combined = "\n".join(texts.values())
    model = mask_java(texts.get("src/main/java/example/model/Customer.java", ""))
    import_checks = {name: imports_ok(text) for name, text in texts.items()}
    layouts = {name: call_layout(text) for name, text in texts.items()}
    explicit_locals = []
    var_count = len(re.findall(r"\bvar\s+\w+\s*=", mask_java(combined)))
    for name, text in texts.items():
        for match in re.finditer(r"(?m)^\s*(?:final\s+)?(?!var\b)([A-Z][\w.<>?, \[\]]*)\s+\w+\s*=\s*(new\b|S\b|Files\.readAllLines\b|String\.format\b|\w+\.split\b)", mask_java(text)):
            explicit_locals.append(f"{name}:{line_number(text, match.start())}")
    handwritten = bool(re.search(r"\b(?:getId|getName|setId|setName|Customer)\s*\([^)]*\)\s*\{", model))
    lombok = bool(re.search(r"@(?:lombok\.)?Data\b", model)) and bool(re.search(r"@(?:lombok\.)?Builder\b", model)) and not handwritten
    ctor = re.search(r"public example\.service\.CustomerDirectory\([^;]+;([\s\S]*?)(?=\n  (?:public|private|protected|static)|\n})",
                     results["bytecode"]["stdout"])
    null_guard = bool(ctor and "java/util/Objects.requireNonNull:" in ctor.group(1))
    try:
        dependencies_match = dependency_declarations(project / "pom.xml") == dependency_declarations(ROOT / "fixtures" / "customer-directory" / "pom.xml")
        dependency_evidence = "Dependency group/artifact/version/scope/classifier/type declarations " + ("match." if dependencies_match else "differ.")
    except (OSError, ET.ParseError) as error:
        dependencies_match = False
        dependency_evidence = str(error)
    compiled = results["compile"]["exit_code"] == 0
    raw_warnings = results["compile"]["stderr"].count("[rawtypes]")
    import_failures = [name for name, (passed, _) in import_checks.items() if not passed]
    chain_failures = {name: layout["chain_violations"] for name, layout in layouts.items() if layout["chain_violations"]}
    argument_failures = {name: layout["argument_violations"] for name, layout in layouts.items() if layout["argument_violations"]}

    def runtime(scenario):
        result = results[scenario]
        return result["exit_code"] == 0, (result["stdout"] + result["stderr"]).strip()

    null_passed, null_evidence = runtime("null")
    entries = [
        (compiled, "javac exit=" + str(results["compile"]["exit_code"]) + "; see validation/results.json."),
        runtime("core"),
        (bool(texts) and not import_failures, "Import failures: " + str(import_failures)),
        (lombok, f"@Data/@Builder without handwritten DTO accessors/constructors: {lombok}."),
        (var_count > 0 and not explicit_locals, f"var initializers={var_count}; redundant obvious locals={explicit_locals}."),
        (compiled and raw_warnings == 0, f"Compiler raw-type warnings={raw_warnings}; compiled={compiled}."),
        runtime("io"),
        runtime("optional"),
        (null_passed and null_guard, f"Objects.requireNonNull in constructor={null_guard}; {null_evidence}"),
        (dependencies_match, dependency_evidence),
        (bool(texts) and not chain_failures, "Same-line chained dots: " + str(chain_failures)),
        (bool(texts) and not argument_failures, "Multi-argument layout failures: " + str(argument_failures)),
    ]
    expectations = [{"text": text, "passed": passed, "evidence": evidence}
                    for text, (passed, evidence) in zip(EXPECTATIONS, entries)]
    passed = sum(entry["passed"] for entry in expectations)
    return {
        "expectations": expectations,
        "summary": {"passed": passed, "failed": len(entries) - passed, "total": len(entries), "pass_rate": passed / len(entries)},
        "execution_metrics": {"output_chars": len(combined), "total_tool_calls": None, "errors_encountered": None},
        "timing": {"total_duration_seconds": None, "total_tokens": None, "status": "Not exposed by this subagent runtime."},
        "eval_feedback": {
            "suggestions": [{"assertion": EXPECTATIONS[3],
                             "reason": "This frozen probe requires @Builder even though the task does not request a builder API. @Data with a generated constructor also removes boilerplate; keep the score but interpret the annotation-specific failure narrowly."}],
            "overall": "Targeted convention probes and behavior checks, not comprehensive Java conformance."
        },
        "metrics": {"java_lines": sum(len(text.splitlines()) for text in texts.values()),
                    "max_line_length": max((len(line) for line in combined.splitlines()), default=0),
                    "var_initializers": var_count, "raw_type_warnings": raw_warnings,
                    "chain_layout_violations": sum(len(value) for value in chain_failures.values()),
                    "argument_layout_violations": sum(len(value) for value in argument_failures.values())},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-fixture", action="store_true", help="Confirm the starting fixture fails the robustness checks.")
    args = parser.parse_args()
    dependencies = fetch_dependencies()
    if args.check_fixture:
        project = ROOT / "fixtures" / "customer-directory"
        results = validate(project, ROOT / "fixtures" / "validation", dependencies)
        grading = grade(project, results)
        (ROOT / "fixtures" / "validation" / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
        assert results["compile"]["exit_code"] == 0, "Fixture must compile"
        assert results["core"]["exit_code"] == 0, "Fixture must demonstrate the original core behavior"
        assert results["null"]["exit_code"] != 0, "Fixture must reproduce null-map acceptance"
        assert results["io"]["exit_code"] != 0, "Fixture must reproduce swallowed IOException"
        print("Fixture reproduces null-map acceptance and swallowed IOException; core behavior passes.")
        return
    numbers = run_numbers()
    metrics = {config: [] for config in CONFIGS}
    for config in CONFIGS:
        for number in numbers:
            run = EVAL_DIR / config / f"run-{number}"
            project = run / "outputs"
            if not (project / "pom.xml").is_file():
                raise FileNotFoundError("Missing complete candidate: " + str(project))
            results = validate(project, run / "validation", dependencies)
            grading = grade(project, results)
            (run / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
            metrics[config].append(grading["summary"]["pass_rate"])
            print(f"{config}/run-{number}: {grading['summary']['passed']}/{grading['summary']['total']}; "
                  f"compile={results['compile']['exit_code']}; core={results['core']['exit_code']}")
    for config, values in metrics.items():
        deviation = statistics.stdev(values) if len(values) > 1 else 0.0
        print(f"{config}: pass rate {statistics.mean(values):.1%} +/- {deviation:.1%}")


if __name__ == "__main__":
    main()