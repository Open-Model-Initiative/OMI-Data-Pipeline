"""'Add content source'

Revision ID: 703075477888
Revises: 37d01b99209f
Create Date: 2024-08-17 06:19:39.007777

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import Enum, text
from odr_core.schemas.user import UserType

# revision identifiers, used by Alembic.
revision: str = "703075477888"
down_revision: Union[str, None] = "37d01b99209f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "content_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=True),
        sa.Column(
            "type",
            sa.Enum("URL", "PATH", "HUGGING_FACE", name="contentsourcetype"),
            nullable=True,
        ),
        sa.Column("value", sa.String(), nullable=True),
        sa.Column(
            "source_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["contents.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_content_sources_id"), "content_sources", ["id"], unique=False
    )
    op.drop_column("contents", "url")

    # Create the enum type
    user_type_enum = Enum(UserType, name="usertype")
    user_type_enum.create(op.get_bind(), checkfirst=True)

    # Update existing values to ensure they match the new enum
    op.execute(
        "UPDATE users SET user_type = 'user' WHERE user_type IS NULL OR user_type = ''"
    )

    # Remove the default value
    op.alter_column("users", "user_type", server_default=None)

    # Alter the column type with explicit casting
    op.execute(
        text(
            "ALTER TABLE users ALTER COLUMN user_type TYPE usertype USING user_type::text::usertype"
        )
    )

    # Set the default value after changing the column type
    op.alter_column(
        "users",
        "user_type",
        type_=user_type_enum,
        nullable=False,
        server_default=text("'user'::usertype"),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Remove the default value
    op.alter_column("users", "user_type", server_default=None)

    # Revert the column type
    op.alter_column("users", "user_type", type_=sa.VARCHAR(length=255), nullable=False)

    # Set the default value back to 'user' as a string
    op.alter_column("users", "user_type", server_default=text("'user'"))

    # Drop the enum type
    sa.Enum(name="usertype").drop(op.get_bind(), checkfirst=True)

    op.add_column(
        "contents",
        sa.Column(
            "url", postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True
        ),
    )
    op.drop_index(op.f("ix_content_sources_id"), table_name="content_sources")
    op.drop_table("content_sources")

    # ### end Alembic commands ###