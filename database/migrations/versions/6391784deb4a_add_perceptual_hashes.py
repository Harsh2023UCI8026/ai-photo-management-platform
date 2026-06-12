"""add_perceptual_hashes

Revision ID: 6391784deb4a
Revises: 27a114a0d22b
Create Date: 2026-06-10

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6391784deb4a"

down_revision: Union[str, Sequence[str], None] = "27a114a0d22b"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.add_column(
        "photos",
        sa.Column(
            "phash",
            sa.String(64),
            nullable=True
        )
    )

    op.add_column(
        "photos",
        sa.Column(
            "dhash",
            sa.String(64),
            nullable=True
        )
    )

    op.add_column(
        "photos",
        sa.Column(
            "ahash",
            sa.String(64),
            nullable=True
        )
    )


def downgrade() -> None:

    op.drop_column("photos", "ahash")

    op.drop_column("photos", "dhash")

    op.drop_column("photos", "phash")