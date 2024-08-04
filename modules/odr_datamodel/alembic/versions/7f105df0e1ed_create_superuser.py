"""'create superuser'

Revision ID: 7f105df0e1ed
Revises: a2a51ea2c819
Create Date: 2024-08-04 21:34:31.596650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from odr_core.config import settings
from odr_core.crud.user import password_hasher


# revision identifiers, used by Alembic.
revision: str = '7f105df0e1ed'
down_revision: Union[str, None] = 'a2a51ea2c819'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    username = settings.DEFAULT_SUPERUSER_USERNAME
    email = settings.DEFAULT_SUPERUSER_EMAIL
    password = password_hasher.hash(settings.DEFAULT_SUPERUSER_PASSWORD)
    is_active = True
    is_superuser = True
    created_at = sa.func.now()
    updated_at = sa.func.now()

    # create superuser
    op.execute(
        f"""
        INSERT INTO "users" (username, email, hashed_password, is_active, is_superuser, created_at, updated_at)
        VALUES ('{username}', '{email}', '{password}', {is_active}, {is_superuser}, '{created_at}', '{updated_at}')
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # delete superuser
    username = settings.DEFAULT_SUPERUSER_USERNAME
    email = settings.DEFAULT_SUPERUSER_EMAIL

    op.execute(
        f"""
        DELETE FROM "users" WHERE username = '{username}' AND email = '{email}'
        """
    )
    # ### end Alembic commands ###
