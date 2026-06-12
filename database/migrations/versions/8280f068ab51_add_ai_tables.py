"""add_ai_tables

Revision ID: 8280f068ab51
Revises: 6391784deb4a
Create Date: 2026-06-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "8280f068ab51"

down_revision: Union[str, Sequence[str], None] = "6391784deb4a"

branch_labels = None

depends_on = None


def upgrade():

    op.create_table(
        "categories",

        sa.Column(
            "id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "photo_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "category_name",
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            "confidence_score",
            sa.Float(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )

    op.create_table(
        "image_embeddings",

        sa.Column(
            "id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "photo_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "embedding",
            postgresql.JSONB(
                astext_type=sa.Text()
            ),
            nullable=False
        ),

        sa.Column(
            "model_name",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text(
                "now()"
            ),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "photo_id"
        )
    )

    op.create_table(
        "search_index",

        sa.Column(
            "id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "photo_id",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "searchable_text",
            sa.Text(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "photo_id"
        )
    )


def downgrade():

    op.drop_table(
        "search_index"
    )

    op.drop_table(
        "image_embeddings"
    )

    op.drop_table(
        "categories"
    )