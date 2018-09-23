from typing import Callable, Optional, Dict, List, Union, Any

from kuku.types import IgnoredListItem

DictOrList = Union[Dict, List]


def unroll(key, value) -> Dict[str, Any]:
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


def merge_deep(src: DictOrList, dst: DictOrList) -> DictOrList:
    """ Merge deep 2 objects. If there is a conflict the `src` key overwrites the `dst` key"""

    if isinstance(src, list) and isinstance(dst, list):
        for i, src_item in enumerate(src):
            if src_item is IgnoredListItem:
                continue
            for j, dst_item in enumerate(dst):
                if i != j:
                    continue
                if isinstance(src_item, dict):
                    merge_deep(src_item, dst_item)
                elif isinstance(src_item, list):
                    dst[j] = src_item
                else:
                    dst[j] = src_item
    elif isinstance(src, dict):
        for key, value in src.items():
            if isinstance(value, dict):
                # get node or create one
                if isinstance(dst, dict):
                    node = dst.setdefault(key, {})
                else:
                    node = value
                merge_deep(value, node)
            else:
                dst[key] = value

    return dst


def filter_deep(target: object, criteria: Optional[Callable] = None) -> object:
    """Apply `criteria` filter to all `target` object values recursively."""

    def test(value: object) -> bool:
        """Test if the value passes the filtering criteria"""

        if not isinstance(value, (list, tuple, set, dict)):
            return value is not None if criteria is None else not criteria(value)
        return True

    def walk(obj):
        if isinstance(obj, (list, tuple, set)):
            return type(obj)(walk(v) for v in obj if test(v))
        elif isinstance(obj, dict):
            return type(obj)((k, walk(v)) for k, v in obj.items() if test(v))
        else:
            return obj

    return walk(target)


def walk_keys(func: Callable, obj: object) -> object:
    """Walk all iterables recursively and apply `func` to all dictionary keys"""

    if isinstance(obj, (list, tuple, set)):
        return type(obj)(walk_keys(func, v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((func(obj, k), walk_keys(func, v)) for k, v in obj.items())
    else:
        return obj
