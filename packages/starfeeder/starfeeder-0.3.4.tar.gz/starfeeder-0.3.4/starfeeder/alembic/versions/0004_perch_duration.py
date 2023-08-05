"""perch_duration

Revision ID: 0004
Revises: 0003
Create Date: 2017-06-24 15:59:50.671146

"""

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from cardinal_pythonlib.sqlalchemy.arrow_types import ArrowMicrosecondType


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mass_event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unlocked_at', ArrowMicrosecondType(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mass_event', schema=None) as batch_op:
        batch_op.drop_column('unlocked_at')

    # ### end Alembic commands ###
