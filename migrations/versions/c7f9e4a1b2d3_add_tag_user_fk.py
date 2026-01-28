"""add tag.user_id

Revision ID: c7f9e4a1b2d3
Revises: 93a660c66a32
Create Date: 2026-01-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7f9e4a1b2d3'
down_revision = '93a660c66a32'
branch_labels = None
depends_on = None


def upgrade():
    # add user_id column to tags (nullable for existing rows)
    op.add_column('tags', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_tags_user_id_users', 'tags', 'users', ['user_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_tags_user_id_users', 'tags', type_='foreignkey')
    op.drop_column('tags', 'user_id')
