from talentagent.agent import MatchAgent
from talentagent.models import Role


def test_agent_returns_ranked_report():
    agent = MatchAgent()
    role = Role("Full Stack Engineer", ("python", "react", "typescript"), min_years=4)
    report = agent.match(role, top_k=3)
    assert len(report.matches) == 3
    assert report.matches[0].score >= report.matches[-1].score


def test_agent_logs_all_three_tools():
    agent = MatchAgent()
    role = Role("Backend Engineer", ("python", "postgres"))
    report = agent.match(role)
    kinds = {entry.split()[0] for entry in report.tool_log}
    assert kinds == {"search_candidates", "filter_by_skill", "get_profile"}


def test_top_match_explanation_lists_satisfied_requirements():
    agent = MatchAgent()
    role = Role("Backend Engineer", ("python", "postgres", "docker"), min_years=5)
    report = agent.match(role)
    top = report.matches[0]
    assert top.satisfied
    assert "Satisfies" in top.explanation
