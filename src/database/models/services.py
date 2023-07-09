from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Service(Base):
    __tablename__ = "services"

    id = Column(String, primary_key=True)
    model_id = Column(String)
    user_id = Column(String)
    url = Column(Text)
    status = Column(String)
    created_at = Column(TIMESTAMP)
