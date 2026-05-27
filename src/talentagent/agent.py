"""Goal-oriented matching agent.

Given a role, the agent runs a short loop: it gathers a candidate pool by
tool-calling the search backend (broad search plus a per-required-skill
filter), ranks the pool through the RAG-style embedding pipeline, and applies
the review gate. The tool log records every call for auditing.
"""

from __future__ import annotations

from talentagent.confidence import ReviewGate
from talentagent.models import Candidate, MatchReport, Role
from talentagent.providers import EmbeddingProvider, HashingEmbeddingProvider
from talentagent.ranking import rank_candidates
from talentagent.search import SearchBackend
from talentagent.tools import ToolRegistry


class MatchAgent:
    """Drives the matching goal from a role to a ranked, gated result set."""

    def __init__(
        self,
        backend: SearchBackend | None = None,
        provider: EmbeddingProvider | None = None,
        gate: ReviewGate | None = None,
    ) -> None:
        self._backend = backend or SearchBackend()
        self._tools = ToolRegistry(self._backend)
        self._provider = provider or HashingEmbeddingProvider()
        self._gate = gate or ReviewGate()

    def _gather(self, role: Role, log: list[str]) -> list[Candidate]:
        """Tool-call the backend to assemble a deduplicated candidate pool."""
        pool: dict[str, Candidate] = {}

        query = f"{role.title} {' '.join(role.required_skills)}"
        log.append(f"search_candidates query={query!r}")
        for cand in self._tools.call("search_candidates", {"query": query, "limit": 20}):
            pool[cand.id] = cand

        for skill in role.required_skills:
            log.append(f"filter_by_skill skill={skill!r}")
            for cand in self._tools.call("filter_by_skill", {"skill": skill}):
                pool[cand.id] = cand

        # Confirm each candidate via get_profile, exercising the third tool.
        confirmed: dict[str, Candidate] = {}
        for cid in sorted(pool):
            log.append(f"get_profile candidate_id={cid!r}")
            confirmed[cid] = self._tools.call("get_profile", {"candidate_id": cid})
        return list(confirmed.values())

    def match(self, role: Role, top_k: int = 5) -> MatchReport:
        """Run the matching loop and return a gated, explained report."""
        log: list[str] = []
        pool = self._gather(role, log)
        matches = rank_candidates(role, pool, self._provider, top_k=top_k)
        needs_review, reason = self._gate.assess(matches)
        return MatchReport(
            role=role,
            matches=tuple(matches),
            needs_review=needs_review,
            review_reason=reason,
            tool_log=tuple(log),
        )
