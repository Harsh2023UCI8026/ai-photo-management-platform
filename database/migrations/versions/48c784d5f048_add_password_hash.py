"""add password hash"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "48c784d5f048"
down_revision: Union[str, Sequence[str], None] = "5f2d55db53ed"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=True
        )
    )


def downgrade() -> None:

    op.drop_column(
        "users",
        "password_hash"
    )