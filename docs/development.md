# Development

How the plugin is built, tested, and shipped. For people sending a change.

## Repository layout

```
.claude-plugin/plugin.json      plugin manifest
skills/learn/SKILL.md           the teaching process
skills/learn/graph-template.md  the saved graph format
skills/learn/pictures.md        when and how to draw, with the theme setting
skills/learn/teach-as-we-go.md  one Predict question per folder during work, and mark this
skills/reset/SKILL.md           back up one topic and start over
agents/researcher.md            fact checker subagent
hooks/session_start.py          asks an open question again after a compaction, says when teach as we go is on
hooks/mirror.py                 writes each lesson to a markdown log for Obsidian
tests/                          hook tests, run with python3 -m unittest discover -s tests
```

## Run the tests

```sh
python3 -B -m unittest discover -s tests
claude plugin validate .
```

The hook tests build fake transcripts and notes folders in a temp directory and run the
hooks as real processes with JSON on stdin. 32 tests as of 0.1.15.

## Test a skill change

A skill is text, so the test is a model following it. Every change to a skill file gets 2
clean runs in a row from a subagent before it ships. The prompt says "Step 1: use the Read
tool on <file>. This Read is required. Step 2: follow that file. After the Read, call no other
tools." A prompt that says "do not call tools" right after "read the file" makes the model
skip the read. The test then measures nothing.

## Try a local copy

```sh
claude --plugin-dir /path/to/learning-companion
```

## Ship a change

1. Bump `version` in `.claude-plugin/plugin.json`. Installed copies update only on a version
   change. A README only change needs no bump.
2. Write the commit message for a reader who was not there. Subject: what a person gets.
   Body: what was wrong, what changed, what was measured, what reversed and why, what is
   left out. Plain words. No sentence over 25 words.
3. Push to main. Installed copies pick it up on their next marketplace update.

## Language rules for every file

Short sentences. Common words. Define a term in the sentence it first appears. Give the
number, not the idea of the number. No em dashes or en dashes. These rules apply to the
skill text, the README, the docs, and commit messages.
