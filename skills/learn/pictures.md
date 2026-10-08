# Pictures

How to draw a picture during a lesson. The map uses this too.

## When to draw

Draw when the idea is a shape words carry badly. A flow, a chain of calls, a tree, two options side by side, a thing on a number line.
Do not draw when one sentence or one code block carries it. A picture that restates the sentence next to it is noise.
Each lesson draws the map, and then at most 2 more pictures. Each one needs a reason.

Rules for the drawing:

- Show the mechanism, not its name. A box that says "closure" says nothing. The arrow from the inner func to the outer variable says it.
- At most 7 elements in a picture that is not the map. If the brief lists more, cut until it fits. The map follows its own size rules in SKILL.md.
- Label every arrow with what moves or why: `calls`, `points at`, `returns`.
- One figure, one claim. The caption under it states the claim in one sentence.
- Mark unknowns with `?`. Never draw a relationship the learner has not agreed to.

## Theme

Settings live in `<root>/settings.md`, where root is `LEARNING_NOTES_ROOT` or `~/.learning/`.

```
# Learning Companion settings
Theme: light
```

Default is light. If the file does not exist, treat it as light and do not create it.
When the learner says "use dark pictures" or "use light pictures", write the setting and say it will apply from the next picture.
A light theme puts the light colors on the bare `:root`. A dark theme puts the dark colors there and the light ones in the override blocks.
Either way, both palettes exist, so the viewer's own theme switch still works.

## Page shape

One file per picture, in the scratchpad folder. Publish with the Artifact tool and follow its rules. Load the artifact-design skill first, the tool requires it.
Use mermaid, a text format that the viewer draws as boxes and arrows, for flows, trees, and sequences. Use inline SVG for geometry and number lines.

```html
<title>Closure Keeps n</title>
<style>
  /* Layout: one figure, caption below, 65 character measure. */
  :root {
    --bg: #ffffff; --ink: #1f2a30; --muted: #6b7a82; --accent: #0b6e8f;
    --font: ui-sans-serif, system-ui, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #141a1e; --ink: #e6ebee; --muted: #93a1a9; --accent: #5cc3e6; color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #141a1e; --ink: #e6ebee; --muted: #93a1a9; --accent: #5cc3e6; color-scheme: dark;
  }
  body { background: var(--bg); color: var(--ink); font-family: var(--font); padding: 24px 16px; }
  figure { margin: 0 auto; max-width: 720px; }
  figcaption { color: var(--muted); margin-top: 12px; max-width: 65ch; }
  .mermaid { overflow-x: auto; }
</style>
<figure>
  <pre class="mermaid">
graph TD
  make["make() runs once"] -->|declares| n["n := 0"]
  make -->|returns| inner["inner func"]
  inner -->|points at, not a copy| n
  c1["c() first call"] -->|n++ gives 1| n
  c2["c() second call"] -->|n++ gives 2| n
  </pre>
  <figcaption>The inner func points at the one n that make created, so every call changes the same n.</figcaption>
</figure>
```

## Map page

The map uses the same page with 3 additions. The background is white. A bar above the drawing has 3 buttons, minus, plus, and reset, that scale the drawing from 30 to 300 percent. The drawing sits in a scroll box with a border.
Above 10 nodes, each layer is a mermaid subgraph named `Layer 1, roots` to `Layer N, goal`, so the picture shows the layers as boxes.

```html
<div class="bar">
  <button id="out" type="button">minus</button>
  <button id="in" type="button">plus</button>
  <button id="reset" type="button">reset</button>
  <span id="pct">100%</span>
</div>
<div class="box"><div class="zoom" id="zoom">
  <pre class="mermaid">
graph TD
  subgraph L1[Layer 1, roots]
    A[first root]
  end
  subgraph L2[Layer 2, goal]
    B[goal]
  end
  A -->|why| B
  </pre>
</div></div>
<script>
  var s = 1, z = document.getElementById('zoom'), p = document.getElementById('pct');
  function apply(){ z.style.transform = 'scale(' + s + ')'; p.textContent = Math.round(s*100) + '%'; }
  document.getElementById('in').onclick = function(){ s = Math.min(3, s + 0.2); apply(); };
  document.getElementById('out').onclick = function(){ s = Math.max(0.3, s - 0.2); apply(); };
  document.getElementById('reset').onclick = function(){ s = 1; apply(); };
</script>
```

Styles for the bar and the box: `.bar` is a flex row with an 8 pixel gap. `.box` has `overflow: auto`, a 1 pixel border in `--line`, and `max-height: 80vh`. `.zoom` has `transform-origin: top left` and `display: inline-block`.

For a dark theme, swap the two color sets. Dark values go on the bare `:root` with `color-scheme: dark`. Light values go in the two override blocks without it.
Keep the `<title>` to 2 to 4 words that name the picture. Put the one sentence claim in the publish description.

## Save

Add `Picture: <link>` to the node the picture explains. On Resume, show that link again when the node comes up.
To change a picture later, republish to the same link. Do not make a second link for the same claim.
