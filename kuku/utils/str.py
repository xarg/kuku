import re


def camelize(string: str) -> str:
    """Transform snake case into camelcase"""

    string = re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    return string[0].lower() + string[1:]
