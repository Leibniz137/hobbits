import pathlib
import shlex
import subprocess

import pytest

DOCKER_NETWORK = 'hobbits'
DOCKER_IMAGE = 'thenateway/hobbits-endpoint'   # XXX: you must trust this image
DOCKER_HOBBITS_RELAYER = 'hobbits-relayer'
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
def docker_relayer(docker_network):
    cleanup = shlex.split(f'docker rm -f {DOCKER_HOBBITS_RELAYER}')
    subprocess.run(cleanup, check=False)

    setup = shlex.split(
        'docker run -d'
        f' --network {docker_network}'
        f' --name {DOCKER_HOBBITS_RELAYER}'
        ' -p 10000:10000'
        f' {DOCKER_IMAGE}'
        ' -b tcp://0.0.0.0:10000 -t tcp://hobbits-endpoint:18000'
    )
    completed_proc = subprocess.run(
        setup,
        stdout=subprocess.PIPE,
        encoding='utf-8',
        check=True
    )
    container_id = completed_proc.stdout.strip()
    yield container_id

    teardown = shlex.split(f'docker rm -f {DOCKER_HOBBITS_RELAYER}')
    subprocess.run(teardown, check=True)


@pytest.fixture(scope="session")
def docker_endpoint(docker_network):
    cleanup = shlex.split(f'docker rm -f {DOCKER_HOBBITS_ENDPOINT}')
    subprocess.run(cleanup, check=False)

    setup = shlex.split(
        "docker run -d"
        f" --hostname {DOCKER_HOBBITS_ENDPOINT}"
        f" --network {docker_network}"
        f" --name {DOCKER_HOBBITS_ENDPOINT}"
        " --entrypoint netcat"
        f" {DOCKER_IMAGE}"
        " -l -p 18000"
    )
    completed_proc = subprocess.run(
        setup,
        stdout=subprocess.PIPE,
        encoding='utf-8',
        check=True
    )
    container_id = completed_proc.stdout.strip()
    yield container_id

    teardown = shlex.split(f'docker rm -f {container_id}')
    subprocess.run(teardown, check=True)


def test_200_status_code(docker_endpoint, docker_relayer):
    subprocess.run(
        shlex.split('netcat -c localhost 10000'),
        input=(
            "EWP 0.2 RPC 5 5\n"
            "hellohello\n"
        ).encode('utf-8'),
        cwd=pathlib.Path(__file__).parent,
    )

    completed_proc = subprocess.run(
        shlex.split(f'docker logs {DOCKER_HOBBITS_ENDPOINT}'),
        capture_output=True,
    )
    endpoint_stdout = completed_proc.stdout
    expected = (
        "EWP 0.2 RPC 5 5\n"
        "hellohello"
    )
    assert endpoint_stdout == completed_proc.stdout
