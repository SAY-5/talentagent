from talentagent.corpus import CORPUS
from talentagent.models import Role
from talentagent.providers import HashingEmbeddingProvider
from talentagent.ranking import rank_candidates, score_candidate


def test_score_breakdown_components_in_range():
    role = Role("Backend Engineer", ("python", "postgres"), min_years=5)
    cand = next(c for c in CORPUS if c.id == "c001")
    match = score_candidate(role, cand, HashingEmbeddingProvider())
    assert 0.0 <= match.breakdown.skill_coverage <= 1.0
    assert 0.0 <= match.breakdown.experience_fit <= 1.0
    assert 0.0 <= match.breakdown.semantic_similarity <= 1.0
    assert 0.0 <= match.score <= 1.0


def test_ranking_is_sorted_descending():
    role = Role("Python Engineer", ("python", "docker"))
    matches = rank_candidates(role, list(CORPUS), HashingEmbeddingProvider())
    scores = [m.score for m in matches]
    assert scores == sorted(scores, reverse=True)
