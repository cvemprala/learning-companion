# Tools people already use for this, and what this one does

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
