import os

import pytest

from kuku.render import render
from kuku.templates import find

HERE = os.path.abspath(os.path.dirname(__file__))


def test_render():
    templates = find(os.path.join(HERE, "fixtures/templates"))

    with pytest.raises(KeyError):
        render({}, templates)

    rendering = render(
        {"name": "test", "internalPort": 80, "externalPort": 80}, templates
    )

    assert len(rendering) == len(templates)
