from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    project_id = Column(String)
    server = Column(String)
    created_at = Column(TIMESTAMP)