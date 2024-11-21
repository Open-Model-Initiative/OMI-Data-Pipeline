# SPDX-License-Identifier: Apache-2.0
"""'Enable pgvector extension'

Revision ID: 0eb4fb67e01c
Revises: 7f105df0e1ed
Create Date: 2024-08-05 21:22:33.632850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb4fb67e01c'
down_revision: Union[str, None] = '7f105df0e1ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
    # ### end Alembic commands ###
