# Learning Companion

A Claude Code plugin that teaches hard topics so they stay understood, not memorized.
You say "teach me X". Claude finds the edge of what you know and draws a map of the topic.
It teaches one node at a time, then asks you to derive a fact it never told you. It saves a
graph of what you understand, and the next session starts from your weakest node.

## Credits

Everything here starts with Eero Alvar. His video
[How I Learn Difficult Things](https://www.youtube.com/watch?v=ciC6ffUqI8k) gives the
framework: understanding is the links between facts, not the pile. His repo
[amosblomqvist/learn](https://github.com/amosblomqvist/learn) turns that framework into a
three phase process for the pi coding agent: probe, plan, teach. He shows it in his second
video, [How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU).

Learning Companion is motivated and inspired explicitly by that repo. It rebuilds the
process for Claude Code in its own words, and adds a saved knowledge graph so the system
remembers what you understand. Everything below is my reading of his ideas, written as
steps I can follow.

## Install

You need [Claude Code](https://code.claude.com/docs/en/setup). No other tools.

Run these two commands in Claude Code, one at a time.

```text
/plugin marketplace add cvemprala/learning-companion
```

```text
/plugin install learning-companion@learning-companion
```

Restart Claude Code. Then say "teach me how git rebase works" or any topic you want.

One setting to change first. Claude Code shows grey predicted text in the input box, called
prompt suggestions. During a lesson that text is often the answer. Turn it off in `/config`
under **Prompt suggestions**, or add this to `~/.claude/settings.json`:

```json
{ "promptSuggestionEnabled": false }
```

To try it from a local clone without installing:

```sh
claude --plugin-dir /path/to/learning-companion
```

Your saved graphs go in `~/.learning/` by default. Set `LEARNING_NOTES_ROOT` to change it.

## What a session looks like

1. You say "teach me how git rebase works".
2. One picker: Full lesson, Quick (footholds and one derivation), or Resume.
3. Probe. Graded questions, starting from the deepest root, until the edge is found. Each answer is graded on the next question. Options are sorted A to Z, so the right one is not always first.
4. Map. Drawn as a picture, listed in chat. You approve it.
5. Teach. One node at a time. Foothold, Edge, Your turn, Click.
6. Test. Derive something untold.
7. Save. The graph gets its marks, the review sheet is written, and the lesson lands in the Obsidian log.

## Read more

| Page | For |
|---|---|
| [The method](docs/method.md) | Why each step is there, with the two students example and the 9 steps |
| [Commands](docs/commands.md) | Everything you can type, and every word that works inside a lesson |
| [Learn while you work](docs/learn-while-you-work.md) | Teach as we go, mark this, and when to use the Learning output style instead |
| [Your notes and Obsidian](docs/notes-and-obsidian.md) | The graph, the review sheet, the log, settings, and opening it all as a vault |
| [Tools people already use](docs/prior-work.md) | learn, vibe-wise, the Learning output style, and /teach, and what this one does |
| [Development](docs/development.md) | Layout, tests, how a skill change is checked, how to ship |

## Status

Version 0.1.14. Used daily by one person since 2026-10-05, across 4 live lessons. 32
hook tests pass. Every skill change is checked with 2 clean subagent runs before it
ships. Teach as we go is an experiment, shipped as one commit so one revert removes it.
Feedback welcome. Open an issue with the session that went wrong and what you expected.

## License

[MIT](LICENSE). Anyone can use, copy, change, and share this work, including for
commercial use. Keep the license notice with copies. The ideas come from Eero Alvar, as
credited above. The words and files here are my own.
