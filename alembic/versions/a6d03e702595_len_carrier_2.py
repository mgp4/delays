"""len(Carrier) > 2

Revision ID: a6d03e702595
Revises: 00f0f9915d1d
Create Date: 2016-09-28 03:59:20.296736

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a6d03e702595'
down_revision = '00f0f9915d1d'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('flight', 'carrier',
               existing_type=sa.String(length=2),
               type_=sa.String(length=3),
               existing_nullable=False)


def downgrade():
    op.alter_column('flight', 'carrier',
               existing_type=sa.String(length=3),
               type_=sa.String(length=2),
               existing_nullable=False)
