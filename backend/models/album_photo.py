from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class AlbumPhoto(Base):

    __tablename__ = "album_photos"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    album_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("albums.id"),
        nullable=False
    )

    photo_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("photos.id"),
        nullable=False
    )