"""empty message

Revision ID: b22d35f809a5
Revises: 83b9ec2b26a1
Create Date: 2020-04-20 10:07:53.999882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b22d35f809a5'
down_revision = '83b9ec2b26a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('slug', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'slug')
    # ### end Alembic commands ###
