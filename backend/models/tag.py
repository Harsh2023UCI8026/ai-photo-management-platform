from uuid import uuid4

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class Tag(Base):

    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )