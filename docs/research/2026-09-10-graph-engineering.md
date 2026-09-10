# "Graph engineering" and the BPMN-to-dynamic-workflow idea: fit for the Total Engineering talk

## 1. What "graph engineering" means today

Short answer: it is a **2026 buzzword owned by the AI-agent-framework crowd**, not an established discipline. Three distinct uses exist; only the first is called "graph engineering" by anyone with weight.

1. **Agent orchestration as an explicit graph (the dominant meaning).** LangChain's July 2026 post ["3 Years of Graph Engineering with LangGraph"](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) uses it for designing agent systems as nodes (deterministic code, LLM calls, sub-agents, human pauses) and edges (fixed or model-chosen routes), so you "impose your preconceptions of how the system should work into more constrained paths". Explainers followed within weeks: [V12 Labs](https://www.v12labs.io/blog/2026-08-17-graph-engineering-explained) ("explicitly designing how agents, tools, deterministic code, validators, data, and humans connect to complete a task"), [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/07/graph-engineering/), [AI Builder Club](https://www.aibuilderclub.com/blog/is-graph-engineering-just-langgraph), [TrueFoundry](https://www.truefoundry.com/blog/graph-engineering-enterprise-guide), [Zylos](https://zylos.ai/research/2026-04-14-graph-based-agent-workflow-orchestration-production/). The same pattern under other names: AutoGen GraphFlow, Google ADK workflow agents, [Vercel Workflow DevKit](https://vercel.com/docs/workflows) (durable steps, hooks for human approval), Temporal. Humans appear in this graph only as **approval/interrupt nodes** ([LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)), never as flexible players.
2. **Codebase or engineering data as a knowledge graph.** [Neo4j "codebase knowledge graph"](https://neo4j.com/blog/developer/codebase-knowledge-graph/), GraphRAG over code, and Faros AI modelling all engineering tools as a queryable graph ([Cortex overview](https://www.cortex.io/post/engineering-intelligence-platforms-definition-benefits-tools)). Rarely called "graph engineering"; usually "knowledge graph engineering" or "engineering graph".
3. **Engineering work modelled as a graph of tasks and people.** Nobody uses "graph engineering" for this. The closest are Kanban/flow tools and dynamic-reteaming literature (section 2). If the talk uses the term this way, the presenter is coining it.

Plain verdict: if you say "graph engineering" to this audience, the engineers who know the term will hear "LangGraph-style agent orchestration", which is not the talk's point. The rest will hear a new label.

## 2. BPMN versus dynamic workflows

The critique is old and well documented, but it comes from the BPM world, not from software teams:

- **Adaptive case management.** Swenson et al., [Mastering the Unpredictable](https://www.goodreads.com/book/show/8207560-mastering-the-unpredictable) (2010): knowledge work "by its nature is unpredictable and cannot be handled by more formalized process definition techniques"; exceptions should be supported, not eliminated.
- **CMMN** is OMG's answer: activities "performed in unpredictable order", event-driven, case-file centred ([OMG](https://www.omg.org/cmmn/), [BPMInstitute](https://www.bpminstitute.org/resources/articles/the-power-of-case-based-modeling-why-cmmn-is-essential-for-dynamic-workflows-in-bpm/)). Still niche; a 2024 BPM paper is still [extending it](https://link.springer.com/chapter/10.1007/978-3-031-70445-1_18).
- **Developers' distaste for BPMN** is real and vendor-amplified: [Temporal](https://temporal.io/blog/bpmn-legacy-orchestration-tools-holding-you-back) argues BPMN "cannot serve both non-technical domain experts and developers well"; [Refalo](https://medium.com/@orefalo_66733/the-problem-with-bpel-bpm-and-workflow-engines-b38a04e11fd) on "limited complicated UI/XML-based technology"; [HN thread](https://news.ycombinator.com/item?id=24825572). Expect eye-rolls from BE/DevOps if BPMN is presented as a serious model of their work.
- **Team-side alternatives** (the ones that actually match the talk): Kanban WIP limits force swarming, where the team "isn't allowed to start anything new until the current work is finished" ([Atlassian](https://www.atlassian.com/agile/kanban/wip-limits), [Kanban Zone](https://kanbanzone.com/2020/swarming-as-a-kanban-team/)); mob/ensemble programming; [Team Topologies](https://teamtopologies.com/key-concepts) stream-aligned teams with "minimal, ideally zero, handoffs"; Helfand's [Dynamic Reteaming](https://leaddev.com/culture/dynamic-reteaming-art-and-wisdom-changing-teams-heidi-helfand) with Edmondson's "fluid, porous teams".
- **Evidence is thin.** The [mob programming SLR](https://ieeexplore.ieee.org/iel7/8746989/8753906/08753993.pdf) and the [2024 multivocal review](https://www.researchgate.net/publication/388164214_Mob_Programming_Challenges_Success_Factors_and_Practices_A_Multivocal_Literature_Review_Protocol_with_Preliminary_Results) say most sources are experience reports; Wang and Manos 2023 report about 15% slower per task but 28% faster delivery, a single study. Team Topologies is explicitly [not scientific evidence](https://arxiv.org/pdf/2302.00033). Do not present dynamic allocation as proven; present it as practice.

## 3. Humans and agents in one workflow graph

- **Agents as assignable teammates exist.** GitHub's coding agent: "assign Copilot an issue just like you would a teammate" and get a PR back; the assigner cannot approve the PR, Copilot is a "semi-trusted contributor" ([GitHub blog](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/), [assigning issues](https://github.blog/ai-and-ml/github-copilot/assigning-and-completing-issues-with-coding-agent-in-github-copilot/)). Vercel's [human-in-the-loop durable workflows](https://vercel.com/kb/guide/building-human-in-the-loop-agents-for-community-moderation-with-durable-workflows) and LangGraph interrupts do the same at framework level.
- **The honest limits, all pointing at review load:**
  - METR RCT: experienced devs were **19% slower** with early-2025 tools while believing they were 20% faster ([METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)); the [2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) shows some speedup but METR calls the central estimate unreliable due to selection effects.
  - DORA 2025: AI adoption now correlates with higher throughput **and** higher instability; "AI is an amplifier" of existing practice ([Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report), [dora.dev](https://dora.dev/insights/balancing-ai-tensions/)).
  - Faros: 98% more PRs merged, review time +91%, PR size +154%, bugs +9%, org-level metrics flat ([Productivity Paradox](https://www.faros.ai/ai-productivity-paradox)); 2026 follow-up on 22k devs: bugs per dev +54%, incidents per PR tripled ([Acceleration Whiplash](https://www.faros.ai/research/ai-acceleration-whiplash)).
  - Stack Overflow 2026: 84% use AI, 29% trust it, 66% name "almost right" output as top frustration ([SO blog](https://stackoverflow.blog/2026/02/18/closing-the-developer-ai-trust-gap/)).

Implication for the talk: the agent is a player who shoots a lot and needs cover. The cover (review, tests, verification) is the bottleneck, and that is exactly the Total Football point: someone must drop back.

## 4. Fit for this talk

- **Swimlane image at "Our formation": yes, cheap win.** Four horizontal bands with a token crossing dividers *is* a BPMN swimlane diagram already. Non-football people recognise it instantly as "handoff process". Don't say "BPMN"; say "the swimlane diagram every process tool draws". It also lets FE/QA/DevOps see themselves without knowing what a libero is.
- **Dynamic graph at "Total engineering": yes as a picture, no as a method.** The strong version is the same nodes with lanes gone and edges redrawn per feature. The weak version is a LangGraph-style box-and-arrow diagram, which reads as an architecture slide and drags the talk into tooling.
- **Do not introduce "graph engineering" as a named approach.** Three reasons: (a) the talk argues labels matter less, then adds one; (b) the term is already taken by agent orchestration, so half the room will think LangGraph; (c) once it has a name and a slide, the talk becomes a methodology pitch and the audience starts evaluating instead of listening. The presenter has no evidence base to defend a method (section 2), so the Q&A goes badly.
- **Recommended depth: one visual metaphor, carried by the poster, spoken in plain words.** Say "workflow" and "shape", not "BPMN" or "graph engineering". If a name is wanted at all, put it in a single closing line ("some people call this graph engineering; I just call it covering for each other") and move on.
- One thing worth keeping from the agent-graph literature: the "human approval node". It gives the talk a concrete, non-hype place for AI: the agent is a node that produces, a human is a node that verifies, and the graph decides who verifies. That matches METR/DORA/Faros and keeps the presenter honest.

## 5. Visual sequences for the poster

### A. Lanes to shape (replace or extend "Our formation" -> "Total engineering", 5 clicks)
1. Pitch with four bands: Frontend, Backend, QA, DevOps. Ball (feature) enters top-left.
2. Ball moves to the first divider and stops; a small clock appears at the line. Repeat at each divider (one click, staggered).
3. Dividers fade. Same players, same positions.
4. Ball moves diagonally; one player leaves the Backend zone to receive it, a QA player slides into the space they left. Thin lines link who covers whom.
5. Final frame: same ball, same players, three fewer stops.
Say: "This is the diagram every process tool draws for us. Take away the lines and the same people can do this instead. Nobody changed jobs; someone covered."

### B. Same feature, two routes (side panel next to the pitch, 4 clicks)
1. Left: a swimlane strip, feature moving through four lanes with four handoffs. Right: empty.
2. Right: the same four people drawn as points, no lanes.
3. Edges appear only where this feature needs them: FE to DevOps, QA to BE. Two handoffs, not four.
4. A second, different feature: edges redraw differently. Same people, different shape.
Say: "The team is the same. The route is chosen per feature, not fixed by department. That's the whole change."

### C. The agent as a player (extension of B or a third stop, 4 clicks)
1. Dynamic graph from B with four people.
2. A fifth point appears, labelled "agent". It receives the ball fast and passes it on quickly, several times.
3. The pass from the agent stops at a human point marked "check". The clock appears here instead of at the lane dividers.
4. A second human moves toward "check" to share it; the clock shrinks.
Say: "The agent produces more than one person can review. Somebody has to drop back and cover the review. Which of us does that is the question, not the tool."

Sequence A is the safest; B adds the per-feature idea; C is where the AI part earns its place and where the METR/Faros facts can be spoken in one sentence without a slide.
