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

MODE_ON = "# web-api settings\nMode: teach as we go\n"
MODE_OFF = "# web-api settings\nTheme: dark\n"


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

    def transcript(self, *paths, tool="Write"):
        """A transcript in which this chat wrote each path with the given tool."""
        target = Path(self.tmp.name) / "transcript.jsonl"
        rows = [{"type": "user", "message": {"role": "user", "content": "teach me closures in go"}}]
        for path in paths:
            rows.append({"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "t1", "name": tool, "input": {"file_path": str(path), "content": "x"}}]}})
        target.write_text("\n".join(json.dumps(r) for r in rows) + "\nnot json\n")
        return target

    def run_hook(self, cwd=None, event="SessionStart", source="compact", transcript=None, written=None):
        if transcript is None and written is not None:
            transcript = self.transcript(*written)
        payload = {"hook_event_name": event, "session_id": "s1", "cwd": str(cwd or self.repo), "source": source}
        if transcript is not None:
            payload["transcript_path"] = str(transcript)
        env = dict(os.environ, LEARNING_NOTES_ROOT=str(self.root))
        out = subprocess.run(["python3", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(out.returncode, 0, out.stderr)
        return json.loads(out.stdout) if out.stdout.strip() else None

    def context(self, result):
        return result["hookSpecificOutput"]["additionalContext"]

    def test_no_pending_means_silent(self):
        done = self.folder / "middleware-in-go.md"
        done.write_text(DONE_FILE)
        self.assertIsNone(self.run_hook(written=[done]))

    def test_pending_from_another_chat_is_silent(self):
        (self.folder / "gmp-scheduler.md").write_text(PENDING_FILE.replace("closures in go", "gmp scheduler"))
        self.assertIsNone(self.run_hook(written=[]))
        other = self.folder / "middleware-in-go.md"
        other.write_text(DONE_FILE)
        self.assertIsNone(self.run_hook(written=[other]))

    def test_no_transcript_is_silent(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook())
        self.assertIsNone(self.run_hook(transcript=Path(self.tmp.name) / "missing.jsonl"))

    def test_edit_counts_as_written(self):
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        ctx = self.context(self.run_hook(transcript=self.transcript(path, tool="Edit")))
        self.assertIn("closures in go", ctx)

    def test_review_and_settings_writes_do_not_count(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        review = self.folder / "closures-in-go.review.md"
        review.write_text(PENDING_FILE)
        settings = self.folder / "settings.md"
        settings.write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(written=[review, settings]))

    def test_no_folder_means_silent(self):
        self.assertIsNone(self.run_hook(cwd=self.tmp.name))

    def test_pending_is_reported(self):
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        (self.folder / "middleware-in-go.md").write_text(DONE_FILE)
        result = self.run_hook(source="compact", written=[path])
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
        ctx = self.context(self.run_hook(written=[self.folder / "a.md", self.folder / "b.md"]))
        self.assertIn("closures in go", ctx)
        self.assertIn("git rebase", ctx)
        self.assertIn("which to continue", ctx)

    def test_backups_and_log_are_ignored(self):
        (self.folder / "backups").mkdir()
        (self.folder / "log").mkdir()
        (self.folder / "backups" / "old.md").write_text(PENDING_FILE)
        (self.folder / "log" / "lesson.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(written=[self.folder / "backups" / "old.md", self.folder / "log" / "lesson.md"]))

    def test_symlink_is_ignored(self):
        real = Path(self.tmp.name) / "elsewhere.md"
        real.write_text(PENDING_FILE)
        (self.folder / "link.md").symlink_to(real)
        self.assertIsNone(self.run_hook(written=[self.folder / "link.md"]))

    def test_startup_resume_clear_are_silent(self):
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        for source in ("startup", "resume", "clear"):
            self.assertIsNone(self.run_hook(source=source, written=[path]), source)

    def test_other_event_is_silent(self):
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(event="Stop", written=[path]))

    def test_output_size_does_not_grow_with_notes(self):
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE + ("\n## Node\nFacts: x\n" * 2000))
        small = len(self.context(self.run_hook(written=[path])))
        self.assertLess(small, 1200)

    def test_mode_on_startup_gives_context(self):
        (self.folder / "settings.md").write_text(MODE_ON)
        ctx = self.context(self.run_hook(source="startup"))
        self.assertIn("teach as we go is on", ctx)
        self.assertIn("skills/learn/teach-as-we-go.md", ctx)
        self.assertIn(str(self.folder / "codebase.md"), ctx)
        self.assertIn("5 lines", ctx)
        self.assertIn("## <folder>", ctx)
        self.assertNotIn("compacted", ctx)

    def test_mode_on_every_source(self):
        (self.folder / "settings.md").write_text(MODE_ON)
        for source in ("startup", "resume", "clear", "compact", "fork"):
            self.assertIn("teach as we go is on", self.context(self.run_hook(source=source)), source)

    def test_mode_off_is_silent(self):
        (self.folder / "settings.md").write_text(MODE_OFF)
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(source="startup"))

    def test_no_settings_is_silent(self):
        (self.folder / "closures-in-go.md").write_text(PENDING_FILE)
        self.assertIsNone(self.run_hook(source="startup"))

    def test_compact_with_both_gives_both(self):
        (self.folder / "settings.md").write_text(MODE_ON)
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        ctx = self.context(self.run_hook(source="compact", written=[path]))
        self.assertIn("where does the variable n live?", ctx)
        self.assertIn("teach as we go is on", ctx)
        self.assertLess(ctx.index("compacted"), ctx.index("teach as we go is on"))

    def test_mode_context_is_constant_size(self):
        (self.folder / "settings.md").write_text(MODE_ON)
        small = len(self.context(self.run_hook(source="startup")))
        (self.folder / "settings.md").write_text(MODE_ON + "Other: x\n" * 3000)
        (self.folder / "codebase.md").write_text("# web-api codebase\n" + "\n## folder/n\nFacts: x\n" * 4000)
        self.assertEqual(len(self.context(self.run_hook(source="startup"))), small)

    def test_symlinked_settings_is_ignored(self):
        real = Path(self.tmp.name) / "settings.md"
        real.write_text(MODE_ON)
        (self.folder / "settings.md").symlink_to(real)
        self.assertIsNone(self.run_hook(source="startup"))

    def test_bad_file_is_skipped(self):
        (self.folder / "bad.md").write_bytes(b"\xff\xfe\x00broken")
        path = self.folder / "closures-in-go.md"
        path.write_text(PENDING_FILE)
        self.assertIn("closures in go", self.context(self.run_hook(written=[self.folder / "bad.md", path])))


if __name__ == "__main__":
    unittest.main()
