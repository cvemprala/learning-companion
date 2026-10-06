"""Ask the open lesson question again after a compaction, and say when
teach as we go is on for this repo.

The pending check fires only on the compact source. Opening Claude Code in a
folder is not a promise to learn, so startup, resume, and clear stay silent.
Compaction happens inside a long chat, so if a lesson has an open question
then, the learner is mid lesson and the question would be lost without this.
The mode check fires on every source. It reads one line of the per repo
settings file and nothing else. The learner turned the mode on, so saying so
at startup keeps that promise.
Output size does not grow with the notes. Any error ends with exit 0 and
no output, so a session always continues.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MAX_TOPICS = 5
MODE_LINE = re.compile(r"Mode:\s*teach as we go\s*", re.IGNORECASE)


def notes_root():
    raw = os.environ.get("LEARNING_NOTES_ROOT", "").strip()
    return Path(raw).expanduser() if raw else Path.home() / ".learning"


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


def pending_of(path):
    if path.is_symlink() or not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    match = re.search(r"^## Pending\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not match:
        return None
    block = match.group(1)
    stage = re.search(r"^Stage:\s*(.+)$", block, re.M)
    question = re.search(r"^Question:\s*(.+?)(?=^\w+:|^Awaiting|\Z)", block, re.S | re.M)
    heading = re.search(r"^# (.+)$", text, re.M)
    return {
        "topic": heading.group(1).strip() if heading else path.stem,
        "stage": stage.group(1).strip() if stage else "unknown",
        "question": " ".join(question.group(1).split())[:300] if question else "",
        "path": str(path),
    }


def find_pending(folder):
    if not folder.is_dir():
        return []
    found = []
    for path in sorted(folder.glob("*.md")):
        item = pending_of(path)
        if item:
            found.append(item)
    return found


def context_for(items):
    lines = [
        "Learning Companion: the chat was just compacted and a lesson has an open question. "
        "A compaction is not an answer.",
        "Before doing anything else, use Read on the learn skill at "
        f"{PLUGIN_ROOT / 'skills/learn/SKILL.md'} and on the topic file below.",
        "Then ask the pending question again, exactly as saved, with the same picker when it was a probe.",
        "",
    ]
    for item in items[:MAX_TOPICS]:
        lines.append(f"Topic: {item['topic']}. Stage: {item['stage']}. File: {item['path']}.")
        if item["question"]:
            lines.append(f"Question: {item['question']}")
    if len(items) > MAX_TOPICS:
        lines.append(f"And {len(items) - MAX_TOPICS} more. Ask the learner which topic to continue.")
    elif len(items) > 1:
        lines.append("More than one topic is open. Ask the learner which to continue.")
    return "\n".join(lines)


def mode_on(folder):
    path = folder / "settings.md"
    if path.is_symlink() or not path.is_file():
        return False
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return False
    return any(MODE_LINE.fullmatch(line) for line in lines)


def mode_context(folder):
    return "\n".join([
        "Learning Companion: teach as we go is on for this repo. The learner asked for this.",
        f"Before you change any code, use Read on {PLUGIN_ROOT / 'skills/learn/teach-as-we-go.md'} and follow it.",
        f"Graph file: {folder / 'codebase.md'}. A folder is met when that file has a `## <folder>` heading. "
        "Nothing else counts.",
        "The one rule: before a change of 5 lines or more in a folder that is not met, ask one Predict question. "
        "Config, docs, and tests never ask. One question per folder, ever.",
    ])


def run(payload):
    if not isinstance(payload, dict) or payload.get("hook_event_name") != "SessionStart":
        return None
    cwd = payload.get("cwd") or os.getcwd()
    folder = notes_root() / repo_folder(cwd)
    parts = []
    if payload.get("source") == "compact":
        items = find_pending(folder)
        if items:
            parts.append(context_for(items))
    if mode_on(folder):
        parts.append(mode_context(folder))
    if not parts:
        return None
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n\n".join(parts)}}


def main():
    try:
        output = run(json.loads(sys.stdin.read(1 << 20)))
    except Exception:
        return
    if output:
        print(json.dumps(output))


if __name__ == "__main__":
    main()
