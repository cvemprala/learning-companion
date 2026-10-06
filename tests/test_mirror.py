import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "mirror.py"


def row(kind, blocks, stamp="2026-10-05T20:00:00.000Z", meta=False):
    r = {"type": kind, "timestamp": stamp, "message": {"role": kind, "content": blocks}}
    if meta:
        r["isMeta"] = True
    return r


def text(t):
    return {"type": "text", "text": t}


def skill_call(args, call_id="s9"):
    return row("assistant", [{"type": "tool_use", "id": call_id, "name": "Skill", "input": {"skill": "learning-companion:learn", "args": args}}])


def lesson_rows(with_skill=True):
    rows = [row("user", [text("teach me git rebase")])]
    if with_skill:
        rows.append(row("assistant", [{"type": "tool_use", "id": "s1", "name": "Skill", "input": {"skill": "learning-companion:learn", "args": "git rebase"}}]))
    rows.append(row("user", [text("Base directory for this skill: /x\n\n# Learn\n...")], meta=True))
    rows.append(row("assistant", [{"type": "tool_use", "id": "q1", "name": "AskUserQuestion", "input": {"questions": [{"question": "Probe 1: What is a commit ID made from?", "header": "Probe 1", "options": [{"label": "Content and parent"}, {"label": "Only content"}]}]}}]))
    rows.append(row("user", [{"type": "tool_result", "tool_use_id": "q1", "content": 'Your questions have been answered: "Probe 1: What is a commit ID made from?"="Content and parent". You can now continue with these answers in mind.'}]))
    rows.append(row("assistant", [text("Map:\n\n```mermaid\ngraph TD\n  A --> B\n```\n\nDoes this look right?")]))
    rows.append(row("user", [text("Stop hook feedback: rewrite")]))
    rows.append(row("user", [text("yes go")]))
    return rows


class MirrorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "notes"
        self.repo = Path(self.tmp.name) / "web-api"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.transcript = Path(self.tmp.name) / "t.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def write_transcript(self, rows, extra_lines=()):
        with open(self.transcript, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
            for line in extra_lines:
                f.write(line + "\n")

    def run_hook(self, cwd=None, event="Stop", session="abcdef1234567890", last_reply=None, tz="UTC"):
        payload = {"hook_event_name": event, "session_id": session, "transcript_path": str(self.transcript), "cwd": str(cwd or self.repo)}
        if last_reply is not None:
            payload["last_assistant_message"] = last_reply
        env = dict(os.environ, LEARNING_NOTES_ROOT=str(self.root), TZ=tz)
        out = subprocess.run(["python3", str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, "")
        return out

    def logs(self):
        return sorted(self.root.rglob("log/*.md")) if self.root.exists() else []

    def test_no_skill_means_no_file(self):
        self.write_transcript(lesson_rows(with_skill=False))
        self.run_hook()
        self.assertEqual(self.logs(), [])

    def test_lesson_is_rendered(self):
        self.write_transcript(lesson_rows())
        self.run_hook()
        files = self.logs()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].parent.parent.name, "web-api")
        self.assertEqual(files[0].name, "2026-10-05-git-rebase-abcdef12.md")
        body = files[0].read_text()
        self.assertIn("# git rebase", body)
        self.assertIn("### You\n\nteach me git rebase", body)
        self.assertIn("### Question\n\nProbe 1: What is a commit ID made from?\n\nOptions: Content and parent / Only content", body)
        self.assertIn("**Answer:** Content and parent", body)
        self.assertIn("```mermaid", body)
        self.assertNotIn("Base directory", body)
        self.assertNotIn("Stop hook feedback", body)
        self.assertIn("### You\n\nyes go", body)

    def test_mark_this_is_not_a_lesson(self):
        self.write_transcript([row("user", [text("mark this")]), skill_call("mark this"), row("assistant", [text("## sites/handlers\nMark: Seen")])])
        self.run_hook()
        self.assertEqual(self.logs(), [])

    def test_teach_as_we_go_is_not_a_lesson(self):
        self.write_transcript([row("user", [text("teach as we go")]), skill_call("Teach as we go"), row("assistant", [text("On.")])])
        self.run_hook()
        self.assertEqual(self.logs(), [])

    def test_stop_teaching_is_not_a_lesson(self):
        self.write_transcript([row("user", [text("stop teaching as we go")]), skill_call("stop teaching as we go"), row("assistant", [text("Off.")])])
        self.run_hook()
        self.assertEqual(self.logs(), [])

    def test_lesson_plus_mark_is_mirrored(self):
        rows = lesson_rows() + [row("user", [text("mark this")]), skill_call("mark this: parseOrgHeader")]
        self.write_transcript(rows)
        self.run_hook()
        files = self.logs()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "2026-10-05-git-rebase-abcdef12.md")

    def test_mirror_off_means_no_file(self):
        self.root.mkdir(parents=True)
        (self.root / "settings.md").write_text("# Learning Companion settings\nTheme: light\nMirror: off\n")
        self.write_transcript(lesson_rows())
        self.run_hook()
        self.assertEqual(self.logs(), [])

    def test_rerun_is_identical(self):
        self.write_transcript(lesson_rows())
        self.run_hook()
        first = self.logs()[0].read_text()
        self.run_hook()
        self.assertEqual(len(self.logs()), 1)
        self.assertEqual(self.logs()[0].read_text(), first)

    def test_bad_lines_are_skipped(self):
        self.write_transcript(lesson_rows(), extra_lines=["not json", "{\"type\": \"user\"}"])
        self.run_hook()
        self.assertEqual(len(self.logs()), 1)

    def test_no_git_means_general(self):
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        self.write_transcript(lesson_rows())
        self.run_hook(cwd=plain)
        self.assertEqual(self.logs()[0].parent.parent.name, "general")

    def test_other_event_does_nothing(self):
        self.write_transcript(lesson_rows())
        self.run_hook(event="SessionStart")
        self.assertEqual(self.logs(), [])

    def test_lagging_transcript_gets_last_reply(self):
        self.write_transcript(lesson_rows())
        self.run_hook(last_reply="Node 1 of 4: Closure keeps its variables.")
        body = self.logs()[0].read_text()
        self.assertTrue(body.rstrip().endswith("### Claude\n\nNode 1 of 4: Closure keeps its variables."))
        self.assertEqual(body.count("Node 1 of 4"), 1)

    def test_last_reply_already_in_transcript_is_not_doubled(self):
        rows = lesson_rows() + [row("assistant", [text("Final line.")])]
        self.write_transcript(rows)
        self.run_hook(last_reply="Final line.")
        self.assertEqual(self.logs()[0].read_text().count("Final line."), 1)

    def test_date_uses_local_time(self):
        rows = lesson_rows()
        for r in rows:
            r["timestamp"] = "2026-10-06T00:14:00.000Z"
        self.write_transcript(rows)
        self.run_hook(tz="America/Los_Angeles")
        self.assertEqual(self.logs()[0].name, "2026-10-05-git-rebase-abcdef12.md")

    def test_missing_transcript_does_nothing(self):
        self.transcript = Path(self.tmp.name) / "missing.jsonl"
        self.run_hook()
        self.assertEqual(self.logs(), [])


if __name__ == "__main__":
    unittest.main()
