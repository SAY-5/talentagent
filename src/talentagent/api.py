"""HTTP API exposing the matching agent to the web interface."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from talentagent.agent import MatchAgent
from talentagent.models import MatchReport, Role


class RoleRequest(BaseModel):
    title: str
    required_skills: list[str]
    min_years: int = 0
    description: str = ""
    top_k: int = 5


def _serialize(report: MatchReport) -> dict[str, object]:
    return {
        "role": {
            "title": report.role.title,
            "required_skills": list(report.role.required_skills),
            "min_years": report.role.min_years,
        },
        "needs_review": report.needs_review,
        "review_reason": report.review_reason,
        "confidence": report.confidence,
        "matches": [
            {
                "id": m.candidate.id,
                "name": m.candidate.name,
                "title": m.candidate.title,
                "score": m.score,
                "breakdown": {
                    "skill_coverage": m.breakdown.skill_coverage,
                    "experience_fit": m.breakdown.experience_fit,
                    "semantic_similarity": m.breakdown.semantic_similarity,
                },
                "satisfied": [
                    {"requirement": e.requirement, "matched_skill": e.matched_skill}
                    for e in m.satisfied
                ],
                "missing_requirements": list(m.missing_requirements),
                "explanation": m.explanation,
            }
            for m in report.matches
        ],
    }


def create_app() -> FastAPI:
    app = FastAPI(title="TalentAgent", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    agent = MatchAgent()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/match")
    def match(req: RoleRequest) -> dict[str, object]:
        role = Role(
            title=req.title,
            required_skills=tuple(req.required_skills),
            min_years=req.min_years,
            description=req.description,
        )
        return _serialize(agent.match(role, top_k=req.top_k))

    return app


app = create_app()
