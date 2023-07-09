import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = os.environ.get("DB_URL")

# create the engine and session
engine = create_engine(url)
Session = sessionmaker(bind=engine)


db = Session()
    
