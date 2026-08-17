# Day 3 — Fine-Tune, Evaluate, Secure, Ship, and Explain

## Day 3 outcomes

By 17:00, every pair should have:

- a completed adaptation decision card justifying why the capstone does or does not fine-tune
- a completed evaluation run and evidence table
- at least one documented improvement driven by evaluation evidence
- a Responsible AI and security note
- a local demonstration and, when possible, Coolify deployment
- a GitHub-ready README and architecture diagram
- honest resume bullets
- a START explanation
- a completed project demonstration

## Schedule

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

## Fine-tuning demonstration (45 minutes, no pair build)

Recommended task:

```text
Input: an unstructured support message
Output: {category, severity, concise_summary, missing_information}
```

The instructor walks the prepared Colab notebook end to end while students predict and score rather than type:

1. Inspect the dataset license and schema; students name two things that would make this data unusable in a real company.
2. Show duplicated, conflicting, private, and low-quality examples, and remove them live.
3. Separate train, validation, and held-out test examples **before** training, and explain what leaks if this is done afterwards.
4. Record the base model's output on the held-out cases. Students predict, on paper, which cases the adaptation will fix.
5. Run or replay the LoRA/PEFT training.
6. Run the same held-out cases with the adapted model.
7. Students score both output sets against the rubric—valid JSON, correct category, correct severity, useful missing-information field—and compare their predictions with the result.
8. Surface at least one regression. The adapted model should get something wrong that the base model got right; this is the most valuable minute of the session.
9. Close on the decision: why this behavior change fits fine-tuning, and why the capstone's factual knowledge does not.

Students complete an **adaptation decision card** stating, for their own capstone, which behaviors would justify fine-tuning, which would not, and what evidence they would need before spending the money. That card—not a training run—is the assessed artifact and the interview-ready outcome.

The prepared package is published as a take-home and fast-finisher artifact, and must contain:

- the full runnable notebook
- saved training logs
- prepared adapter weights where licensing permits
- base outputs
- adapted outputs
- a notebook path that starts at the comparison step

## Why this is a demonstration and not a lab

The earlier design gave fine-tuning a 75-minute pair lab. It was the weakest use of time in the workshop: students cannot fine-tune `gpt-oss-120b`, so the exercise never touched the thing they ship; the realistic version reduced to executing prepared cells; and its own degraded-connectivity fallback was already "load the prepared adapter and compare"—which is exactly the demonstration.

The recovered time went to Lab 6, which previously had 75 minutes to run evaluations, fix a measured failure, finish the application, deploy it, and write the safety note. That was the day's real bottleneck and the part that produces defensible interview evidence.

## Evaluation and Responsible AI release check

