"""mass_at_unlock

Revision ID: 0005
Revises: 0004
Create Date: 2017-06-24 20:30:12.310006

"""

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mass_event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mass_at_unlock_kg', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mass_event', schema=None) as batch_op:
        batch_op.drop_column('mass_at_unlock_kg')

    # ### end Alembic commands ###
