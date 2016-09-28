"""Typo: predicted, not predicated.

Revision ID: f8b3a9075001
Revises: d8cff2c7e991
Create Date: 2016-09-28 06:51:18.353043

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f8b3a9075001'
down_revision = 'd8cff2c7e991'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('flight',
                    column_name='predicated_departure',
                    new_column_name='predicted_departure',
                    existing_type=sa.DateTime(),
                    existing_nullable=True)


def downgrade():
    op.alter_column('flight',
                    new_column_name='predicated_departure',
                    column_name='predicted_departure',
                    existing_type=sa.DateTime(),
                    existing_nullable=True)
