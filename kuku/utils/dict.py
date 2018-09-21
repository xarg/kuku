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
