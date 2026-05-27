"""Mock search backend over the candidate corpus.

The backend exposes a small, fixed set of tools the agent is allowed to call.
Each tool validates its arguments and returns plain data structures.
"""

from __future__ import annotations

from talentagent.corpus import CORPUS
from talentagent.models import Candidate


class SearchBackend:
    """In-memory search over a candidate corpus."""

    def __init__(self, corpus: tuple[Candidate, ...] = CORPUS) -> None:
        self._by_id = {c.id: c for c in corpus}
        self._corpus = corpus

    def search_candidates(self, query: str, limit: int = 10) -> list[Candidate]:
        """Return candidates whose text contains any query term."""
        if limit <= 0:
            raise ValueError("limit must be positive")
        terms = [t for t in query.lower().split() if t]
        if not terms:
            return list(self._corpus[:limit])
        scored: list[tuple[int, Candidate]] = []
        for cand in self._corpus:
            hay = cand.text.lower()
            hits = sum(1 for t in terms if t in hay)
            if hits:
                scored.append((hits, cand))
        scored.sort(key=lambda pair: (-pair[0], pair[1].id))
        return [c for _, c in scored[:limit]]

    def get_profile(self, candidate_id: str) -> Candidate:
        """Return a single candidate by id."""
        if candidate_id not in self._by_id:
            raise KeyError(candidate_id)
        return self._by_id[candidate_id]

    def filter_by_skill(self, skill: str) -> list[Candidate]:
        """Return candidates listing the given skill."""
        needle = skill.lower().strip()
        if not needle:
            raise ValueError("skill must be non-empty")
        return [c for c in self._corpus if needle in (s.lower() for s in c.skills)]
