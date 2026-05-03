from query_builder import rank_terms_for_query, combine_query_chunks, build_web_queries


def test_rank_terms_prioritizes_multiword():
    terms = ["diet", "healthy diet", "obesity", "meta analysis", "a"]
    ranked = rank_terms_for_query(terms, max_terms=3)
    assert "healthy diet" in ranked


def test_combine_chunks_no_duplicates():
    q = combine_query_chunks([["alpha", "beta"], ["alpha", "gamma"]], max_terms=5)
    toks = q.split()
    assert toks.count("alpha") == 1


def test_build_web_queries_has_expected_variants():
    bank = {
        "lifestyle_terms": ["lifestyle medicine"],
        "pattern_terms": ["mediterranean diet"],
        "clinical_terms": ["obesity"],
        "condition_terms": ["obesity"],
        "outcome_terms": ["weight loss"],
        "document_type_terms": ["guideline"],
        "implementation_terms": ["implementation"],
        "web_query_hints": ["framework"],
        "nutrition_terms": ["nutrition"],
    }
    queries = build_web_queries(bank)
    assert "systematic_evidence" in queries
    assert "policy_global" in queries
