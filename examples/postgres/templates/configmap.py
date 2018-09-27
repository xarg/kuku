from kubernetes import client


def template(context):
    if "configmap" not in context:
        return

    return client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(name=context["name"]),
        data=context["configmap"],
    )
