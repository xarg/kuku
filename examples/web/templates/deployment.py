from kuku.objects import Deployment


def template(context):
    labels = {"app": context["name"]}

    template_spec = {}
    if "nodeSelector" in context:
        template_spec["nodeSelector"] = context["nodeSelector"]

    template_spec["containers"] = [{"name": context["name"], "image": context["image"]}]

    return Deployment(
        metadata={"name": context["name"], "labels": labels},
        spec={
            "replicas": context["replicas"],
            "template": {"metadata": {"labels": labels}, "spec": template_spec},
        },
    )
