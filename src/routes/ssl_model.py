from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.helpers.docker_api import DockerAPI
from src.database.provider import db

from src.database.models.models import Model
from src.database.repositories.models import ModelRepository
from src.database.services.models import ModelService

router = APIRouter()
docker_api = DockerAPI()


model_repo = ModelRepository(db)
model_service = ModelService(model_repo)


@router.post("/add", response_description="Register new ML backend")
async def register_ml_backend(
    user_id: str, server: str, project_id: str, model_id: str
):
    model = Model(
        id=model_id,
        user_id=user_id,
        project_id=project_id,
        server=server,
        created_at=datetime.now()
    )

    model_service.create_model(model)

    return JSONResponse(
        content="Success create model",
        status_code=200
    )
