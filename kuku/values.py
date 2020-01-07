from typing import List, Mapping

import yaml

from kuku.types import Context
from kuku.utils.dict import unroll_key, merge_deep, IGNORED_LIST_ITEM


def resolve(values: List[str], value_files: List[str]) -> Context:
    """Resolve values from cli and value files"""

    context: Context = {}

    for value_file in value_files:
        with open(value_file) as fd:
            context = merge_deep(yaml.safe_load(fd), context)

    # arguments from the CLI have priority
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
            if not key:
                raise ValueError(format_error)

            context = merge_deep(unroll_key(key, value), context)

    check_placeholder(context)
    return context


def check_placeholder(context: dict) -> None:
    """Assert that all the placeholders have been replaced."""
    for key, value in context.items():
        if isinstance(value, list):
            # Check if we have any placeholder left
            if any([v for v in value if v == IGNORED_LIST_ITEM]):
                raise ValueError(
                    "some item in the list '%s' has not been given a value." % key
                )
        elif isinstance(value, dict):
            check_placeholder(value)
