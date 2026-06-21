
"""create_albums

Revision ID: 4db9657fe153
Revises: 3f2e6b070e70

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4db9657fe153"

down_revision: Union[str, Sequence[str], None] = "3f2e6b070e70"

branch_labels = None

depends_on = None


def upgrade():

    op.create_table(
        "albums",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "user_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "name",
            sa.String(255),
            nullable=False
        )
    )

    op.create_table(
        "album_photos",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "album_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "photo_id",
            sa.String(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["album_id"],
            ["albums.id"]
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        )
    )


def downgrade():

    op.drop_table(
        "album_photos"
    )

    op.drop_table(
        "albums"
    )