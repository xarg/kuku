import yaml

from kuku.types import Rendering

OBJECT_SEPARATOR = "\n---\n"

noalias_dumper = yaml.dumper.SafeDumper
noalias_dumper.ignore_aliases = lambda self, data: True
dumper = lambda data: yaml.dump(data, default_flow_style=False, Dumper=noalias_dumper)


def dump(rendering: Rendering) -> str:
    full_output = []
    for template_path, k8s_objects in rendering.items():
        template_header = "# {}:\n".format(template_path)
        template_output = []
        for k8s_object in k8s_objects:
            template_output.append(dumper(k8s_object.dump()) + "\n")
        template_output = template_header + OBJECT_SEPARATOR.join(template_output)
        full_output.append(template_output)
    return OBJECT_SEPARATOR.join(full_output)
