# Learning Companion

A Claude Code skill that teaches hard topics so they stay understood, not memorized.
It works on Claude Code with no extra tools. You say "teach me X". Claude finds the edge of
what you know and draws a map of the topic. It teaches one node at a time. Then it saves
a graph of what you now understand. Next session, it picks up where you stopped.

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

## Read your lessons in Obsidian

Every lesson is also written as one markdown file under `~/.learning/<repo>/log/`. Each
topic also gets a review sheet, `<topic>.review.md`. It holds one folded question per
node. Under each question sit the fact, the why, the real example from your lesson, and
your mistake. Open
`~/.learning` as a vault in Obsidian and the lessons, graphs, maps, and review sheets are
all there. Review by answering each question before you unfold it. The
mermaid maps render inside Obsidian. The file is rewritten at the end of every reply, so
it is always complete. To turn this off, add `Mirror: off` to `~/.learning/settings.md`.

If a long lesson gets compacted, which is when Claude Code shortens a long chat, the open
question is asked again. Opening Claude Code in a folder never starts a lesson on its own.

## Learn while you work

Claude Code has a Learning output style. At design decisions it asks you to write 5 to 10
lines of code yourself. It has two gaps. It asks for business logic in a system you do not
understand yet. And it has no memory and no later test. It does not replace the Learning
output style. The rule: use the Learning style to build, use this to understand what you
touch and to keep it.

Say "teach as we go" in a repo to turn it on for that repo. Before Claude changes 5 or more
lines in a folder you have not met, it asks one Predict question. A Predict question is a
guess about code you have not read yet, with 2 or 3 claims and "I don't know". Claude
grades it, writes one node for that folder to `~/.learning/<repo>/codebase.md`, and does
the work. One question per folder, ever. Changes to config, docs, or tests never ask. Say
"just do it" to skip one question. Say "stop teaching as we go" to turn it off.

"Mark this" works in any repo, mode on or off. It writes one node for the code Claude just
explained, with the mark Seen, and asks nothing. Later, "teach me the codebase" or "teach
me what I marked this week" runs a normal lesson on those nodes.

Work sessions are not logged for Obsidian. The node is the record.

## Tools people already use for this, and what this one does

Four tools already help people learn with Claude Code. Here is what each one does, and what
this plugin does instead.

