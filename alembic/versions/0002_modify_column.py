from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"


def upgrade():
    op.add_column("models", sa.Column("server", sa.String()))
    op.alter_column("models", "id", existing_type=sa.String(), nullable=False)
    op.alter_column("models", "created_at", existing_type=sa.TIMESTAMP(), nullable=False)

    op.add_column("ml_backends", sa.Column("status", sa.String()))
    op.add_column("ml_backends", sa.Column("endpoint", sa.String()))


def downgrade():
    op.drop_constraint("pk_models", "models", type_="primary")
    op.alter_column("models", "id", existing_type=sa.String(), nullable=True)
    op.alter_column("models", "created_at", existing_type=sa.TIMESTAMP(), nullable=True)
    op.drop_column("models", "server")

    op.drop_column("ml_backends", "status")
    op.drop_column("ml_backends", "endpoint")
