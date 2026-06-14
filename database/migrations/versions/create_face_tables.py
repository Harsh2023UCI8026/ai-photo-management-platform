from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "create_face_tables"

down_revision = "create_search_history"

branch_labels = None

depends_on = None


def upgrade():

    op.create_table(
        "face_clusters",

        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),

        sa.Column(
            "label",
            sa.String(255),
            nullable=True
        )
    )

    op.create_table(
        "faces",

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
            "cluster_id",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "embedding",
            postgresql.JSONB(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["photo_id"],
            ["photos.id"]
        )
    )


def downgrade():

    op.drop_table("faces")
    op.drop_table("face_clusters")