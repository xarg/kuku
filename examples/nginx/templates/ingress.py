from kubernetes import client


def template(context):
    return client.V1beta1Ingress(
        api_version="extensions/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1beta1IngressSpec(
            backend=client.V1beta1IngressBackend(
                service_name=context["name"], service_port=context["externalPort"]
            )
        ),
    )
