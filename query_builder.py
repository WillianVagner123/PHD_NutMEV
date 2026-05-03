from __future__ import annotations

import re
from typing import Dict, List


def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\x00", " ").replace("�", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def compact_free_text_query(query: str, max_terms: int = 14) -> str:
    terms = re.findall(r'[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9\-]+', query or '')
    stop = {
        'and','or','the','of','for','with','in','on','to','a','an',
        'e','ou','de','da','do','das','dos','para','com','em','na','no','nas','nos'
    }
    cleaned = []
    seen = set()
    for term in terms:
        low = term.lower()
        if len(low) < 3 or low in stop:
            continue
        if low not in seen:
            cleaned.append(term)
            seen.add(low)
    return " ".join(cleaned[:max_terms])


def rank_terms_for_query(terms: List[str], max_terms: int, prefer_multiword: bool = True) -> List[str]:
    uniq = []
    seen = set()
    for t in terms:
        t2 = normalize_whitespace(t)
        low = t2.lower()
        if t2 and low not in seen:
            uniq.append(t2)
            seen.add(low)

    def term_score(term: str) -> float:
        words = len(term.split())
        length = len(term)
        multi_bonus = 2.0 if prefer_multiword and words > 1 else 0.0
        len_bonus = 1.0 if 8 <= length <= 42 else 0.0
        ascii_penalty = -0.1 if re.fullmatch(r"[A-Za-z]{1,3}", term) else 0.0
        return multi_bonus + len_bonus + ascii_penalty + min(words, 6) * 0.25

    ranked = sorted(uniq, key=term_score, reverse=True)
    return ranked[:max_terms]


def combine_query_chunks(chunks: List[List[str]], max_terms: int = 16) -> str:
    pools = [list(c) for c in chunks if c]
    out: List[str] = []
    seen = set()
    idx = 0
    while pools and len(out) < max_terms:
        pool = pools[idx % len(pools)]
        if not pool:
            pools.pop(idx % len(pools))
            if not pools:
                break
            continue
        term = pool.pop(0)
        low = term.lower()
        if low not in seen:
            out.append(term)
            seen.add(low)
        idx += 1
    return compact_free_text_query(" ".join(out), max_terms=max_terms)


def build_web_queries(bank: Dict[str, List[str]]) -> Dict[str, str]:
    lifestyle = rank_terms_for_query(bank.get("lifestyle_terms", []), 10)
    patterns = rank_terms_for_query(bank.get("pattern_terms", []), 10)
    clinical = rank_terms_for_query(bank.get("clinical_terms", []) or bank.get("condition_terms", []), 10)
    outcomes = rank_terms_for_query(bank.get("outcome_terms", []), 10)
    docs = rank_terms_for_query(bank.get("document_type_terms", []), 10)
    impl = rank_terms_for_query(bank.get("implementation_terms", []), 12)
    hints = rank_terms_for_query(bank.get("web_query_hints", []), 8)
    nutrition = rank_terms_for_query(bank.get("nutrition_terms", []), 10)

    core = lifestyle + patterns + clinical + impl + docs + hints
    pt_terms = [t for t in core if any(ch in t for ch in "çãõáéíóúâêôà")]
    en_terms = [t for t in core if t not in pt_terms]

    q_balanced_en = combine_query_chunks([en_terms, clinical, docs, hints], max_terms=14)
    q_balanced_pt = combine_query_chunks([pt_terms or bank.get("condition_terms", []), docs, hints], max_terms=14)
    q_implementation = combine_query_chunks([impl, outcomes, patterns, docs], max_terms=14)
    q_guidelines = combine_query_chunks([clinical, docs, hints, patterns], max_terms=14)
    q_framework = combine_query_chunks([lifestyle, impl, nutrition], max_terms=14)
    q_systematic = combine_query_chunks([patterns, clinical, outcomes, ["systematic review", "meta-analysis"]], max_terms=14)
    q_policy_global = combine_query_chunks([hints, docs, ["guideline", "consensus", "framework", "policy"], clinical], max_terms=14)

    return {
        "balanced_en": compact_free_text_query(q_balanced_en, 12),
        "balanced_pt": compact_free_text_query(q_balanced_pt, 12),
        "implementation": compact_free_text_query(q_implementation, 12),
        "guidelines_docs": compact_free_text_query(q_guidelines, 12),
        "framework": compact_free_text_query(q_framework, 12),
        "systematic_evidence": compact_free_text_query(q_systematic, 12),
        "policy_global": compact_free_text_query(q_policy_global, 12),
    }
