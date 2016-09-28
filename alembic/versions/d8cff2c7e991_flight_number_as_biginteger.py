"""Flight number as BigInteger.

Revision ID: d8cff2c7e991
Revises: a6d03e702595
Create Date: 2016-09-28 04:15:12.007518

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd8cff2c7e991'
down_revision = 'a6d03e702595'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('flight', 'flight_number',
               existing_type=sa.Integer(),
               type_=sa.BigInteger(),
               existing_nullable=False)


def downgrade():
    op.alter_column('flight', 'flight_number',
               existing_type=sa.BigInteger(),
               type_=sa.Integer(),
               existing_nullable=False)
