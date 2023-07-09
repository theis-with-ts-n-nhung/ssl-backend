from sqlalchemy.orm import Session
from src.database.models.ml_backends import MLBackend


class MLBackendRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ml_backend(self, ml_backend: MLBackend):
        self.db.add(ml_backend)
        self.db.commit()
        self.db.refresh(ml_backend)

        print("REPO debug ", ml_backend.__dict__)
        return ml_backend

    def update_ml_backend_status(self, ml_backend: MLBackend, status: str):
        ml_backend.status = status
        self.db.add(ml_backend)
        self.db.commit()
        # self.db.refresh(ml_backend)
        return ml_backend

    def get_ml_backend_by_user(self, user_id: str):
        return self.db.query(MLBackend).filter(MLBackend.user_id == user_id).all()
    
    def get_ml_backend_by_id(self, ml_backend_id: str):
        return self.db.query(MLBackend).filter(MLBackend.id == ml_backend_id).first()