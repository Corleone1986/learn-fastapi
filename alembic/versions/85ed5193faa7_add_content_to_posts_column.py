"""add content to posts column

Revision ID: 85ed5193faa7
Revises: 6bee96d9e980
Create Date: 2023-05-04 17:23:46.736752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85ed5193faa7'
down_revision = '6bee96d9e980'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
