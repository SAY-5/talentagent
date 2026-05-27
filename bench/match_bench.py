"""Benchmark the match path: rank a large candidate corpus against a role.

Generates a deterministic synthetic corpus, then times how long it takes to
score and rank every candidate. Prints a JSON line with the measured numbers
so the regression gate can parse it.
"""

from __future__ import annotations

import argparse
import json
import random
import time

from talentagent.models import Candidate, Role
from talentagent.providers import HashingEmbeddingProvider
from talentagent.ranking import rank_candidates

SKILL_POOL = (
    "python", "postgres", "docker", "kubernetes", "react", "typescript",
    "go", "rust", "spark", "airflow", "pytorch", "numpy", "redis", "django",
    "fastapi", "terraform", "aws", "graphql", "kotlin", "swift",
)
TITLES = (
    "Backend Engineer", "Frontend Engineer", "Full Stack Engineer",
    "Data Engineer", "Platform Engineer", "Machine Learning Engineer",
)


def build_corpus(size: int, seed: int = 1234) -> list[Candidate]:
    rng = random.Random(seed)
    corpus: list[Candidate] = []
    for i in range(size):
        n = rng.randint(3, 7)
        skills = tuple(rng.sample(SKILL_POOL, n))
        title = rng.choice(TITLES)
        corpus.append(
            Candidate(
                id=f"g{i:06d}",
                name=f"Candidate {i}",
                title=title,
                skills=skills,
                years_experience=rng.randint(1, 15),
                summary=f"{title} working with {', '.join(skills)}.",
            )
        )
    return corpus


def run(size: int, repeats: int) -> dict[str, float]:
    corpus = build_corpus(size)
    role = Role(
        "Backend Engineer",
        ("python", "postgres", "docker"),
        min_years=5,
        description="Builds and operates Python services with relational storage.",
    )
    provider = HashingEmbeddingProvider()
    durations: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        ranked = rank_candidates(role, corpus, provider, top_k=10)
        durations.append(time.perf_counter() - start)
    assert len(ranked) == 10
    best = min(durations)
    return {
        "corpus_size": float(size),
        "repeats": float(repeats),
        "best_seconds": round(best, 6),
        "candidates_per_second": round(size / best, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=5000)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run(args.size, args.repeats)))


if __name__ == "__main__":
    main()
