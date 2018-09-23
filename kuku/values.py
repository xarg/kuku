from typing import List

import yaml

from kuku.types import Context
from kuku.utils.dict import merge_deep, unroll


def resolve(values: List[str], value_files: List[str]) -> Context:
    """Resolve values from cli and value files"""

    context: Context = {}

    # first read values from files
    for value_file in value_files:
        with open(value_file) as fd:
            context = merge_deep(yaml.load(fd), context)

    for key_values in values:
        if "," in key_values:
            extended_key_values = key_values.split(",")
        else:
            extended_key_values = [key_values]

        for key_value in extended_key_values:
            format_error = "Invalid key=value format for: {}".format(key_value)
            if "=" not in key_value:
                raise ValueError(format_error)

            key, value = key_value.split("=")
            if key == "":
                raise ValueError(format_error)

            context = merge_deep(unroll(key, value), context)
    return context
