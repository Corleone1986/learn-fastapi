"""add foreign-key to posts table

Revision ID: 464b28ee2b62
Revises: 5bed88fd0965
Create Date: 2023-05-04 21:21:33.650103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464b28ee2b62'
down_revision = '5bed88fd0965'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer(), nullable=False , ))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

    pass
