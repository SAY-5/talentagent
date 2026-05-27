"""Ranking quality metrics: precision@k and NDCG@k."""

from __future__ import annotations

import math


def precision_at_k(ranked_ids: list[str], relevant: set[str], k: int) -> float:
    """Fraction of the top k results that are relevant."""
    if k <= 0:
        raise ValueError("k must be positive")
    top = ranked_ids[:k]
    if not top:
        return 0.0
    hits = sum(1 for cid in top if cid in relevant)
    return hits / len(top)


def ndcg_at_k(ranked_ids: list[str], relevant: set[str], k: int) -> float:
    """Normalized discounted cumulative gain over the top k results.

    Relevance is binary: a candidate in `relevant` has gain 1, others 0.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    dcg = 0.0
    for i, cid in enumerate(ranked_ids[:k]):
        if cid in relevant:
            dcg += 1.0 / math.log2(i + 2)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    if idcg == 0.0:
        return 0.0
    return dcg / idcg
