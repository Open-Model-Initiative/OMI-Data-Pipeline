"""'Add dco_accepted column to users table'

Revision ID: a72b966658fb
Revises: 266a32db1499
Create Date: 2024-09-16 18:44:44.335931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a72b966658fb'
down_revision: Union[str, None] = '266a32db1499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('dco_accepted', sa.Boolean(), nullable=False, server_default='false'))
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('users', 'dco_accepted')
    # ### end Alembic commands ###
