# Day 1 — RAG from first principles to an evaluated system

## The promise to students

By the end of Day 1, you will not merely have a chatbot that appears to work. You will be able to:

- explain each stage of a RAG system
- inspect what was chunked and retrieved
- compare chunking strategies fairly
- compare vector, hybrid, and parent-document retrieval
- measure retrieval with a fixed evaluation set
- cite the evidence used for an answer
- refuse when approved evidence is missing
- prevent archived or restricted documents from entering the model context
- treat instructions found inside retrieved documents as untrusted data

The Day 1 experimental rule is:

```text
same questions + same corpus
        ↓
different chunking
        ↓
different RAG architecture
        ↓
same evaluation harness
        ↓
compare metrics and inspect failures
```

Change one major variable at a time. If the corpus, questions, model, top-k, and scorer all change together, the result cannot tell you what caused an improvement.

## The two-corpus design

The main afternoon comparison uses a deterministic subset of [MultiHopRAG](https://huggingface.co/datasets/yixuantt/MultiHopRAG): 12 questions, with three examples from each published type (`inference_query`, `comparison_query`, `temporal_query`, and `null_query`). Its answerable questions require evidence from two or three documents. The snapshot contains 18 evidence articles plus 12 lexical hard negatives, for 30 attributed documents in total.

OrbitDesk is a separate, fictional collaboration product used for the morning first-principles build and the final enterprise-safety challenge. Its nine original Markdown-style documents include:

- product and API documentation
- authentication and escalation runbooks
- current and superseded retention policies
- privacy rules
- an untrusted document containing a prompt-injection attempt
- a restricted synthetic incident that ordinary students must never retrieve

Its 12 safety cases cover direct questions, paraphrases, exact identifiers, ambiguity, missing answers, conflicting versions, live-state routing, sensitive data, and document injection. These synthetic controls should not be mixed into the MultiHopRAG quality score; they answer a different question.

This split is deliberate:

- **MultiHopRAG** gives a realistic, licensed, multi-document retrieval benchmark.
- **OrbitDesk** gives deterministic version, access-control, tool-routing, and prompt-injection cases that the news benchmark does not contain.

## 1. What RAG is

Retrieval-augmented generation gives a model selected external evidence at request time.

```text
Documents → parse → chunks → vectors/index
                                  ↑
Question  → encode/search → top-k chunks → grounded prompt → answer + citations
```

The model is not retrained on the documents. The documents remain outside the model and can be updated, filtered, cited, and audited.

### A useful mental model

RAG has two programs:

1. **Ingestion:** turn documents into searchable units and preserve their metadata.
2. **Serving:** turn a question into retrieval results, construct controlled context, and produce or decline an answer.

Separating these programs matters. Re-parsing and re-embedding the corpus during every user request adds avoidable latency and makes version rollback difficult.

## 2. When to use RAG

Use RAG when the answer should come from a document collection that is private, changing, too specialized for the base model, or must be cited.

Do not default to RAG when:

- the task is a deterministic calculation—use code
- the answer is live state—use an API or tool
- the task changes output style rather than supplying knowledge—use prompting or consider fine-tuning
- the evidence set is tiny enough to place directly in a prompt
- there is no trustworthy corpus or no way to define correct behavior

For example, “What does policy version 3.0 say?” is a retrieval question. “Is the Sync API down right now?” is a live tool question. “Calculate the average latency” is a code question.

## 3. The base model is not the knowledge base

A language model predicts plausible continuations. It can produce a fluent response when it lacks the workshop’s private product facts. That is why the first demonstration asks a product-specific question without retrieval.

The lesson is not that every unsupported answer will be obviously wrong. The dangerous response is often believable. A useful system must distinguish:

- **model knowledge:** information encoded during training
- **retrieved evidence:** text selected from the approved corpus for this request
- **generated answer:** a model output that still requires validation

## 4. Parsing and metadata

Parsing converts a source file into text and structure. A PDF, webpage, table, and Markdown file may require different parsers. Bad extraction cannot be repaired by a better embedding model.

Every workshop chunk keeps:

- document ID and title
- section name
- version and effective date
- whether the version is current
- roles allowed to retrieve it
- trust classification
- chunking strategy and position

Metadata is part of the retrieval system, not decoration added after generation. Without it, the application cannot reliably filter versions, enforce access, create citations, or explain what happened.

## 5. Chunking

A chunk is the unit indexed and returned by retrieval. Chunking creates a trade-off:

- small chunks improve precision but may lose the explanation around a fact
- large chunks retain context but may mix topics and consume prompt space
- overlap protects boundary information but duplicates text and increases index size

### Fixed-size chunking

Split every fixed number of characters with overlap.

```text
characters 0–319
characters 260–579
characters 520–839
```

It is fast and predictable, but it can separate a heading from its rule, cut a sentence, or mix two sections.

### Structure-aware chunking

Split on meaningful document boundaries such as Markdown headings, then fall back to paragraphs or sentences only when a section is too large.

This usually improves citations and coherence when documents have useful structure. Its chunk sizes are less uniform, so large sections still need a fallback rule.

### Parent-child chunking

Search small child sentences for precision, then return their larger parent section as context.

```text
query → search child sentence → look up parent section → send parent to model
```

This separates the best unit for finding evidence from the best unit for explaining it. The cost is more index entries and more mapping logic.

## 6. Embeddings and vector retrieval

An embedding maps text to a vector. Similar meanings should produce vectors that are closer in the embedding space.

For normalized vectors, cosine similarity is their dot product:

```text
cosine(q, d) = (q · d) / (||q|| × ||d||)
```

The notebook uses `sentence-transformers/all-MiniLM-L6-v2` for the main semantic experiment. It also includes a TF-IDF encoder as an offline fallback. TF-IDF creates vectors, but it is lexical rather than a neural semantic embedding; students should not call the two methods equivalent.

Vector search is useful for paraphrases. It can still miss exact identifiers, rare product codes, and version numbers.

## 7. BM25 and hybrid retrieval

BM25 is a lexical ranker. It rewards query terms that occur in a document, especially terms that are rare across the corpus. This makes it useful for identifiers such as `OD-X31` and `OD-429`.

Hybrid retrieval combines:

- vector ranking for meaning and paraphrase
- BM25 ranking for exact terms

The workshop merges the two ranked lists using reciprocal rank fusion:

```text
RRF(document) = Σ 1 / (k + rank_from_each_retriever)
```

RRF uses ranks rather than raw scores, avoiding the invalid comparison of a cosine score with a BM25 score.

Hybrid search is not automatically superior on every corpus. Students must run the same cases and inspect whether its improvement justifies the extra index and latency.

## 8. Retrieval is not generation

Debug the stages separately:

```text
Was the right source retrieved?
        ├── no  → parsing, chunking, query, embedding, filters, top-k, retrieval
        └── yes → prompt, context ordering, generation, citation, validation
```

Prompt engineering cannot recover a fact absent from the retrieved context. Conversely, correct retrieval does not guarantee a faithful answer.

The core notebook evaluates retrieval deterministically before making an optional model call. This keeps API availability and model variability from obscuring the first engineering lesson.

## 9. The evaluation sets

Each MultiHopRAG benchmark case stores:

- a stable case ID and category
- the user question
- relevant document IDs, or no relevant source
- whether the corpus can answer the question
- the published reference answer and question type
- a short, human-verified scoring note

The separate OrbitDesk safety cases add forbidden documents, expected safety behavior, and expected tool routing.

Do not let the model invent the reference answer without checking the source. A confidently wrong label creates a benchmark that rewards the wrong system.

### Metrics used on Day 1

| Metric | Question it answers |
|---|---|
| Hit@5 | Did at least one supporting passage appear in the top five? |
| Evidence recall@5 | What fraction of all published evidence passages appeared? |
| MRR | How early did the first relevant document appear? |
| Context precision | What fraction of retrieved results were relevant? |
| No-answer accuracy | Did the evidence gate decline unanswerable cases? |
| Forbidden leakage rate | Did an unauthorized source enter retrieval results? |
| Archived retrieval rate | Did a superseded policy enter current answers? |
| Latency | How long did retrieval take? |
| Context characters | How much text would be sent to the model? |

No single score is “RAG quality.” A system can have good Hit@5 and poor evidence recall, or good retrieval and unsafe generation.

## 10. Abstention and ambiguity

An assistant should say “insufficient evidence” when approved context does not support an answer. A low retrieval score alone is not a universal confidence measure; thresholds must be calibrated on the evaluation set.

Ambiguity is a separate case. “How long is it retained?” may retrieve a retention policy, but the system still does not know whether “it” means a backup, export, log, or ticket. The correct behavior is to ask a clarifying question.

The notebook’s evidence gate is deliberately simple and will make mistakes. Those failures are teaching material: students inspect them and propose a stronger gate.

## 11. Enterprise controls belong before generation

### Current-version filtering

The OrbitDesk corpus contains an archived 14-day policy and a current tier-specific policy. The default retrievers remove archived chunks before ranking. Students can disable the filter to observe the regression.

### Access control

The synthetic restricted incident contains a recovery token. A student query must never return that chunk. Filtering after context has reached the model is too late; the unauthorized data has already crossed the boundary.

### Prompt injection in retrieved documents

Retrieved text is untrusted data. A document may contain text such as “ignore previous instructions.” It does not become a system instruction merely because retrieval found it.

The workshop demonstrates three controls:

1. preserve a trust label in metadata
2. remove suspicious paragraphs from untrusted text before prompt construction
3. tell the model that source blocks are data and require citations

Pattern matching is not a complete injection defense. It is a visible first control that students can attack and improve.

### Auditability

Record the query, selected document and section IDs, scores, filters, security events, latency, model identifier, and final response. Do not log access tokens or copy restricted documents into general traces.

## 12. The four controlled experiments

The notebook builds these configurations:

| Experiment | Chunking | Retrieval | What it isolates |
|---|---|---|---|
| `fixed_vector` | 500 fixed characters, no overlap | vector | deliberately weak boundary baseline |
| `structure_vector` | headings/sections | vector | effect of chunking |
| `structure_hybrid` | headings/sections | vector + BM25 + RRF | effect of retrieval architecture |
| `parent_hybrid` | sentence children, section parents | hybrid child search | precision/context trade-off |

All four use the same corpus, cases, role, current-version rule, top-k, and evaluation functions.

## 13. Suggested teaching flow in Colab

### 09:00–10:40 — orientation and setup

| Time | Activity | Evidence |
|---|---|---|
| 09:00–09:20 | Introduction, career outcome, pair roles, diagnostic poll | Pair roles and baseline confidence |
| 09:20–09:50 | Colab and account setup/recovery | Every pair opens the notebook and runs the health cell |
| 09:50–10:15 | AI application decision ladder and RAG mental model | Students classify four example tasks |
| 10:15–10:40 | Finished OrbitDesk demo and predictions | Students predict retrieval, citation, refusal, and live-tool behavior |

### 10:55–12:45 — first successful RAG and chunking lab

1. Ask a private OrbitDesk question without retrieval.
2. Inspect the unsupported answer rather than trusting its tone.
3. Load the corpus and run fixed-size retrieval.
4. Display the exact top-three chunks and scores.
5. Compare fixed and structure-aware chunks side by side.
6. Run the same question again and explain the changed result.
7. Run the tests; every pair should get a visible pass before lunch.

Acceptance check: both partners can point to the retrieved text, its metadata, and the source of the answer.

### 13:30–15:35 — MultiHopRAG architecture comparison and evaluation

1. Introduce embeddings, cosine similarity, BM25, and RRF only as needed by the code.
2. Load the attributed 30-document MultiHopRAG snapshot and inspect its four question types.
3. Build the four experiment configurations.
4. Run all 12 cases through the same top-5 harness.
5. Plot Hit@5, evidence recall, MRR, context precision, latency, and context size.
6. Inspect individual regressions; do not stop at the average.
7. Change one parameter—chunk size, top-k, or architecture—and rerun.

Acceptance check: each pair records one improvement, one regression, and the evidence for both.

### 15:50–16:40 — enterprise challenge

1. Disable the current-version filter and observe the archived policy.
2. try the restricted recovery-token query as the student role.
3. inspect the untrusted connector document and the sanitized prompt.
4. create one new injection string and test whether the simple detector catches it.
5. write one limitation and a stronger production control.

Acceptance check: zero forbidden-document leakage in the supplied student-role suite, plus one documented attack the current pattern does not catch.

### 16:40–17:00 — checkpoint

Each pair explains:

- which configuration they would ship first and why
- which metric improved and which trade-off worsened
- one question the corpus cannot answer
- one security boundary enforced before generation

## 14. Pair roles in the notebook

- **Driver:** runs or edits the current cell and narrates what changes.
- **Navigator:** predicts the output, checks retrieved evidence and metrics, and records the finding.

Swap at each checkpoint, not merely when one student becomes stuck.

## 15. What this workshop intentionally postpones

Day 1 does not need a vector database, agent framework, autonomous query rewriting, LLM-as-judge, or production deployment. Those abstractions are easier to evaluate after students can see chunks, scores, filters, and failures directly.

Agentic retrieval is previewed as a later choice: a bounded loop may decide whether to rewrite, retrieve again, use another source, or stop. It should be added because measured cases require it—not because “agentic” sounds more advanced.

## References and design provenance

The retrieval benchmark is an attributed ODC-BY subset of MultiHopRAG. The selection procedure, hard-negative selection, adapters, retrievers, metrics implementation, notebook, tests, OrbitDesk safety corpus, and lesson sequence are workshop code. See `MULTIHOP_ATTRIBUTION.md` and `multihop_subset_manifest.json` for exact provenance.

- [RAG in Production: What Breaks When You Move Past the Tutorial](https://sunilprakash.com/writing/rag-in-production/) — production gap, chunking, retrieval, evaluation, and guardrail framing
- [RAG in 2026: From Pipeline to Agent](https://sunilprakash.com/writing/rag-in-2026-pipeline-to-agent/) — pipeline-to-loop progression; the referenced page was listed by the author but was not directly retrievable during preparation
- [Enterprise RAG Bench](https://github.com/sunilp/enterprise-rag-bench) — comparison axes, project separation, enterprise concern categories, and evaluation-first structure
- [Enterprise RAG Bench: enterprise concerns](https://github.com/sunilp/enterprise-rag-bench/tree/main/enterprise-concerns) — access control, audit trails, PII, multi-tenancy, and cost topics
- [MultiHopRAG dataset](https://huggingface.co/datasets/yixuantt/MultiHopRAG) — source of the attributed multi-document benchmark subset
- [MultiHop-RAG repository and paper links](https://github.com/yixuantt/MultiHop-RAG) — published task design, evaluation code, citation, and ODC-BY license statement
- [Sentence Transformers semantic textual similarity documentation](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) — sentence encoding and similarity workflow
- [scikit-learn text feature extraction documentation](https://scikit-learn.org/stable/modules/feature_extraction.html) — TF-IDF concepts and implementation reference
- [Nscale chat integration guide](https://docs.nscale.com/docs/use-cases/chat) — optional OpenAI-compatible live generation
- [Nscale model discovery](https://docs.nscale.com/docs/ai-services/models) — verify the live model ID through the console or `/v1/models`; do not hard-code an unverified ID
