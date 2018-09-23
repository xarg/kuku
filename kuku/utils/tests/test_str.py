from kuku.utils.str import camelize


def test_camelize():
    assert camelize("foo") == "foo"
    assert camelize("Foo") == "foo"
    assert camelize("foo_bar") == "fooBar"
    assert camelize("foo_bar_baz") == "fooBarBaz"
    assert camelize("foo_barBaz") == "fooBarBaz"
