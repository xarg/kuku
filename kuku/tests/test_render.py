import os

import pytest

from kuku.render import render
from kuku.templates import find
from kuku.types import Context

HERE = os.path.abspath(os.path.dirname(__file__))


def test_render():
    templates = find(os.path.join(HERE, "fixtures/templates"))

    with pytest.raises(KeyError):
        render(Context(), templates)

    rendering = render(
        Context({"name": "test", "internalPort": 80, "externalPort": 80}), templates
    )

    assert len(rendering) == len(templates)
