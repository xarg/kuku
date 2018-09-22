from typing import Callable


def merge_deep(src: dict, dst: dict) -> dict:
    """ Merge (deep) 2 dicts. If there is a conflict the `src` key overwrites the `dst` key"""

    for key, value in src.items():
        if isinstance(value, dict):
            # get node or create one
            node = dst.setdefault(key, {})
            merge_deep(value, node)
        else:
            dst[key] = value

    return dst


def remove_none(obj: object) -> object:
    """ Remove all values that have None in them"""

    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)(
            (remove_none(k), remove_none(v))
            for k, v in obj.items()
            if k is not None and v is not None
        )
    else:
        return obj


def walk_keys(func: Callable, obj: object) -> object:
    """Walk all iterables recursively and apply func to dictionary keys"""

    if isinstance(obj, (list, tuple, set)):
        return type(obj)(walk_keys(func, x) for x in obj)
    elif isinstance(obj, dict):
        return type(obj)((func(k), walk_keys(func, v)) for k, v in obj.items())
    else:
        return obj
