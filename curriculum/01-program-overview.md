# Modern AI Engineering: Build, Evaluate, Ship, and Explain

## Three-Day Curriculum for Final-Year CSE and AI/ML Students

**Duration:** 3 days, 8 hours per day, including lunch and breaks  
**Cohort:** 60 students working as 30 pairs  
**Delivery style:** Show, build, test, improve, and explain  
**Primary model:** `gpt-oss-120b` through the Nscale API  
**Primary environments:** Python, Google Colab, Cline, GitHub, and Coolify  
**Curriculum status:** Execution-ready design, revision 2; dependency versions and model IDs must be frozen after a final dry run  
**Research checked:** 16 August 2026

> **Revision 2 changes.** Fine-tuning became a demonstration plus a decision card instead of a pair lab. AI-assisted development was promoted from a background habit to a first-class Day 2 block pointed at a real component. MCP was trimmed to roughly 95 minutes. The evaluation harness gained a scheduled build slot. Lab 1 became defect diagnosis rather than transcription. The independent-domain track was removed in favour of stretch depth on the common project. Each day now reserves a named float block. Rationale is stated inline at each change.

## Workshop promise

By the end of the workshop, each pair should be able to say:

> We built and demonstrated an AI application that retrieves evidence from documents, cites its sources, selects bounded tools, and exposes useful capabilities through MCP. We wrote the harness that measures it, used it to find a real failure, fixed that failure, and can show the before and after. We used an AI coding assistant on part of it and can say exactly which part and how we verified it. We can explain the architecture, trade-offs, security risks, failures, and next improvements.

The goal is not to make students experts in every AI technique in three days. The goal is to give them a repeatable engineering process they can use to build future projects independently:

```text
Understand the problem
        ↓
Choose the simplest suitable AI pattern
        ↓
Build one observable component at a time
        ↓
Evaluate with representative cases
        ↓
Add safety and operational controls
        ↓
Ship, document, and explain the evidence
```

## Why this curriculum should improve career readiness

The curriculum deliberately combines technical and human skills. The World Economic Forum identifies AI and big data, cybersecurity, technological literacy, analytical thinking, and lifelong learning among skills growing in importance. The workshop therefore assesses students through decisions, debugging, evidence, collaboration, and explanation—not code generation alone. [World Economic Forum, *Future of Jobs Report 2025*](https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/)

The 2025 Stack Overflow Developer Survey found that more respondents distrusted AI-tool accuracy than trusted it, and that “almost right” output and debugging AI-generated code were common frustrations. Consequently, Cline is taught as an engineering assistant inside a plan-review-test workflow, not as a substitute for understanding. [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/ai)

Students leave with evidence that can be inspected in an interview:

- a working GitHub-ready project
- meaningful commit history and pair collaboration
- an architecture diagram
- a RAG pipeline with citations
- a bounded tool-calling agent
- a small Python MCP server connected to Cline
- an evaluation harness the pair built with an AI coding assistant under review
- a task-specific evaluation set and results table
- a Responsible AI and security note
- deployment or a reliable local demonstration
- honest resume bullets
- a concise START project explanation

## Fixed delivery assumptions

- There are 60 students, organized into 30 stable pairs.
- Students have reasonable Python, CS, ML, and AI theory knowledge, but practical proficiency varies.
- Some students have used GitHub, LLM APIs, RAG, or agents; many have not built a complete system.
- Each student receives an Nscale service credential. The current Nscale documentation uses service tokens and an OpenAI-compatible Python client. Do not call these credentials “API keys” in setup material because Nscale documents API-key removal in favor of service tokens. [Nscale chat guide](https://docs.nscale.com/docs/use-cases/chat), [Nscale deprecations](https://docs.nscale.com/docs/faqs/deprecations)
- No reliable internet guarantee exists.
- Pre-work and setup checks can be distributed before the event.
- No formal grade is required. Participation, checkpoint evidence, and the final project demonstration are the completion signals.
- Every pair builds the same project. Fast pairs go deeper on that system rather than starting a different one; see section 11.

### Time-allocation interpretation

The preferred 2-hour explanation, 2-hour demonstration, and 4-hour exercise balance describes a 25/25/50 learning ratio. Because lunch and breaks are included in the eight-hour day, each day below contains 6 hours 45 minutes of active learning and 1 hour 15 minutes of breaks.

The active blocks are approximately:

- 75 minutes explanation, decision-making, and debrief
- 90 minutes instructor demonstration
- 222 minutes student implementation, testing, and presentation
- 18 minutes named float

Averaged across the three days that is roughly 18% explanation, 22% demonstration, 55% exercise, and 5% reserve. Explanation sits slightly under the 25% target and exercise slightly over, which is the intended direction for this cohort: these students have the theory and lack the practice.

Demonstrations include prediction and inspection questions, so students remain active rather than watching passively.

### Float blocks are deliberate

Each day reserves an explicit 15–20 minute float block. With 30 pairs and mixed practical proficiency, the largest schedule risk is a single environment or credential problem cascading into the next checkpoint. The float block absorbs that. If the room is on schedule, spend it on the fast-finisher extensions or an extra evaluation rerun; never plan content into it in advance.

## Learning outcomes

By the end of Day 3, a participating student should be able to:

1. Call an OpenAI-compatible LLM API safely using an environment-held Nscale service token.
2. Decide when a problem needs prompting, RAG, a deterministic workflow, an agent, MCP, or fine-tuning.
3. Explain tokens, context, embeddings, retrieval, tool calling, and model limitations in plain language.
4. Implement and debug a small RAG pipeline from understandable components.
5. Measure whether retrieval found the supporting source before blaming the LLM.
6. Implement a bounded agent loop with typed tools, validation, stopping conditions, and logs.
7. Explain the difference between an agent, a workflow, a tool call, an API, and MCP.
8. Build a small Python MCP server and connect it to Cline over local STDIO.
9. Explain what fine-tuning changes, and read a demonstrated base-versus-adapted comparison well enough to decide when adaptation is the right tool.
10. Create a task-specific evaluation set containing normal, edge, and adversarial cases, and build the harness that runs it.
11. Apply concrete privacy, prompt-injection, least-privilege, secret-handling, and human-approval controls.
12. Deliver a real feature through an AI coding assistant using a specification → plan → implement → inspect → test → document workflow, and state what was generated versus personally verified.
13. Package an application with a health check, environment configuration, errors, logs, and reproducible setup.
14. Deploy through Coolify when connectivity permits or produce a reliable local demonstration when it does not.
15. Explain personal contribution and technical trade-offs through README evidence and the START method.

### Alignment with the original institutional themes

| Original fourth-year theme | Practical interpretation in this curriculum |
|---|---|
| Enterprise AI and Responsible AI | Students design an enterprise-style knowledge and action assistant, map its data and risk boundaries, test prompt injection, and document human oversight. |
| AI for software development and productivity | A dedicated Day 2 block, not a background habit: students ship one real capstone component—the evaluation harness—through spec, plan, diff review, tests, and debugging with an AI coding assistant, and must state what was generated versus personally verified. |
| Capstone implementation | One guided application is developed through daily checkpoints rather than invented at the end. |
| Technical assessment | Students demonstrate working behavior, evaluation evidence, a known limitation, and personal contribution without a formal grade. |
| Career readiness | Students finish a GitHub-ready repository, deployment/local demo, architecture, README, resume bullet, and START interview explanation. |

This keeps the proposal's required outcomes visible while replacing vague coverage with observable engineering work.

