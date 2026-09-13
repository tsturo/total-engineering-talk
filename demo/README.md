# Live demo: one ticket, a team of agents

A tiny reports app and one Jira-style ticket. The workflow in `.claude/workflows/ship-ticket.js` is the notebook drawing from the talk, as a file that runs.

## Before the talk

```
cd demo
npm test          # 3 tests pass
git status        # clean, so the diff after the run is only the agents' work
claude
```

In Claude Code, check that `/ship-ticket` is listed (type `/ship` and look at the completions). Do one full dry run the day before; note how long it takes and what the summary looked like.

To reset the demo after a run:

```
git checkout -- . && git clean -fd src public test
```

## The demo, about 5 minutes

1. **The ticket.** Open `tickets/ENG-142.md`. Same ticket as on the poster: PDF export, header, page numbers, filters, a button.
2. **The file.** Open `.claude/workflows/ship-ticket.js`. Point at the five phases in `meta`, then at the pipeline: build, test, review, push back. This is the right page of the notebook, as code. About 80 lines, plain JavaScript, no framework.
3. **Run it.** In Claude Code type `/ship-ticket`. Open `/workflows` and leave the progress tree on screen.
4. **Talk over the run** with the pitch. Which agent is playing now, who is waiting, which piece got pushed back. `/workflows` shows agents per phase, tokens and time.
5. **The result.** The summary comes back to the terminal, to you. Show `git status` and `npm test`. Nothing was committed. The ticket is at the touchline.

## What to say about the pieces

- **The orchestrator** is the script plus its first agent. It reads the ticket and decides the shape: how many pieces, which files each one owns. Nothing is fixed in advance; three pieces today, two or five for another ticket.
- **Builders** are plain agents, one per piece, in parallel. They own disjoint files, so they never collide.
- **Tester** runs the suite per piece and fixes its own piece if red.
- **Reviewers** are three agents with three prompts: code quality, attacker, user. Same agent type, different lens. One of them saying no is enough to push the piece back to its builder once.
- **Ship** is one last agent that runs everything and writes the hand-over. It does not merge. You do.
- **Structured output.** The orchestrator and the reviewers return JSON that matches a schema, so the script can branch on it. That is what makes the pushback loop deterministic code instead of a hope.

## If it goes wrong

Say so. The run stop on the poster shows the same pipeline, so go back to the poster and finish there. If the run is only slow, keep talking over the pitch, then show the summary when it lands.

## Where the script for an ad hoc run lives

When you ask Claude Code in plain words to orchestrate something, it writes a script like this one on the fly and saves it under `~/.claude/projects/<session>/workflows/`. Pressing `s` in `/workflows` saves that script as a reusable command. That is how this file started.
