from talentagent.search import SearchBackend


def test_search_finds_python_candidates():
    backend = SearchBackend()
    results = backend.search_candidates("python backend")
    assert results
    assert any("python" in c.skills for c in results)


def test_get_profile_round_trips():
    backend = SearchBackend()
    cand = backend.get_profile("c001")
    assert cand.name == "Ada Reyes"


def test_filter_by_skill_is_case_insensitive():
    backend = SearchBackend()
    react = backend.filter_by_skill("React")
    assert {c.id for c in react} == {
        c.id for c in backend.filter_by_skill("react")
    }
    assert react
