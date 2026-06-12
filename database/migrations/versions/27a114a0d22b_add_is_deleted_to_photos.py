"""add_is_deleted_to_photos"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "27a114a0d22b"
down_revision: Union[str, Sequence[str], None] = "48c784d5f048"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "photos",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


def downgrade() -> None:
    op.drop_column("photos", "is_deleted")