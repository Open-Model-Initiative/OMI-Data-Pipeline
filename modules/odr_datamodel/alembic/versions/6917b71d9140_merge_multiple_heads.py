"""merge multiple heads

Revision ID: 6917b71d9140
Revises: 282031c50195, a72b966658fb
Create Date: 2024-09-27 21:44:58.708711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6917b71d9140'
down_revision: Union[str, None] = ('282031c50195', 'a72b966658fb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
