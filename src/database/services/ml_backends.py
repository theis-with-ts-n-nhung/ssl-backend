from src.database.models.ml_backends import MLBackend
from src.database.repositories.ml_backends import MLBackendRepository


class MLBackendService:
    def __init__(self, ml_backend_repo: MLBackendRepository):
        self.ml_backend_repo = ml_backend_repo

    def create_ml_backend(self, ml_backend: MLBackend):
        return self.ml_backend_repo.create_ml_backend(ml_backend)
    
    def update_ml_backend_status(self, ml_backend: MLBackend, status: str):
        return self.ml_backend_repo.update_ml_backend_status(ml_backend, status)

    def get_ml_backend_by_user(self, user_id: str):
        return self.ml_backend_repo.get_ml_backend_by_user(user_id)

    def get_ml_backend_by_id(self, ml_backend_id: str):
        return self.ml_backend_repo.get_ml_backend_by_id(ml_backend_id)