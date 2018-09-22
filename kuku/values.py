from typing import List

import yaml

from kuku.types import Context
from kuku.utils.dict import merge_deep


def resolve(values: List[str], value_files: List[str]) -> Context:
    """Resolve values from cli and value files"""

    context: Context = {}

    # first read values from files
    for value_file in value_files:
        with open(value_file) as fd:
            context = merge_deep(yaml.load(fd), context)

    for key_values in values:
        if "," in key_values:
            exntended_key_values = key_values.split(",")
        else:
            exntended_key_values = [key_values]

        for key_value in exntended_key_values:
            if "=" not in key_value:
                print("Invalid key=value format for: {}".format(key_value))
                exit(1)
            key, value = key_value.split("=")
            context = merge_deep({key: value}, context)
    return context
