import hashlib
import json
import unittest

import prepare_runs
from grade_runs import CONFIGS, EVAL_DIR, ITERATION, ROOT, RUNS


class InputTests(unittest.TestCase):
    def test_saved_prompts_differ_only_by_frozen_skill_instructions(self):
        case = json.loads((ROOT / "evals/evals.json").read_text())["evals"][0]
        for iteration_number in [2, 3, 4]:
            iteration = ROOT / f"iteration-{iteration_number}"
            eval_dir = iteration / EVAL_DIR.name
            skill = (iteration / "skill_snapshot.md").read_text()
            metadata = json.loads((eval_dir / "eval_metadata.json").read_text())
            self.assertEqual((ITERATION / "skill_snapshot.md").read_text(), skill)
            self.assertEqual(hashlib.sha256(skill.encode()).hexdigest(), metadata["skill_sha256"])
            self.assertEqual(case["expectations"], metadata["assertions"])
            self.assertEqual(prepare_runs.DELIVERY, metadata["delivery_instructions"])
            baseline = case["prompt"] + "\n\n" + metadata["delivery_instructions"]
            for config in CONFIGS:
                expected = baseline if config == "without_skill" else "Apply these teaching instructions:\n\n" + skill + "\n\nLearner request:\n" + baseline
                for number in RUNS:
                    with self.subTest(iteration=iteration_number, configuration=config, run=number):
                        self.assertEqual(expected + "\n", (eval_dir / config / f"run-{number}/prompt.txt").read_text())

    def test_preparation_refuses_overwrite_without_changing_frozen_metadata(self):
        for iteration_number in [2, 3, 4]:
            iteration = ROOT / f"iteration-{iteration_number}"
            path = iteration / EVAL_DIR.name / "eval_metadata.json"
            before = path.read_bytes()
            with self.subTest(iteration=iteration_number):
                with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
                    prepare_runs.main(iteration)
                self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()