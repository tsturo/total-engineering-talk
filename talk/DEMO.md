# Live demo: one prompt, a team of agents, on this presentation

You open Claude Code in this repo, type one prompt, and the agents add a new stop to the talk while the room watches. The reveal is reloading the poster and finding Arvydas Sabonis in it.

## Before the talk

Run the demo in a separate copy of the repo, so the presentation you are showing cannot break mid-run:

```
git worktree add ../total-engineering-demo master
cd ../total-engineering-demo
claude
```

The portrait render is already in `talk/img/sabonis.png`, so the worktree has it.

Do one dry run the day before. Afterwards: `git checkout -- . && git clean -fd talk` inside the worktree.

## The prompt (about 3 to 4 minutes)

```
Use a workflow for the task in docs/sabonis.md: a researcher, a builder, a checker, one pushback if the checker rejects. Do not commit.
```

Three agent types and a pipeline with one pushback. The brief with the details is `docs/sabonis.md`, open it on screen before typing the prompt if the room wants to see what the agents get. The orchestrator is the script Claude writes for this prompt.

## While it runs

- `/workflows` shows the progress tree: phases, agents, tokens, time. Leave it on screen.
- Talk over it with the pitch: the researcher is refinement, the builder is a builder, the checker is the reviewer who can push back.

## After it lands

- Open `talk/index.html` from the worktree in a new tab and jump to the new stop. Sabonis is on the poster.
- Ask: `show me the workflow script you wrote`. Claude opens the JavaScript file it generated, saved under `~/.claude/projects/<session>/workflows/`. Point at `meta.phases`, `pipeline`, and the pushback branch: the notebook drawing as code, about 40 lines, written for this one prompt.
- In `/workflows`, `s` saves that script as a reusable slash command. A team keeps these in `.claude/workflows/` next to the code.
- Say what you did not do: you did not write the workflow and you did not open the editor. You described the shape in a sentence, and you are the one who decides whether it gets merged.

## If it goes wrong

Say so and go back to the poster. The run stop shows the same pipeline.
