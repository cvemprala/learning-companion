# Learn while you work

Claude Code has a Learning output style. At design decisions it asks you to write 5 to 10
lines of code yourself. It has two gaps. It asks for business logic in a system you do not
understand yet. And it has no memory and no later test. It does not replace the Learning
output style. The rule: use the Learning style to build, use this to understand what you
touch and to keep it.

Say "teach as we go" in a repo to turn it on for that repo. Claude asks one question first:
who writes the code, you or Claude. The answer is saved for that repo.

Before Claude changes 5 or more lines in a folder you have not met, it asks one Predict
question. A Predict question is a guess about code you have not read yet, with 2 or 3
claims and "I don't know". Claude grades it and writes one node for that folder to
`~/.learning/<repo>/codebase.md`. One question per folder, ever. Changes to config, docs,
or tests never ask. Say "just do it" to skip one question.

If Claude writes the code, it then does the work. If you write the code, Claude instead
gives one short block per step: the fact the step rests on, why the step looks the way it
does, and the step itself in one sentence. Then you write it. Claude never writes a step it
gave to you. Say "just write it" to hand one step back to Claude.

Say "stop teaching as we go" to turn the mode off.

"Mark this" works in any repo, mode on or off. It writes one node for the code Claude just
explained, with the mark Seen, and asks nothing. Later, "teach me the codebase" or "teach
me what I marked this week" runs a normal lesson on those nodes.

Work sessions are not logged for Obsidian. The node is the record.
