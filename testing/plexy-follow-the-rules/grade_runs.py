#!/usr/bin/env python3
"""Grade the ten native-account-action runs using AST and real repository behavior.

Run from anywhere. Each candidate is imported in its own subprocess; no third-party
dependencies or substituted repository implementations are needed.
"""

import argparse
import ast
import dataclasses
import importlib.util
import inspect
import json
import statistics
import subprocess
import sys
from pathlib import Path
from typing import get_type_hints

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "iteration-1" / "eval-0-native-account-action"
CONFIGS = ["with_skill", "without_skill"]
RUNS = [1, 2, 3, 4, 5]
EXPECTATIONS = json.loads((ROOT / "evals" / "evals.json").read_text())["evals"][0]["expectations"]


def require(condition, evidence):
    if not condition:
        raise AssertionError(evidence)


def grade_file(path):
    text = path.read_text()
    try:
        tree = ast.parse(text)
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(ROOT / "fixtures" / "project"))
        from accounts.models import Account
        from accounts.repository import AccountRepository, NotFoundError

        spec = importlib.util.spec_from_file_location("accounts.rename_account", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        action_type = module.RenameAccountAction
    except Exception as error:
        return result([
            {"text": label, "passed": False, "evidence": f"Cannot load action: {type(error).__name__}: {error}"}
            for label in EXPECTATIONS
        ], text)

    def native_dataclass():
        require(dataclasses.is_dataclass(action_type), "Action is not a dataclass.")
        require(action_type.__dataclass_params__.frozen, "Action dataclass is not frozen.")
        fields = dataclasses.fields(action_type)
        require([field.name for field in fields] == ["repository"], "Expected only the repository injection field.")
        require(get_type_hints(action_type).get("repository") is AccountRepository, "Repository annotation differs.")
        node = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == action_type.__name__)
        require(not any(isinstance(child, ast.FunctionDef) and child.name == "__init__" for child in node.body),
                "Constructor is hand-written rather than generated.")
        action = action_type(AccountRepository())
        try:
            action.repository = AccountRepository()
        except dataclasses.FrozenInstanceError:
            return "Frozen dataclass; typed repository field; generated constructor; reassignment rejected."
        raise AssertionError("Action repository can be reassigned.")

    def signature():
        parameters = inspect.signature(action_type.execute).parameters
        require(list(parameters) == ["self", "account_id", "rename_to"], f"Unexpected parameters: {list(parameters)}")
        require(parameters["rename_to"].kind is inspect.Parameter.KEYWORD_ONLY, "rename_to is not keyword-only.")
        hints = get_type_hints(action_type.execute)
        require(hints.get("account_id") is str and hints.get("rename_to") is str,
                "Expected str annotations on account_id and rename_to.")
        require(hints.get("return") is Account, "Expected Account return annotation.")
        return "execute(self, account_id: str, *, rename_to: str) -> Account."

    def rename():
        repository = AccountRepository()
        original = repository.save(Account("a-1", "Original"))
        other = repository.save(Account("a-2", "Untouched"))
        renamed = action_type(repository).execute("a-1", rename_to="Renamed")
        require(type(renamed) is Account and renamed.account_id == "a-1" and renamed.name == "Renamed",
                f"Unexpected renamed value: {renamed!r}")
        require(repository.find("a-1") is renamed, "Returned account is not the saved account.")
        require(renamed is not original and original.name == "Original", "Original object was mutated or reused.")
        require(repository.find("a-2") is other, "Unrelated account changed.")
        return "Correct account saved and returned; original immutable instance and second account unchanged."

    def explicit_preference():
        names = ["  Renamed\t ", "", "  naïve 🌲  "]
        for name in names:
            repository = AccountRepository()
            repository.save(Account("a-1", "Original"))
            renamed = action_type(repository).execute("a-1", rename_to=name)
            require(renamed.name == name and repository.find("a-1").name == name,
                    f"Name {name!r} was normalized or rejected: {renamed.name!r}")
        return f"Saved exact names for whitespace, empty-string, and Unicode cases: {names!r}."

    def not_found():
        repository = AccountRepository()
        original = repository.save(Account("a-1", "Original"))
        try:
            action_type(repository).execute("missing", rename_to="New")
        except Exception as error:
            require(type(error) is NotFoundError, f"Wrong exception: {type(error).__name__}: {error}")
            require(error.args == ("missing",), f"Wrong exception arguments: {error.args!r}")
        else:
            raise AssertionError("Missing account did not raise an exception.")
        require(repository.find("missing") is None and repository.find("a-1") is original,
                "Missing-account path changed stored accounts.")
        return "Existing NotFoundError raised with args ('missing',); no missing account created; existing account unchanged."

    def native_dependencies():
        aliases = {}
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
                    aliases[alias.asname or alias.name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                name = node.module or ""
                imports.append("." * node.level + name)
                for alias in node.names:
                    aliases[alias.asname or alias.name] = f"{name}.{alias.name}"
        allowed = {"dataclasses", "__future__", ".models", ".repository", "accounts.models", "accounts.repository"}
        require(set(imports) <= allowed, f"Non-native imports: {sorted(set(imports) - allowed)}")
        calls = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name):
                calls.append(aliases.get(node.func.id, node.func.id))
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                calls.append(f"{aliases.get(node.func.value.id, node.func.value.id)}.{node.func.attr}")
        require("dataclasses.replace" in calls, "No dataclasses.replace call found.")
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        require(classes == ["RenameAccountAction"], f"Unrelated classes added: {classes}")
        require(not any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in tree.body),
                "Unrelated module-level helpers added.")
        unexpected = {item.name for item in path.parent.iterdir()} - {"rename_account.py", "implementation_note.md"}
        require(not unexpected, f"Unrequested output files: {sorted(unexpected)}")
        return f"dataclasses.replace used; native imports {imports}; only the requested action class and output files."

    expectations = []
    for label, check in zip(EXPECTATIONS, [native_dataclass, signature, rename, explicit_preference, not_found,
                                         native_dependencies]):
        try:
            evidence = check()
            passed = True
        except Exception as error:
            evidence = f"{type(error).__name__}: {error}"
            passed = False
        expectations.append({"text": label, "passed": passed, "evidence": evidence})
    return result(expectations, text)


