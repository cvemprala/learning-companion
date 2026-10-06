# Learning Companion

A Claude Code skill that teaches hard topics so they stay understood, not memorized.
It works on Claude Code with no extra tools. You say "teach me X". Claude finds the edge of
what you know and draws a map of the topic. It teaches one node at a time. Then it saves
a graph of what you now understand. Next session, it picks up where you stopped.

## Credits

Everything here starts with Eero Alvar. His video
[How I Learn Difficult Things](https://www.youtube.com/watch?v=ciC6ffUqI8k) gives the
framework: understanding is the links between facts, not the pile. His repo
[amosblomqvist/learn](https://github.com/amosblomqvist/learn), shown in his second video
[How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU), turns that
framework into a three phase process for the pi coding agent: probe, plan, teach.

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

To try it from a local clone without installing:

```sh
claude --plugin-dir /path/to/learning-companion
```

Your saved graphs go in `~/.learning/` by default. Set `LEARNING_NOTES_ROOT` to change it.

## Commands

What you type, and what happens.

| You type | What happens |
|---|---|
| `teach me <topic>` | Starts a lesson. Also triggers on "help me understand" and "I want to learn". |
| `/learning-companion:learn <topic>` | Same as above, by command. |
| `/learning-companion:reset` | Moves one topic's notes into a backups folder after you confirm. Nothing is deleted. |

Words that work inside a lesson.

| You say | What happens |
|---|---|
| `map` | Stops the probe early and goes to the map. |
| `skip` or `just tell me` | Claude teaches the current step directly instead of asking you to try. |
| `Resume`, in the first picker | Continues a saved topic from its weakest node. |
| `use dark pictures` or `use light pictures` | Sets the theme for the map and other pictures. Light is the default. |

## What a session looks like

1. You say "teach me how git rebase works".
2. One picker: Full lesson, Quick (footholds and one derivation), or Resume.
3. Probe. Graded questions until the edge is found. Each answer is graded on the next question.
4. Map. Drawn as a picture, listed in chat. You approve it.
5. Teach. One node at a time. Foothold, Edge, Your turn, Click.
6. Test. Derive something untold.
7. Save. The graph is written with marks.

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
enough. Each one is checked before anything is built on it.

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

### Step 9. Save the graph

Each node is saved with a mark: Strong, Developing, or Revisit. The file lives outside any
git worktree, so it survives cleanup. Next session, Claude reads the graph, skips Strong
nodes, and starts at the weakest one. A memorized fact has one hold on memory. A fact
with many edges can be rebuilt from its neighbours when forgotten. The graph is how the
system keeps those neighbours.

## Status

In progress. The skill text and graph template are being built step by step with tests.

## Repository layout

```
.claude-plugin/plugin.json      plugin manifest
skills/learn/SKILL.md           the teaching process
skills/learn/graph-template.md  the saved graph format
skills/learn/pictures.md        when and how to draw, with the theme setting
skills/reset/SKILL.md           back up one topic and start over
agents/researcher.md            fact checker subagent
```

## License

[MIT](LICENSE). Anyone can use, copy, change, and share this work, including for
commercial use. Keep the license notice with copies. The ideas come from Eero Alvar, as
credited above. The words and files here are my own.
