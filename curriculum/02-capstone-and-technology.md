# Shared capstone and technology choices

## Shared capstone

### AI Support Engineering Assistant

The common project is a support and operations assistant for a fictional software product. The supplied document set should contain:

- product documentation
- API usage notes
- troubleshooting runbooks
- service-status data
- support and privacy policies
- a few intentionally ambiguous or conflicting passages
- one clearly labeled adversarial document for the prompt-injection exercise

The assistant must:

1. Answer product and troubleshooting questions using RAG.
2. Cite the retrieved document and section used for its answer.
3. Admit when the supplied knowledge base does not contain the answer.
4. Use a tool to retrieve a service's current status from prepared local JSON data.
5. Create a **draft** support ticket preview, but require human confirmation before any real write action.
6. Record tool decisions and useful timing information without logging secrets.
7. Expose selected read-only functionality through a small MCP server.
8. Run a provided evaluation set and show results.
9. Handle one prompt-injection attempt and one sensitive-data request safely.
10. Run behind a simple web interface and FastAPI backend, or use the prepared local fallback.

### Why this project

The project is recognizable across AI Engineer, Data Scientist, Python Developer, Full-Stack Developer, and Software Engineer interviews. It demonstrates integration and judgment rather than only a notebook. The same architecture also transfers naturally to healthcare administration, sales knowledge, electronics troubleshooting, education, and internal enterprise tools.

### Architecture

```text
Browser / simple web UI
          |
          v
FastAPI application  ---->  health check and structured logs
          |
          v
Bounded assistant workflow
   |             |                 |
   |             |                 +--> draft_ticket(...) [preview only]
   |             +--> get_service_status(...) [local JSON]
   +--> search_knowledge_base(...) [RAG]
                    |
                    +--> parser -> chunks -> embeddings -> similarity search
                    |                                  |
                    +----------------------------------+
                                     |
                                     v
                         selected context + citations
                                     |
                                     v
                         gpt-oss-120b through Nscale

Shared service functions
          |
          +--> Thin Python MCP adapter
                    |
                    +--> resource: support://runbook
                    +--> tool: search_knowledge_base
                    +--> tool: get_service_status
                              |
                              v
                         Cline MCP host

Evaluation harness
   +--> retrieval hit@k
   +--> citation check
   +--> answer rubric
   +--> tool-route accuracy
   +--> safety/adversarial cases
   +--> latency and failures
```

### Engineering principle

The MCP server must be a thin adapter over the same tested service functions used by the web application. Students should not duplicate RAG or business logic inside the MCP file. This teaches separation of concerns and makes the relationship clear:

```text
RAG = how the system retrieves evidence
Tool calling = how a model requests a function
Agent = how the application decides and loops
MCP = a standard interface through which a host discovers and invokes capabilities
```

### Recommended repository shape

```text
ai-support-engineer/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── llm_client.py
│   ├── rag.py
│   ├── agent.py
│   ├── tools.py
│   └── logging_config.py
├── mcp_server/
│   └── server.py
├── data/
│   ├── documents/
│   ├── service_status.json
│   └── prepared_index/
├── evals/
│   ├── cases.jsonl
│   ├── run_evals.py
│   └── results.example.json
├── tests/
│   ├── test_retrieval.py
│   └── test_tools.py
├── web/
│   └── index.html
├── notebooks/
│   ├── rag_from_primitives.ipynb
│   └── fine_tuning_comparison.ipynb
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── EVALUATION.md
├── RESPONSIBLE_AI.md
└── requirements.txt
```

The instructor should provide the structure and interface shell. Students implement the important AI and evaluation components rather than spending the workshop on HTML or boilerplate.

## Technology decisions

### LLM and Nscale

