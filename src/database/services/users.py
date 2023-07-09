from src.database.models.users import User
from src.database.repositories.users import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: User):
        existing_user = self.user_repo.get_user(user.id)
        if existing_user:
            # Update the existing user with the new data
            existing_user.token = user.token
            existing_user.server = user.server
            existing_user.created_at = user.created_at
            return self.user_repo.update_user(existing_user)
        else:
            return self.user_repo.create_user(user)

    def get_user(self, user_id: str):
        return self.user_repo.get_user(user_id)