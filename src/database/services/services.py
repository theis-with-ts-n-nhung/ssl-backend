from src.database.models.services import Service
from src.database.repositories.services import ServiceRepository


class ServiceService:
    def __init__(self, service_repo: ServiceRepository):
        self.service_repo = service_repo

    def create_service(self, service: Service):
        return self.service_repo.create_service(service)

    def get_services_by_user(self, user_id: str):
        return self.service_repo.get_services_by_user(user_id)

    def update_service(self, service: Service):
        return self.service_repo.update_service(service)