"""Fast, offline tests for the exact code used in the Colab notebook."""

from pathlib import Path

import pytest

from rag_workshop import (
    DenseRetriever,
    GroundedAssistant,
    HybridRetriever,
    TfidfEncoder,
    evaluate_retriever,
    fixed_size_chunks,
    load_documents,
    load_eval_cases,
    parent_child_chunks,
    structure_aware_chunks,
    summarize_results,
)


DATA = Path(__file__).parent / "data"


@pytest.fixture(scope="module")
def documents():
    return load_documents(DATA / "corpus.json")


@pytest.fixture(scope="module")
def cases():
    return load_eval_cases(DATA / "eval_cases.json")


@pytest.fixture(scope="module")
def benchmark_documents():
    return load_documents(DATA / "multihop_corpus.json")


@pytest.fixture(scope="module")
def benchmark_cases():
    return load_eval_cases(DATA / "multihop_eval_cases.json")


@pytest.fixture(scope="module")
def structure_chunks(documents):
    return structure_aware_chunks(documents)


@pytest.fixture(scope="module")
def hybrid(structure_chunks):
    return HybridRetriever(structure_chunks, TfidfEncoder())


def test_workshop_assets_have_expected_size(documents, cases):
    assert len(documents) == 9
    assert len(cases) == 12
    assert len({case.case_id for case in cases}) == 12


def test_multihop_subset_is_balanced_and_self_contained(
    benchmark_documents, benchmark_cases
):
    assert len(benchmark_documents) == 30
    assert len(benchmark_cases) == 12
    counts = {
        category: sum(case.category == category for case in benchmark_cases)
        for category in {case.category for case in benchmark_cases}
    }
    assert counts == {
        "comparison_query": 3,
        "inference_query": 3,
        "null_query": 3,
        "temporal_query": 3,
    }
    available_ids = {document.doc_id for document in benchmark_documents}
    for case in benchmark_cases:
        assert set(case.relevant_doc_ids) <= available_ids
        assert case.reference_answer
        if case.answerable:
            assert 2 <= len(case.relevant_doc_ids) <= 3
            assert len(case.evidence_markers) == len(case.relevant_doc_ids)
        else:
            assert case.relevant_doc_ids == ()
            assert case.evidence_markers == ()


def test_fixed_chunking_can_cut_a_semantic_boundary(documents):
    chunks = fixed_size_chunks(documents, chunk_size=180, overlap=30)
    assert len(chunks) > len(documents)
    assert all(chunk.section == "unknown (fixed-size split)" for chunk in chunks)
    assert any(not chunk.text.endswith((".", "!", "?", "#")) for chunk in chunks)


def test_structure_chunking_keeps_titles_and_metadata(structure_chunks):
    rate_limit = [
        chunk
        for chunk in structure_chunks
        if chunk.doc_id == "api-guide" and chunk.section == "Rate limits and OD-429"
    ]
    assert len(rate_limit) == 1
    assert "120 Sync API requests per minute" in rate_limit[0].text
    assert rate_limit[0].metadata["is_current"] is True
    assert "student" in rate_limit[0].metadata["allowed_roles"]


def test_invalid_fixed_chunk_parameters_are_rejected(documents):
    with pytest.raises(ValueError, match="chunk_size"):
        fixed_size_chunks(documents, chunk_size=100, overlap=100)


def test_access_control_filters_before_returning_context(hybrid):
    results = hybrid.search("Maya Rao temporary recovery token", k=5, role="student")
    assert "incident-8842" not in {result.chunk.doc_id for result in results}

    security_results = hybrid.search(
        "Maya Rao temporary recovery token", k=3, role="security"
    )
    assert security_results[0].chunk.doc_id == "incident-8842"


def test_current_only_filter_excludes_archived_policy(hybrid):
    current_results = hybrid.search("backup retention 14 days", k=5, role="student")
    assert "retention-archived" not in {result.chunk.doc_id for result in current_results}

    all_versions = hybrid.search(
        "backup retention 14 days", k=5, role="student", current_only=False
    )
    assert "retention-archived" in {result.chunk.doc_id for result in all_versions}


def test_hybrid_retrieval_finds_exact_identifier(hybrid):
    results = hybrid.search("What does OD-X31 mean?", k=3)
    assert results[0].chunk.doc_id == "product-guide"
    assert "bm25" in results[0].channels


def test_parent_retriever_returns_parent_context(documents):
    children, parents = parent_child_chunks(documents)
    from rag_workshop import ParentRetriever

    retriever = ParentRetriever(children, parents, TfidfEncoder())
    result = retriever.search("OD-A17 audience value", k=1)[0]
    assert result.chunk.doc_id == "auth-runbook"
    assert "First compare the audience" in result.chunk.text
    assert result.channels[0] == "parent"


def test_grounded_assistant_abstains_on_missing_and_ambiguous_questions(hybrid):
    assistant = GroundedAssistant(hybrid)
    missing = assistant.answer("What telephone number offers support on Sundays?")
    ambiguous = assistant.answer("How long is it retained?")
    assert missing.abstained is True
    assert "Insufficient evidence" in missing.answer
    assert ambiguous.abstained is True
    assert "clarification" in ambiguous.answer


def test_grounded_assistant_routes_live_state_to_tool(hybrid):
    response = GroundedAssistant(hybrid).answer("Is the Sync API down right now?")
    assert response.abstained is True
    assert response.routed_tool == "get_service_status"


def test_untrusted_injection_is_removed_before_prompt(hybrid):
    response = GroundedAssistant(hybrid).answer(
        "What are the reset steps in the community connector migration note?"
    )
    assert response.abstained is False
    assert "removed_prompt_injection_like_paragraph" in response.security_events
    assert "IGNORE ALL PREVIOUS INSTRUCTIONS" not in response.prompt
    assert "disable the connector" in response.prompt


def test_evaluation_harness_uses_all_cases_without_leakage(hybrid, cases):
    rows = evaluate_retriever("structure_hybrid", hybrid, cases, k=3)
    summary = summarize_results(rows)
    assert len(rows) == len(cases)
    assert summary["cases"] == 12
    assert summary["forbidden_leakage_rate"] == 0
    assert summary["archived_retrieval_rate"] == 0


def test_dense_and_hybrid_share_the_search_contract(structure_chunks):
    dense = DenseRetriever(structure_chunks, TfidfEncoder())
    hybrid = HybridRetriever(structure_chunks, TfidfEncoder())
    for retriever in (dense, hybrid):
        results = retriever.search("OD-429 Retry-After", k=3)
        assert len(results) == 3
        assert results[0].rank == 1
        assert results[0].chunk.doc_id == "api-guide"
