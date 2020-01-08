import json
from typing import Dict, List, Union, Any

DictOrList = Union[Dict, List]

TEMPORARY_LITERAL_SEPARATOR = "(kuku-dot-goes-here)"
# Placeholder list item to be ignored for deep merges of lists: must be JSON serializable !
IGNORED_LIST_ITEM = "(kuku-ignored-list-item)"


def unroll_key(key, value) -> Dict[str, Any]:
    """Unroll a dot notation key (i.e: k1.k2.0.k3) to a dictionary structure and set it's last leaf to `value`"""

    if "." not in key:
        return {key: value}

    # temporary replace literal dots (.) with a placeholder so we don't unroll them
    if "\\." in key:
        key = key.replace("\\.", TEMPORARY_LITERAL_SEPARATOR)

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
                    # Insert placeholders that hopefully will be replaced with other value or from value file.
                    res.append(IGNORED_LIST_ITEM if i != index else walk(path[1:]))
                return res
        except ValueError:
            pass

        return {item: walk(path[1:])}

    unrolled_key = json.dumps(walk(key.split(".")))
    unrolled_key = unrolled_key.replace(TEMPORARY_LITERAL_SEPARATOR, ".")
    return json.loads(unrolled_key)


def merge_deep(src: dict, dst: dict) -> dict:
    """ Merge (deep) 2 dicts. If there is a conflict the `src` key overwrites the `dst` key"""

    for key, value in src.items():
        if isinstance(value, dict):
            # get node or create one
            node = dst.setdefault(key, {})
            merge_deep(value, node)
        elif isinstance(value, list):
            if key not in dst:
                dst[key] = value
            else:
                out = []
                for i in range(max(len(dst[key]), len(value))):
                    if i >= len(dst[key]):
                        out.extend(value[i:])
                        break
                    if i < len(value) and value[i] != IGNORED_LIST_ITEM:
                        out.append(value[i])
                    else:
                        out.append(dst[key][i])
                dst[key] = out
        else:
            dst[key] = value

    return dst
