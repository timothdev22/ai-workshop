"""Build the self-contained Day 1 Colab notebook from the shared source files."""

from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).parent
OUTPUT = ROOT / "notebooks" / "day1_rag_workshop_colab.ipynb"


def markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def embedded_assets_cell() -> str:
    assets = {
        "rag_workshop.py": ROOT / "student_code" / "rag_workshop.py",
        "test_rag_workshop.py": ROOT / "student_code" / "test_rag_workshop.py",
        "data/corpus.json": ROOT / "student_code" / "data" / "corpus.json",
        "data/eval_cases.json": ROOT / "student_code" / "data" / "eval_cases.json",
        "data/multihop_corpus.json": ROOT / "student_code" / "data" / "multihop_corpus.json",
        "data/multihop_eval_cases.json": ROOT / "student_code" / "data" / "multihop_eval_cases.json",
        "data/multihop_subset_manifest.json": ROOT / "student_code" / "data" / "multihop_subset_manifest.json",
    }
    encoded = {
        target: base64.b64encode(path.read_bytes()).decode("ascii")
        for target, path in assets.items()
    }
    return f'''# This cell creates the exact shared student module, data, and tests.
from pathlib import Path
import base64

EMBEDDED_FILES = {encoded!r}
for target, payload in EMBEDDED_FILES.items():
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(payload))

print("Created:")
for target in EMBEDDED_FILES:
    print(" -", target)
'''


cells = [
    markdown(
        """# Day 1 — Build and evaluate RAG from first principles

**MultiHopRAG benchmark + OrbitDesk safety pack · Google Colab edition**

Today we keep the corpus, questions, top-k, access role, and evaluation harness fixed. We change chunking and retrieval architecture, then explain the metric movement.

```text
same questions + same corpus
        ↓
different chunking
        ↓
different RAG architecture
        ↓
same evaluation harness
        ↓
compare metrics
```

Retrieval, evaluation, safety checks, charts, and tests work without an API key. The two generation cells are optional and use Nscale only when Colab Secrets are configured.
"""
    ),
    markdown(
        """## Pair agreement

- **Driver:** runs or edits the cell and narrates the change.
- **Navigator:** predicts the result, checks evidence and metrics, and records the finding.
- Swap at each numbered checkpoint.

Do not run all cells silently. Predict first, run second, explain third.
"""
    ),
    code(
        """# Colab setup: about 2–4 minutes on a fresh runtime.
%pip install -q "sentence-transformers==5.7.0" "pytest==9.1.1" "openai>=2,<3"
"""
    ),
    code(embedded_assets_cell()),
    markdown(
        """## Checkpoint 0 — prove the environment and shared code work

These are fast offline tests. A failure is useful evidence: read the failing test name before changing anything.
"""
    ),
    code(
        """!python -m pytest -q -s
"""
    ),
    code(
        """import importlib
import platform

import matplotlib.pyplot as plt
import pandas as pd

import rag_workshop
importlib.reload(rag_workshop)
from rag_workshop import *

documents = load_documents("data/corpus.json")  # small synthetic safety/first-principles pack
cases = load_eval_cases("data/eval_cases.json")
benchmark_documents = load_documents("data/multihop_corpus.json")
benchmark_cases = load_eval_cases("data/multihop_eval_cases.json")

print("Python:", platform.python_version())
print("OrbitDesk safety documents/cases:", len(documents), len(cases))
print("MultiHopRAG benchmark documents/cases:", len(benchmark_documents), len(benchmark_cases))
assert len(documents) == 9 and len(cases) == 12
assert len(benchmark_documents) == 30 and len(benchmark_cases) == 12
"""
    ),
    markdown(
        """## Optional live model connection

In Colab, add `NSCALE_SERVICE_TOKEN` and the instructor-verified `NSCALE_MODEL_ID` under the key icon (**Secrets**). Never paste a token into a notebook cell. The retrieval lesson does not depend on this connection.
"""
    ),
    code(
        """import os

LIVE_LLM_AVAILABLE = False
live_llm = None

try:
    from google.colab import userdata
    service_token = userdata.get("NSCALE_SERVICE_TOKEN")
    model_id = userdata.get("NSCALE_MODEL_ID")
except Exception:
    service_token = os.getenv("NSCALE_SERVICE_TOKEN")
    model_id = os.getenv("NSCALE_MODEL_ID")

if service_token and model_id:
    from openai import OpenAI

    nscale_client = OpenAI(
        api_key=service_token,
        base_url="https://inference.api.nscale.com/v1",
        timeout=45.0,
        max_retries=2,
    )

    def live_llm(prompt: str) -> str:
        response = nscale_client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300,
        )
        return response.choices[0].message.content

    LIVE_LLM_AVAILABLE = True
    print("Live generation ready with model:", model_id)
else:
    print("No live secrets found. Continuing with the fully offline retrieval path.")
"""
    ),
    markdown(
        """## 1 — Establish the unsupported baseline

The question below concerns a fictional error code. Predict what a model might do without the private corpus. If live generation is unavailable, discuss the risk and continue; do not invent a result and label it as a model response.
"""
    ),
    code(
        """baseline_question = "What does OrbitDesk error OD-X31 mean, and what should I do first?"

if LIVE_LLM_AVAILABLE:
    baseline_answer = live_llm(
        "Answer this support question. If you do not know, say so.\\n\\n" + baseline_question
    )
    print(baseline_answer)
else:
    print("SKIPPED: add Colab Secrets to capture a real unsupported baseline.")

print("\\nRecord: Did the response cite approved OrbitDesk evidence? Could you verify it?")
"""
    ),
    markdown(
        """## 2 — Inspect the corpus before building an index

RAG quality starts with documents and metadata. Find the current and archived retention documents, then find which role can access the restricted incident.
"""
    ),
    code(
        """corpus_view = pd.DataFrame([
    {
        "doc_id": document.doc_id,
        "title": document.title,
        "version": document.version,
        "current": document.is_current,
        "roles": ", ".join(document.allowed_roles),
        "trust": document.trust,
        "characters": len(document.content),
    }
    for document in documents
])
display(corpus_view)
"""
    ),
    markdown(
        """## 3 — First success: fixed chunks + an offline vector index

TF-IDF is a lexical vector representation, not a neural semantic embedding. We use it first because it is fast, transparent, and needs no model download. The acceptance criterion is visible top-three evidence with metadata.
"""
    ),
    code(
        """fixed_chunks = fixed_size_chunks(documents, chunk_size=180, overlap=0)
fixed_vector = DenseRetriever(fixed_chunks, TfidfEncoder())

first_results = fixed_vector.search(baseline_question, k=3, role="student")
for result in first_results:
    print(f"rank={result.rank} score={result.score:.3f} {result.citation}")
    print(result.chunk.text[:420].replace("\\n", " "))
    print()
"""
    ),
    markdown(
        """### Diagnose the fixed-size boundary

Look for a chunk that starts or ends mid-sentence. Ask:

1. Did a heading stay with the rule it describes?
2. Is the citation section meaningful?
3. How much duplicated text did overlap create?
"""
    ),
    code(
        """for chunk in fixed_chunks[:8]:
    print(chunk.chunk_id, "|", chunk.section, "|", repr(chunk.text[:90]))
"""
    ),
    markdown(
        """## Checkpoint 1 — change only the chunking strategy

Keep the corpus, encoder, query, filters, and top-k unchanged. Predict which result will move before running the cell.
"""
    ),
    code(
        """structure_chunks = structure_aware_chunks(documents, max_chars=700)
structure_vector = DenseRetriever(structure_chunks, TfidfEncoder())

chunk_comparison = pd.DataFrame([
    {
        "strategy": "fixed",
        "chunks": len(fixed_chunks),
        "mean_chars": sum(map(lambda c: len(c.text), fixed_chunks)) / len(fixed_chunks),
        "meaningful_section_labels": sum(c.section != "unknown (fixed-size split)" for c in fixed_chunks),
    },
    {
        "strategy": "structure",
        "chunks": len(structure_chunks),
        "mean_chars": sum(map(lambda c: len(c.text), structure_chunks)) / len(structure_chunks),
        "meaningful_section_labels": sum(c.section != "unknown (fixed-size split)" for c in structure_chunks),
    },
])
display(chunk_comparison)

for result in structure_vector.search(baseline_question, k=3):
    print(f"rank={result.rank} score={result.score:.3f} {result.citation}")
    print(result.chunk.text[:420].replace("\\n", " "))
    print()
"""
    ),
    markdown(
        """## 4 — Use a neural sentence embedding

`all-MiniLM-L6-v2` maps queries and chunks to normalized vectors. If the download fails, the cell explicitly falls back to TF-IDF so the workshop continues. Record which encoder actually ran.
"""
    ),
    code(
        """try:
    semantic_encoder_factory = lambda: SentenceTransformerEncoder(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    # Build one small index now so download/model errors happen at this checkpoint.
    _health_retriever = DenseRetriever(structure_chunks, semantic_encoder_factory())
    encoder_label = "sentence-transformers/all-MiniLM-L6-v2"
except Exception as error:
    print("Embedding fallback activated:", type(error).__name__, str(error)[:180])
    semantic_encoder_factory = TfidfEncoder
    encoder_label = "TF-IDF FALLBACK"

print("Encoder used:", encoder_label)
"""
    ),
    markdown(
        """## 5 — Build four controlled MultiHopRAG experiments

The benchmark snapshot contains 12 attributed questions—three inference, three comparison, three temporal, and three null—with 18 evidence articles and 12 lexical hard negatives. From this point through Checkpoint 2, every experiment uses this same snapshot and the same top-5 evaluation.

- `fixed_vector`: weak chunking baseline
- `structure_vector`: isolates chunking
- `structure_hybrid`: adds BM25 and reciprocal rank fusion
- `parent_hybrid`: searches child sentences and returns parent sections
"""
    ),
    code(
        """benchmark_fixed_chunks = fixed_size_chunks(
    benchmark_documents, chunk_size=500, overlap=0
)
benchmark_structure_chunks = structure_aware_chunks(
    benchmark_documents, max_chars=700
)

fixed_vector = DenseRetriever(benchmark_fixed_chunks, semantic_encoder_factory())
structure_vector = DenseRetriever(benchmark_structure_chunks, semantic_encoder_factory())
structure_hybrid = HybridRetriever(benchmark_structure_chunks, semantic_encoder_factory())

child_chunks, parent_map = parent_child_chunks(benchmark_documents, parent_max_chars=900)
parent_hybrid = ParentRetriever(child_chunks, parent_map, semantic_encoder_factory())

# Keep a separate retriever for the later synthetic enterprise-safety exercises.
safety_hybrid = HybridRetriever(structure_chunks, semantic_encoder_factory())

experiments = {
    "fixed_vector": fixed_vector,
    "structure_vector": structure_vector,
    "structure_hybrid": structure_hybrid,
    "parent_hybrid": parent_hybrid,
}
print("Built:", ", ".join(experiments))
"""
    ),
    markdown(
        """### Inference versus temporal retrieval

Select one inference query and one temporal query. Predict whether all required evidence will fit in the top five, then inspect the first result and retrieval channel.
"""
    ),
    code(
        """probe_questions = {
    case.category: case.question
    for case in (benchmark_cases[0], benchmark_cases[6])
}

rows = []
for probe_name, question in probe_questions.items():
    for experiment_name, retriever in experiments.items():
        results = retriever.search(question, k=5)
        top = results[0]
        rows.append({
            "probe": probe_name,
            "experiment": experiment_name,
            "top_document": top.chunk.doc_id,
            "section": top.chunk.section,
            "channels": "+".join(top.channels),
            "top_5_documents": [result.chunk.doc_id for result in results],
        })
display(pd.DataFrame(rows))
"""
    ),
    markdown(
        """## Checkpoint 2 — run the same MultiHopRAG evaluation harness

We evaluate retrieval before generation. Hit@5, evidence recall, MRR, context precision, latency, and context size are computed by the same functions for every experiment. The three null queries test abstention.
"""
    ),
    code(
        """all_eval_rows = []
summary_rows = []

for experiment_name, retriever in experiments.items():
    experiment_rows = evaluate_retriever(
        experiment_name, retriever, benchmark_cases, k=5, role="student"
    )
    all_eval_rows.extend(experiment_rows)
    summary_rows.append({
        "experiment": experiment_name,
        **summarize_results(experiment_rows),
    })

summary = pd.DataFrame(summary_rows).set_index("experiment")
display(summary.round(3))
"""
    ),
    code(
        """quality_metrics = ["hit_at_k", "mrr", "context_precision", "no_answer_accuracy"]
summary[quality_metrics].plot(kind="bar", figsize=(11, 5), ylim=(0, 1.05))
plt.title("Quality metrics — same corpus, questions, top-k, filters, and scorer")
plt.ylabel("score")
plt.xticks(rotation=15)
plt.grid(axis="y", alpha=0.25)
plt.show()

summary[["mean_latency_ms", "mean_context_characters"]].plot(
    kind="bar", subplots=True, figsize=(11, 7), legend=False
)
plt.suptitle("Costs and trade-offs (latency varies by runtime)")
plt.tight_layout()
plt.show()
"""
    ),
    markdown(
        """### Failure clinic: averages hide the useful cases

Filter the table to find:

- a relevant document not retrieved
- a multi-document case with partial recall
- an unanswerable case the evidence gate would answer
- a configuration that retrieves more context without improving precision
"""
    ),
    code(
        """details = pd.DataFrame(results_as_dicts(all_eval_rows))
display(details[[
    "experiment", "case_id", "category", "hit_at_k", "recall_at_k",
    "reciprocal_rank", "context_precision", "predicted_answerable",
    "correct_no_answer", "context_characters", "retrieved_doc_ids"
]].sort_values(["case_id", "experiment"]))
"""
    ),
    markdown(
        """## 6 — Build a grounded answer path

`GroundedAssistant` applies an ambiguity check and evidence gate, builds citations, labels source blocks as data, and optionally calls the configured model. First run it without generation so the retrieval decision remains visible.
"""
    ),
    code(
        """offline_assistant = GroundedAssistant(safety_hybrid)

for question in [
    "What does OD-X31 mean, and what should the user avoid doing first?",
    "What telephone number offers support on Sundays?",
    "How long is it retained?",
    "Is the Sync API down right now?",
]:
    response = offline_assistant.answer(question)
    print("QUESTION:", question)
    print("DECISION:", response.answer)
    print("abstained=", response.abstained, "tool=", response.routed_tool)
    print("citations=", response.citations)
    print()
"""
    ),
    markdown(
        """### Optional grounded generation

The same safe prompt displayed below is passed to Nscale only when secrets are available. Check every claim against the cited source; a citation-shaped string is not proof by itself.
"""
    ),
    code(
        """grounded_question = "What does OD-X31 mean, and what should the user avoid doing first?"

if LIVE_LLM_AVAILABLE:
    live_assistant = GroundedAssistant(safety_hybrid, llm=live_llm)
    grounded_response = live_assistant.answer(grounded_question)
    print(grounded_response.answer)
    print("Sources selected:", grounded_response.citations)
else:
    grounded_response = offline_assistant.answer(grounded_question)
    print("MODEL CALL SKIPPED. Inspect the grounded prompt instead:\\n")
    print(grounded_response.prompt)
"""
    ),
    markdown(
        """## 7 — Enterprise challenge: version, access, and document injection

Security controls must apply before source text enters the model context. Predict each result before running it.
"""
    ),
    code(
        """# Version control: the archived source appears only when current_only=False.
version_question = "Is backup retention 14, 30, or 90 days?"
current = safety_hybrid.search(version_question, k=5, current_only=True)
all_versions = safety_hybrid.search(version_question, k=5, current_only=False)

print("Current-only documents:", [result.chunk.doc_id for result in current])
print("All-version documents:", [result.chunk.doc_id for result in all_versions])

# Access control: student results must never contain the restricted incident.
secret_question = "What is Maya Rao's temporary recovery token?"
student_results = safety_hybrid.search(secret_question, k=5, role="student")
security_results = safety_hybrid.search(secret_question, k=3, role="security")

print("\\nStudent-role documents:", [result.chunk.doc_id for result in student_results])
print("Security-role top document:", security_results[0].chunk.doc_id)
assert "incident-8842" not in {result.chunk.doc_id for result in student_results}
"""
    ),
    code(
        """injection_question = "What are the reset steps in the community connector migration note?"
injection_response = offline_assistant.answer(injection_question)

print("Security events:", injection_response.security_events)
print("Suspicious instruction remains in final prompt:",
      "IGNORE ALL PREVIOUS INSTRUCTIONS" in injection_response.prompt)
print("\\nSanitized prompt:\\n")
print(injection_response.prompt)
"""
    ),
    markdown(
        """## Checkpoint 3 — student experiments

Choose one experiment. Change only the named variable, rerun all 12 cases, and record one improvement and one regression.

1. **Chunk size:** compare fixed sizes 300, 500, and 900 with the same overlap ratio.
2. **Top-k:** compare 3, 5, and 8. Watch Hit@k, evidence recall, context precision, and context characters.
3. **Filter regression:** evaluate with archived documents allowed, then add an explicit test that fails.
4. **Injection attack:** create a payload not matched by `INJECTION_PATTERNS`; describe a stronger defense.
5. **Golden-set growth:** add one answerable and one unanswerable case with human-verified labels.

Use a result record like this:

```text
Hypothesis:
Variable changed:
Everything held constant:
Metric improved:
Metric regressed:
Case inspected:
Decision:
```
"""
    ),
    code(
        """# STUDENT CELL — copy an existing experiment and change one variable.
# Example starting point:

student_chunks = fixed_size_chunks(benchmark_documents, chunk_size=300, overlap=30)
student_retriever = DenseRetriever(student_chunks, semantic_encoder_factory())
student_rows = evaluate_retriever(
    "student_experiment", student_retriever, benchmark_cases, k=5
)

display(pd.DataFrame([{
    "experiment": "student_experiment",
    **summarize_results(student_rows),
}]).round(3))
"""
    ),
    markdown(
        """## Exit ticket

Each partner must be able to answer:

1. Where did the answer’s evidence come from?
2. Which change moved a metric, and why do you think it moved?
3. Which case still fails?
4. What does the system refuse or route elsewhere?
5. Which control runs before generation?

Save the summary table and one failure row as Day 1 evidence.
"""
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"name": "day1_rag_workshop_colab.ipynb", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT} with {len(cells)} cells")
