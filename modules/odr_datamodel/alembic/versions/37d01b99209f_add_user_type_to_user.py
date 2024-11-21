# SPDX-License-Identifier: Apache-2.0
"""'Add user_type to user'

Revision ID: 37d01b99209f
Revises: 4f394aae9708
Create Date: 2024-08-10 09:51:02.160329

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = "37d01b99209f"
down_revision: Union[str, None] = "4f394aae9708"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a temporary table object
    users = table("users", column("user_type", sa.String))

    # Add the user_type column if it doesn't exist
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS user_type VARCHAR(255)")

    # Set the default value for existing rows
    op.execute(
        users.update().values(user_type="user").where(users.c.user_type.is_(None))
    )

    # Alter the column to set the default for new rows
    op.alter_column(
        "users",
        "user_type",
        existing_type=sa.String(),
        nullable=False,
        server_default="user",
    )


def downgrade() -> None:
    # Remove the default
    op.alter_column(
        "users",
        "user_type",
        existing_type=sa.String(),
        nullable=True,
        server_default=None,
    )

    # Drop the column
    op.drop_column("users", "user_type")
