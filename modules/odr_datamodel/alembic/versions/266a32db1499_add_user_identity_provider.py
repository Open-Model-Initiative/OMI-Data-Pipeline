"""'Add user identity provider'

Revision ID: 266a32db1499
Revises: b27020226eaf
Create Date: 2024-09-13 01:27:40.745429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '266a32db1499'
down_revision: Union[str, None] = 'b27020226eaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('identity_provider', sa.String(), nullable=True))
    # set default value for identity_provider
    op.execute("UPDATE users SET identity_provider = 'omi'")
    op.create_index(op.f('ix_users_identity_provider'), 'users', ['identity_provider'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_identity_provider'), table_name='users')
    op.drop_column('users', 'identity_provider')
    # ### end Alembic commands ###