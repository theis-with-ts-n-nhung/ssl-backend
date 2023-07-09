import os
from python_on_whales import docker
from typing import List, Dict


class DockerAPI():
    def __init__(self) -> None:
        pass

    def build_image(
        self, name: str, dockerfile: str, env: Dict[str, str] = {}, context: str = None,
    ):
        if context:
            dockerfile_path = context
        else:
            dockerfile_path = os.path.dirname(dockerfile) 

        result = docker.buildx.build(
            tags=name,
            context_path=dockerfile_path,
            file=dockerfile,
            build_args=env
        )

        return result

    def run_container(
        self,
        image_name: str,
        port: List[tuple],
        environment: Dict[str, str],
        **kwargs
    ):
        container = docker.run(
            name=image_name,
            image=image_name,
            publish=port,
            envs=environment,
            detach=True,
            networks=["ssl"],
            volumes=kwargs["volumnes"]
        )
        return container


if __name__ == "__main__":
    api = DockerAPI()
    # api.build_image(
    #     "test_backend",
    #     "/Users/sangtnguyen/Coding/University/thesis-f/label-std-ssl-mlbackend/mixmatch/Dockerfile",
    # )

    container = api.run_container(
        "mixmatch",
        port=[],
        environment={},
    )

    print(container)