"""
Initial migration
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = ""


# Define the table schemas
def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("token", sa.String()),
        sa.Column("server", sa.String()),
        sa.Column("created_at", sa.TIMESTAMP()),
    )

    op.create_table(
        "models",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String()),
        sa.Column("project_id", sa.String()),
        sa.Column("created_at", sa.TIMESTAMP()),
        sa.UniqueConstraint("id", "user_id"),
    )

    op.create_table(
        "services",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("model_id", sa.String(), unique=True),
        sa.Column("user_id", sa.String(), unique=True),
        sa.Column("url", sa.Text()),
        sa.Column("created_at", sa.TIMESTAMP()),
        sa.UniqueConstraint("id", "user_id"),
    )

    op.create_table(
        "ml_backends",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), unique=True),
        sa.Column("project_id", sa.String(), unique=True),
        sa.Column("created_at", sa.TIMESTAMP()),
        sa.UniqueConstraint("id", "user_id"),
    )

    op.create_foreign_key(
        "fk_ml_backends_user_id",
        "ml_backends",
        "users",
        ["user_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_models_user_id",
        "models",
        "users",
        ["user_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_services_model_id",
        "services",
        "models",
        ["model_id", "user_id"],  # Update foreign key columns
        ["id", "user_id"],  # Update referenced columns
    )


def downgrade():
    op.drop_table("services")
    op.drop_table("models")
    op.drop_table("ml_backends")
    op.drop_table("users")