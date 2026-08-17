# Instructor preparation and infrastructure

## Instructor preparation

### Two weeks before

- Confirm the exact room schedule and break times.
- Form 30 pairs and six support pods.
- Request two lab assistants or technically confident volunteers in addition to the lead instructor. If none are available, appoint rotating pod contacts and rely on the documented help protocol.
- Distribute pre-work and setup checker.
- Confirm secure service-token distribution.
- Confirm GitHub access and whether repository creation is permitted.
- Test Nscale access from the college network.
- Ask the college for one wired-network option and hotspot policy.
- Decide whether the instructor's Coolify deployment is shared or each pair gets a deployment.

### One week before: freeze the workshop

- Verify Nscale base URL, authentication, model ID, tool-calling behavior, and model list.
- Pin Python dependencies from a clean Python 3.11 environment.
- Pin the stable MCP SDK version tested with the installed Cline version.
- Verify the Cline MCP configuration on Windows lab machines.
- Select and pin the embedding model.
- Select and pin the fine-tuning model and Colab runtime for the demonstration.
- Run every notebook from top to bottom in a clean account.
- Verify the Lab 1 defective pipeline: it must run without crashing, return confidently wrong answers, and be repairable in 65 minutes by a pair of average speed.
- Dry-run Lab 4 with the assistant tooling students will actually use, on a free-tier configuration, and time it.
- Confirm the free-tier coding-assistant configuration works from the college network at 30-pair concurrency, and prepare a fallback if rate limits bite.
- Build the Docker image and deploy it through Coolify.
- Run the complete evaluation set against the reference project.
- Scan the repository and Git history for secrets.
- Record a full reference demonstration.

### Required instructor assets

- starter repository
- completed reference repository
- **Lab 1 defective pipeline** with the four planted defects, plus an instructor key explaining each defect's mechanism and observable symptom
- checkpoint tags or branches for setup, RAG, agent, eval harness, MCP, and final
- printable or locally hosted lab sheets
- `ASSISTANT_LOG.md` template and a worked example
- reference `run_evals.py` for pairs whose Lab 4 harness does not converge, released only at the end of the lab
- small licensed document corpus, plus the approved alternate corpora for domain variation
- prepared index and embeddings
- keyword-search fallback
- cached Python wheelhouse or local package mirror where feasible
- fine-tuning take-home package: notebook, adapter, logs, and saved comparison outputs
- sanitized example `.env`
- Docker image or saved image archive
- saved API response fixtures clearly labeled as fixtures
- troubleshooting cards for the ten most likely failures
- setup checker and results format
- shared issue board and checkpoint board
- reference demo video and screenshots

## Infrastructure failure modes

### Level 1 — Normal internet

- Live Nscale generation and embeddings
- Live Colab fine-tuning
- GitHub push and pull
- Cline model calls
- Coolify deployment

### Level 2 — Slow or intermittent internet

- Use local/precomputed embeddings.
- Reduce LLM requests and use pair-shared calls.
- Use prepared response fixtures for repeated instructor demonstrations.
- Continue local MCP over STDIO.
- Commit locally and push later.
- Replay the fine-tuning demonstration from saved logs and outputs instead of training live.
- Deploy only the reference build while students prepare deployment files.
- If coding-assistant capacity is constrained, run Lab 4 as one assistant per pod with the pod working through the same workflow on a shared screen, then each pair adapting the result. The review discipline survives; only the typing is shared.

### Level 3 — No internet

- Run retrieval with the prepared index or keyword fallback.
- Use saved LLM fixtures, clearly labeled as recorded outputs.
- Build and test the agent using a deterministic mock model route.
- Build and connect the local MCP server to a test client if Cline cannot call a remote model.
- Replay the fine-tuning comparison from saved base/adapted outputs and run the scoring activity on paper.
- Run Lab 4 against a locally hosted or offline-capable assistant if one is available; otherwise hand pairs a *deliberately flawed* generated harness and run the review, diagnosis, and correction steps against it. The reviewing skill is the point and it survives without a live assistant.
- Run all deterministic tests and evaluation checks locally.
- Produce the repository, README, architecture, threat model, resume bullet, and START explanation.
- Demonstrate the instructor's recorded deployment and explain the exact later push/deploy steps.

The core learning outcomes must survive Level 3 even though a live model call or public URL may not.

