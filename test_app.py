#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest
from kubernetes import client, config


def test_abc():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(
            "%s\t%s\t%s"
            % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
        )


@pytest.mark.parametrize("num_pods", (3,))
@pytest.mark.repeat(10)
@pytest.mark.applymanifests("configs", files=["nginx.yaml"])
def test_nginx(kube, kubeconfig, num_pods):
    """An example test against an Nginx deployment."""

    # wait for the manifests loaded by the 'applymanifests' marker
    # to be ready on the cluster
    kube.wait_for_registered(timeout=30)

    deployments = kube.get_deployments()
    nginx_deploy = deployments.get("nginx-deployment")
    assert nginx_deploy is not None

    pods = nginx_deploy.get_pods()
    assert len(pods) == num_pods, f"nginx expected with {num_pods} replicas"

    for pod in pods:
        containers = pod.get_containers()
        assert len(containers) == 1, "nginx pod should have one container"
