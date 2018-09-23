from kubernetes import client


def template(context):
    return client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=client.V1ObjectMeta(name=context["name"]),
    )
