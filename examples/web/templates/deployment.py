from kubernetes import client


def template(context):
    labels = {"app": context["name"]}

    template_spec = client.V1PodSpec(
        containers=[client.V1Container(name=context["name"], image=context["image"])]
    )

    if "nodeSelector" in context:
        template_spec.node_selector = client.V1NodeSelector(
            node_selector_terms=context["nodeSelector"]
        )

    return client.V1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1DeploymentSpec(
            replicas=context["replicas"],
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels), spec=template_spec
            ),
        ),
    )
