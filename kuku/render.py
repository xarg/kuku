from copy import deepcopy

from kuku.types import Context, Templates, Rendering


def render(context: Context, templates: Templates) -> Rendering:
    """Given a `context` of values and a list of `templates` render them to k8s objects"""

    rendering = {}
    for template_path, template_func in templates.items():
        # pass a copy of the context to the template function and get it's k8s objects
        k8s_objects = template_func(deepcopy(context))
        if not isinstance(k8s_objects, (list, tuple)):
            k8s_objects = [k8s_objects]
        rendering[template_path] = k8s_objects

    return rendering
