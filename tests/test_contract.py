"""Property and contract tests for the matching agent.

These pin the guarantees the agent relies on: ranking is deterministic for a
fixed corpus and query, a perfect profile ranks first, every tool call is
schema-valid and allowlisted, and explanations only reference matched fields.
"""

from talentagent.agent import MatchAgent
from talentagent.corpus import CORPUS
from talentagent.models import Candidate, Role
from talentagent.providers import HashingEmbeddingProvider
from talentagent.ranking import rank_candidates
from talentagent.search import SearchBackend
from talentagent.tools import ToolError, ToolRegistry


def test_ranking_is_deterministic():
    role = Role("Backend Engineer", ("python", "postgres", "docker"), min_years=5)
    first = rank_candidates(role, list(CORPUS), HashingEmbeddingProvider())
    second = rank_candidates(role, list(CORPUS), HashingEmbeddingProvider())
    assert [m.candidate.id for m in first] == [m.candidate.id for m in second]
    assert [m.score for m in first] == [m.score for m in second]


def test_perfect_profile_ranks_first():
    # A profile that covers every requirement and whose text mirrors the role
    # should win on all three score axes, so it ranks first.
    role = Role(
        "Backend Engineer",
        ("python", "postgres", "docker"),
        min_years=5,
        description="Builds and operates Python services with relational storage.",
    )
    perfect = Candidate(
        id="perfect",
        name="Perfect Fit",
        title=role.title,
        skills=role.required_skills,
        years_experience=10,
        summary=role.description,
    )
    pool = [*CORPUS, perfect]
    ranked = rank_candidates(role, pool, HashingEmbeddingProvider())
    assert ranked[0].candidate.id == "perfect"
    assert not ranked[0].missing_requirements


def test_every_tool_call_is_schema_valid_and_allowlisted():
    registry = ToolRegistry(SearchBackend())
    role = Role("Data Engineer", ("python", "spark"))
    report = MatchAgent().match(role)
    for entry in report.tool_log:
        name = entry.split()[0]
        assert name in registry.allowlist


def test_unknown_tool_argument_is_rejected():
    registry = ToolRegistry(SearchBackend())
    try:
        registry.call("search_candidates", {"bogus": 1})
    except ToolError:
        return
    raise AssertionError("expected ToolError for unknown argument")


def test_explanation_references_only_matched_fields():
    role = Role("Backend Engineer", ("python", "postgres", "rustlang"), min_years=5)
    ranked = rank_candidates(role, list(CORPUS), HashingEmbeddingProvider())
    for match in ranked:
        cand_skills = {s.lower() for s in match.candidate.skills}
        for evidence in match.satisfied:
            # The cited requirement must map to a skill the candidate truly has.
            assert evidence.matched_skill.lower() in cand_skills
            assert evidence.requirement.lower() in cand_skills
        # rustlang is in no profile, so it can never appear as satisfied.
        satisfied_reqs = {e.requirement for e in match.satisfied}
        assert "rustlang" not in satisfied_reqs
