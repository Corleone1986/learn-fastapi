"""add lase few columns  to posts table

Revision ID: d1ce2d0221d2
Revises: 464b28ee2b62
Create Date: 2023-05-04 21:33:35.013918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1ce2d0221d2'
down_revision = '464b28ee2b62'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'create_at')
    pass
