#!/usr/bin/env python3
"""Grade frozen JSON-loader outputs; never repair evaluated candidates."""

import ast
import builtins
import errno
import importlib.util
import io
import json
import statistics
import sysconfig
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "iteration-1" / "eval-0-json-settings"
CONFIGS = ["with_skill", "without_skill"]
RUNS = [1, 2, 3, 4, 5]
EXPECTATIONS = json.loads((ROOT / "evals" / "evals.json").read_text())["evals"][0]["expectations"]


def check_values(loader, directory):
    values = [{}, {"name": "Zürich 東京", "nested": {"items": [1, None, True, ""]}}]
    for value in values:
        path = directory / "valid.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        for argument in (str(path), path):
            result = loader(argument)
            assert type(result) is dict and result == value, repr(result)
    return "Empty/nested Unicode objects preserved for string and Path inputs (4 calls)."


def check_types(loader, directory):
    for value in ([], [1], None, "text", True, False, 42, 1.5):
        path = directory / "scalar.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        try:
            loader(path)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted non-object: {value!r}")
    return "All 8 non-object examples rejected with ValueError."


def check_missing(loader, directory):
    path = directory / "missing.json"
    try:
        loader(str(path))
    except FileNotFoundError as error:
        assert type(error) is FileNotFoundError, type(error).__name__
        assert error.filename == str(path), repr(error.filename)
        assert error.errno == errno.ENOENT, repr(error.errno)
        assert error.__cause__ is None and error.__context__ is None, "Wrapped native exception"
    else:
        raise AssertionError("Missing file did not raise FileNotFoundError")
    return "Original FileNotFoundError with filename and ENOENT; no translated cause/context."


def check_json(loader, directory):
    for document in ('{"x": }', '{\n "x": 1,\n}', 'not JSON'):
        path = directory / "invalid.json"
        path.write_text(document, encoding="utf-8")
        try:
            json.loads(document)
        except json.JSONDecodeError as error:
            expected = (error.msg, error.doc, error.pos, error.lineno, error.colno)
            native_context = type(error.__context__)
        try:
            loader(path)
        except json.JSONDecodeError as error:
            actual = (error.msg, error.doc, error.pos, error.lineno, error.colno)
            assert type(error) is json.JSONDecodeError and actual == expected, repr(actual)
            assert error.__cause__ is None and type(error.__context__) is native_context, "Wrapped native exception"
        else:
            raise AssertionError("Malformed JSON did not raise JSONDecodeError")
    return "Native JSON diagnostics preserved for all 3 malformed documents."


def check_cleanup(loader, directory):
    original_open = builtins.open
    original_io_open = io.open
    for document, exception in (('{}', None), ('{"x": }', json.JSONDecodeError), ('[]', ValueError)):
        path = directory / "cleanup.json"
        path.write_text(document, encoding="utf-8")
        handles = []

        def tracked_open(*args, **kwargs):
            handle = original_open(*args, **kwargs)
            handles.append(handle)
            return handle

        def tracked_io_open(*args, **kwargs):
            handle = original_io_open(*args, **kwargs)
            handles.append(handle)
            return handle

        with patch("builtins.open", tracked_open), patch("io.open", tracked_io_open):
            try:
                loader(path)
            except Exception as error:
                assert exception is not None and isinstance(error, exception), repr(error)
            else:
                assert exception is None, "Invalid document accepted"
        assert handles, "No Python file handles observed; alternative IO needs manual review"
        leaked = [handle for handle in handles if not handle.closed]
        for handle in leaked:
            handle.close()
        assert not leaked, f"{len(leaked)} unclosed handle(s)"
    return "Observed real file handles closed after success and both error paths."


def is_standard_library(module):
    spec = importlib.util.find_spec(module)
    if spec is None:
        return False
    if spec.origin in ("built-in", "frozen"):
        return True
    if not spec.origin:
        return False
    origin = Path(spec.origin).resolve()
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    return origin.is_relative_to(stdlib) and not {"site-packages", "dist-packages"} & set(origin.parts)


def check_structure(tree):
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module, "Extra local module dependency"
            imports.append(node.module.split('.')[0])
        assert not isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef, ast.Await)), (
            f"Unjustified structure for this local-file-only task: {type(node).__name__}"
        )
        if isinstance(node, ast.FunctionDef):
            assert not node.decorator_list, f"Decorator on {node.name}"
    assert all(is_standard_library(module) for module in imports), f"Non-stdlib imports: {imports}"
    unrelated = {"argparse", "asyncio", "concurrent", "threading", "multiprocessing", "socket", "urllib"}
    assert not set(imports) & unrelated, f"Unrequested runtime capabilities: {imports}"
    loaders = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "load_settings"]
    assert len(loaders) == 1, "Expected a visible top-level load_settings function"
    args = loaders[0].args
    assert len(args.posonlyargs + args.args) == 1 and not args.kwonlyargs and not args.vararg and not args.kwarg, (
        "Loader adds operating-mode/configuration arguments"
    )
    return f"Direct synchronous function; stdlib imports {sorted(set(imports))}; no framework/decorators."


def grade(outputs):
    source_path = outputs / "settings.py"
    namespace = {"__name__": "evaluated_settings", "__file__": str(source_path)}
    try:
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        exec(compile(tree, str(source_path), "exec"), namespace)
        loader = namespace["load_settings"]
        assert callable(loader), "load_settings is not callable"
    except Exception as error:
        return {
            "expectations": [
                {"text": text, "passed": False, "evidence": f"Module/API failure: {type(error).__name__}: {error}"}
                for text in EXPECTATIONS
            ],
            "summary": {"passed": 0, "failed": len(EXPECTATIONS), "total": len(EXPECTATIONS), "pass_rate": 0.0},
            "completion": {"passed": False},
        }
    checks = [check_values, check_types, check_missing, check_json, check_cleanup, check_structure]
    expectations = []
    with tempfile.TemporaryDirectory(prefix="grading-", dir=outputs.parent) as temporary:
        for text, check in zip(EXPECTATIONS, checks):
            try:
                evidence = check(tree) if check is check_structure else check(loader, Path(temporary))
                passed = True
            except Exception as error:
                evidence = f"{type(error).__name__}: {error}"
                passed = False
            expectations.append({"text": text, "passed": passed, "evidence": evidence})
    passed = sum(item["passed"] for item in expectations)
    note_path = outputs / "design.md"
    design_present = note_path.exists() and bool(note_path.read_text(encoding="utf-8").strip())
    return {
        "expectations": expectations,
        "summary": {"passed": passed, "failed": len(checks) - passed, "total": len(checks), "pass_rate": passed / len(checks)},
        "completion": {
            "passed": all(item["passed"] for item in expectations[:5]) and design_present,
            "design_note_present": design_present,
        },
        "metrics": {
            "source_lines": len(source.splitlines()),
            "source_chars": len(source),
            "function_count": sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)),
            "class_count": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
        },
    }


def main():
    results = {config: [] for config in CONFIGS}
    for config in CONFIGS:
        for run in RUNS:
            run_dir = EVAL_DIR / config / f"run-{run}"
            grading = grade(run_dir / "outputs")
            (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")
            results[config].append(grading)
            print(f"{config}/run-{run}: {grading['summary']['passed']}/6; completion={grading['completion']['passed']}")
    for config, runs in results.items():
        lines = [run["metrics"]["source_lines"] for run in runs if "metrics" in run]
        if lines:
            print(f"{config}: source lines {statistics.mean(lines):.1f} +/- {statistics.stdev(lines) if len(lines) > 1 else 0:.1f}; runs={lines}")


if __name__ == "__main__":
    main()