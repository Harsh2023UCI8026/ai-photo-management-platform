from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class PhotoTag(Base):

    __tablename__ = "photo_tags"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    photo_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("photos.id"),
        nullable=False
    )

    tag_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("tags.id"),
        nullable=False
    )