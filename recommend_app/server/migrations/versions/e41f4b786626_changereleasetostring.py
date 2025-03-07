"""changereleasetostring

Revision ID: e41f4b786626
Revises: 83ea71b1da30
Create Date: 2024-06-17 14:44:26.099318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e41f4b786626'
down_revision = '83ea71b1da30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.alter_column('release_date',
               existing_type=sa.DATE(),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.alter_column('release_date',
               existing_type=sa.String(length=20),
               type_=sa.DATE(),
               existing_nullable=False)

    # ### end Alembic commands ###
