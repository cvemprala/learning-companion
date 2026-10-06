---
name: reset
description: Use when the user asks to reset, clear, restart, or forget their learning notes for a topic, or to start a topic over from zero.
disable-model-invocation: true
---

# Reset one topic

Moves one topic's graph file into a backups folder and leaves everything else alone.
Runs only when the user invokes it. Nothing moves before the user confirms in a picker.

## Find the files

Root folder: `LEARNING_NOTES_ROOT`, default `~/.learning/`.
Repo folder: the name of the git root folder, or `general` when there is no repo.
Topic files: every `*.md` in that folder, not in `backups/`.

If the folder has no topic files, say "No learning notes for this repo" and stop.

## Ask which topic

If the user named a topic, match it to one file by its `# <topic>` heading or its file name.
If the match is unclear or no topic was named, ask one AskUserQuestion with the topic names as options.
With more than 4 topics, list them in chat and ask the user to type one.

## Show, then confirm

Before asking, show in chat:

- The file path.
- The topic's node count and how many are Strong.
- Where the backup will go: `<repo folder>/backups/<file name>-<YYYY-MM-DD-HHMM>.md`.
- One line: the map picture on claude.ai is not deleted. Only the local link to it goes.

Then one AskUserQuestion, header `Reset`, two options: **Cancel** (keep the notes) and **Reset topic** (back up and start over).
Invoking the command is not a confirmation. Silence is not a confirmation. Only **Reset topic** is.

## Do it

On Cancel: say "Nothing changed" and stop.

On Reset topic:

1. `mkdir -p` the backups folder.
2. If the backup name already exists, add seconds to the stamp. Never overwrite a backup.
3. `mv` the topic file to the backup path.
4. Show the backup path. Say "Say teach me <topic> to start over".

If the move fails, show the error. Do not say it was reset. Do not try another file.

## Never

- Never delete. Only move into `backups/`.
- Never touch another topic, another repo folder, or `backups/`.
- Never edit the file before moving it.
- Never run without the picker answer **Reset topic**.
