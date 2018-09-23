import os
import pkgutil

from kuku.types import Templates

TEMPLATE_FUNCTION_NAME = "template"


def find(templates_dir: str) -> Templates:
    """Given a templates directory and import all python templates"""

    templates = {}

    for module_info in pkgutil.iter_modules([templates_dir]):
        module = module_info.module_finder.find_module(module_info.name).load_module()
        template_path = os.path.join(templates_dir, module_info.name + ".py")
        # only consider python modules with a template function
        template_func = getattr(module, TEMPLATE_FUNCTION_NAME, None)
        if template_func:
            templates[template_path] = template_func

    if not templates:
        raise ValueError(
            "No kuku python templates files found in {}".format(templates_dir)
        )

    return templates
