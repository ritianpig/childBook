"""empty message

Revision ID: a2a2748470dc
Revises: effb90d2fa81
Create Date: 2018-11-18 19:00:16.592122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a2748470dc'
down_revision = 'effb90d2fa81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('form_id', sa.String(length=200), nullable=True))
    op.add_column('users', sa.Column('login_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'login_time')
    op.drop_column('users', 'form_id')
    # ### end Alembic commands ###
