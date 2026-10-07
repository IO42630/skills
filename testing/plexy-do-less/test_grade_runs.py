import unittest

from grade_runs import normalized_source, successful_test


class GraderTest(unittest.TestCase):
    def test_scope_allows_equivalent_conversion_expressions(self):
        before = "def milliseconds_to_seconds(milliseconds):\n    return milliseconds / 100\n"
        after = "def milliseconds_to_seconds(milliseconds):\n    return milliseconds * 0.001\n"
        self.assertEqual(normalized_source(before), normalized_source(after))

    def test_scope_detects_unrelated_changes(self):
        before = "def milliseconds_to_seconds(milliseconds):\n    return milliseconds / 100\n"
        after = before + "\ndef unrelated():\n    return 1\n"
        self.assertNotEqual(normalized_source(before), normalized_source(after))

    def test_test_execution_requires_actual_success(self):
        event = {
            "kind": "TerminalBlockUpdatedEvent",
            "command": "python3 -m unittest -v test_timeout.py",
            "exitCode": 0,
            "output": "Ran 3 tests in 0.001s\n\nOK\n",
        }
        self.assertTrue(successful_test([event]))
        self.assertFalse(successful_test([{**event, "exitCode": 1}]))
        self.assertFalse(successful_test([{**event, "output": "Claim: tests passed"}]))
        self.assertFalse(successful_test([{**event, "command": "printf OK"}]))
        self.assertFalse(successful_test([]))


if __name__ == "__main__":
    unittest.main()