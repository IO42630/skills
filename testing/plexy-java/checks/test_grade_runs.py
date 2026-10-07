import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("grade_runs", Path(__file__).resolve().parents[1] / "grade_runs.py")
GRADER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRADER)


class GraderTests(unittest.TestCase):
    def test_discovers_all_paired_runs_in_numeric_order(self):
        with tempfile.TemporaryDirectory(dir=GRADER.ROOT) as directory:
            root = Path(directory)
            for config in GRADER.CONFIGS:
                for number in [10, 2, 1, 5, 4, 3]:
                    (root / config / f"run-{number}").mkdir(parents=True)
                (root / config / "notes").mkdir()
                (root / config / "run-99").touch()
            self.assertEqual(GRADER.run_numbers(root), [1, 2, 3, 4, 5, 10])

    def test_unpaired_runs_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=GRADER.ROOT) as directory:
            root = Path(directory)
            for config in GRADER.CONFIGS:
                (root / config / "run-1").mkdir(parents=True)
            (root / "with_skill" / "run-2").mkdir()
            with self.assertRaisesRegex(ValueError, "paired"):
                GRADER.run_numbers(root)

    def test_empty_run_sets_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=GRADER.ROOT) as directory:
            root = Path(directory)
            for config in GRADER.CONFIGS:
                (root / config).mkdir()
            with self.assertRaisesRegex(ValueError, "No runs"):
                GRADER.run_numbers(root)

    def test_import_groups_and_wildcards(self):
        self.assertTrue(GRADER.imports_ok("import java.util.List;\nimport lombok.Data;\nimport example.model.Customer;")[0])
        self.assertFalse(GRADER.imports_ok("import java.util.*;")[0])
        self.assertFalse(GRADER.imports_ok("import example.model.Customer;\nimport java.util.List;")[0])

    def test_single_line_calls_fail(self):
        result = GRADER.call_layout('names.stream().sorted().toList();\nString.format("%s,%s", name, id);')
        self.assertEqual(result["chain_violations"], [1, 1])
        self.assertEqual(result["argument_violations"], [2])

    def test_multiline_calls_pass(self):
        result = GRADER.call_layout('names.stream()\n    .sorted()\n    .toList();\nString.format(\n    "%s,%s",\n    name,\n    id\n);')
        self.assertEqual(result["chain_violations"], [])
        self.assertEqual(result["argument_violations"], [])
        self.assertEqual(len(result["multi_argument_calls"]), 1)

    def test_declarations_comments_and_literals_are_exempt(self):
        result = GRADER.call_layout('public Thing(String id, String name) { }\n// a().b();\nString s = "a().b(),c";\n/* f(a, b); */')
        self.assertEqual(result["chain_violations"], [])
        self.assertEqual(result["multi_argument_calls"], [])

    def test_nested_calls_each_checked(self):
        result = GRADER.call_layout('map.put(\n    id,\n    new Thing(id, name)\n);')
        self.assertEqual(result["argument_violations"], [3])
        self.assertEqual(len(result["multi_argument_calls"]), 2)

    def test_missing_parenthesis_line_break_fails(self):
        result = GRADER.call_layout('f(\n    first,\n    second);')
        self.assertEqual(result["argument_violations"], [1])

    def test_frozen_metadata_matches_grader(self):
        evals = json.loads((GRADER.ROOT / "evals" / "evals.json").read_text())
        metadata = json.loads((GRADER.EVAL_DIR / "eval_metadata.json").read_text())
        self.assertEqual(evals["evals"][0]["expectations"], GRADER.EXPECTATIONS)
        self.assertEqual(metadata["assertions"], GRADER.EXPECTATIONS)
        self.assertEqual(metadata["prompt"], evals["evals"][0]["prompt"])

    def test_dependency_duplicates_are_not_collapsed(self):
        dependency = "<dependency><groupId>a</groupId><artifactId>b</artifactId><version>1</version></dependency>"
        prefix = '<project xmlns="http://maven.apache.org/POM/4.0.0"><dependencies>'
        suffix = "</dependencies></project>"
        single = GRADER.dependency_declarations(io.StringIO(prefix + dependency + suffix))
        duplicate = GRADER.dependency_declarations(io.StringIO(prefix + dependency * 2 + suffix))
        self.assertNotEqual(single, duplicate)
        self.assertEqual(len(duplicate), 2)

    def test_arguments_in_strings_are_not_counted(self):
        result = GRADER.call_layout('f("x,y,(z)");\ng(\n    "a,b",\n    "c,d"\n);')
        self.assertEqual(result["multi_argument_calls"], [2])
        self.assertEqual(result["argument_violations"], [])


if __name__ == "__main__":
    unittest.main()