"""empty message

Revision ID: 3612a4a275f7
Revises: 7a83e38a868f
Create Date: 2018-11-27 10:53:54.522878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3612a4a275f7'
down_revision = '7a83e38a868f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_order', sa.Column('timestamp', sa.String(length=100), nullable=True))
    op.drop_column('user_order', 'order_num')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_order', sa.Column('order_num', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('user_order', 'timestamp')
    # ### end Alembic commands ###
