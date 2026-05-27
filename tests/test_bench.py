"""Smoke test for the benchmark harness so it stays runnable."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bench"))

from match_bench import build_corpus, run  # noqa: E402


def test_build_corpus_is_deterministic():
    a = build_corpus(50)
    b = build_corpus(50)
    assert [c.id for c in a] == [c.id for c in b]
    assert len(a) == 50


def test_bench_run_reports_throughput():
    result = run(size=200, repeats=2)
    assert result["corpus_size"] == 200
    assert result["candidates_per_second"] > 0
