import uuid
from kubernetes import client, config


def deploy_challenge(challenge_image):
    instance_id = str(uuid.uuid4())[:8]

    # Load Kubernetes configuration
    config.load_kube_config()

    # Define the Deployment
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name=f"challenge-instance-{instance_id}",
            labels={"app": "challenge", "instance": instance_id}
        ),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": "challenge", "instance": instance_id}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "challenge", "instance": instance_id}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="challenge-container",
                            image=challenge_image,
                            ports=[client.V1ContainerPort(container_port=80)],
                        )
                    ],
                    image_pull_secrets=[
                        client.V1LocalObjectReference(name="hamravesh-registery")
                    ]
                )
            )
        )
    )

    # Create the Deployment
    apps_v1 = client.AppsV1Api()
    apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
    print(f"Deployment challenge-instance-{instance_id} created.")

    # Define the Service with NodePort type
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=f"challenge-service-{instance_id}"),
        spec=client.V1ServiceSpec(
            selector={"app": "challenge", "instance": instance_id},
            ports=[client.V1ServicePort(
                port=80, target_port=80, protocol="TCP", node_port=None)],
            type="NodePort"
        )
    )

    # Create the Service
    core_v1 = client.CoreV1Api()
    service_response = core_v1.create_namespaced_service(namespace="default", body=service)
    print(f"Service challenge-service-{instance_id} created.")

    # Retrieve the random NodePort assigned to the service
    node_port = None
    for port in service_response.spec.ports:
        if port.node_port:
            node_port = port.node_port

    if not node_port:
        raise Exception("Failed to retrieve a random NodePort.")

    # port_forward_process = subprocess.Popen(
    #     ["kubectl", "port-forward", f"svc/challenge-service-{instance_id}", f"{node_port}:{node_port}"],
    #     stdout=subprocess.PIPE, stderr=subprocess.PIPE
    # )

    # time.sleep(5)

    url = f"http://localhost:{node_port}"
    return url


# if __name__ == "__main__":
#     challenge_image = "registry.hamdocker.ir/the-atid/flask-my-app:latest"
#
#     challenge_url = deploy_challenge(challenge_image)
#     print(f"Challenge instance URL: {challenge_url}")