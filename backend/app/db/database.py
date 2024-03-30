from sqlmodel import Session, SQLModel, create_engine

from user import models
from config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def close_db():
    SQLModel.metadata.drop_all(engine)
