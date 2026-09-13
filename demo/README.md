# Live demo: one prompt, a team of agents

A tiny reports app (no dependencies, three tests) and one ticket. It exists only so the agents have something small to work on. You open Claude Code, type one prompt, and Claude writes and runs the workflow in front of the room.

## Before the talk

```
cd demo
npm test        # 3 tests pass
claude
```

Do one dry run the day before to see the timing. Reset afterwards with `git checkout -- . && git clean -fd`.

## The prompt (about 2 minutes to run)

```
Use a workflow to review this project for bugs. Three reviewers in parallel, each with a different lens: code correctness, security, and what a user would notice. For every finding, one skeptic agent tries to refute it; keep only what survives. One last agent writes a short summary sorted by severity. Do not change any files.
```

Three agent types and a pipeline: reviewers fan out, each finding goes to a skeptic as soon as its reviewer is done, a writer closes. Findings are real, the app has a few soft spots on purpose (no input validation on the report id or filters, unescaped values in the HTML table).

## While it runs

- `/workflows` shows the progress tree: phases, agents, tokens, time. Leave it on screen.
- Talk over it with the pitch: reviewers are the three reviewers from the run, skeptics are the pushback, the writer is the hand-over to the touchline.

## After it lands

- Ask: `show me the workflow script you wrote`. Claude opens the JavaScript file it generated and saved under `~/.claude/projects/<session>/workflows/`. Point at `meta.phases`, `parallel`, `pipeline`, and the schema: the notebook drawing as code, about 40 lines, written by the tool for this one prompt.
- In `/workflows`, `s` saves that script as a reusable slash command. Say that a team keeps these in `.claude/workflows/` next to the code.

## If there is time: the build variant (5 to 10 minutes)

```
Use a workflow to implement tickets/ENG-142.md. One planner splits it into pieces that touch different files, one builder per piece in parallel, one tester per piece, then three reviewers per piece: code, security, product. If a reviewer rejects a piece, send it back to its builder once. Finish with a summary for me. Do not commit.
```

Same shape as the run stop on the poster. Only start it if the room has ten minutes; otherwise show the prompt and say what it would do.

## If it goes wrong

Say so and go back to the poster. The run stop shows the same pipeline.
