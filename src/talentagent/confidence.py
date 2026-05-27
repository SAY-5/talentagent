"""Confidence assessment and the human-review gate.

A clear top match auto-returns. A weak or ambiguous result set is flagged for
human review instead of asserting a confident match.
"""

from __future__ import annotations

from dataclasses import dataclass

from talentagent.models import RankedMatch


@dataclass(frozen=True)
class ReviewGate:
    """Decides whether a ranked result set needs human review.

    Two signals drive the gate:
      - the top score must clear `min_top_score` (low signal otherwise), and
      - the top two scores must differ by at least `min_margin` (ambiguous
        otherwise).
    Lowering `min_top_score` or `min_margin` shifts the confident/review
    boundary.
    """

    min_top_score: float = 0.45
    min_margin: float = 0.08

    def assess(self, matches: list[RankedMatch]) -> tuple[bool, str]:
        """Return (needs_review, reason)."""
        if not matches:
            return True, "no candidates matched the role"
        top = matches[0]
        if top.score < self.min_top_score:
            return True, (
                f"top score {top.score:.3f} below threshold {self.min_top_score:.3f}"
            )
        if len(matches) >= 2:
            margin = top.score - matches[1].score
            if margin < self.min_margin:
                return True, (
                    f"top two scores within {margin:.3f}, below margin "
                    f"{self.min_margin:.3f}"
                )
        return False, "clear top match"
