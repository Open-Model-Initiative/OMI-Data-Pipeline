# SPDX-License-Identifier: Apache-2.0
"""Add annotations and embedding models

Revision ID: 3e141c1abc3f
Revises: d712027f6e8b
Create Date: 2024-07-20 14:25:21.662996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e141c1abc3f'
down_revision: Union[str, None] = 'd712027f6e8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'embedding_engines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_embedding_engines_id'), 'embedding_engines', ['id'], unique=False)
    op.create_index(op.f('ix_embedding_engines_name'), 'embedding_engines', ['name'], unique=False)
    op.create_table(
        'annotation_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('ecosystem', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('annotation_schema', sa.JSON(), nullable=True),
        sa.Column('license', sa.String(), nullable=True),
        sa.Column('license_url', sa.String(), nullable=True),
        sa.Column('added_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['added_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotation_sources_id'), 'annotation_sources', ['id'], unique=False)
    op.create_index(op.f('ix_annotation_sources_name'), 'annotation_sources', ['name'], unique=False)
    op.create_table(
        'annotations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=True),
        sa.Column('annotation', sa.JSON(), nullable=True),
        sa.Column('manually_adjusted', sa.Boolean(), nullable=True),
        sa.Column('overall_rating', sa.Float(), nullable=True),
        sa.Column('from_user_id', sa.Integer(), nullable=True),
        sa.Column('from_team_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['content_id'], ['contents.id'], ),
        sa.ForeignKeyConstraint(['from_team_id'], ['teams.id'], ),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotations_id'), 'annotations', ['id'], unique=False)
    op.create_table(
        'content_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('embedding_engine_id', sa.Integer(), nullable=True),
        sa.Column('from_user_id', sa.Integer(), nullable=True),
        sa.Column('from_team_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['content_id'], ['contents.id'], ),
        sa.ForeignKeyConstraint(['embedding_engine_id'], ['embedding_engines.id'], ),
        sa.ForeignKeyConstraint(['from_team_id'], ['teams.id'], ),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_embeddings_id'), 'content_embeddings', ['id'], unique=False)
    op.create_table(
        'annotation_embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('annotation_id', sa.Integer(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('embedding_engine_id', sa.Integer(), nullable=True),
        sa.Column('from_user_id', sa.Integer(), nullable=True),
        sa.Column('from_team_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
        sa.ForeignKeyConstraint(['embedding_engine_id'], ['embedding_engines.id'], ),
        sa.ForeignKeyConstraint(['from_team_id'], ['teams.id'], ),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotation_embeddings_id'), 'annotation_embeddings', ['id'], unique=False)
    op.create_table(
        'annotation_ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('annotation_id', sa.Integer(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('rated_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
        sa.ForeignKeyConstraint(['rated_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotation_ratings_id'), 'annotation_ratings', ['id'], unique=False)
    op.create_table(
        'annotation_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('annotation_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('reported_by_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
        sa.ForeignKeyConstraint(['reported_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annotation_reports_id'), 'annotation_reports', ['id'], unique=False)
    op.create_table(
        'annotation_sources_link',
        sa.Column('annotation_id', sa.Integer(), nullable=False),
        sa.Column('annotation_source_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['annotation_id'], ['annotations.id'], ),
        sa.ForeignKeyConstraint(['annotation_source_id'], ['annotation_sources.id'], ),
        sa.PrimaryKeyConstraint('annotation_id', 'annotation_source_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('annotation_sources_link')
    op.drop_index(op.f('ix_annotation_reports_id'), table_name='annotation_reports')
    op.drop_table('annotation_reports')
    op.drop_index(op.f('ix_annotation_ratings_id'), table_name='annotation_ratings')
    op.drop_table('annotation_ratings')
    op.drop_index(op.f('ix_annotation_embeddings_id'), table_name='annotation_embeddings')
    op.drop_table('annotation_embeddings')
    op.drop_index(op.f('ix_content_embeddings_id'), table_name='content_embeddings')
    op.drop_table('content_embeddings')
    op.drop_index(op.f('ix_annotations_id'), table_name='annotations')
    op.drop_table('annotations')
    op.drop_index(op.f('ix_annotation_sources_name'), table_name='annotation_sources')
    op.drop_index(op.f('ix_annotation_sources_id'), table_name='annotation_sources')
    op.drop_table('annotation_sources')
    op.drop_index(op.f('ix_embedding_engines_name'), table_name='embedding_engines')
    op.drop_index(op.f('ix_embedding_engines_id'), table_name='embedding_engines')
    op.drop_table('embedding_engines')
    # ### end Alembic commands ###
