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
Use a workflow to add one stop to this presentation, right after the "Does not exist" stamp (step s11-ultra in talk/index.html): Arvydas Sabonis, the closest thing to a total player, in another sport. A 2.21 m centre who shot three-pointers and passed like a guard. Read talk/README.md first, the Editing section explains how stops and scenes work.

Three agents in a pipeline. A researcher collects his real career facts and picks six stats for a card in the same style as the footballer cards in talk/index.html (class card, six bars, hi/mid/lo colours), with a one-line source note. A builder adds the stop: a new step after s11-ultra with camera data, the card, a portrait from talk/img/sabonis.png if it exists or a basketball jersey number 11 drawn in SVG, a small "Almost" stamp, and speaker notes in plain language, no slogans. A checker runs node scripts/check.mjs and confirms the new stop appears and no other stop's scene changed. If the checker rejects it, send it back to the builder once. Finish with a summary of what changed. Do not commit.
```

Three agent types (researcher, builder, checker) and a pipeline with one pushback. The orchestrator is the script Claude writes for this prompt.

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
