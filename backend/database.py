import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv("../.env")
postgre_sql_database_url = os.environ.get("DB_URL")
engine = create_engine(postgre_sql_database_url)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
