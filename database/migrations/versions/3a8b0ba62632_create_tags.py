"""create_tags

Revision ID: 3a8b0ba62632
Revises: 4db9657fe153
Create Date: 2026-06-20

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3a8b0ba62632"

down_revision: Union[str, Sequence[str], None] = "4db9657fe153"

branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "tags",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "name",
            sa.String(100),
            nullable=False,
            unique=True
        )
    )

    op.create_table(
        "photo_tags",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "photo_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "tag_id",
            sa.String(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        ),

        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"]
        )
    )


def downgrade() -> None:

    op.drop_table("photo_tags")
    op.drop_table("tags")