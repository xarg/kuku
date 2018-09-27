import yaml

# don't dump with aliases
noalias_dumper = yaml.dumper.SafeDumper
noalias_dumper.ignore_aliases = lambda self, data: True  # type: ignore


def str_presenter(yaml_dumper, data):
    """Use block style for multiline strings"""
    if len(data.splitlines()) > 1:  # check for multiline string
        return yaml_dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return yaml_dumper.represent_scalar("tag:yaml.org,2002:str", data)


noalias_dumper.add_representer(str, str_presenter)


def dumper(data):
    return yaml.dump(data, default_flow_style=False, Dumper=noalias_dumper)
