"""Core data types for roles, candidates, and ranked matches."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Candidate:
    """A candidate profile in the search corpus."""

    id: str
    name: str
    title: str
    skills: tuple[str, ...]
    years_experience: int
    summary: str

    @property
    def text(self) -> str:
        """Flat text used for embedding the profile."""
        return f"{self.title}. {self.summary} Skills: {', '.join(self.skills)}."


@dataclass(frozen=True)
class Role:
    """A role to match candidates against."""

    title: str
    required_skills: tuple[str, ...]
    min_years: int = 0
    description: str = ""

    @property
    def text(self) -> str:
        """Flat text used for embedding the role."""
        skills = ", ".join(self.required_skills)
        return f"{self.title}. {self.description} Requires: {skills}."


@dataclass(frozen=True)
class Evidence:
    """A single grounded reason a candidate satisfies the role."""

    requirement: str
    matched_skill: str


@dataclass(frozen=True)
class ScoreBreakdown:
    """How a match score was composed."""

    skill_coverage: float
    experience_fit: float
    semantic_similarity: float

    @property
    def total(self) -> float:
        return round(
            0.5 * self.skill_coverage
            + 0.2 * self.experience_fit
            + 0.3 * self.semantic_similarity,
            6,
        )


@dataclass(frozen=True)
class RankedMatch:
    """A candidate ranked against a role with a grounded explanation."""

    candidate: Candidate
    score: float
    breakdown: ScoreBreakdown
    satisfied: tuple[Evidence, ...]
    missing_requirements: tuple[str, ...]

    @property
    def explanation(self) -> str:
        """Human-readable explanation referencing only matched fields."""
        if self.satisfied:
            hits = "; ".join(
                f"{e.requirement} via {e.matched_skill}" for e in self.satisfied
            )
            base = f"Satisfies {len(self.satisfied)} requirement(s): {hits}."
        else:
            base = "Satisfies no listed requirements."
        if self.missing_requirements:
            base += f" Missing: {', '.join(self.missing_requirements)}."
        return base


@dataclass(frozen=True)
class MatchReport:
    """The full result set returned by the agent loop."""

    role: Role
    matches: tuple[RankedMatch, ...]
    needs_review: bool
    review_reason: str
    tool_log: tuple[str, ...] = field(default_factory=tuple)
