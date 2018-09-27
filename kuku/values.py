from typing import List

import yaml

from kuku.types import Context
from kuku.utils.dict import unroll_key


def resolve(values: List[str], value_files: List[str]) -> Context:
    """Resolve values from cli and value files"""

    chain = []
    resolved_key_values = []

    # arguments from the CLI have priority
    for key_values in reversed(values):
        if "," in key_values:
            extended_key_values = key_values.split(",")
        else:
            extended_key_values = [key_values]

        for key_value in extended_key_values:
            format_error = "Invalid key=value format for: {}".format(key_value)
            if "=" not in key_value:
                raise ValueError(format_error)

            key, value = key_value.split("=")
            if not key:
                raise ValueError(format_error)

            resolved_key_values.append(unroll_key(key, value))

    chain.extend(resolved_key_values)

    for value_file in reversed(value_files):
        with open(value_file) as fd:
            chain.append(yaml.load(fd))

    return Context(*chain)
