"""add_favorites

Revision ID: 3f2e6b070e70
Revises: create_face_tables
Create Date: 2026-06-19 16:54:56.614584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f2e6b070e70'
down_revision: Union[str, Sequence[str], None] = 'create_face_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "photos",
        sa.Column(
            "is_favorite",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        )
    )


def downgrade() -> None:

    op.drop_column(
        "photos",
        "is_favorite"
    )
