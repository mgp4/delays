"""Carriers: some columns need to be larger.

Revision ID: fa2c791c2546
Revises: a1aaff57e2ff
Create Date: 2016-10-13 22:31:23.091094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa2c791c2546'
down_revision = 'a1aaff57e2ff'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('carrier', 'call_sign',
               existing_type=sa.String(length=3),
               type_=sa.String(length=70),
               existing_nullable=True)
    op.alter_column('carrier', 'name',
               existing_type=sa.String(length=70),
               type_=sa.String(length=100),
               existing_nullable=True)


def downgrade():
    op.alter_column('carrier', 'name',
               existing_type=sa.String(length=100),
               type_=sa.String(length=70),
               existing_nullable=True)
    op.alter_column('carrier', 'call_sign',
               existing_type=sa.String(length=70),
               type_=sa.String(length=3),
               existing_nullable=True)
