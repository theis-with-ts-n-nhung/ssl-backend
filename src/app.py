from fastapi import FastAPI

from src.routes.label_studio import router as LabelStudioRoutes
from src.routes.ssl_backend import router as SSLBackendRoutes
from src.routes.ssl_model import router as SSLModelRoutes
from src.routes.inference_endpoint import router as InferenceRoutes


from starlette.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(
    LabelStudioRoutes, tags=["Label Studio"], prefix="/label-studio"
)
app.include_router(
    SSLBackendRoutes, tags=["SSL ML Backend"], prefix="/ssl-backend"
)

app.include_router(
    SSLModelRoutes, tags=["SSL ML Model"], prefix="/ssl-model"
)

app.include_router(
    InferenceRoutes, tags=["Inference Endpoint"], prefix="/inference"
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "PUT", "DELETE", "OPTION", "GET"],
    allow_headers=["*"],
)
