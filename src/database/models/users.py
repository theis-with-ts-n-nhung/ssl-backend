from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    token = Column(String)
    server = Column(String)
    created_at = Column(TIMESTAMP)
