# Facilitator action plan

Use this as the operational checklist. The linked day files contain the teaching detail, explanations, and lab instructions.

## First decisions to make

- Confirm the 09:00–17:00 timing and included breaks.
- Confirm whether two assistants are available. If not, appoint one rotating contact in each of six five-pair support pods.
- Freeze one common capstone and the small list of approved domain variants.
- Decide whether students will deploy individually, share a Coolify target, or demonstrate locally.
- Confirm that all 30 pairs receive an Nscale key and can use GitHub and Cline on the lab network.

## Two weeks before

- Form 30 pairs and six support pods.
- Distribute the [pre-work and setup checker](03-pre-work-and-setup.md).
- Test Nscale, GitHub, Colab, Cline, package installation, and Coolify from the college network.
- Prepare the starter repository, completed reference repository, checkpoint branches, and instructor answer keys.
- Prepare the licensed document corpus, prebuilt index, response fixtures, keyword-search fallback, and offline instructions.
- Assign pair roles and explain that driver and reviewer switch after lunch.

## One week before: freeze everything

- Pin the Nscale base URL, model ID, authentication method, Python version, dependencies, embedding model, MCP SDK, and Cline version.
- Run every notebook and lab from a clean machine and a clean account.
- Time the broken-RAG repair, coding-assistant workflow, MCP connection, evaluation run, and deployment.
- Verify the 12-case golden set and save known-good results.
- Test all three infrastructure modes in [instructor preparation and infrastructure](08-instructor-preparation-and-infrastructure.md).
- Scan the repository and Git history for credentials.
- Record a short reference demonstration and capture screenshots.

## Day before the workshop

- Re-run the setup checker from the student environment.
- Verify 30 usable Nscale credentials without displaying them publicly.
- Put printed or local copies of the lab sheets, decision cards, threat model, release checklist, START template, and troubleshooting cards in reach.
- Open the checkpoint board and issue board.
- Preload the reference application, prepared fine-tuning outputs, Docker image, and fallback fixtures.
- Keep one known-good machine connected to the projector.

## Daily teaching rhythm

1. Show the outcome and working artifact first.
2. Explain only the concepts needed for the next task.
3. Ask pairs to predict behavior before running the demo.
4. Let pairs build, observe failures, and keep evidence.
5. Stop for a short failure clinic rather than repeating a lecture.
6. End with a commit, a two-minute pair explanation, and red/amber/green status.

Keep the intended balance across each eight-hour day: about two hours of explanation, two hours of demonstration, and four hours of student work. Float blocks absorb setup and debugging delays; do not pre-fill them with extra theory.

## Three-day quick view

| Day | Main build | End-of-day evidence | Detailed schedule |
|---|---|---|---|
| 1 | Repair and integrate evidence-backed RAG | Working cited RAG, 12-case set, baseline results, threat model, commit | [Day 1](04-day-1-rag.md) |
| 2 | Add a bounded agent, evaluation harness, and thin MCP adapter | Tool trace, tested harness, Cline MCP calls, assistant-review log, commit | [Day 2](05-day-2-agents-ai-assisted-development-and-mcp.md) |
| 3 | Evaluate, improve, secure, package, and explain | Before/after evidence, safety note, demo, README, resume bullet, START answer | [Day 3](06-day-3-evaluate-ship-and-career.md) |

## MCP preparation checklist

Prepare one small Python MCP server that reuses already-tested capstone functions and includes:

- one read-only resource
- one RAG/search tool
- one simple, bounded action tool
- typed inputs, clear tool descriptions, and structured responses
- input validation, useful errors, and correct logging
- a local STDIO configuration tested through Cline
- one case where Cline should call a tool and one where it should not

During the demo, explicitly cover permissions, secrets, prompt injection through tool content, approval before side effects, and why write operations must not be auto-approved. Advanced pairs may add another tool or deploy through Coolify only after the common checkpoint is complete.

## What to watch while students work

- A plan exists before agent or assistant-generated implementation begins.
- Both partners can explain the design; one confident student is not carrying the pair.
- Students classify failures as retrieval, generation, routing, tool, safety, or infrastructure problems.
- Improvements are supported by before/after evidence.
- Generated code is reviewed and tested, not accepted because it runs once.
- Claims in the README and resume bullets match what the pair actually built.

## Minimum completion bar

A pair is ready to demo when it has a reproducible local run, cited RAG output, bounded tool use, an evaluation result, one evidence-driven improvement, a responsible-AI note, a clean repository, and a START explanation both students can deliver.

Deployment is valuable but must not block completion when the network is unreliable.
