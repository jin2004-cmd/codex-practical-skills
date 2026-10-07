import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("session_checkpoint.py")


class CounterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = Path(self.temp.name) / "state.json"

    def call(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), "--state", str(self.state), *args],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return json.loads(result.stdout) if ok else result

    def test_read_only_status_and_five_turns(self):
        self.assertFalse(self.call("status")["due"])
        self.assertFalse(self.state.exists())
        for number in range(5):
            result = self.call("tick", "--turn-key", str(number))
        self.assertEqual(result["count"], 5)
        self.assertTrue(result["due"])
        repeated = self.call("tick", "--turn-key", "4")
        self.assertEqual(repeated["count"], 5)
        self.assertFalse(repeated["counted"])

    def test_completion_needs_real_summary_and_preserves_dedup(self):
        self.call("tick", "--turn-key", "one")
        previous = self.state.read_bytes()
        summary = Path(self.temp.name) / "summary.md"
        self.call("complete", "--checkpoint", str(summary), ok=False)
        self.assertEqual(previous, self.state.read_bytes())
        summary.write_text("  ", encoding="utf-8")
        self.call("complete", "--checkpoint", str(summary), ok=False)
        self.assertEqual(previous, self.state.read_bytes())
        summary.write_text("# Checkpoint\nVerified outcome; next action.\n", encoding="utf-8")
        result = self.call("complete", "--checkpoint", str(summary))
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["last_checkpoint"]["covered_turns"], 1)
        self.assertEqual(self.call("tick", "--turn-key", "one")["count"], 0)

    def test_bad_or_unknown_state_is_not_reset(self):
        for raw in ("not-json", '{"schema_version":99}',
                    '{"schema_version":1,"interval":5,"count":-1,"recent_key_hashes":[]}'):
            self.state.write_text(raw, encoding="utf-8")
            self.call("tick", "--turn-key", "new", ok=False)
            self.assertEqual(self.state.read_text(encoding="utf-8"), raw)

    def test_replayed_completion_is_idempotent_and_cannot_cover_new_turns(self):
        summary = Path(self.temp.name) / "summary.md"
        summary.write_text("# First checkpoint\nVerified first task.\n", encoding="utf-8")
        self.call("tick", "--turn-key", "first")
        self.call("complete", "--checkpoint", str(summary))
        previous = self.state.read_bytes()
        repeated = self.call("complete", "--checkpoint", str(summary))
        self.assertEqual(repeated["last_checkpoint"]["covered_turns"], 1)
        self.assertEqual(previous, self.state.read_bytes())
        self.call("tick", "--turn-key", "second")
        previous = self.state.read_bytes()
        self.call("complete", "--checkpoint", str(summary), ok=False)
        self.assertEqual(previous, self.state.read_bytes())
        summary.write_text("# Updated checkpoint\nVerified second task.\n", encoding="utf-8")
        self.assertEqual(self.call("complete", "--checkpoint", str(summary))["count"], 0)


if __name__ == "__main__":
    unittest.main()
