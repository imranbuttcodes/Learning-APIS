from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from .databases import Base

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
        server_default='True',
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()")
    )