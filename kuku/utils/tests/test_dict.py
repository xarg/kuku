from kuku.types import IgnoredListItem
from kuku.utils.dict import filter_deep, walk_keys, merge_deep, unroll


def test_unroll():
    assert unroll("a.b.c", 1) == {"a": {"b": {"c": 1}}}
    assert unroll("a.0.c", 1) == {"a": [{"c": 1}]}
    assert unroll("a.1.c", 1) == {"a": [IgnoredListItem, {"c": 1}]}


def test_merge_deep():
    assert merge_deep({"a": 1}, {"b": 1}) == {"a": 1, "b": 1}
    assert merge_deep({"a": 1}, {"a": 2}) == {"a": 1}
    assert merge_deep({"a": [1]}, {"a": "c"}) == {"a": [1]}
    assert merge_deep({"a": [1]}, {"a": {"b": "c"}}) == {"a": [1]}
    assert merge_deep({"a": {"b": 1}}, {"a": {"c": 1}}) == {"a": {"b": 1, "c": 1}}
    assert merge_deep([1], [2]) == [1]
    assert merge_deep([{"a": 1}], [{"b": 2}]) == [{"a": 1, "b": 2}]
    assert merge_deep([{"a": 1}, {"c": 3}], [{"b": 2}]) == [{"a": 1, "b": 2}, {"c": 3}]
    assert merge_deep([{"a": 1}, {"b": 1}], [{"a": 2}, {"b": 2}]) == [
        {"a": 1},
        {"b": 1},
    ]
    assert merge_deep([IgnoredListItem, 2], [1]) == [1, 2]


def test_filter_deep_none():
    assert filter_deep([1, None]) == [1]
    assert filter_deep({"a": None, "b": 1}) == {"b": 1}
    assert filter_deep({"a": {"b": {"c": 1, "d": None}}}) == {"a": {"b": {"c": 1}}}
    assert filter_deep([{"a": "b"}, {"c": None}]) == [{"a": "b"}, {}]


def test_filter_deep_criteria():
    assert filter_deep([1, 2, 3], lambda v: v % 2 == 0) == [1, 3]
    assert filter_deep({"a": 1, "b": 2, "c": 3}, lambda v: v % 2 == 0) == {
        "a": 1,
        "c": 3,
    }
    assert filter_deep({"a": {"b": 2, "c": 3}}, lambda v: v % 2 == 0) == {"a": {"c": 3}}


def test_walk_keys():
    assert walk_keys(lambda obj, k: k.upper(), {"a": ["b"]}) == {"A": ["b"]}
    assert walk_keys(lambda obj, k: k.upper(), {"a": [{"b": 1}]}) == {"A": [{"B": 1}]}
