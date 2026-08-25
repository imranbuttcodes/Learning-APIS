from datetime import datetime
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker


load_dotenv()

postgres_user = os.getenv("DB_USER")
postgres_password = os.getenv("DB_PASSWORD")
postgres_host = os.getenv("DB_HOST")
postgres_port = os.getenv("DB_PORT")
postgres_db = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{postgres_user}:{postgres_password}@"
    f"{postgres_host}:{postgres_port}/{postgres_db}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
