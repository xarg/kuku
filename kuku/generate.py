from kuku.types import Context, Templates, Rendering


def generate(context: Context, templates: Templates) -> Rendering:
    k8s_objects = {}
    for template_path, template_func in templates.items():
        objects = template_func(context)
        if not isinstance(objects, list):
            objects = [objects]
        k8s_objects[template_path] = objects

    return k8s_objects
