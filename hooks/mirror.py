"""Mirror a lesson into a markdown file that Obsidian can open.

Runs on the Stop event. Reads the session transcript. If the learn skill was
used in this session, renders the whole lesson to <root>/<repo>/log/<file>.md.
Rewrites the file each time, so running twice gives the same result.
Never blocks the session: any error ends with exit 0 and no output.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_NAME = "learning-companion:learn"
SKIP_USER_PREFIXES = ("Base directory for this skill", "Stop hook feedback:", "[Request interrupted")


def notes_root():
    raw = os.environ.get("LEARNING_NOTES_ROOT", "").strip()
    return Path(raw).expanduser() if raw else Path.home() / ".learning"


def mirror_enabled(root):
    settings = root / "settings.md"
    if not settings.is_file():
        return True
    try:
        for line in settings.read_text(encoding="utf-8").splitlines():
            if re.fullmatch(r"Mirror:\s*off\s*", line, re.IGNORECASE):
                return False
    except (OSError, UnicodeError):
        return True
    return True


def repo_folder(cwd):
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=2,
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip()).name
    except (OSError, subprocess.SubprocessError):
        pass
    return "general"


def load_transcript(path):
    rows = []
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict) and row.get("type") in ("user", "assistant"):
                rows.append(row)
    return rows


def blocks_of(row):
    content = row.get("message", {}).get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content if isinstance(content, list) else []


def result_text(block):
    content = block.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def parse_answer(text):
    match = re.search(r'="(.*)"\.?(?:\s*You can now continue|\s*Read the answers carefully|\s*$)', text, re.S)
    return match.group(1).strip() if match else text.strip()


def slug(text, limit=40):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:limit].rstrip("-") or "lesson"


def local_date(stamp):
    try:
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        return moment.astimezone().date().isoformat()
    except (ValueError, AttributeError):
        return datetime.now().date().isoformat()


def render(rows, session_id, repo, transcript_path, last_reply=""):
    topic = None
    started = None
    skill_used = False
    questions = {}
    turns = []
    for row in rows:
        if row.get("isMeta"):
            continue
        stamp = row.get("timestamp")
        if started is None and stamp:
            started = stamp
        for block in blocks_of(row):
            kind = block.get("type")
            if kind == "text":
                text = block.get("text", "").strip()
                if not text or text.startswith(SKIP_USER_PREFIXES):
                    continue
                if row["type"] == "user" and topic is None:
                    topic = text
                turns.append(("You" if row["type"] == "user" else "Claude", text))
            elif kind == "tool_use":
                name = block.get("name")
                params = block.get("input", {}) or {}
                if name == "Skill" and params.get("skill") == SKILL_NAME:
                    skill_used = True
                    if params.get("args"):
                        topic = params["args"]
                elif name == "AskUserQuestion":
                    qs = params.get("questions") or []
                    if qs:
                        q = qs[0]
                        options = " / ".join(o.get("label", "") for o in q.get("options", []))
                        questions[block.get("id")] = len(turns)
                        turns.append(("Question", q.get("question", "").strip() + (f"\n\nOptions: {options}" if options else "")))
            elif kind == "tool_result" and block.get("tool_use_id") in questions:
                turns.append(("Answer", parse_answer(result_text(block))))
    if not skill_used:
        return None, None
    last_reply = (last_reply or "").strip()
    if last_reply and not (turns and turns[-1] == ("Claude", last_reply)):
        turns.append(("Claude", last_reply))
    topic = topic or "lesson"
    date = local_date(started) if started else datetime.now().date().isoformat()
    lines = [
        "---",
        f"topic: {topic}",
        f"repo: {repo}",
        f"date: {date}",
        f"session: {session_id}",
        f"transcript: {transcript_path}",
        "---",
        "",
        f"# {topic}",
        "",
    ]
    for label, text in turns:
        if label == "Answer":
            lines += [f"**Answer:** {text}", ""]
        else:
            lines += [f"### {label}", "", text, ""]
    filename = f"{date}-{slug(topic)}-{session_id[:8]}.md"
    return filename, "\n".join(lines)


def run(payload):
    if not isinstance(payload, dict) or payload.get("hook_event_name") != "Stop":
        return
    transcript = payload.get("transcript_path")
    session_id = str(payload.get("session_id") or "session")
    cwd = payload.get("cwd") or os.getcwd()
    if not transcript or not Path(transcript).is_file():
        return
    root = notes_root()
    if not mirror_enabled(root):
        return
    rows = load_transcript(transcript)
    repo = repo_folder(cwd)
    filename, body = render(rows, session_id, repo, transcript, payload.get("last_assistant_message"))
    if not filename:
        return
    folder = root / repo / "log"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / filename
    tmp = target.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    os.replace(tmp, target)


def main():
    try:
        run(json.loads(sys.stdin.read(1 << 20)))
    except Exception:
        return


if __name__ == "__main__":
    main()
