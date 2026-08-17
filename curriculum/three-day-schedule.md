# Three-Day AI Engineering Workshop Schedule

## Day 1 — Understand, Choose, and Build Evidence-Backed RAG

| Time | Mode | Session | Student evidence |
|---|---|---|---|
| 09:00–09:20 | Explain + activity | Career outcome, pair roles, rules, and diagnostic poll | Pair role sheet and baseline confidence |
| 09:20–09:55 | Explain | Modern AI application mental model and decision ladder | Prompt/RAG/agent/MCP/fine-tune decision card |
| 09:55–10:40 | Demo | Finished capstone first: normal path, evidence, tool call, MCP, eval, attack, and deployment | Students predict each component before reveal |
| 10:40–10:55 | Break | — | — |
| 10:55–12:00 | Guided build | Lab 1: diagnose and repair a deliberately broken RAG pipeline, then capture the plain-LLM baseline failure | Repaired pipeline, defect log, captured baseline failure |
| 12:00–12:25 | Explain + activity | Architecture decision clinic: choose the simplest suitable pattern | Completed decision table with justification |
| 12:25–12:45 | Float | Reserve: setup recovery, blocked pairs, or fast-finisher extension | — |
| 12:45–13:30 | Lunch | — | — |
| 13:30–14:10 | Demo | RAG quality: chunking, metadata, top-k, hybrid fallback, citations, and retrieval-vs-generation failure | Before/after retrieval trace |
| 14:10–15:40 | Guided build | Lab 2: integrate citation-backed RAG and create a 12-case golden set | RAG module, cases file, baseline results |
| 15:40–15:55 | Break | — | — |
| 15:55–16:40 | Challenge | Red-team the knowledge base: indirect prompt injection, PII request, missing answer, conflicting sources | Threat card, failed behavior, mitigation proposal |
| 16:40–17:00 | Checkpoint | Pair explanation, commit, and traffic-light status | Day 1 commit and checkpoint record |

## Day 2 — Agents, AI-Assisted Development, and MCP

| Time | Mode | Session | Student evidence |
|---|---|---|---|
| 09:00–09:20 | Explain + activity | Retrieval error clinic: classify yesterday's failures | Pair selects one measured improvement |
| 09:20–09:55 | Explain | Workflow vs agent; tool contracts, state, stopping, retries, and approval | Agent-loop sketch and risk boundary |
| 09:55–10:40 | Demo | Manual Nscale tool-calling loop with visible trace and intentional failures | Predicted route, trace review, failure diagnosis |
| 10:40–10:55 | Break | — | — |
| 10:55–12:10 | Guided build | Lab 3: hand-write the bounded agent and three typed tools | Working loop, validation, max-iteration test |
| 12:10–12:45 | Demo | AI-assisted development: spec → plan → challenge → diff review → test → debug, on live capstone code | Annotated plan critique and one rejected suggestion |
| 12:45–13:30 | Lunch | — | — |
| 13:30–14:40 | Guided build | Lab 4: ship the evaluation harness through a coding assistant under review | `run_evals.py`, results table, generated-vs-verified log |
| 14:40–14:55 | Break | — | — |
| 14:55–15:15 | Float | Reserve: blocked pairs, harness repair, or fast-finisher extension | — |
| 15:15–15:40 | Demo | MCP mental model; connect a prepared server to Cline; inspect resource/tool boundaries and permissions | Successful prepared MCP call |
| 15:40–16:45 | Guided build | Lab 5: expose existing capstone services through a thin MCP adapter over STDIO | Server, resource, tools, configuration, test calls |
| 16:45–17:00 | Checkpoint | Pair explanation, commit, and traffic-light status | Day 2 commit and checkpoint record |

## Day 3 — Fine-Tune, Evaluate, Secure, Ship, and Explain

| Time | Mode | Session | Student evidence |
|---|---|---|---|
| 09:00–09:20 | Explain + activity | Day 2 failure clinic and evaluation scoreboard | Pair identifies highest-value remaining failure |
| 09:20–09:55 | Explain | Prompting vs RAG vs tools vs fine-tuning; dataset and split intuition | Adaptation decision card |
| 09:55–10:40 | Demo | Prepared PEFT/LoRA Colab: data → train → base-vs-adapted held-out comparison, including a regression | Students predict gains and failure modes, then score the instructor's outputs |
| 10:40–10:55 | Break | — | — |
| 10:55–12:15 | Guided build | Lab 6: full evaluation run, then evidence-driven improvement | Results file, before/after comparison, documented trade-off |
| 12:15–12:45 | Explain + activity | Evaluate and manage risk: evidence, human oversight, privacy, prompt injection, and excessive agency | Completed release/safety checklist |
| 12:45–13:30 | Lunch | — | — |
| 13:30–14:05 | Demo | Package and ship: tests, Docker, health check, secrets, Coolify, logs, and rollback | Deployment trace and known-good command |
| 14:05–15:20 | Guided build | Lab 7: finish the project, write `RESPONSIBLE_AI.md`, deploy or prepare the local demo | Working demo, safety note, final commit |
| 15:20–15:35 | Break | — | — |
| 15:35–15:50 | Float | Reserve: deployment recovery, blocked pairs, or extra eval rerun | — |
| 15:50–16:25 | Career sprint | README, architecture, resume bullet, contribution statement, and START rehearsal | Portfolio packet |
| 16:25–16:55 | Demo carousel | Every pair presents in parallel pods; selected pairs give spotlight demonstrations | Demo checklist and peer feedback |
| 16:55–17:00 | Close | Next 30-day build plan and responsible portfolio use | Individual next-step commitment |
