import unittest

from grade_runs import analyze, distribution, grade


class GradingTests(unittest.TestCase):
    def test_words_exclude_style_and_script(self):
        metrics = analyze('<html lang="en"><title>Total</title><style>hidden words</style><main><h1>Trace</h1><p>Child returns three.</p><script>hidden words</script></main></html>')
        self.assertEqual(5, metrics["word_count"])
        self.assertTrue(metrics["has_semantic_structure"])
        self.assertTrue(metrics["has_language"])

    def test_optional_source_links_are_not_core_dependencies(self):
        metrics = analyze('<a href="https://docs.python.org/">Source</a><style>p { color: black; }</style>')
        self.assertTrue(metrics["static_self_contained"])

    def test_core_dependencies_are_detected(self):
        metrics = analyze('<link rel="stylesheet" href="lesson.css"><script src="https://example.com/a.js"></script><style>body { background: url(image.png) }</style>')
        self.assertEqual(["lesson.css", "https://example.com/a.js", "image.png"], metrics["required_dependencies"])
        self.assertFalse(metrics["static_self_contained"])

    def test_missing_review_never_counts_as_pass(self):
        result = grade("<html>recursive worked example practice</html>", ["Shows why the return is used."])
        self.assertEqual(1, result["summary"]["unverified"])
        self.assertIsNone(result["summary"]["pass_rate"])

    def test_missing_artifact_fails_even_with_positive_review(self):
        review = {"expectations": [{"text": "A lesson exists.", "passed": True, "evidence": "Claimed."}]}
        result = grade(None, ["A lesson exists."], review)
        self.assertEqual(1, result["summary"]["failed"])
        self.assertEqual(0, result["summary"]["pass_rate"])

    def test_review_cannot_silently_omit_or_change_expectations(self):
        with self.assertRaises(ValueError):
            grade("<html></html>", ["One", "Two"], {"expectations": []})
        with self.assertRaises(ValueError):
            grade("<html></html>", ["One"], {"expectations": [{"text": "Different", "passed": True, "evidence": "Text."}]})

    def test_review_needs_evidence(self):
        with self.assertRaises(ValueError):
            grade("<html></html>", ["One"], {"expectations": [{"text": "One", "passed": True, "evidence": ""}]})

    def test_numeric_result_is_not_a_boolean_review(self):
        with self.assertRaises(ValueError):
            grade("<html></html>", ["One"], {"expectations": [{"text": "One", "passed": 1, "evidence": "Text."}]})

    def test_explicit_negative_and_unverified_decisions_are_preserved(self):
        review = {"expectations": [
            {"text": "One", "passed": True, "evidence": "A trace is shown."},
            {"text": "Two", "passed": False, "evidence": "No fresh exercise."},
            {"text": "Three", "passed": None, "evidence": "Not checked."},
        ]}
        result = grade("<html></html>", ["One", "Two", "Three"], review)
        self.assertEqual({"passed": 1, "failed": 1, "unverified": 1, "total": 3, "pass_rate": None}, result["summary"])

    def test_unavailable_metrics_remain_null(self):
        self.assertIsNone(distribution([None, None])["mean"])
        self.assertEqual(2, distribution([1, 2, 3])["mean"])


if __name__ == "__main__":
    unittest.main()