- Use `gpt-oss-120b` through Nscale for generation and tool calling.
- OpenAI documents `gpt-oss-120b` as an open-weight, fine-tunable reasoning model with function-calling and structured-output capabilities. [Official OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-oss-120b)
- Nscale documents an OpenAI-compatible Chat Completions workflow and tool definitions. Use a small provider adapter so the application is not tightly coupled to one model. [Nscale chat guide](https://docs.nscale.com/docs/use-cases/chat), [Nscale Chat Completions reference](https://docs.nscale.com/api-reference/inference/create-chat-completion)
- Discover and verify the available model identifier through Nscale's current model list or `/v1/models` during the instructor dry run; do not guess it in student code. [Nscale model documentation](https://docs.nscale.com/docs/ai-services/models)
- Keep `NSCALE_SERVICE_TOKEN`, `NSCALE_BASE_URL`, and `NSCALE_MODEL_ID` in environment variables.
- Even if the assigned access has no stated rate limit, bound retries, concurrent calls, output tokens, and agent iterations. Network and service failures can still occur.

### Embeddings and retrieval

- First demonstration: a tiny, transparent pipeline using prepared text, an embedding function, NumPy cosine similarity, and visible top-k chunks.
- Project path: a local embedding model or a verified Nscale embedding model, selected and pinned after the dry run.
- Fallback: distribute precomputed embeddings and an index plus a keyword-search implementation.
- Do not make the workshop dependent on downloading a large embedding model on Day 1.
- A vector database framework is optional. Students must understand the stored vectors, metadata, top-k result, and failure mode before using an abstraction.

### Agent implementation

- Build one manual bounded loop before using a framework.
- Maximum default iterations: 3.
- Tools have typed schemas, concise descriptions, validated inputs, defined errors, and no hidden side effects.
- Keep deterministic steps deterministic. Do not ask an agent to perform routing that a simple condition can handle reliably.
- Require approval before any external write or consequential operation.

### AI-assisted development

- Treat the coding assistant as a first-class workshop topic with its own demonstration and lab, not as a tool students happen to have open.
- Baseline tool: Cline with a free-tier model configuration. Students who already use Claude Code, Codex, Copilot, or Cursor may use those instead; the workflow being taught is tool-independent and must be reproducible in whichever assistant the pair uses.
- The assistant is applied to a **real capstone component** (the evaluation harness), never to a throwaway exercise. Students must be able to point at shipped code and say what the assistant produced and what they changed.
- Required discipline: written acceptance criteria before prompting, a plan before code, line-by-line diff review, tests run and one failure reproduced, and a documentation update covering only what was actually verified.
- Because Day 1 and Day 2 morning are hand-written, students meet the assistant already knowing what correct code for this system looks like. Do not move the assistant earlier.

### MCP

- Use the current stable official Python MCP SDK version that passes the instructor dry run; pin the version.
- Baseline transport: local STDIO, because the internet is uncertain and the MCP specification recommends STDIO support for local client-launched servers. [MCP transport specification](https://modelcontextprotocol.io/specification/draft/basic/transports)
- Baseline host: Cline. Cline supports local STDIO servers and remote Streamable HTTP servers. [Cline MCP documentation](https://docs.cline.bot/mcp/mcp-overview)
- Stretch path: deploy a remote Streamable HTTP endpoint through Coolify.
- Do not build new examples on legacy HTTP+SSE.
- “Build from scratch” means writing the server, tool/resource definitions, validation, error behavior, and client configuration from a blank Python file using the official SDK. It does not mean reimplementing JSON-RPC or the transport protocol.

### Fine-tuning: demonstration, not a lab

Fine-tuning is taught as a **decision and a demonstration**, not as a pair-built deliverable. The reasoning is deliberate:

- Students cannot fine-tune the model they actually ship, so the exercise never connects to the capstone.
- The realistic version of the lab is "run the instructor's prepared notebook," which teaches cell-execution rather than engineering judgement.
- Every degraded-connectivity path already reduced to "load the prepared adapter," so the lab's own fallback was the demonstration.

What remains is the part that carries interview value: knowing **when** adaptation beats prompting, RAG, or tools, and being able to read a base-versus-adapted comparison honestly.

Delivery rules:

- Do not attempt to fine-tune `gpt-oss-120b` during the workshop.
- Use an instructor-tested 0.5B–1.5B permissively licensed model in Colab.
- Use PEFT/LoRA so only a small set of additional parameters is trained. Hugging Face documents PEFT as a way to adapt models without training every parameter and provides a LoRA workflow. [Hugging Face PEFT documentation](https://huggingface.co/docs/peft/quicktour)
- The task should change behavior, not inject current facts. Recommended task: convert support messages into a consistent severity/category/summary JSON structure.
- The demonstration must end on a base-versus-adapted held-out comparison, including at least one regression. A training cell that runs without a comparison is not a completed demonstration.
- Publish the full notebook as a take-home and fast-finisher artifact, with data, adapter, logs, and both output sets, so motivated students can complete it after the workshop.

### Application and deployment

- Python 3.11 is the conservative local baseline unless the dry run validates another version.
- Use FastAPI with a supplied minimal browser interface.
- Use Colab for the from-primitives RAG and fine-tuning notebooks.
- Package the final app in Docker and deploy through Coolify when connectivity permits.
- Provide a working local command and saved demonstration path even when deployment succeeds.

