import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "session_start.py"

PENDING_FILE = """# closures in go
Repo: web-api
Map: none

## Functions are values
Mark: Strong (2026-10-05)

## Pending
Stage: Probe 4
Question: After pair() returns, where does the variable n live?
Awaiting answer.
"""

DONE_FILE = """# middleware in go
Repo: web-api

## Closure
Mark: Strong (2026-10-05)
"""


class SessionStartTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "notes"
        self.repo = Path(self.tmp.name) / "web-api"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.folder = self.root / "web-api"
        self.folder.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, cwd=None, event="SessionStart", source="compact"):
        payload = {"hook_event_name": event, "session_id": "s1", "cwd": str(cwd or self.repo), "source": source}
        env = dict(os.environ, LEARNING_NOTES_ROOT=str(self.root))
        out = subprocess.run(["python3", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout) if out.stdout.strip() else None

    def context(self, result):
        return result["hookSpecificOutput"]["additionalContext"]

    def test_no_pending_means_silent(self):
        (self.folder / "middleware-in-go.md").write_text(DONE_FILE)
        self.assertIsNone(self.run_hook())

    def test_no_folder_means_silent(self):
        self.assertIsNone(self.run_hook(cwd=self.tmp.name))

    def test_pending_is_reported(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        (self.folder / "middleware-in-go.md").write_text(DONE_FILE)
        result = self.run_hook(source="compact")
        self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "SessionStart")
        ctx = self.context(result)
        self.assertIn("Topic: closures in go. Stage: Probe 4.", ctx)
        self.assertIn("where does the variable n live?", ctx)
        self.assertNotIn("Awaiting answer", ctx)
        self.assertIn(str(self.folder / "closures-in-go.md"), ctx)
        self.assertIn("skills/learn/SKILL.md", ctx)
        self.assertIn("not an answer", ctx)
        self.assertNotIn("middleware", ctx)

    def test_two_pending_asks_which(self):
        (self.folder / "a.md").write_text(PENDING_FILE)
        (self.folder / "b.md").write_text(PENDING_FILE.replace("closures in go", "git rebase"))
        ctx = self.context(self.run_hook())
        self.assertIn("closures in go", ctx)
        self.assertIn("git rebase", ctx)
        self.assertIn("which to continue", ctx)

    def test_backups_and_log_are_ignored(self):
        (self.folder / "backups").mkdir()
        (self.folder / "log").mkdir()
        (self.folder / "backups" / "old.md").write_text(PENDING_FILE)
        (self.folder / "log" / "lesson.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook())

    def test_symlink_is_ignored(self):
        real = Path(self.tmp.name) / "elsewhere.md"
        real.write_text(PENDING_FILE)
        (self.folder / "link.md").symlink_to(real)
        self.assertIsNone(self.run_hook())

    def test_startup_resume_clear_are_silent(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        for source in ("startup", "resume", "clear"):
            self.assertIsNone(self.run_hook(source=source), source)

    def test_other_event_is_silent(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(event="Stop"))

    def test_output_size_does_not_grow_with_notes(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE + ("\n## Node\nFacts: x\n" * 2000))
        small = len(self.context(self.run_hook()))
        self.assertLess(small, 1200)

    def test_bad_file_is_skipped(self):
        (self.folder / "bad.md").write_bytes(b"\xff\xfe\x00broken")
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        self.assertIn("closures in go", self.context(self.run_hook()))


if __name__ == "__main__":
    unittest.main()
