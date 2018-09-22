from kubernetes import client


def template(context):
    template_spec = client.V1PodSpec(
        containers=[client.V1Container(name=context["name"], image=context["image"])]
    )

    if "nodeSelector" in context:
        template_spec.node_selector = client.V1NodeSelector(
            node_selector_terms=context["nodeSelector"]
        )

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
