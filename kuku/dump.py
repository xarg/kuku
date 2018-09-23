import yaml

from kuku.types import Rendering
from kuku.utils.dict import filter_deep, walk_keys
from kuku.utils.str import camelize

OBJECT_SEPARATOR = "\n---\n"

noalias_dumper = yaml.dumper.SafeDumper
noalias_dumper.ignore_aliases = lambda self, data: True  # type: ignore
dumper = lambda data: yaml.dump(data, default_flow_style=False, Dumper=noalias_dumper)


def _transform_keys(obj: object, key: str):
    """Camelize keys for non-builtin objects"""

    return key if isinstance(obj, (dict, list, tuple)) else camelize(key)


def dump(rendering: Rendering) -> str:
    """Dump all templates rendering into a yaml string"""

    full_output = []
    for template_path, k8s_objects in rendering.items():
        template_output = []
        template_header = "# Source: {}\n".format(template_path)
        for k8s_object in k8s_objects:
            # remove all None values recursively to make for a more compact object
            k8s_object = filter_deep(k8s_object.to_dict())
            # make all keys that belong to k8s objects camelCase
            k8s_object = walk_keys(_transform_keys, k8s_object)

            template_output.append(dumper(k8s_object) + "\n")
        full_output.append(template_header + OBJECT_SEPARATOR.join(template_output))
    return OBJECT_SEPARATOR.join(full_output)
