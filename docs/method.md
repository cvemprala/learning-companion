# The method

How a lesson is built, and why each step is there. The ideas come from Eero Alvar's
video [How I Learn Difficult Things](https://www.youtube.com/watch?v=ciC6ffUqI8k).

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
