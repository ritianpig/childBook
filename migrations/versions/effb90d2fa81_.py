"""empty message

Revision ID: effb90d2fa81
Revises: bdd6afa74598
Create Date: 2018-11-11 13:49:01.084471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'effb90d2fa81'
down_revision = 'bdd6afa74598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_messages', sa.Column('image', sa.String(length=200), nullable=True))
    op.drop_column('book_messages', 'cover')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_messages', sa.Column('cover', mysql.VARCHAR(length=200), nullable=True))
    op.drop_column('book_messages', 'image')
    # ### end Alembic commands ###
