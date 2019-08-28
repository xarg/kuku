import os

import pytest
import yaml

from kuku.types import Context
from kuku.values import resolve

HERE = os.path.abspath(os.path.dirname(__file__))
VALUES_STAGING_FILE = os.path.join(HERE, "fixtures/values/values-staging.yaml")
VALUES_PRODUCTION_FILE = os.path.join(HERE, "fixtures/values/values-production.yaml")


@pytest.mark.parametrize(
    "values, expected",
    [
        (["k=v"], {"k": "v"}),
        (["k1=v1,k2=v2"], {"k1": "v1", "k2": "v2"}),
        (["k1=v1,k2=v2", "k3=v3"], {"k1": "v1", "k2": "v2", "k3": "v3"}),
        (["k="], {"k": ""}),
    ],
)
def test_valid_values(values, expected):
    assert resolve(values, []) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        (["a.b=v1", "a.c=v2"], {"a": {"b": "v1", "c": "v2"}}),
        (["a.b.c=v1", "a.b.d=v2"], {"a": {"b": {"c": "v1", "d": "v2"}}}),
    ],
)
def test_nested_dicts(values, expected):
    assert resolve(values, []) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        (["a.0.b=v1", "a.0.c=v2"], {"a": [{"c": "v2"}]}),
        # (["a.0.b=v1", "a.1.c=v2"], [{"a": [{"c": "v2"}]}, {"a": [{"b": "v1"}]}]),
    ],
)
def test_nested_lists(values, expected):
    assert resolve(values, []) == expected


@pytest.mark.parametrize(
    "values", [["k"], ["=v"], ["="], ["k=1,=2"], ["a.b.c=1,=2"], ["a.0.c=1,=2"]]
)
def test_resolve_invalid_values(values):
    with pytest.raises(ValueError):
        resolve(values, [])


def test_cli_values_value_files():
    values = resolve([], [VALUES_STAGING_FILE])
    with open(VALUES_STAGING_FILE) as fd:
        assert values == yaml.load(fd)

    # putting the same file twice should not change the resulting values
    assert resolve([], [VALUES_STAGING_FILE, VALUES_STAGING_FILE]) == values

    # cli values override values from files
    assert resolve(["env=production"], [VALUES_STAGING_FILE])["env"] == "production"

    # multiple values override (last wins)
    assert resolve(["env=1", "env=2"], [VALUES_STAGING_FILE])["env"] == "2"

    # nested override
    assert (
        resolve(["nodeSelector.node-label=pool-2"], [VALUES_STAGING_FILE])[
            "nodeSelector"
        ]["node-label"]
        == "pool-2"
    )


def test_value_files_override():
    values = resolve([], [VALUES_STAGING_FILE])
    assert values["nodeSelector"]["node-label"] == "pool-1"

    values = resolve([], [VALUES_STAGING_FILE, VALUES_PRODUCTION_FILE])
    assert values["nodeSelector"]["node-label"] == "pool-2"
