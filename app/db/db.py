from sqlmodel import SQLModel, create_engine, Session
from app.db.config import settings

#  usa directamente db_link desde .env
DATABASE_URL = settings.db_link

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)