"""empty message

Revision ID: 6fba84e094d9
Revises: 3612a4a275f7
Create Date: 2018-11-27 18:22:17.315533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fba84e094d9'
down_revision = '3612a4a275f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_sign_in', sa.Column('days2', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_sign_in', 'days2')
    # ### end Alembic commands ###
