# Your notes, and reading them in Obsidian

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

## The files

Everything lives under `~/.learning/`, or the folder in `LEARNING_NOTES_ROOT`. One folder per
repo, named by the git root folder, and `general/` for topics with no repo.

| File | What it holds |
|---|---|
| `<repo>/<topic>.md` | The graph. One node per fact, with a mark: Strong, Developing, Revisit, Not yet asked. The map link. The open question, if any. |
| `<repo>/<topic>.review.md` | The review sheet. One folded question per node, answer under it. |
| `<repo>/log/<date>-<topic>-<session>.md` | The lesson, as it happened. Written by the mirror hook after every reply. |
| `<repo>/codebase.md` | Nodes from work sessions, one per folder. From teach as we go and mark this. |
| `<repo>/settings.md` | Per repo settings. Today only `Mode: teach as we go`. |
| `<repo>/backups/` | Where reset moves things. Nothing is deleted. |
| `settings.md` at the root | Settings for every repo. `Theme: light` or `dark`. `Mirror: on` or `off`. |

Marks mean this. Strong: you derived a fact that was never said. Developing: you recalled it in a
probe or followed the edge. Revisit: you missed it. Not yet asked: untaught.
