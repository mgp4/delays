"""Flight number can contain chars?

Revision ID: 23c1e61027c7
Revises: f8b3a9075001
Create Date: 2016-09-29 23:08:00.477721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23c1e61027c7'
down_revision = 'f8b3a9075001'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('flight', 'flight_number',
               existing_type=sa.BigInteger(),
               type_=sa.String(length=5),
               existing_nullable=False)


def downgrade():
    op.alter_column('flight', 'flight_number',
               existing_type=sa.String(length=5),
               type_=sa.BigInteger(),
               existing_nullable=False)
