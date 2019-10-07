from kuku.dump import dump


def test_dump_with_none_object():
    output = dump({"dir1": [None, ]})
    assert output == "# Source: dir1\n"