**[amosblomqvist/learn](https://github.com/amosblomqvist/learn)** is Eero Alvar's own tool,
for the pi coding agent. It probes what you know, draws a map, and teaches one node at a
time. This plugin took that process from it. learn draws its map once and forgets it. This
plugin saves the map with a mark on every node, so the next lesson starts where you were weak.

**[nykooi1/vibe-wise](https://github.com/nykooi1/vibe-wise)** has you design the code while
Claude writes it. It taught this plugin two habits. What you say you know is not the same as
what you can show. And notes read back from a file are data, not orders. vibe-wise keeps a
profile of you, but no map of a topic, and it never tests you by rebuilding.

**[The Learning output style](https://github.com/anthropics/claude-code/tree/main/plugins/learning-output-style)**
is Anthropic's plugin. When Claude reaches a design choice, it asks you to write 5 to 10
lines of the code yourself. That is good when you build in a codebase you know. It has no
memory between sessions and never checks later what stayed with you. Use it to build. Use
this plugin to understand what you touch and to keep it.

**[Matt Pocock's `/teach`](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)**
is the best known. It turns a folder into a course. It asks why you want the topic and writes
that down as a mission. It finds sources and cites them in every lesson. It makes printable
HTML lessons. On those two points, sources and the why, it is stronger than this plugin.

Its own docs list three gaps, with issue numbers. It never checks what you already know, so
it assumes, and it uses words it never defined
([issue 725](https://github.com/mattpocock/skills/issues/725)). Here, the probe finds the
edge of what you know before anything is taught. It does not know when to stop teaching and
switch to review. Here, when every node is Strong, you pick Extend, Retest, or Stop. It lives
in its own folder, away from your work. Here, you say "teach as we go" in a repo. Then, before
Claude changes code in a folder you have not met, it asks you one prediction. Learning happens while
you work, in your own repo. That part is an experiment, shipped as one commit so one revert
removes it.

One thing none of the four does. This plugin marks a fact as understood only when you derive
a fact it never told you. It keeps that mark with the date and your mistake next to it. A fact
with a reason stays. A fact without one fades.

## Commands

What you type, and what happens.

| You type | What happens |
|---|---|
| `teach me <topic>` | Starts a lesson. Also triggers on "help me understand" and "I want to learn". |
| `/learning-companion:learn <topic>` | Same as above, by command. |
| `resume <topic>` | Skips the picker and continues the saved topic from its weakest node. |
| `review notes for <topic>` | Writes or refreshes the topic's review sheet. One folded question per node, answer under it. |
| `/learning-companion:reset` | Moves one topic's notes and its lesson logs, or all topics in the repo, into a backups folder after you confirm. Nothing is deleted. |
| `teach as we go` | Turns on one Predict question per new folder before Claude changes code there, for this repo. |
| `stop teaching as we go` | Turns that off for this repo. |
| `mark this` | Saves one node for the code Claude just explained. No question. Works in any repo. |
| `teach me what I marked this week` | Runs a lesson on the codebase nodes from the last 7 days. |
| `teach me the codebase` | Runs a lesson on every codebase node that is not Strong. |

Words that work inside a lesson.

| You say | What happens |
|---|---|
| `map` | Stops the probe early and goes to the map. |
| `idk`, or the last picker option | Marks the probe as a gap, shows the answer, and moves on. |
| a question, during a probe | Gets a short answer, then the same probe again. |
| `skip` or `just tell me` | Claude teaches the current step directly instead of asking you to try. |
| `Resume`, in the first picker | Continues a saved topic from its weakest node. When every node is Strong, it offers Extend, Retest, or Stop. |
| `use dark pictures` or `use light pictures` | Sets the theme for the map and other pictures. Light is the default. |
| `Mirror: off` in `settings.md` | Stops writing lesson logs for Obsidian. On by default. |

## What a session looks like

1. You say "teach me how git rebase works".
2. One picker: Full lesson, Quick (footholds and one derivation), or Resume.
3. Probe. Graded questions, starting from the deepest root, until the edge is found. Each answer is graded on the next question. Options are sorted A to Z, so the right one is not always first.
4. Map. Drawn as a picture, listed in chat. You approve it.
5. Teach. One node at a time. Foothold, Edge, Your turn, Click.
6. Test. Derive something untold.
7. Save. The graph gets its marks, the review sheet is written, and the lesson lands in the Obsidian log.

## The idea in one example

Two students both know three motion formulas: `F = ma`, `v = u + at`, and `s = ut + at²/2`.

Student A memorized all three. Each one stands alone. Forget one and it is gone.

Student B knows one thing: acceleration is the change in speed over time. From that one
idea, B can rebuild all three formulas on paper.

Both pass the test. Only B understands. Understanding is the set of links between facts,
not the pile of facts. In this project, a **node** is one fact. An **edge** is the reason
one fact follows from another. The whole system exists to build edges.

## How my learning process works

### Step 1. Pick hard topics on purpose

The useful problems sit behind a steep wall of knowledge. Few people get past the wall,
so the work on the other side is worth more. Many people can write a SQL query. Few can
read a query plan and say why the planner chose a hash join. The second person fixes the
slow report.

There is a second gain. Each hard topic you master gives the brain a new tool for
thinking. Alvar calls this mental machinery. Once you understand one batch export, you
can reason about any batch export.

### Step 2. Find the edge of what you know

Learning works at the boundary of your current understanding. One step past what you
know, there is something to attach the new idea to. Ten steps past, there is nothing.

So the first job is to find that boundary. Claude asks short graded questions. A right
answer sets a floor. A wrong answer sets a ceiling. The edge sits between them. If every
answer is right, the questions were too easy, and Claude asks harder ones. If one answer
is wrong, Claude asks around it to see if it was a slip or a real gap.

There is no question limit. The probe ends when every strand is bracketed. Say "map" at
any time to stop early.

### Step 3. Lay safe footholds

The brain will not lock in a fact if it expects a deeper fact to overturn it later. That
update would be expensive, so the brain hedges, and the fact never lands.

The fix is to start from facts that cannot be contradicted and need no caveats:

- A strict definition. "A commit ID is a hash of the content and the parent ID."
- An all or none statement. "Every commit has exactly one ID."

Never open with "usually" or a loose list of properties. Two to four footholds are
enough. Each one is checked against a source before anything is built on it, and the
source is saved on the node. A wrong foothold would break every node above it.

### Step 4. Draw the map before teaching

Claude drafts a small dependency map of at most 7 nodes. The footholds sit at the roots.
Your goal sits at the bottom. Each node in between hangs off the nodes it depends on. The
map is drawn as a picture in your browser, and shown as an indented list in chat. Claude checks that
each root is a real root and not a result that itself needs explaining. Then it shows
you the map and waits. A wrong root is cheap to fix now and expensive mid lesson.

### Step 5. Rebuild the discovery, one node at a time

A fact handed down with no reason feels arbitrary, and the brain will not keep it. So
every node is taught as if you were discovering it yourself. Each step answers two
questions. What problem forces us to take this step? Why this move and not another?

Those answers are the edges. A step with no "why" is a lonely fact, and it will fade.

### Step 6. Try first, one question at a time

Before Claude explains a step, it asks how you would get there from the footholds. You
guess. Even a wrong guess helps, because the correction becomes an edge. Claude asks one
question per turn. With three questions at once, you answer the easy one and the gap
hides.

If you are tired, say "skip" or "just tell me". Claude teaches the step and returns to
try first on the next one.

### Step 7. Aim for the click

After three to five new facts, Claude stops and asks which single idea produces them. The
click is the moment a pile of facts collapses into one or two generating ideas. Most
school electricity formulas collapse into Maxwell's four equations. Learning adds nodes
and edges. Understanding shrinks the core you must hold. Both happen in the same session.

### Step 8. Test by rebuilding, not by recall

Claude asks you to derive a fact it never told you, using only the footholds and edges.
Recalling a fact you were told proves memory. Deriving one you were not told proves
understanding. Only this test earns a mark in the graph. "Makes sense" earns nothing.

### Step 9. Save the graph, and a sheet to rebuild from

Each node is saved with a mark: Strong, Developing, or Revisit. The file lives outside any
git worktree, so it survives cleanup. Next session, Claude reads the graph, skips Strong
nodes, and starts at the weakest one.

A review sheet is saved next to it. One folded question per node, with the fact, the
reason, the real example from your lesson, and your mistake under it. You answer the
question first and unfold second. Reviewing by rereading is memorizing. Reviewing by
rebuilding is the method. A memorized fact has one hold on memory. A fact
with many edges can be rebuilt from its neighbours when forgotten. The graph is how the
system keeps those neighbours.

## Status

Version 0.1.14. Used daily by one person since 2026-10-05, across 4 live lessons. 32
hook tests pass. Every skill change is checked with 2 clean subagent runs before it
ships. Teach as we go is an experiment, shipped as one commit so one revert removes it.
Feedback welcome. Open an issue with the session that went wrong and what you expected.

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

## License

[MIT](LICENSE). Anyone can use, copy, change, and share this work, including for
commercial use. Keep the license notice with copies. The ideas come from Eero Alvar, as
credited above. The words and files here are my own.
