import shlex
import subprocess

import pytest


@pytest.fixture(scope="session")
def endpoint():
    container_name = 'hobbits-endpoint'
    cleanup = shlex.split(f'docker rm -f {container_name}')
    subprocess.run(cleanup, check=False)

    docker_run = shlex.split(
        "docker run -d"
        " --hostname hobbits-endpoint"
        " --network hobbits"
        f" --name {container_name}"
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
