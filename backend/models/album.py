from uuid import uuid4

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class Album(Base):

    __tablename__ = "albums"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )