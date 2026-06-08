from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.database.base import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    md5_hash: Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )