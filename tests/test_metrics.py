from talentagent.metrics import ndcg_at_k, precision_at_k


def test_precision_counts_relevant_in_top_k():
    ranked = ["a", "b", "c", "d"]
    assert precision_at_k(ranked, {"a", "c"}, 2) == 0.5
    assert precision_at_k(ranked, {"a", "b"}, 2) == 1.0


def test_ndcg_rewards_relevant_high_ranks():
    relevant = {"a", "b"}
    top_first = ndcg_at_k(["a", "b", "x"], relevant, 3)
    spread = ndcg_at_k(["x", "a", "b"], relevant, 3)
    assert top_first == 1.0
    assert spread < top_first


def test_ndcg_is_zero_with_no_relevant():
    assert ndcg_at_k(["x", "y"], {"a"}, 2) == 0.0
