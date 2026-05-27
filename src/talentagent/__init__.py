"""TalentAgent: goal-oriented candidate-to-role matching agent."""

from talentagent.agent import MatchAgent
from talentagent.models import Candidate, MatchReport, RankedMatch, Role

__all__ = ["Candidate", "MatchAgent", "MatchReport", "RankedMatch", "Role"]
