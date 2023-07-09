from datetime import datetime
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import multiprocessing

from src.helpers.label_studio import LabelStudioAPI
from src.helpers.docker_api import DockerAPI
from src.helpers.proxy_manager import NginxProxyManagerAPI
from src.helpers.cloudflared import CloudflaredAPI
from src.config.ssl_template import DOCKERFILES
from src.utils import generate_random_string, health_check
from src.database.provider import db

from src.database.models.models import Model
from src.database.repositories.models import ModelRepository
from src.database.services.models import ModelService

from src.database.models.ml_backends import MLBackend
from src.database.repositories.ml_backends import MLBackendRepository
from src.database.services.ml_backends import MLBackendService

from src.database.models.services import Service
from src.database.repositories.services import ServiceRepository
from src.database.services.services import ServiceService


router = APIRouter()
docker_api = DockerAPI()
cloudflaredAPI = CloudflaredAPI()

proxy_api = NginxProxyManagerAPI(
    host="http://127.0.0.1.nip.io",
    port=81,
    user="tsdocode@gmail.com",
    password="2112001a"
)


model_repo = ModelRepository(db)
model_service = ModelService(model_repo)

mlbackend_repo = MLBackendRepository(db)
mlbackend_service = MLBackendService(mlbackend_repo)

service_repo = ServiceRepository(db)
service_service = ServiceService(service_repo)


def bg_build_inference_endpoint(
    token: str, server: str, project_id: str, backend_id: str
):
    api = LabelStudioAPI(url=server)
    api.set_token(token)
    user = api.get_user()['email']
    username = user.split("@")[0]

    model = model_service.get_model_by_project_and_user(
        user_id=user,
        project_id=project_id
    )
    model_id = str(model.id)

    inference_id = f"inference_{username}_{model_id}_{generate_random_string(4)}"

    inference = Service(
        id=inference_id,
        model_id=model_id,
        user_id=user,
        created_at=datetime.now(),
        status="init 💤"
    )

    print("Add inference endpoint")
    inference = service_service.create_service(inference)

    # build docker image
    dockerfile = os.environ["INFERENCE_DOCKERFILE"]

    process = multiprocessing.Process(
        target=docker_api.build_image, 
        args=(inference_id, dockerfile),
        kwargs={
            "context": os.environ["INFERENCE_BUILD_CONTEXT"]
        }
    )

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
            "image_name": inference_id,
            "port": [],
            "environment": environment,
            "volumnes": [(os.environ["BENTOML_STORE"], "/home/user/bentoml")]
        }
    )

    process.start()
    process.join()

    inference.status = "created 💡"
    inference = service_service.update_service(inference)

    username = user.split("@")[0]

    # domain_name = proxy_api.create_proxy_host(
    #     domain_name=inference_id,
    #     forward_host=inference_id,
    #     forward_port=3000
    # )

    domain_name = f"{inference_id}.tsdocode.online"

    cloudflaredAPI.add_host(
        f"{inference_id}:3000",
        domain_name
    )

    health = health_check(domain_name, health="/healthz")

    if health:
        inference.url = f"{inference_id}.tsdocode.online"
        inference.status = "ready ✅"
        service_service.update_service(inference)
        cloudflaredAPI.add_host(
            f"http://{inference_id}:3000",
            f"{inference_id}.tsdocode.online"
        )


@router.post("/deploy", response_description="Deploy latest model of project")
async def register_ml_backend(
    token: str, server: str, project_id: str, backend_id: str
):
    process = multiprocessing.Process(
        target=bg_build_inference_endpoint,
        args=(token, server, project_id, backend_id)
    )
    process.start()
    return JSONResponse(
        content="Creating your backend",
        status_code=200
    )


@router.get("/", response_description="List ML endpoints by user")
async def list_ml_backend(
    token: str, server: str
):
    api = LabelStudioAPI(url=server)
    api.set_token(token)
    user = api.get_user()['email']

    results = service_service.get_services_by_user(user)

    results = [i.__dict__ for i in results]
    for i in results:
        i.pop("_sa_instance_state")
        i['created_at'] = i['created_at'].strftime("%m/%d/%Y, %H:%M:%S")

    return JSONResponse(
        content=results,
        status_code=200
    )


# @router.get("/backend", response_description="Get ML Backend by ID")
# async def get_ml_backend_by_id(
#     ml_backend_id: str
# ):
#     result = mlbackend_service.get_ml_backend_by_id(ml_backend_id).__dict__
#     result.pop("_sa_instance_state")
#     result['created_at'] = result['created_at'].strftime("%m/%d/%Y, %H:%M:%S")

#     return JSONResponse(
#         content=result,
#         status_code=200
#     )


# @router.delete("/backend", response_description="Delete ML Backend by ID")
# async def delete_ml_backend_by_id(
#     ml_backend_id: str
# ):
#     # TODO
#     # stop container
#     # unlink label studio
#     # delete in db

#     return JSONResponse(
#         content="Implement soon",
#         status_code=200
#     )
