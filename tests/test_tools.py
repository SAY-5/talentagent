import pytest

from talentagent.search import SearchBackend
from talentagent.tools import ToolError, ToolRegistry


@pytest.fixture
def registry():
    return ToolRegistry(SearchBackend())


def test_allowlist_is_fixed(registry):
    assert registry.allowlist == {
        "search_candidates",
        "get_profile",
        "filter_by_skill",
    }


def test_unknown_tool_is_rejected(registry):
    with pytest.raises(ToolError):
        registry.call("delete_everything", {})


def test_wrong_arg_type_is_rejected(registry):
    with pytest.raises(ToolError):
        registry.call("search_candidates", {"query": "python", "limit": "lots"})


def test_valid_call_dispatches(registry):
    cand = registry.call("get_profile", {"candidate_id": "c003"})
    assert cand.id == "c003"
