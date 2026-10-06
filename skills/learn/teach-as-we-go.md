# Teach as we go

## Mode line

On when `<root>/<repo>/settings.md` has `Mode: teach as we go` under `# <repo> settings`.
"Stop teaching as we go" removes the line. Delete the file if only the heading is left.

## Met

**Met** means `codebase.md` has the heading `## <folder>`. Grep `^## <folder>$`. Nothing else counts. No file, nothing met.
The folder is the path from the git root, 2 segments at most. `sites/handlers/v2/foo.go` gives `sites/handlers`. A root file gives `root`.

## When to ask

Ask before a change when all three hold:

1. The folder is not met.
2. The change adds or edits 5 lines or more.
3. The change is not only config, docs, or tests: `tests/`, `docs/`, `_test.go`, `.test.ts`, `.spec.ts`, `.md`, `.json`, `.yaml`, `.yml`, `.toml`.

One question per folder, ever. The node makes the folder met.

## Predict shape

One AskUserQuestion, this exact shape. Ask, then stop. Nothing after the options. The grade comes in the next reply.

```
header:   Predict
question: <the change in one sentence>. <a question answerable by reasoning from what is on screen>
options:  2 or 3 claims, then one last option: I don't know
```

Ask what they can work out, not what they must look up.
Example: where does validation live, handler, middleware, or repository?
Write the right claim first. Mutate it into each wrong option by one misconception. No reasoning inside any option.

## Grade

The next reply starts with `Predict: right.` or `Predict: wrong. Answer: X. Why: one sentence.`
Idk is wrong, said idk. Then the node, then the work.

## Node

Append to `codebase.md`. A new file gets the header from `graph-template.md`.

```
## sites/handlers
Produced by: root
Facts: <1 to 3, what the folder does>
Mark: Revisit (YYYY-MM-DD)
Probe: Predict, wrong, said <claim>, answer <claim>
Seen in: sites/handlers/create_site.go:41
Edge to rebuild: <why the fact must be so>
Date: YYYY-MM-DD
```

Right: Developing. Wrong or idk: Revisit. `Date` is the met day, never changed.

## Just do it

Skip the question. Write nothing. The folder stays unmet, asked next time.
On the third skip in one session, ask once whether to turn the mode off for this repo.

## Mark this

Any repo, mode on or off. One node for the folder just discussed, Mark: Seen, no `Probe:` line, no question.
Facts and Edge come from what was just said. Show it. **Seen** means met, not yet asked.
