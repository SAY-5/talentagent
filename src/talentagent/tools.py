"""Tool interface the agent uses to reach the search backend.

Every tool call goes through `ToolRegistry.call`, which checks the tool is on
the allowlist and that its arguments match the declared schema before
dispatching. This keeps the agent's tool use constrained and auditable.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from talentagent.search import SearchBackend


@dataclass(frozen=True)
class ToolSpec:
    """Declared name and argument types for an allowlisted tool."""

    name: str
    arg_types: dict[str, type]
    handler: Callable[..., Any]


class ToolError(Exception):
    """Raised when a tool call is not allowlisted or fails validation."""


class ToolRegistry:
    """Holds the allowlisted tools and validates every call."""

    def __init__(self, backend: SearchBackend) -> None:
        self._specs: dict[str, ToolSpec] = {}
        self._register("search_candidates", {"query": str, "limit": int},
                       backend.search_candidates)
        self._register("get_profile", {"candidate_id": str}, backend.get_profile)
        self._register("filter_by_skill", {"skill": str}, backend.filter_by_skill)

    def _register(self, name: str, arg_types: dict[str, type],
                  handler: Callable[..., Any]) -> None:
        self._specs[name] = ToolSpec(name, arg_types, handler)

    @property
    def allowlist(self) -> frozenset[str]:
        return frozenset(self._specs)

    def schema_of(self, name: str) -> dict[str, type]:
        return dict(self._specs[name].arg_types)

    def call(self, name: str, args: dict[str, Any]) -> Any:
        """Validate and dispatch a single tool call."""
        if name not in self._specs:
            raise ToolError(f"tool not allowlisted: {name}")
        spec = self._specs[name]
        for key, value in args.items():
            if key not in spec.arg_types:
                raise ToolError(f"unknown argument {key!r} for {name}")
            expected = spec.arg_types[key]
            if not isinstance(value, expected):
                raise ToolError(
                    f"argument {key!r} for {name} expected {expected.__name__}"
                )
        return spec.handler(**args)
