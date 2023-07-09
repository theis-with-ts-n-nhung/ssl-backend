from src.database.models.models import Model
from src.database.repositories.models import ModelRepository


class ModelService:
    def __init__(self, model_repo: ModelRepository):
        self.model_repo = model_repo

    def create_model(self, model: Model):
        return self.model_repo.create_model(model)

    def get_model_by_project_and_user(self, project_id: str, user_id: str):
        return self.model_repo.get_model_by_project_user(
            project_id=project_id,
            user_id=user_id,
        )
