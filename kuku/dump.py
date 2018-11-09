from types import MethodType

from kuku.types import Rendering
from kuku.utils.yaml import dumper

OBJECT_SEPARATOR = "\n---\n"


def _camelized_to_dict(self):
    """Override the default k8s object to_dict to camelize it's keys"""

    result = {}

    for attr, camel_attr in self.attribute_map.items():
        value = getattr(self, attr)

        if isinstance(value, list):
            result[camel_attr] = list(
                map(
                    lambda x: _camelized_to_dict(x) if hasattr(x, "to_dict") else x,
                    value,
                )
            )
        elif hasattr(value, "to_dict"):
            result[camel_attr] = _camelized_to_dict(value)
        elif isinstance(value, dict):
            result[camel_attr] = dict(
                map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict")
                    else item,
                    value.items(),
                )
            )
        else:
            # ignore None values - we don't need the for the output
            if value is not None:
                result[camel_attr] = value

    return result


def dump(rendering: Rendering) -> str:
    """Dump all templates rendering into a yaml string"""

    full_output = []
    for template_path, k8s_objects in rendering.items():
        template_output = []
        template_header = "# Source: {}\n".format(template_path)
        for k8s_object in k8s_objects:
            # Override the default to_dict method so we can update the k8s keys
            k8s_object.to_dict = MethodType(_camelized_to_dict, k8s_object)
            k8s_object = k8s_object.to_dict()

            template_output.append(dumper(k8s_object) + "\n")
        full_output.append(template_header + OBJECT_SEPARATOR.join(template_output))
    return OBJECT_SEPARATOR.join(full_output)
