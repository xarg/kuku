import os

import pytest

from kuku.templates import find

HERE = os.path.abspath(os.path.dirname(__file__))


def test_find_templates():
    templates = find(os.path.join(HERE, "fixtures/templates"))
    assert len(templates) == 2
    assert all([t.endswith(".py") for t, v in templates.items()])

    with pytest.raises(ValueError):
        find(os.path.join(HERE, "fixtures/values"))