def result(expectations, text):
    passed = sum(item["passed"] for item in expectations)
    total = len(expectations)
    return {
        "expectations": expectations,
        "summary": {"passed": passed, "failed": total - passed, "total": total, "pass_rate": passed / total},
        "execution_metrics": {"output_chars": len(text)},
        "metrics": {"source_lines": len(text.splitlines()), "source_chars": len(text)},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="Grade one source file and print JSON without writing results.")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(grade_file(args.check.resolve()), indent=2))
        return

    metrics = {config: [] for config in CONFIGS}
    for config in CONFIGS:
        for run in RUNS:
            run_dir = EVAL_DIR / config / f"run-{run}"
            source = run_dir / "outputs" / "rename_account.py"
            if not source.is_file():
                raise FileNotFoundError(f"Missing benchmark output: {source}")
            process = subprocess.run(
                [sys.executable, "-B", str(Path(__file__).resolve()), "--check", str(source)],
                check=True, capture_output=True, text=True, timeout=20,
            )
            grading = json.loads(process.stdout)
            (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
            metrics[config].append(grading["summary"]["pass_rate"])
            print(f"{config}/run-{run}: {grading['summary']['passed']}/{grading['summary']['total']} checks passed")
            for expectation in grading["expectations"]:
                if not expectation["passed"]:
                    print(f"  FAIL: {expectation['text']} {expectation['evidence']}")
    print(f"\n=== Pass-rate variance over {len(RUNS)} runs ===")
    for config, values in metrics.items():
        print(f"{config}: {statistics.mean(values):.1%} +/- {statistics.stdev(values):.1%}")


if __name__ == "__main__":
    main()