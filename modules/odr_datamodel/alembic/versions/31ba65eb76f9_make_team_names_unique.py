# SPDX-License-Identifier: Apache-2.0
"""'Make team names unique'

Revision ID: 31ba65eb76f9
Revises: 2f2d84a873f5
Create Date: 2024-10-11 22:11:44.302197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31ba65eb76f9'
down_revision: Union[str, None] = '2f2d84a873f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_team_name', 'teams', ['name'])


def downgrade() -> None:
    op.drop_constraint('unique_team_name', 'teams', type_='unique')
