import yaml

from kuku.types import Rendering
from kuku.utils.dict import remove_none, walk_keys
from kuku.utils.str import camelize

OBJECT_SEPARATOR = "\n---\n"

noalias_dumper = yaml.dumper.SafeDumper
noalias_dumper.ignore_aliases = lambda self, data: True  # type: ignore
dumper = lambda data: yaml.dump(data, default_flow_style=False, Dumper=noalias_dumper)


def dump(rendering: Rendering) -> str:
    full_output = []
    for template_path, k8s_objects in rendering.items():
        template_header = "# Source: {}\n".format(template_path)
        template_output = []
        for k8s_object in k8s_objects:
            k8s_object = remove_none(k8s_object.to_dict())
            k8s_object = walk_keys(camelize, k8s_object)
            template_output.append(dumper(k8s_object) + "\n")
        full_output.append(template_header + OBJECT_SEPARATOR.join(template_output))
    return OBJECT_SEPARATOR.join(full_output)
