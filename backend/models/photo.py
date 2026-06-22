from uuid import uuid4
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base
from sqlalchemy import Boolean

from sqlalchemy import DateTime
from datetime import datetime
 


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
    unique=True,
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

    thumbnail_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )


    is_favorite: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
    nullable=False
    )


    is_archived: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
    nullable=False
    )





    phash: Mapped[str | None] = mapped_column(
    String(64),
    nullable=True
    )

    dhash: Mapped[str | None] = mapped_column(
    String(64),
    nullable=True
    )

    ahash: Mapped[str | None] = mapped_column(
    String(64),
    nullable=True
    )



    created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow,
    nullable=False
    )


