"""Create the deterministic Day 1 subset of yixuantt/MultiHopRAG.

The script downloads the two upstream JSON files, selects three examples from
each question type, adds one lexical hard-negative article per question, and
writes the workshop's Document/EvalCase JSON schema. The generated snapshot is
committed so the Colab lesson does not depend on a live Hugging Face download.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parent
DATA = ROOT / "student_code" / "data"
BASE_URL = "https://huggingface.co/datasets/yixuantt/MultiHopRAG/resolve/main"

# Three deliberately readable examples from each published question type.
SELECTED_QUERY_INDICES = (68, 187, 9, 27, 35, 37, 12, 34, 146, 18, 38, 128)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "both", "by", "did", "do",
    "does", "for", "from", "has", "have", "in", "is", "it", "of", "on", "or",
    "that", "the", "their", "to", "was", "were", "what", "which", "while", "with",
}


def download_json(filename: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        f"{BASE_URL}/{filename}", headers={"User-Agent": "ai-workshop-subset-builder/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS and len(token) > 2
    }


def doc_id(article: dict[str, Any]) -> str:
    digest = hashlib.sha1(article["url"].encode("utf-8")).hexdigest()[:12]
    return f"mhr-{digest}"


def select_hard_negative(
    query: dict[str, Any], corpus: list[dict[str, Any]], excluded_urls: set[str]
) -> dict[str, Any]:
    query_tokens = tokens(query["query"])

    def score(article: dict[str, Any]) -> tuple[float, str]:
        article_tokens = tokens(f"{article['title']} {article['body']}")
        overlap = len(query_tokens & article_tokens) / max(len(query_tokens), 1)
        return overlap, article["url"]

    candidates = [article for article in corpus if article["url"] not in excluded_urls]
    return max(candidates, key=score)


def as_document(article: dict[str, Any]) -> dict[str, Any]:
    author = article.get("author") or "Unknown author"
    content = (
        f"# {article['title']}\n\n"
        "## Article metadata\n"
        f"Source: {article['source']}\n"
        f"Author: {author}\n"
        f"Published: {article['published_at']}\n"
        f"Category: {article['category']}\n"
        f"Original URL: {article['url']}\n\n"
        f"## Article body\n{article['body'].strip()}"
    )
    return {
        "doc_id": doc_id(article),
        "title": article["title"],
        "version": "MultiHopRAG-snapshot",
        "effective_date": article["published_at"],
        "is_current": True,
        "allowed_roles": ["student", "support", "security"],
        "trust": "external-attributed",
        "content": content,
    }


def main() -> None:
    questions = download_json("MultiHopRAG.json")
    corpus = download_json("corpus.json")
    corpus_by_url = {article["url"]: article for article in corpus}
    selected_questions = [questions[index] for index in SELECTED_QUERY_INDICES]

    evidence_urls = {
        evidence["url"]
        for question in selected_questions
        for evidence in question["evidence_list"]
    }
    missing = evidence_urls - corpus_by_url.keys()
    if missing:
        raise ValueError(f"Evidence URLs missing from corpus: {sorted(missing)}")

    hard_negatives: dict[int, dict[str, Any]] = {}
    excluded = set(evidence_urls)
    for source_index, question in zip(SELECTED_QUERY_INDICES, selected_questions):
        article = select_hard_negative(question, corpus, excluded)
        hard_negatives[source_index] = article
        excluded.add(article["url"])

    subset_urls = evidence_urls | {article["url"] for article in hard_negatives.values()}
    subset_articles = sorted(
        (corpus_by_url.get(url) or next(a for a in hard_negatives.values() if a["url"] == url)
         for url in subset_urls),
        key=lambda article: article["url"],
    )

    eval_cases = []
    for source_index, question in zip(SELECTED_QUERY_INDICES, selected_questions):
        evidence = question["evidence_list"]
        answerable = bool(evidence)
        eval_cases.append(
            {
                "case_id": f"multihop-{source_index}-{question['question_type']}",
                "category": question["question_type"],
                "question": question["query"],
                "relevant_doc_ids": [doc_id(corpus_by_url[item["url"]]) for item in evidence],
                "evidence_markers": [item["fact"] for item in evidence],
                "answerable": answerable,
                "reference_answer": question["answer"],
                "expected_behavior": (
                    f"Retrieve evidence across {len(evidence)} documents, then answer: "
                    f"{question['answer']}"
                    if answerable
                    else "Return insufficient information because the dataset supplies no evidence."
                ),
            }
        )

    manifest = {
        "dataset": "yixuantt/MultiHopRAG",
        "dataset_url": "https://huggingface.co/datasets/yixuantt/MultiHopRAG",
        "repository_url": "https://github.com/yixuantt/MultiHop-RAG",
        "license": "ODC-BY",
        "selected_query_indices": list(SELECTED_QUERY_INDICES),
        "question_type_counts": {
            question_type: sum(q["question_type"] == question_type for q in selected_questions)
            for question_type in sorted({q["question_type"] for q in selected_questions})
        },
        "evidence_article_count": len(evidence_urls),
        "hard_negative_article_count": len(hard_negatives),
        "total_article_count": len(subset_articles),
        "hard_negative_urls_by_query_index": {
            str(index): article["url"] for index, article in hard_negatives.items()
        },
    }

    DATA.mkdir(parents=True, exist_ok=True)
    outputs = {
        "multihop_corpus.json": [as_document(article) for article in subset_articles],
        "multihop_eval_cases.json": eval_cases,
        "multihop_subset_manifest.json": manifest,
    }
    for filename, value in outputs.items():
        path = DATA / filename
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {path} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
