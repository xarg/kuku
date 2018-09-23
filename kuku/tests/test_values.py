import os

import pytest
import yaml

from kuku.values import resolve

HERE = os.path.abspath(os.path.dirname(__file__))
VALUES_STAGING_FILE = os.path.join(HERE, "fixtures/values/values-staging.yaml")
VALUES_PRODUCTION_FILE = os.path.join(HERE, "fixtures/values/values-production.yaml")


def test_valid_values():
    assert resolve(["k=v"], []) == {"k": "v"}
    assert resolve(["k1=v1,k2=v2"], []) == {"k1": "v1", "k2": "v2"}
    assert resolve(["k1=v1,k2=v2", "k3=v3"], []) == {"k1": "v1", "k2": "v2", "k3": "v3"}
    assert resolve(["k1=v1,k2=v2", "k3=v3"], []) == {"k1": "v1", "k2": "v2", "k3": "v3"}


def test_nested_dicts():
    assert resolve(["a.b=v1", "a.c=v2"], []) == {"a": {"b": "v1", "c": "v2"}}
    assert resolve(["a.b.c=v1", "a.b.d=v2"], []) == {"a": {"b": {"c": "v1", "d": "v2"}}}


def test_nested_lists():
    assert resolve(["a.0.b=v1", "a.0.c=v2"], []) == {"a": [{"b": "v1", "c": "v2"}]}


def test_resolve_invalid_values():
    with pytest.raises(ValueError):
        resolve(["k"], [])

    assert resolve(["k="], []) == {"k": ""}

    with pytest.raises(ValueError):
        resolve(["=v"], [])

    with pytest.raises(ValueError):
        resolve(["="], [])

    with pytest.raises(ValueError):
        resolve(["k=1,=2"], [])

    with pytest.raises(ValueError):
        resolve(["a.b.c=1,=2"], [])

    with pytest.raises(ValueError):
        resolve(["a.0.c=1,=2"], [])


def test_value_file():
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
    values = resolve([], [VALUES_STAGING_FILE, VALUES_PRODUCTION_FILE])
    assert values == {}
