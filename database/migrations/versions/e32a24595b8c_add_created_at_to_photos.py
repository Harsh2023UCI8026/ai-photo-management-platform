"""add_created_at_to_photos

Revision ID: e32a24595b8c
Revises: 3a8b0ba62632
Create Date: 2026-06-21 23:52:32.057615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e32a24595b8c'
down_revision: Union[str, Sequence[str], None] = '3a8b0ba62632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "photos",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )




def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "photos",
        "created_at"
    )