from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class SearchIndex(Base):

    __tablename__ = "search_index"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    photo_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("photos.id"),
        nullable=False,
        unique=True
    )

    searchable_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )