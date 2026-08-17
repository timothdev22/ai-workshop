# Day 1 — Understand, Choose, and Build Evidence-Backed RAG

## Day 1 outcomes

By 17:00, every pair should have:

- a functioning repository and Nscale health check
- a visible baseline LLM failure
- a repaired RAG pipeline that returns source metadata, plus a defect log explaining each fix
- a 12-case evaluation set draft
- baseline retrieval results
- an architecture decision sheet
- a one-page threat model and prompt-injection observation
- a Day 1 checkpoint commit

## Schedule

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

## Day 1 concept boundary

Teach only the transformer and embedding theory needed to answer these practical questions:

- Why can an LLM sound certain when it is wrong?
- Why does context length not remove the need for retrieval quality?
- What does an embedding preserve well, and what can it miss?
- How do chunking and top-k change the answer?
- How can we tell whether retrieval or generation failed?
- Why should cited answers still be checked?

Avoid transformer derivations, attention-matrix calculations, and historical surveys.

## Lab 1: repair a broken RAG pipeline

Typing a full pipeline from an empty file in one sitting strands the least practised third of the room in boilerplate while the confident third finishes early and disengages. Instead, students receive a **complete, runnable, deliberately defective** pipeline and diagnose it. Every student reads working reference code for parsing, chunking, embedding, and similarity search; the effort goes into understanding behavior rather than transcription.

The starter notebook runs end to end and returns confidently wrong answers. It contains four planted defects:

```text
1. Chunker splits on a fixed character count, cutting sentences and
   separating headings from the text they describe.
2. Chunk metadata is built but never attached to the retrieved result,
   so citations cannot be produced.
3. Similarity is computed on unnormalised vectors, so long chunks
   dominate the top-k regardless of relevance.
4. The prompt appends retrieved context without instructing the model
   to answer only from it, so the model silently falls back to its
   own knowledge when retrieval misses.
```

Students should:

1. Ask `gpt-oss-120b` a question whose answer exists only in the supplied product documentation, with retrieval disabled.
2. Save the unsupported baseline response as the comparison point.
3. Run the defective pipeline on the same question and record what it returns.
4. Inspect the intermediate values—chunks, metadata, vectors, top-k scores, final prompt—and locate each defect from evidence rather than by reading a hint sheet.
5. Repair the defects one at a time, rerunning the same question after each fix.
6. Record which fix changed which observable behavior. Not every fix will help visibly; that is a finding, not a failure.
7. Return an answer with document and section citations.
8. Return “insufficient evidence” when no chunk supports an answer.
9. Compare the baseline, defective, and repaired outputs in plain language.

Acceptance criteria: the repaired pipeline cites a correct source for a supported question, declines a question the documents do not answer, and the pair can explain the mechanism behind at least three of the four defects.

Fast-finisher extension: plant a fifth defect of their own design and hand the notebook to a neighbouring pair to diagnose.

## Lab 2: evaluation begins before polishing

Each pair starts from a provided six-case seed and expands it to at least 12 cases:

- 3 directly answerable questions
- 2 paraphrased questions
- 1 multi-document question
- 1 question not covered by the documents
- 1 ambiguous question
- 1 conflicting-source question
- 1 prompt-injection document case
- 1 sensitive-data request
- 1 tool-routing case for Day 2

For every case, store:

- user question
- expected source or expected no-answer behavior
- expected tool, if any
- safety expectation
- short scoring note

Do not use the model to generate the expected answer without human verification against the source.

## Practical evaluation metrics

Use simple metrics students can calculate and explain:

- **Retrieval hit@3:** Did one of the top three chunks contain the expected supporting evidence?
- **Citation correctness:** Does the cited source actually support the answer?
- **Answer score:** 0 = incorrect/unsupported, 1 = partly correct, 2 = correct and sufficiently grounded.
- **No-answer behavior:** Did the assistant refuse to invent information when evidence was missing?
- **Latency:** How long did the end-to-end request take?

The objective is comparison, not a magical score. Students should change one variable at a time and rerun the same cases.
