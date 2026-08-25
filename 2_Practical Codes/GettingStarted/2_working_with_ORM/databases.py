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


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        nullable=False
    )

    published: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()")
    )


Base.metadata.create_all(engine)
print("Tables created successfully.")



SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

post = Post(
    title="My Testing Post WIth ORM",
    content="This is the content of my first post.",
    published=True
)

session.add(post)
session.commit()
session.close()
print("Post created successfully.")