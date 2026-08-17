# Day 2 — Agents, AI-Assisted Development, and MCP

Day 2 carries three topics in a deliberate order. Students first hand-write an agent loop, so they know what correct code for this system looks like. Only then do they bring an AI coding assistant to a real component—the evaluation harness—because reviewing generated code is meaningless without that prior standard. MCP comes last and stays deliberately small: a thin adapter over services that already exist and are already tested.

## Day 2 outcomes

By 17:00, every pair should have:

- a plan reviewed before implementation
- a bounded manual agent/tool loop, hand-written
- three typed tools with safe behavior
- a trace or structured event log
- a working evaluation harness that runs the Day 1 case file and prints a results table
- agent route cases added to the evaluation set
- a written record of what the coding assistant generated and what the pair corrected
- a Python MCP server exposing existing capstone services over STDIO
- one correct tool selection and one correct non-call demonstrated through Cline
- a Day 2 checkpoint commit

## Schedule

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

## Why AI-assisted development gets its own block

The original design treated the coding assistant as a background habit demonstrated in passing. That undersells the skill students will use most on day one of a job, and it is the wrong way round: an assistant used before students can recognise correct code teaches dependence, while an assistant used after teaches review.

The block is therefore placed at midday on Day 2, after a hand-written agent loop and before MCP, and it is pointed at a component the project genuinely needs. The evaluation harness is the right target because it is well-specified, testable, independent of the running application, and previously the one piece of the capstone that never had scheduled build time.

## The assistant workflow

The instructor demonstration should model this exact sequence on live capstone code, and students should repeat it in Lab 4:

1. Write a small requirement and acceptance criteria **before opening the assistant**.
2. Ask the assistant to inspect the relevant files.
3. Ask for a plan with no code changes.
4. Challenge at least one assumption in the plan and require a revision.
5. Approve one small implementation step.
6. Review the diff line by line and reject anything unexplained.
7. Run tests and reproduce one failure.
8. Ask the assistant to diagnose from the evidence, not from a guess.
9. Apply the smallest suitable fix.
10. Update documentation with what was actually verified.

Students should see that an assistant's plan is a proposal, not proof. The demonstration must include at least one suggestion the instructor rejects on the record, with the reason stated aloud.

Pairs who already use Claude Code, Codex, Copilot, or Cursor daily may use their own tool. The workflow is what is assessed, not the vendor. Those students are also the natural pod contacts for pairs meeting an assistant for the first time.

## Lab 3: bounded agent

Required tools:

```text
search_knowledge_base(query, top_k)
get_service_status(service_name)
draft_support_ticket(title, severity, evidence)
```

Rules:

- `search_knowledge_base` is read-only and returns text plus source metadata.
- `get_service_status` reads prepared local JSON.
- `draft_support_ticket` returns a preview object only; it does not create an external ticket.
- Validate service names, severity, length, and required evidence.
- Log tool name, success/failure, duration, and correlation ID.
- Do not log the service token, full private user data, or hidden reasoning.
- Stop after three agent iterations.
- Return a clear error when a tool fails.
- Ask the user for missing required information instead of inventing it.

Students add at least five route cases:

- answer directly without a tool
- use RAG
- use status tool
- request missing ticket fields
- reject or safely preview a consequential action

Lab 3 is hand-written. Coding assistants stay closed for this lab; the point is that students can produce and defend this loop themselves before delegating anything.

## Lab 4: ship the evaluation harness with a coding assistant

This is the AI-assisted development lab. The deliverable is `evals/run_evals.py`—the component that turns Day 1's case file from a document into measurement, and the piece the project has needed since Day 1.

**Step 1 — specify before prompting (10 min, assistant closed).**
The pair writes acceptance criteria by hand:

```text
Input:  evals/cases.jsonl and the existing app services
Output: per-case result rows plus a summary table
Metrics: retrieval hit@3, citation correctness, answer score,
         no-answer behavior, expected-tool match, latency
Must:   run offline against fixtures, exit non-zero on harness error,
        never print the service token, be rerunnable without edits
```

**Step 2 — plan and challenge (15 min).**
Ask the assistant to inspect the repository and propose a plan with no code changes. The pair must record one assumption they challenged and what changed as a result. A plan accepted unmodified is a sign the pair did not read it.

**Step 3 — implement in reviewed steps (30 min).**
Approve one step at a time. Review each diff line by line. Anything the pair cannot explain gets rejected and re-requested, not accepted with a shrug.

**Step 4 — run, fail, diagnose (15 min).**
Run the harness against the real case file. It will fail or produce a suspicious result—cases are messy and metrics are subtle. Reproduce the failure, hand the assistant the evidence rather than a guess, and apply the smallest fix.

Every pair then adds their five agent route cases from Lab 3 to the case file and reruns the harness on the complete set.

**Required artifact — `ASSISTANT_LOG.md`:**

```text
What I specified before prompting:
What the assistant planned:
The assumption I challenged and why:
What I accepted unchanged:
What I rejected or rewrote, and why:
What I verified by running, not by reading:
What I still do not fully understand in this code:
```

That last line is graded as honesty, not weakness, and it is the line that most often turns into a good interview answer.

Acceptance criteria: the harness runs the full case file end to end, prints a results table, works against offline fixtures, contains no secrets, and both partners can explain any line an instructor points at. A pair who cannot explain their own harness has not finished the lab regardless of whether it runs.

## Lab 5: thin MCP adapter

MCP is scoped to roughly 95 minutes—a demonstration plus one focused lab. It is a genuinely useful integration skill and a common interview topic, but it is an interface over capabilities the pair has already built and tested. The engineering lesson is the thinness of the adapter, and that lesson does not require more time than this.

First teach the four roles:

```text
User <-> MCP host (Cline) <-> MCP client connection <-> MCP server <-> service/data
```

Students then create a Python server that exposes:

- resource: `support://runbook`
- tool: `search_knowledge_base(query: str, top_k: int = 3)`
- tool: `get_service_status(service_name: str)`
- bounded action tool: `draft_support_ticket(summary: str, severity: str)`

The action tool creates a reviewable draft only; it does not send, publish, or modify an external system. Use it to teach the difference between reading data and causing a side effect. If a later extension performs a real write, it must show the exact proposed action and require explicit user approval.

Required engineering behaviors:

- typed parameters
- useful docstrings/tool descriptions
- bounded inputs
- structured result containing source/status metadata
- helpful error messages
- logging to the correct stream
- no credentials embedded in source or configuration
- reused capstone service functions
- a structured preview before any action with side effects

Connect the server to Cline using local STDIO. Cline should discover the tools, and each pair should demonstrate one correct tool selection and one case where Cline should not call a tool.

The official MCP security guidance warns that local servers execute with the client's privileges and recommends explicit consent, restricted access, and STDIO for limiting access to the client. Use this as a practical discussion of permissions, secret handling, malicious instructions arriving through tool content, accurate tool descriptions, approval before side effects, and why auto-approving write operations is dangerous—not as a long security lecture. [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)

## MCP stretch task

Only pairs that finish the common checkpoint may choose one:

- add a user-selected MCP prompt for incident triage
- add a second read-only resource
- add another bounded tool
- add unit tests for schema/error behavior
- compare ambiguous and precise tool descriptions
- deploy with Streamable HTTP through Coolify

Remote deployment must use authentication, HTTPS, origin validation, and least privilege. A public unauthenticated tool with a write action is not an acceptable stretch result.
