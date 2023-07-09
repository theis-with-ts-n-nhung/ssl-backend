from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MLBackend(Base):
    __tablename__ = "ml_backends"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    project_id = Column(String)
    created_at = Column(TIMESTAMP)
    status = Column(String)
    endpoint = Column(String)

