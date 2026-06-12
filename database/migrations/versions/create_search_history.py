from alembic import op
import sqlalchemy as sa


revision = "create_search_history"

down_revision = "8280f068ab51"

branch_labels = None

depends_on = None


def upgrade():

    op.create_table(
        "search_history",

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
            "query",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        )
    )


def downgrade():

    op.drop_table(
        "search_history"
    )