---
name: reset
description: Use when the user asks to reset, clear, restart, or forget their learning notes for a topic, or to start a topic over from zero.
disable-model-invocation: true
---

# Reset one topic

Moves one topic's graph file and its lesson logs into a backups folder and leaves everything else alone.
Runs only when the user invokes it. Nothing moves before the user confirms in a picker.

## Find the files

Root folder: `LEARNING_NOTES_ROOT`, default `~/.learning/`.
Repo folder: the name of the git root folder, or `general` when there is no repo.
Topic files: every `*.md` in that folder, not `settings.md`, not `*.review.md`, and not in `backups/` or `log/`.
Review sheet: `<topic>.review.md` next to the graph, when it exists. It moves with the graph.
Log files: every `*.md` in `log/` whose `topic:` line matches the topic heading, compared in lowercase.

If the folder has no topic files, say "No learning notes for this repo" and stop.

## Ask which topic

If the user named a topic, match it to one file by its `# <topic>` heading or its file name.
If the match is unclear or no topic was named, ask one AskUserQuestion with the topic names as options.
When the folder has 2 or more topics, add one more option: **All topics in <repo>**.
With more than 3 topics, list them in chat and ask the user to type one, or "all".

## Show, then confirm

Before asking, show in chat:

- The file path, or for all topics, the folder path and the list of files.
- The node count and how many are Strong, per file.
- Where the backup will go: `<repo folder>/backups/<file name>-<YYYY-MM-DD-HHMM>.md`. All topics share one stamp.
- The log files for this topic, by name, and where they go: `<repo folder>/backups/log/<same name>`. Say "no logs" when there are none.
- One line: the map pictures on claude.ai are not deleted. Only the local links go.

Then one AskUserQuestion, header `Reset`, two options: **Cancel** (keep the notes) and **Reset topic** (back up and start over).
For all topics the second option is **Reset all N topics**, with N the count.
Invoking the command is not a confirmation. Silence is not a confirmation. Only the reset option is.

## Do it

On Cancel: say "Nothing changed" and stop.

On Reset topic:

1. `mkdir -p` the backups folder.
2. If the backup name already exists, add seconds to the stamp. Never overwrite a backup.
3. `mv` the topic file to the backup path. Move `<topic>.review.md` the same way, with the same stamp. For all topics, move each file in turn with the shared stamp.
4. `mkdir -p` `backups/log/`, then `mv` each matching log file there, keeping its name. If the name exists, add the stamp.
5. Show the backup paths, graph and logs. Say "Say teach me <topic> to start over".

If the move fails, show the error. Do not say it was reset. Do not try another file.

## Never

- Never delete. Only move into `backups/`.
- Never touch another repo folder or `backups/`. In `log/`, move only files whose topic matches. One topic means one graph file and its logs. All topics means every graph file and every log in this folder.
- Never edit the file before moving it.
- Never run without the picker answer **Reset topic**.
