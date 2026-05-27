"""Ranking quality and explanation grounding for the differentiator.

A small labeled set pairs roles with the candidates that genuinely fit them.
The metric tests prove the right candidates surface on top, and the grounding
test proves every cited requirement is actually present in the candidate's
profile, so an explanation cannot reference a field the candidate lacks.
"""

from talentagent.agent import MatchAgent
from talentagent.metrics import ndcg_at_k, precision_at_k
from talentagent.models import Role

# Roles with their known best-fit candidates from the mock corpus. Relevance is
# judged on whether a candidate covers the role's required skills.
LABELED = [
    (
        Role(
            "Senior Python Backend Engineer",
            ("python", "postgres", "docker"),
            min_years=6,
            description="Builds and operates Python services with relational storage.",
        ),
        {"c008", "c001", "c003"},
    ),
    (
        Role(
            "Frontend Engineer",
            ("react", "typescript"),
            min_years=3,
            description="Develops React interfaces and component libraries.",
        ),
        {"c002", "c003"},
    ),
    (
        Role(
            "Platform Engineer",
            ("kubernetes", "docker", "terraform"),
            min_years=5,
            description="Operates container platforms and infrastructure as code.",
        ),
        {"c006", "c010"},
    ),
]


def _ranked_ids(role: Role, k: int) -> list[str]:
    report = MatchAgent().match(role, top_k=k)
    return [m.candidate.id for m in report.matches]


def test_precision_at_3_surfaces_best_fit():
    for role, relevant in LABELED:
        ranked = _ranked_ids(role, 3)
        assert precision_at_k(ranked, relevant, 3) >= 0.66


def test_ndcg_at_3_is_high():
    scores = []
    for role, relevant in LABELED:
        ranked = _ranked_ids(role, 5)
        scores.append(ndcg_at_k(ranked, relevant, 3))
    assert min(scores) >= 0.8
    assert sum(scores) / len(scores) >= 0.9


def test_top_result_explanation_is_grounded():
    # Every requirement cited in a top result must be a skill the candidate
    # actually lists, so explanations cannot hallucinate a match.
    for role, _ in LABELED:
        report = MatchAgent().match(role, top_k=3)
        for match in report.matches:
            cand_skills = {s.lower() for s in match.candidate.skills}
            for evidence in match.satisfied:
                assert evidence.requirement.lower() in cand_skills
                assert evidence.matched_skill.lower() in cand_skills
            # And missing requirements are genuinely absent.
            for missing in match.missing_requirements:
                assert missing.lower() not in cand_skills
