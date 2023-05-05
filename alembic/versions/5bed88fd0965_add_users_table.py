"""add users table

Revision ID: 5bed88fd0965
Revises: 85ed5193faa7
Create Date: 2023-05-04 20:06:11.596484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bed88fd0965'
down_revision = '85ed5193faa7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer, nullable=False),
                 sa.Column('email', sa.String(), nullable=False),
                 sa.Column('password', sa.String(), nullable=False),
                 sa.Column('create_at', sa.TIMESTAMP(timezone=True),server_default=sa.text("now()") ,nullable=False),
                 sa.PrimaryKeyConstraint('id'),
                 sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
