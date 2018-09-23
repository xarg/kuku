from kubernetes import client


def template(context):
    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                {"port": context["externalPort"], "targetPort": context["internalPort"]}
            ],
            selector={"app": context["name"]},
        ),
    )
