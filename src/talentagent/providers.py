"""Embedding provider seam with a deterministic local default.

The agent depends only on the EmbeddingProvider protocol. A real provider
(hosted embedding service) can be dropped in without touching the agent, while
CI and tests use the deterministic HashingEmbeddingProvider, which is hermetic
and offline.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol, runtime_checkable

_TOKEN = re.compile(r"[a-z0-9]+")


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Maps text to a fixed-length vector."""

    dim: int

    def embed(self, text: str) -> list[float]:
        ...


class HashingEmbeddingProvider:
    """Deterministic bag-of-tokens embedding using feature hashing.

    Each token is hashed into one of `dim` buckets with a stable sign, so the
    same text always yields the same vector with no network or model state.
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def _tokens(self, text: str) -> list[str]:
        return _TOKEN.findall(text.lower())

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for token in self._tokens(text):
            digest = hashlib.sha1(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dim
            sign = 1.0 if digest[4] & 1 else -1.0
            vec[bucket] += sign
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0.0:
            return vec
        return [v / norm for v in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors."""
    if len(a) != len(b):
        raise ValueError("vectors must share dimension")
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    return max(0.0, min(1.0, dot))
