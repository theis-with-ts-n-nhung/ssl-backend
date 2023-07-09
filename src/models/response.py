from fastapi import HTTPException


class Response:
    """Response class"""

    def ResponseModel(data):
        return {
            "status_code": 200,
            "data": data
        }

    def ErrorResponseModel(error, code, message):
        return HTTPException(status_code=code, headers=error, detail=message)