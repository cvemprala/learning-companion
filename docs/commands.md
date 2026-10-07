# Commands

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
