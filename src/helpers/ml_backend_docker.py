import os
import docker
from typing import Dict


class DockerAPI():
    def __init__(self) -> None:
        self.client = docker.from_env()

    def build_image(
        self, name: str, dockerfile: str, env: Dict[str, str] = {}
    ):
        dockerfile_path = os.path.dirname(dockerfile) 
        logs = self.client.api.build(
            path=dockerfile_path,
            dockerfile=dockerfile,
            tag=name,
            buildargs=env,
            decode=True,
            rm=True,
        )

        for log in logs:
            if "stream" in log:
                print(log['stream'], end="")
        return log

    def run_container(
        self,
        image_name: str,
        port: Dict[str, str],
        environment: Dict[str, str],
        **kwargs
    ):
        container = self.client.containers.run(
            image_name,
            ports=port,
            environment=environment,

            **kwargs
        )
        return container


if __name__ == "__main__":
    api = DockerAPI()
    api.build_image(
        "test_backend",
        "D:\\Thesis\\code\\label-std-ssl-mlbackend\\my_ml_backend\\Dockerfile",
    )

    container = api.run_container(
        "test_backend",
        port={
             '9090/tcp': 9090
        },
        environment={},
    )

    print(container)