"""Migracion Inicial de prueba

Revision ID: 57286e62b45b
Revises: 
Create Date: 2020-04-08 12:56:54.711336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57286e62b45b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('asdas', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'asdas')
    # ### end Alembic commands ###
