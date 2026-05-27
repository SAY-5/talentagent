"""Confidence assessment and the human-review gate.

A clear top match auto-returns. A weak or ambiguous result set is flagged for
human review instead of asserting a confident match.
"""

from __future__ import annotations

from dataclasses import dataclass

from talentagent.models import RankedMatch


@dataclass(frozen=True)
class Decision:
    """The gate's verdict over a ranked set."""

    needs_review: bool
    reason: str
    confidence: float


@dataclass(frozen=True)
class ReviewGate:
    """Decides whether a ranked result set needs human review.

    Two signals drive the gate:
      - the top score must clear `min_top_score` (low signal otherwise), and
      - the top two scores must differ by at least `min_margin` (ambiguous
        otherwise).
    Lowering `min_top_score` or `min_margin` shifts the confident/review
    boundary.

    The confidence in [0, 1] is a calibrated blend of how far the top score
    clears its threshold and how cleanly it separates from the runner-up. It is
    reported even when the set is sent to review so a reviewer can rank queues.
    """

    min_top_score: float = 0.45
    min_margin: float = 0.08

    def confidence(self, matches: list[RankedMatch]) -> float:
        """Calibrated confidence over the ranked set, in [0, 1]."""
        if not matches:
            return 0.0
        top = matches[0].score
        score_signal = min(1.0, top / self.min_top_score) if self.min_top_score else 1.0
        if len(matches) >= 2:
            margin = top - matches[1].score
            margin_signal = min(1.0, margin / self.min_margin) if self.min_margin else 1.0
        else:
            margin_signal = 1.0
        return round(0.6 * score_signal + 0.4 * margin_signal, 6)

    def decide(self, matches: list[RankedMatch]) -> Decision:
        """Return the full decision including a calibrated confidence."""
        conf = self.confidence(matches)
        if not matches:
            return Decision(True, "no candidates matched the role", conf)
        top = matches[0]
        if top.score < self.min_top_score:
            return Decision(
                True,
                f"top score {top.score:.3f} below threshold {self.min_top_score:.3f}",
                conf,
            )
        if len(matches) >= 2:
            margin = top.score - matches[1].score
            if margin < self.min_margin:
                return Decision(
                    True,
                    f"top two scores within {margin:.3f}, below margin "
                    f"{self.min_margin:.3f}",
                    conf,
                )
        return Decision(False, "clear top match", conf)

    def assess(self, matches: list[RankedMatch]) -> tuple[bool, str]:
        """Backward-compatible (needs_review, reason) view of the decision."""
        decision = self.decide(matches)
        return decision.needs_review, decision.reason
