import shlex
import subprocess

import pytest

DOCKER_NETWORK = 'hobbits'
DOCKER_IMAGE = 'hobbits-relayer'
DOCKER_HOBBITS_ENDPOINT = 'hobbits-endpoint'


@pytest.fixture(scope="session")
def docker_network():
    cleanup = shlex.split(f'docker network rm {DOCKER_NETWORK}')
    subprocess.run(cleanup, check=False)

    setup = shlex.split(f'docker network create {DOCKER_NETWORK}')
    subprocess.run(setup, check=True)
    yield DOCKER_NETWORK

    teardown = shlex.split(f'docker network rm {DOCKER_NETWORK}')
    subprocess.run(teardown, check=True)


@pytest.fixture(scope="session")
def endpoint(docker_network):
    cleanup = shlex.split(f'docker rm -f {DOCKER_HOBBITS_ENDPOINT}')
    subprocess.run(cleanup, check=False)

    docker_run = shlex.split(
        "docker run -d"
        f" --hostname {DOCKER_HOBBITS_ENDPOINT}"
        f" --network {docker_network}"
        f" --name {DOCKER_HOBBITS_ENDPOINT}"
        " --entrypoint netcat"
        " hobbits-relayer -l -p 18000"
    )
    completed_proc = subprocess.run(
        docker_run,
        stdout=subprocess.PIPE,
        encoding='utf-8',
        check=True
    )
    container_id = completed_proc.stdout.strip()
    yield container_id
    docker_rmf = shlex.split(f'docker rm -f {container_id}')
    subprocess.run(docker_rmf, check=True)


def test_200_status_code(endpoint):
    pass
