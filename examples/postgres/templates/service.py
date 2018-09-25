from kubernetes import client


def template(context):
    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1ServiceSpec(
            ports=[{"port": 5432}], selector={"app": context["name"]}
        ),
    )
