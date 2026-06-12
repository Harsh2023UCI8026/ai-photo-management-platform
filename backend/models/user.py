from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    google_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )