from uuid import uuid4

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class ImageEmbedding(Base):

    __tablename__ = "image_embeddings"

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

    embedding: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    from datetime import datetime

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )