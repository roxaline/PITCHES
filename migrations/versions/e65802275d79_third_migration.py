"""third Migration

Revision ID: e65802275d79
Revises: 33915667acb4
Create Date: 2019-03-01 13:10:01.056714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e65802275d79'
down_revision = '33915667acb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitches', sa.Column('dislike', sa.Integer(), nullable=True))
    op.add_column('pitches', sa.Column('like', sa.Integer(), nullable=True))
    op.drop_column('pitches', 'downvote')
    op.drop_column('pitches', 'upvote')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitches', sa.Column('upvote', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('pitches', sa.Column('downvote', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('pitches', 'like')
    op.drop_column('pitches', 'dislike')
    # ### end Alembic commands ###
