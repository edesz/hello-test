from app import show_msg


import pytest


def test_show_msg():
    assert show_msg() == "hello"


@pytest.mark.parametrize("num_pods", (3,))
@pytest.mark.repeat(10)
@pytest.mark.applymanifests("configs", files=["dask.yaml"])
def test_dask_deployment(kube, kubeconfig, num_pods):
    """Test a Dask worker deployment with n > 1 replicas."""

    assert kubeconfig == "~/.kube/config"

    # wait for the manifests loaded by the 'applymanifests' marker
    # to be ready on the cluster
    kube.wait_for_registered(timeout=60)

    deployments = kube.get_deployments()
    # print(len(deployments))

    nginx_deploy = deployments.get("dask-worker")
    assert nginx_deploy is not None

    pods = nginx_deploy.get_pods()
    # print(len(pods))
    assert len(pods) == num_pods, f"dask should deploy with {num_pods} replicas"

    for pod in pods:
        containers = pod.get_containers()
        # print(len(containers))
        assert (
            len(containers) == 1
        ), "dask worker pods should have one container"
