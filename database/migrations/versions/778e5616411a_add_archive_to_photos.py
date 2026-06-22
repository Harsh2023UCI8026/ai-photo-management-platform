"""add_archive_to_photos

Revision ID: 778e5616411a
Revises: e32a24595b8c
Create Date: 2026-06-22 11:19:57.222775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '778e5616411a'
down_revision: Union[str, Sequence[str], None] = 'e32a24595b8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "photos",
        sa.Column(
            "is_archived",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        )
    )


def downgrade() -> None:

    op.drop_column(
        "photos",
        "is_archived"
    )