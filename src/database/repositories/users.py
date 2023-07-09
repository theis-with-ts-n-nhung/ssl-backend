from sqlalchemy.orm import Session

from src.database.models.users import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user: User):
        self.db.add(user)  # Optional if user is already in session
        self.db.commit()
        self.db.refresh(user)
        return user