import pytest

from kuku.utils.dict import unroll_key


@pytest.mark.parametrize(
    "key_value, expected",
    [[("a.b.c", 1), {"a": {"b": {"c": 1}}}], [("a.0.c", 1), {"a": [{"c": 1}]}]],
)
def test_unroll(key_value, expected):
    assert unroll_key(*key_value) == expected
