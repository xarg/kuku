import re


def camelize(string: str) -> str:
    string = re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    return string[0].lower() + string[1:]
