"""Predicated departure column.

Revision ID: 00f0f9915d1d
Revises: 5def81573f31
Create Date: 2016-09-28 03:49:03.447803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f0f9915d1d'
down_revision = '5def81573f31'
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flight', sa.Column('predicated_departure', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flight', 'predicated_departure')
    ### end Alembic commands ###
