"""create posts table

Revision ID: 6bee96d9e980
Revises: 
Create Date: 2023-05-04 17:11:08.042890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bee96d9e980'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts" ,sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
