import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import collect_evidence


class CollectionTest(unittest.TestCase):
    def test_reused_agent_id_does_not_mix_runs(self):
        with tempfile.TemporaryDirectory(dir=collect_evidence.ROOT) as directory:
            root = Path(directory)
            eval_dir = root / "iteration-1" / "eval-0-scoped-timeout-fix"
            output = eval_dir / "with_skill" / "run-4" / "outputs"
            output.mkdir(parents=True)
            (output / "reply.txt").write_text("Fixed.\n")
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text(json.dumps({
                "evals": [{"id": 0, "prompt": "Fix timeout", "expectations": []}]}))
            assignments = root / "assignments.json"
            assignments.write_text(json.dumps({"agent-3": ["do-less-with-4", "with_skill", 4]}))
            session = root / "session"
            (session / "subagents").mkdir(parents=True)
            (session / "subagents" / "agent-3-do-less-with-4-transcript.md").write_text("New run\n")
            events = []
            for name, step in [("do-less-without-1", "old"), ("do-less-with-4", "new")]:
                events.append({"event": {"agentEvent": {
                    "agent": {"id": "agent-3", "name": name},
                    "kind": "ToolBlockUpdatedEvent", "stepId": step, "text": name}}})
            (session / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
            with patch.object(collect_evidence, "ROOT", root), \
                    patch.object(collect_evidence, "EVAL_DIR", eval_dir), \
                    patch("sys.argv", ["collect_evidence.py", str(session),
                                       "--assignments", str(assignments)]), \
                    contextlib.redirect_stdout(io.StringIO()):
                collect_evidence.main()
            trace = json.loads((output.parent / "trace.json").read_text())
            self.assertEqual([s["event"]["stepId"] for s in trace["steps"]], ["new"])


if __name__ == "__main__":
    unittest.main()