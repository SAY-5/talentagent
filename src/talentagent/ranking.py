"""Ranking of candidates against a role with grounded explanations."""

from __future__ import annotations

from talentagent.models import (
    Candidate,
    Evidence,
    RankedMatch,
    Role,
    ScoreBreakdown,
)
from talentagent.providers import EmbeddingProvider, cosine_similarity


def _skill_evidence(role: Role, candidate: Candidate) -> tuple[
    tuple[Evidence, ...], tuple[str, ...]
]:
    """Match each required skill to a real candidate skill.

    Evidence is only created from skills the candidate actually lists, so an
    explanation can never reference a requirement the candidate does not meet.
    """
    cand_skills = {s.lower(): s for s in candidate.skills}
    satisfied: list[Evidence] = []
    missing: list[str] = []
    for req in role.required_skills:
        key = req.lower()
        if key in cand_skills:
            satisfied.append(Evidence(requirement=req, matched_skill=cand_skills[key]))
        else:
            missing.append(req)
    return tuple(satisfied), tuple(missing)


def score_candidate(
    role: Role, candidate: Candidate, provider: EmbeddingProvider
) -> RankedMatch:
    """Score a single candidate against a role."""
    satisfied, missing = _skill_evidence(role, candidate)
    total_reqs = len(role.required_skills) or 1
    skill_coverage = len(satisfied) / total_reqs

    if role.min_years <= 0:
        experience_fit = 1.0
    else:
        experience_fit = min(1.0, candidate.years_experience / role.min_years)

    semantic = cosine_similarity(
        provider.embed(role.text), provider.embed(candidate.text)
    )
    breakdown = ScoreBreakdown(
        skill_coverage=round(skill_coverage, 6),
        experience_fit=round(experience_fit, 6),
        semantic_similarity=round(semantic, 6),
    )
    return RankedMatch(
        candidate=candidate,
        score=breakdown.total,
        breakdown=breakdown,
        satisfied=satisfied,
        missing_requirements=missing,
    )


def rank_candidates(
    role: Role,
    candidates: list[Candidate],
    provider: EmbeddingProvider,
    top_k: int | None = None,
) -> list[RankedMatch]:
    """Rank candidates by score, descending, with a stable tie break on id."""
    matches = [score_candidate(role, c, provider) for c in candidates]
    matches.sort(key=lambda m: (-m.score, m.candidate.id))
    if top_k is not None:
        matches = matches[:top_k]
    return matches
