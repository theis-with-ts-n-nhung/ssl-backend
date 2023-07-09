from sqlalchemy.orm import Session

from src.database.models.models import Model


class ModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_model(self, model: Model):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_model_by_project_user(
            self, project_id: str, user_id: str
    ) -> Model:
        return self.db.query(Model).filter_by(project_id=project_id, user_id=user_id).first()