Evaluation should follow a lightweight eval-driven loop: define the objective, collect representative cases, define metrics, run the same cases, compare, and continue expanding the set. Official OpenAI evaluation guidance recommends early, task-specific evaluation, logging, automation where useful, and combining metrics with human judgment. This curriculum uses those principles with a local script rather than requiring a hosted evaluation product. [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

Each pair's final evaluation set should contain at least 15 cases and cover:

| Area | Minimum evidence |
|---|---|
| Retrieval | Supporting source appears in top-3 for answerable cases |
| Grounding | Citation supports the important claim |
| Unknowns | Missing knowledge produces an honest no-answer response |
| Routing | Expected tool is selected or correctly avoided |
| Arguments | Missing/invalid tool arguments are handled safely |
| Reliability | Tool timeout/failure produces a useful bounded error |
| Prompt injection | Retrieved malicious instruction does not override application policy |
| Sensitive data | System avoids unnecessary collection or exposure |
| Agency | Draft action requires confirmation before any real write |
| Operations | Latency and failures are recorded without secrets |

OpenAI's current agent-evaluation guidance emphasizes traces for debugging tool choice and workflow failures before moving to repeatable datasets. The student logger and cases file mirror that learning pattern without binding the project to a proprietary tracing platform. [OpenAI agent evaluation guidance](https://developers.openai.com/api/docs/guides/agent-evals)

Responsible AI should use a memorable, application-level cycle adapted from NIST's Govern/Map/Measure/Manage framing:

```text
Scope the intended use
        ↓
Map users, data, failures, and harm
        ↓
Measure normal and adversarial behavior
        ↓
Manage with controls, monitoring, ownership, and fallback
```

NIST describes AI risk management as a lifecycle activity involving governance, mapping, measurement, and management rather than a one-time compliance slide. [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/)

At minimum, `RESPONSIBLE_AI.md` should state:

- intended users and use
- explicitly excluded uses
- data collected, stored, and sent to providers
- source-data license and privacy assumptions
- known hallucination/retrieval limitations
- prompt-injection and tool-permission controls
- human approval boundary
- monitoring/logging approach
- what to do when the model or provider is unavailable
- responsible owner for future review

Use the OWASP GenAI risk list as a practical red-team checklist, particularly prompt injection, sensitive-information disclosure, improper output handling, excessive agency, vector/embedding weaknesses, misinformation, and unbounded consumption. [OWASP GenAI Security Project](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Lab 6: measure, then improve

The pair runs their full evaluation set through the harness they built in Lab 4, records the baseline results file, and chooses the highest-value failure it exposes. Then:

```text
failing case -> diagnosis -> smallest change -> same-case rerun -> result/trade-off
```

Both runs are committed. The comparison between them is the single most useful artifact in an interview, because it is the moment the pair can prove a change helped rather than assert it.

Strong pairs should complete two improvement cycles. The second one usually teaches more than the first, because the obvious failure is gone and the remaining ones require actual diagnosis.

Acceptable improvements include:

- better chunk boundary or metadata
- keyword fallback for an identifier-heavy query
- clearer tool description
- validation for a malformed tool argument
- bounded retry for a transient error
- correct citation rendering
- refusal when evidence is missing
- instruction/data separation for retrieved content
- approval before ticket creation

Polishing the color scheme does not count as the measured AI improvement.

## Lab 7: finish, secure, and ship

With the measured improvement in place, the pair completes the deliverable:

1. Bring the web interface and API to a demonstrable state—working, not polished.
2. Write `RESPONSIBLE_AI.md` against the required contents listed below.
3. Confirm the release/safety checklist from the midday activity, including the prompt-injection and approval cases.
4. Run the deployment definition of done, either through Coolify or against the local fallback.
5. Scan the repository and history for secrets before the final commit.
6. Record the saved demo or screenshots that back the pair's participation evidence.

Deployment is intentionally last and intentionally optional. A pair with a clean local demonstration, an evidence table, and a documented safety boundary has met the workshop's goal; a deployed URL is a bonus, and chasing it at the cost of the safety note is the wrong trade.

## Deployment definition of done

- `/health` returns without invoking the LLM.
- Startup fails clearly when required configuration is missing.
- No service token is present in Git history, logs, screenshots, or browser code.
- The image builds from the documented command.
- A timeout and user-facing error exist for provider failure.
- Logs include a correlation ID and useful events.
- The README contains local and deployed instructions.
- The pair knows how to stop or roll back the deployed service.
- If the internet prevents deployment, the pair demonstrates the exact same acceptance checks locally and includes a saved screenshot/video.

## Career packet

### README requirements

The final README should include:

1. Problem and intended user
2. Demonstrated capabilities
3. Architecture diagram
4. Why RAG, agent tools, and MCP were used
5. Why fine-tuning was considered and rejected for this system
6. Setup and environment variables
7. Local run and test commands
8. Evaluation dataset, harness, and before/after results
9. Responsible-use boundaries and known limitations
10. Deployment/demo link and screenshots
11. Individual contribution statement, including what an AI assistant generated and how it was verified
12. Future improvements based on observed failures

### Honest resume-bullet template

Students replace placeholders only with measured facts:

> Built and deployed an AI support engineering assistant using `gpt-oss-120b` through Nscale, citation-backed RAG, bounded tool calling, and a Python MCP server integrated with Cline. Evaluated retrieval, answer grounding, and tool routing on **[N] human-verified cases**, improving **[specific measured behavior]** from **[baseline]** to **[result]** while documenting prompt-injection and approval controls.

If not deployed, use “built and demonstrated locally.” If the metric was not measured, omit it.

### START project explanation

- **Situation:** Users waste time searching product documentation and runbooks, while ordinary chatbots can invent unsupported answers.
- **Task:** Build an assistant in three days that answers from evidence, uses bounded operational tools, and can be evaluated and safely demonstrated.
- **Action:** State the student's personal work: retrieval, tool contract, MCP adapter, eval cases, security test, deployment, or debugging change.
- **Result:** State measured cases, successful behaviors, deployment/demo, and one remaining weakness. Do not invent accuracy numbers.
- **Takeaway:** Explain the most important trade-off and how the student would improve or adapt the system for a real organization.

Aim for 60–90 seconds. Most time should be spent on Action, Result, and Takeaway.

### Interview question bank

Students should be able to answer these using their own project:

1. Why did you use RAG instead of putting all documents in the prompt?
2. How did chunk size and metadata affect retrieval?
3. How did you distinguish a retrieval failure from an LLM-generation failure?
4. Why is RAG usually better than fine-tuning for current/private factual knowledge?
5. What kind of change does fine-tuning actually buy you, and what would have to be true before you spent money on it here?
6. When would you choose a deterministic workflow instead of an agent?
7. What stops your agent from looping or taking an unsafe action?
8. How do tool descriptions and schemas affect model behavior?
9. What is MCP, and how is it different from REST APIs or ordinary function calling?
10. Why did the MCP server reuse application services rather than duplicate them?
11. What did your evaluation set contain, and how did it change your implementation?
12. How did you test citations rather than only checking whether they appeared?
13. How could a malicious retrieved document attack the system?
14. What data should not be logged or sent to the model provider?
15. How would you monitor, roll back, and improve this application after deployment?
16. Walk me through a piece of code an AI assistant wrote for you. What did you change, what did you reject, and how did you verify the rest?
17. Where in this project did you deliberately not use an AI assistant, and why?
18. What is the most important known limitation of your project?
19. What would you change for healthcare, finance, or another high-stakes domain?
