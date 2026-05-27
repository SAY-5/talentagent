"""Decision table for the confidence-gated review step.

A strong, well-separated match returns confident. A weak or ambiguous query is
flagged for review. Lowering the thresholds shifts the confident/review
boundary, which the last cases pin down.
"""

import pytest

from talentagent.confidence import ReviewGate
from talentagent.models import (
    Candidate,
    RankedMatch,
    ScoreBreakdown,
)


def _match(cid: str, score: float) -> RankedMatch:
    cand = Candidate(cid, cid, "Engineer", ("python",), 5, "summary")
    breakdown = ScoreBreakdown(score, score, score)
    return RankedMatch(cand, score, breakdown, (), ())


def _set(*scores: float) -> list[RankedMatch]:
    return [_match(f"c{i}", s) for i, s in enumerate(scores)]


# (label, scores, expected needs_review) under the default gate.
DEFAULT_TABLE = [
    ("strong and separated", (0.90, 0.50), False),
    ("strong but tied", (0.90, 0.88), True),
    ("weak top score", (0.30, 0.10), True),
    ("empty result set", (), True),
]


@pytest.mark.parametrize("label,scores,expected", DEFAULT_TABLE)
def test_default_gate_decision_table(label, scores, expected):
    gate = ReviewGate()
    decision = gate.decide(_set(*scores))
    assert decision.needs_review is expected, label


def test_confidence_is_higher_for_clear_matches():
    gate = ReviewGate()
    clear = gate.decide(_set(0.90, 0.50)).confidence
    ambiguous = gate.decide(_set(0.90, 0.88)).confidence
    assert clear > ambiguous
    assert 0.0 <= ambiguous <= 1.0 and 0.0 <= clear <= 1.0


def test_lowering_threshold_shifts_the_boundary():
    # A query that the strict gate sends to review becomes confident once the
    # thresholds are relaxed, proving the boundary is threshold-driven.
    borderline = _set(0.40, 0.30)
    strict = ReviewGate(min_top_score=0.45, min_margin=0.08)
    relaxed = ReviewGate(min_top_score=0.35, min_margin=0.05)
    assert strict.decide(borderline).needs_review is True
    assert relaxed.decide(borderline).needs_review is False
