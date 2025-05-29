import uuid
from kubernetes import client, config

def deploy_challenge(challenge_image, ports):
    print(ports)
    base_url = "192.168.36.2:8182"
    instance_id = str(uuid.uuid4())[:8]

    config.load_kube_config("/root/.kube")

    # Map container ports
    container_ports = [
        client.V1ContainerPort(container_port=port.port, name=port.title)
        for port in ports
    ]

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
                            image=f"{base_url}/{challenge_image}",
                            ports=container_ports
                        )
                    ],
                    image_pull_secrets=[
                        client.V1LocalObjectReference(name="hamravesh-registery")
                    ]
                )
            )
        )
    )

    apps_v1 = client.AppsV1Api()
    apps_v1.create_namespaced_deployment(namespace="default", body=deployment)
    print(f"Deployment challenge-instance-{instance_id} created.")

    # Create service ports for NodePort service
    service_ports = [
        client.V1ServicePort(
            name=port.title,
            port=port.port,
            target_port=port.port,
            protocol="TCP"
        ) for port in ports
    ]

    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=f"challenge-service-{instance_id}"),
        spec=client.V1ServiceSpec(
            selector={"app": "challenge", "instance": instance_id},
            ports=service_ports,
            type="NodePort"
        )
    )

    core_v1 = client.CoreV1Api()
    service_response = core_v1.create_namespaced_service(namespace="default", body=service)
    print(f"Service challenge-service-{instance_id} created.")

    # Retrieve NodePorts for each port
    port_map = {}
    for port in service_response.spec.ports:
        port_map[port.name] = port.node_port

    if "ctf-smart-developer" in challenge_image and "ssh" in port_map:
        ssh_node_port = port_map["ssh"]
        server_address = f"176.101.48.153:{ssh_node_port}"
        
        deployment.spec.template.spec.containers[0].env = [
            client.V1EnvVar(name="SERVER_ADDRESS", value=server_address)
        ]
        
        apps_v1.patch_namespaced_deployment(
            name=f"challenge-instance-{instance_id}",
            namespace="default",
            body=deployment
        )
        print(f"Updated deployment with SERVER_ADDRESS: {server_address}")

    urls = {title: f"http://176.101.48.153:{node_port}" for title, node_port in port_map.items() if node_port}

    return urls

