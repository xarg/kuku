from kubernetes import client


def template(context):
    pod_spec_volumes = []
    pod_spec_volume_mounts = []
    stateful_set_spec_volume_claim_templates = []

    for pvc in context.get("pvc"):
        stateful_set_spec_volume_claim_templates.append(
            client.V1PersistentVolumeClaim(
                metadata=client.V1ObjectMeta(
                    name=pvc["name"],
                    annotations={
                        "volume.beta.kubernetes.io/storage-class": pvc["class"]
                    },
                ),
                spec=client.V1PersistentVolumeClaimSpec(
                    access_modes=["ReadWriteOnce"],
                    resources=client.V1ResourceRequirements(
                        requests={"storage": pvc["size"]}
                    ),
                ),
            )
        )
        pod_spec_volume_mounts.append(
            client.V1VolumeMount(name=pvc["name"], mount_path=pvc["mountPath"])
        )

    if "configmap" in context:
        volume_name = "{}-config".format(context["name"])
        pod_spec_volumes.append(
            client.V1Volume(
                name=volume_name,
                config_map=client.V1ConfigMapVolumeSource(name=context["name"]),
            )
        )
        pod_spec_volume_mounts.append(
            client.V1VolumeMount(name=volume_name, mount_path="/etc/postgresql/")
        )

    labels = {"app": context["name"]}
    pg_isready_exec = client.V1ExecAction(command=["gosu postgres pg_isready"])

    return client.V1StatefulSet(
        api_version="apps/v1beta1",
        kind="StatefulSet",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1StatefulSetSpec(
            service_name=context["name"],
            replicas=context["replicas"],
            selector=client.V1LabelSelector(match_labels=labels),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="postgres",
                            image=context["image"],
                            lifecycle=client.V1Lifecycle(
                                pre_stop=client.V1Handler(
                                    _exec=client.V1ExecAction(
                                        command=[
                                            'gosu postgres pg_ctl -D "$PGDATA" -m fast -w stop'
                                        ]
                                    )
                                )
                            ),
                            liveness_probe=client.V1Probe(
                                _exec=pg_isready_exec,
                                initial_delay_seconds=120,
                                timeout_seconds=5,
                                failure_threshold=6,
                            ),
                            readiness_probe=client.V1Probe(
                                _exec=pg_isready_exec,
                                initial_delay_seconds=10,
                                timeout_seconds=5,
                                period_seconds=30,
                                failure_threshold=999,
                            ),
                            ports=[client.V1ContainerPort(container_port=5432)],
                            volume_mounts=pod_spec_volume_mounts,
                            resources=client.V1ResourceRequirements(
                                **context["resources"]
                            )
                            if "resources" in context
                            else None,
                        )
                    ],
                    volumes=pod_spec_volumes,
                    node_selector=context.get("nodeSelector"),
                ),
            ),
            volume_claim_templates=stateful_set_spec_volume_claim_templates,
        ),
    )
