import tempfile
import unittest
from pathlib import Path

from grade_runs import ROOT, grade

REFERENCE = '''import json

def load_settings(path):
    with open(path, encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return data
'''


class GraderTests(unittest.TestCase):
    def evaluate(self, source, note="Direct local JSON loader."):
        with tempfile.TemporaryDirectory(prefix="grader-test-", dir=ROOT) as temporary:
            outputs = Path(temporary) / "outputs"
            outputs.mkdir()
            if source is not None:
                (outputs / "settings.py").write_text(source, encoding="utf-8")
            (outputs / "design.md").write_text(note, encoding="utf-8")
            return grade(outputs)

    def test_reference_passes(self):
        result = self.evaluate(REFERENCE)
        self.assertEqual(result["summary"]["passed"], 6)
        self.assertTrue(result["completion"]["passed"])

    def test_missing_module_fails(self):
        result = self.evaluate(None)
        self.assertEqual(result["summary"]["passed"], 0)
        self.assertFalse(result["completion"]["passed"])

    def test_invalid_module_fails(self):
        result = self.evaluate("this is not valid Python!")
        self.assertEqual(result["summary"]["passed"], 0)

    def test_missing_validation_fails(self):
        source = REFERENCE.replace(
            '    if not isinstance(data, dict):\n        raise ValueError("Expected a JSON object")\n', ''
        )
        result = self.evaluate(source)
        self.assertFalse(result["expectations"][1]["passed"])
        self.assertFalse(result["completion"]["passed"])

    def test_wrapped_native_errors_fail(self):
        source = '''import json
def load_settings(path):
    try:
        with open(path, encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, ValueError) as error:
        raise RuntimeError("Cannot load settings") from error
    if not isinstance(data, dict):
        raise ValueError("Expected an object")
    return data
'''
        result = self.evaluate(source)
        self.assertFalse(result["expectations"][2]["passed"])
        self.assertFalse(result["expectations"][3]["passed"])
        self.assertFalse(result["completion"]["passed"])

    def test_leaked_handle_fails(self):
        source = REFERENCE.replace(
            '    with open(path, encoding="utf-8") as stream:\n        data = json.load(stream)',
            '    stream = open(path, encoding="utf-8")\n    data = json.load(stream)',
        )
        result = self.evaluate(source)
        self.assertFalse(result["expectations"][4]["passed"])
        self.assertFalse(result["completion"]["passed"])

    def test_structure_does_not_override_completion(self):
        result = self.evaluate(REFERENCE + '\nclass UnneededFramework:\n    pass\n')
        self.assertFalse(result["expectations"][5]["passed"])
        self.assertTrue(result["completion"]["passed"])

    def test_extra_configuration_fails_structure(self):
        result = self.evaluate(REFERENCE.replace('load_settings(path)', 'load_settings(path, backend="json")'))
        self.assertFalse(result["expectations"][5]["passed"])
        self.assertTrue(result["completion"]["passed"])

    def test_missing_design_note_is_incomplete(self):
        result = self.evaluate(REFERENCE, note="")
        self.assertEqual(result["summary"]["passed"], 6)
        self.assertFalse(result["completion"]["passed"])


if __name__ == "__main__":
    unittest.main()