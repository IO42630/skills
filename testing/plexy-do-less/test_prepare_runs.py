import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prepare_runs


class PreparationTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=prepare_runs.ROOT)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        fixtures = self.root / "evals" / "fixtures"
        fixtures.mkdir(parents=True)
        (fixtures / "timeout.py").write_text("return_value = 1\n")
        (self.root / "evals" / "evals.json").write_text(json.dumps({
            "evals": [{"id": 0, "prompt": "Fix timeout", "expectations": []}]}))
        self.skill = self.root / "SKILL.md"
        self.skill.write_text("Frozen skill\n")
        self.eval_dir = self.root / "iteration-1" / "eval-0-scoped-timeout-fix"

    def prepare(self, *arguments):
        with patch.object(prepare_runs, "ROOT", self.root), \
                patch.object(prepare_runs, "SKILL", self.skill), \
                patch.object(prepare_runs, "EVAL_DIR", self.eval_dir), \
                patch("sys.argv", ["prepare_runs.py", *arguments]), \
                contextlib.redirect_stdout(io.StringIO()):
            prepare_runs.main()

    def test_append_preserves_existing_runs_and_snapshot(self):
        self.prepare()
        original = self.eval_dir / "with_skill" / "run-1" / "outputs" / "timeout.py"
        original.write_text("Fixed candidate\n")
        self.prepare("--additional-runs", "2")
        self.assertEqual(original.read_text(), "Fixed candidate\n")
        manifest = json.loads((self.root / "iteration-1" / "manifest.json").read_text())
        self.assertEqual(manifest["runs_per_configuration"], 5)
        for config in ["with_skill", "without_skill"]:
            self.assertEqual(len(list((self.eval_dir / config).iterdir())), 5)
            for number in [4, 5]:
                self.assertEqual((self.eval_dir / config / f"run-{number}" / "outputs"
                                  / "timeout.py").read_text(), "return_value = 1\n")
        self.assertEqual((self.root / "iteration-1" / "skill-snapshot" / "SKILL.md").read_text(),
                         "Frozen skill\n")

    def test_existing_target_is_not_overwritten(self):
        self.prepare()
        target = self.eval_dir / "without_skill" / "run-4"
        target.mkdir()
        with self.assertRaisesRegex(SystemExit, "Refusing to overwrite"):
            self.prepare("--additional-runs", "2")
        self.assertFalse((self.eval_dir / "with_skill" / "run-4").exists())

    def test_changed_skill_is_rejected(self):
        self.prepare()
        self.skill.write_text("Different skill\n")
        with self.assertRaisesRegex(SystemExit, "changed"):
            self.prepare("--additional-runs", "2")
        self.assertFalse((self.eval_dir / "with_skill" / "run-4").exists())


if __name__ == "__main__":
    unittest.main()