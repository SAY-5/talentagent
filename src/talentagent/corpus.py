"""In-repo mock corpus of candidate profiles."""

from __future__ import annotations

from talentagent.models import Candidate

CORPUS: tuple[Candidate, ...] = (
    Candidate(
        id="c001",
        name="Ada Reyes",
        title="Senior Backend Engineer",
        skills=("python", "postgres", "docker", "kubernetes", "fastapi"),
        years_experience=8,
        summary="Builds and operates Python services with relational storage.",
    ),
    Candidate(
        id="c002",
        name="Bo Tran",
        title="Frontend Engineer",
        skills=("typescript", "react", "css", "vite"),
        years_experience=5,
        summary="Develops React interfaces and component libraries.",
    ),
    Candidate(
        id="c003",
        name="Cira Okoye",
        title="Full Stack Engineer",
        skills=("python", "react", "typescript", "postgres", "docker"),
        years_experience=6,
        summary="Ships full stack features across Python backends and React.",
    ),
    Candidate(
        id="c004",
        name="Dev Malik",
        title="Data Engineer",
        skills=("python", "spark", "airflow", "postgres"),
        years_experience=7,
        summary="Designs batch pipelines and warehouse models.",
    ),
    Candidate(
        id="c005",
        name="Esra Vance",
        title="Machine Learning Engineer",
        skills=("python", "pytorch", "numpy", "docker"),
        years_experience=4,
        summary="Trains and serves models for retrieval and ranking.",
    ),
    Candidate(
        id="c006",
        name="Finn Adler",
        title="Platform Engineer",
        skills=("go", "kubernetes", "terraform", "docker"),
        years_experience=9,
        summary="Operates container platforms and infrastructure as code.",
    ),
    Candidate(
        id="c007",
        name="Gaia Nilsson",
        title="Junior Frontend Engineer",
        skills=("javascript", "react", "html"),
        years_experience=2,
        summary="Builds web UIs and learns the React ecosystem.",
    ),
    Candidate(
        id="c008",
        name="Hari Bose",
        title="Senior Python Engineer",
        skills=("python", "django", "postgres", "redis", "docker"),
        years_experience=10,
        summary="Leads Python backend teams and database design.",
    ),
    Candidate(
        id="c009",
        name="Ivy Lund",
        title="Mobile Engineer",
        skills=("swift", "kotlin", "graphql"),
        years_experience=5,
        summary="Builds native mobile clients.",
    ),
    Candidate(
        id="c010",
        name="Jad Karam",
        title="DevOps Engineer",
        skills=("python", "kubernetes", "docker", "terraform", "aws"),
        years_experience=6,
        summary="Automates deploys and runs production Kubernetes.",
    ),
)
