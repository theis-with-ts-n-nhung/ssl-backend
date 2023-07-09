from datetime import datetime
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from src.helpers.label_studio import LabelStudioAPI
from src.models.response import Response
from src.database.provider import db

from src.database.models.users import User
from src.database.repositories.users import UserRepository
from src.database.services.users import UserService

router = APIRouter()

user_repo = UserRepository(db)
user_service = UserService(user_repo)


@router.get("/user", response_description="Check label studio tokens")
def get_user(token: str, server: str):
    api = LabelStudioAPI(url=server)
    api.set_token(token)

    return JSONResponse(
        content=api.get_user(),
        status_code=200
    )


@router.post("/auth", response_description="Check label studio tokens")
async def check_tokens(token: str, server: str):
    try:
        api = LabelStudioAPI(url=server)
        api.set_token(token)

        result = api.auth()

        if result:
            studio_user = api.get_user()
            user = User(
                id=studio_user['email'],
                token=token,
                server=server,
                created_at=datetime.now()
            )

            result = user_service.create_user(user)

            if result:
                return Response.ResponseModel("Valid token, created user")
            else:
                return Response.ErrorResponseModel(
                    "Invalid tokens", 403,
                    f"Your token is not valid for server {server}"
                )
        else:        
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=f"Your token is not valid for server {server}"
            )
        
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=f"Your token is not valid for server {server}"
        )
        

@router.post("/list_project", response_description="List user project")
async def list_project(token: str, server: str):
    print(server)

    api = LabelStudioAPI(url=server)
    api.set_token(token)

    print(token)

    result = api.list_project()

    print(result)

    if isinstance(result, bool):
        return Response.ErrorResponseModel(
            "Invaid request", 404, "You request is invalid"
        )
    else:
        return Response.ResponseModel(result)
