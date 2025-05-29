import uuid
from kubernetes import client, config
from kubernetes.stream import stream
import time


def deploy_challenge(challenge_image, ports):
    if "dani-first-server" in challenge_image:
        return deploy_ftp_challenge(challenge_image, ports)
    print(ports)
    base_url = "192.168.36.2:8182"
    instance_id = str(uuid.uuid4())[:8]

    config.load_kube_config("/root/.kube")


    resources = client.V1ResourceRequirements(
        limits={
            "cpu": "100m",
            "memory": "256Mi"
        },
        requests={
            "memory": "256Mi"
        }
    )
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
                            ports=container_ports,
                            resources=resources
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

        print("Waiting for pod to be ready...")
        time.sleep(10)  # Give some time for the pod to restart with new env vars
        
        # Get the pod name
        pods = core_v1.list_namespaced_pod(
            namespace="default",
            label_selector=f"app=challenge,instance={instance_id}"
        )
        
        if pods.items:
            pod_name = pods.items[0].metadata.name
            print(f"Found pod: {pod_name}")
            
            # Wait for pod to be in Running state
            max_retries = 30
            for i in range(max_retries):
                pod = core_v1.read_namespaced_pod(name=pod_name, namespace="default")
                if pod.status.phase == "Running":
                    print("Pod is running, executing commands...")
                    break
                print(f"Waiting for pod to be ready... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("Warning: Pod did not become ready in time")
                
            try:
                # Execute the PHP artisan commands
                command = ["sh", "-c", "php artisan config:clear && php artisan config:cache"]
                
                exec_response = stream(
                    core_v1.connect_get_namespaced_pod_exec,
                    name=pod_name,
                    namespace="default",
                    command=command,
                    container="challenge-container",
                    stderr=True,
                    stdin=False,
                    stdout=True,
                    tty=False
                )
                
                print("Command execution output:")
                print(exec_response)
                print("PHP artisan commands executed successfully")
                
            except Exception as e:
                print(f"Error executing command in pod: {e}")
        else:
            print("No pods found for the deployment")

    urls = {title: f"http://176.101.48.153:{node_port}" for title, node_port in port_map.items() if node_port}

    return urls

def deploy_ftp_challenge(challenge_image, ports):
    print(ports)
    base_url = "192.168.36.2:8182"
    instance_id = str(uuid.uuid4())[:8]

    config.load_kube_config("/root/.kube")


    resources = client.V1ResourceRequirements(
        limits={
            "cpu": "200m",
            "memory": "200Mi"
        },
        requests={
            "memory": "200Mi"
        }
    )


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

    port_map = {}
    for port in service_response.spec.ports:
        port_map[port.name] = port.node_port

    patch_body = {
        "spec": {
            "ports": [
                {
                    "name": "ftp-passive",
                    "port": port_map["ftp-passive"],
                    "targetPort": port_map["ftp-passive"],
                    "protocol": "TCP"
                }
            ]
        }
    }

    core_v1 = client.CoreV1Api()
    service_response = core_v1.patch_namespaced_service(namespace="default", body=patch_body, name=f"challenge-service-{instance_id}")
    print(f"Service challenge-service-{instance_id} updated.")

    # Map container ports
    container_ports = [
        client.V1ContainerPort(container_port=port.port, name=port.title)
        for port in ports if port.title != 'ftp-passive'
    ]

    container_ports.append(
        client.V1ContainerPort(container_port=str(port_map["ftp-passive"]), name="ftp-passive")
    )

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
                            ports=container_ports,
                            resources=resources,
                            env=[
                                client.V1EnvVar(
                                    name="FTP_PASSIVE_PORT",
                                    value=str(port_map["ftp-passive"])
                                )
                            ]
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


    urls = {title: f"http://176.101.48.153:{node_port}" for title, node_port in port_map.items() if node_port}

    return urls

