from typing import Dict, List, Union, Any

from kuku.types import IgnoredListItem

DictOrList = Union[Dict, List]


def unroll_key(key, value) -> Dict[str, Any]:
    """Unroll a dot notation key (i.e: k1.k2.0.k3) to a dictionary structure and set it's last leaf to `value`"""

    if "." not in key:
        return {key: value}

    def walk(path):
        # last item -> set value
        if not path:
            return value

        item = path[0]
        try:
            index = int(item)
            if str(index) == item:
                res = []
                for i in range(index + 1):
                    res.append(IgnoredListItem if i != index else walk(path[1:]))
                return res
        except ValueError:
            pass

        return {item: walk(path[1:])}

    return walk(key.split("."))
