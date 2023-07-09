from sqlalchemy.orm import Session

from src.database.models.services import Service


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_service(self, service: Service):
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def update_service(self, service: Service):
        return self.create_service(service)

    def get_services_by_user(self, user_id: str):
        return self.db.query(Service).filter(Service.user_id == user_id).all()
