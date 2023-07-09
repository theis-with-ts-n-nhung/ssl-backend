from datetime import datetime
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import multiprocessing

from src.helpers.label_studio import LabelStudioAPI
from src.helpers.docker_api import DockerAPI
from src.helpers.proxy_manager import NginxProxyManagerAPI
from src.config.ssl_template import DOCKERFILES
from src.utils import generate_random_string, health_check
from src.database.provider import db

from src.database.models.ml_backends import MLBackend
from src.database.repositories.ml_backends import MLBackendRepository
from src.database.services.ml_backends import MLBackendService

router = APIRouter()
docker_api = DockerAPI()

proxy_api = NginxProxyManagerAPI(
    host="http://127.0.0.1.nip.io",
    port=81,
    user="tsdocode@gmail.com",
    password="2112001a"
)


mlbackend_repo = MLBackendRepository(db)
mlbackend_service = MLBackendService(mlbackend_repo)


def bg_register_ml_backend(
    token: str, server: str, project_id: str, base_model: str, label_type: str
):
    api = LabelStudioAPI(url=server)
    api.set_token(token)
    user = api.get_user()['email']

    mlbackend_repo = MLBackendRepository(db)
    mlbackend_service = MLBackendService(mlbackend_repo)

    backend_id = f"{base_model}_{label_type}_{generate_random_string(4)}"

    # create new ml backend in db
    ml_backend = MLBackend(
        id=backend_id,
        user_id=user,
        project_id=project_id,
        created_at=datetime.now(),
        status="init 💤"
    )

    print("Add new ml_backend")
    ml_backend = mlbackend_service.create_ml_backend(ml_backend)

    print("Backround DEBUG ", ml_backend.__dict__)

    print("Backround DEBUG ", ml_backend._sa_instance_state)

    # build docker image
    dockerfile = DOCKERFILES["resnet18_mixmatch"]

    process = multiprocessing.Process(
        target=docker_api.build_image, args=(backend_id, dockerfile)
    )
    ml_backend = mlbackend_service.update_ml_backend_status(ml_backend, "starting 🧾")
    # print("Starting debug ", ml_backend.__dict__)
    process.start()
    # Wait for the process to finish
    process.join()

    environment = {
        "HOSTNAME": "http://studio:8000",
        "API_KEY": token,
        "MLFLOW_URI": "http://mlflow:5001",
        "YATAI_URI": "http://yatai:3000",
        "USER_ID": user,
        "PROJECT_ID": project_id,
        "VISION_SSL_API": "http://host.docker.internal:8001",
    }

    process = multiprocessing.Process(
        target=docker_api.run_container,
        kwargs={
            "image_name": backend_id,
            "port": [],
            "environment": environment,
            "volumnes": [(os.environ["BENTOML_STORE"], "/root/bentoml")]
        }
    )

    ml_backend = mlbackend_service.update_ml_backend_status(ml_backend, "created 💡")

    process.start()

    username = user.split("@")[0]

    domain_name = proxy_api.create_proxy_host(
        domain_name=f"{username}_{backend_id}",
        forward_host=backend_id,
        forward_port=9090
    )

    health = health_check(domain_name)

    if health:
        link_result = api.link_ml_backend(
            name=backend_id,
            project_id=project_id,
            ml_backend_url=f"http://{backend_id}:9090"
        )

        ml_backend.endpoint = "http://" + domain_name
        ml_backend = mlbackend_service.update_ml_backend_status(ml_backend, "ready ✅")

        print(link_result.text)


@router.post("/register", response_description="Register new ML backend")
async def register_ml_backend(
    token: str, server: str, project_id: str, base_model: str, label_type: str
):
    process = multiprocessing.Process(
        target=bg_register_ml_backend,
        args=(token, server, project_id, base_model, label_type)
    )
    process.start()

    return JSONResponse(
        content="Creating your backend",
        status_code=200
    )


@router.get("/backends", response_description="Register new ML backend")
async def list_ml_backend(
    token: str, server: str
):
    api = LabelStudioAPI(url=server)
    api.set_token(token)
    user = api.get_user()['email']

    results = mlbackend_service.get_ml_backend_by_user(user)

    results = [i.__dict__ for i in results]
    for i in results:
        i.pop("_sa_instance_state")
        i['created_at'] = i['created_at'].strftime("%m/%d/%Y, %H:%M:%S")

    return JSONResponse(
        content=results,
        status_code=200
    )


@router.get("/backend", response_description="Get ML Backend by ID")
async def get_ml_backend_by_id(
    ml_backend_id: str
):
    result = mlbackend_service.get_ml_backend_by_id(ml_backend_id).__dict__
    result.pop("_sa_instance_state")
    result['created_at'] = result['created_at'].strftime("%m/%d/%Y, %H:%M:%S")

    return JSONResponse(
        content=result,
        status_code=200
    )


@router.delete("/backend", response_description="Delete ML Backend by ID")
async def delete_ml_backend_by_id(
    ml_backend_id: str
):
    # TODO
    # stop container
    # unlink label studio
    # delete in db

    return JSONResponse(
        content="Implement soon",
        status_code=200
    )
