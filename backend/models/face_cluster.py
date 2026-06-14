from uuid import uuid4

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class FaceCluster(Base):

    __tablename__ = "face_clusters"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    label: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )