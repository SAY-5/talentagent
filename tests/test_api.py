from fastapi.testclient import TestClient

from talentagent.api import create_app


def test_health():
    client = TestClient(create_app())
    assert client.get("/health").json() == {"status": "ok"}


def test_match_endpoint_returns_explanations():
    client = TestClient(create_app())
    resp = client.post(
        "/match",
        json={
            "title": "Backend Engineer",
            "required_skills": ["python", "postgres"],
            "min_years": 5,
            "top_k": 3,
        },
    )
    body = resp.json()
    assert resp.status_code == 200
    assert len(body["matches"]) == 3
    assert "explanation" in body["matches"][0]
    assert "needs_review" in body
    assert 0.0 <= body["confidence"] <= 1.0
