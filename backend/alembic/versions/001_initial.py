"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-15 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('youtube_refresh_token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create providers table
    op.create_table('providers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('config', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_providers_name'), 'providers', ['name'], unique=True)
    
    # Create items table
    op.create_table('items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('poster_url', sa.String(), nullable=True),
        sa.Column('overview', sa.Text(), nullable=True),
        sa.Column('genres', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('runtime', sa.Integer(), nullable=True),
        sa.Column('tmdb_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_external_id'), 'items', ['external_id'], unique=False)
    op.create_index(op.f('ix_items_source'), 'items', ['source'], unique=False)
    op.create_index(op.f('ix_items_title'), 'items', ['title'], unique=False)
    op.create_index(op.f('ix_items_tmdb_id'), 'items', ['tmdb_id'], unique=False)
    
    # Create events table
    op.create_table('events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(), nullable=False),
        sa.Column('raw', postgresql.JSON(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_user_id'), 'events', ['user_id'], unique=False)
    op.create_index(op.f('ix_events_item_id'), 'events', ['item_id'], unique=False)
    op.create_index(op.f('ix_events_provider_id'), 'events', ['provider_id'], unique=False)
    op.create_index(op.f('ix_events_event_type'), 'events', ['event_type'], unique=False)
    op.create_index(op.f('ix_events_occurred_at'), 'events', ['occurred_at'], unique=False)
    
    # Create embeddings table with pgvector
    op.create_table('embeddings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('vector', sa.dialects.postgresql.VECTOR(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('dimensions', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_embeddings_item_id'), 'embeddings', ['item_id'], unique=False)
    op.create_index(op.f('ix_embeddings_model'), 'embeddings', ['model'], unique=False)
    
    # Create recommendations table
    op.create_table('recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('algorithm', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recommendations_user_id'), 'recommendations', ['user_id'], unique=False)
    op.create_index(op.f('ix_recommendations_item_id'), 'recommendations', ['item_id'], unique=False)
    op.create_index(op.f('ix_recommendations_score'), 'recommendations', ['score'], unique=False)
    
    # Add foreign key constraints
    op.create_foreign_key(None, 'events', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'events', 'items', ['item_id'], ['id'])
    op.create_foreign_key(None, 'events', 'providers', ['provider_id'], ['id'])
    op.create_foreign_key(None, 'embeddings', 'items', ['item_id'], ['id'])
    op.create_foreign_key(None, 'recommendations', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'recommendations', 'items', ['item_id'], ['id'])


def downgrade() -> None:
    # Remove foreign key constraints
    op.drop_constraint(None, 'recommendations', type_='foreignkey')
    op.drop_constraint(None, 'recommendations', type_='foreignkey')
    op.drop_constraint(None, 'embeddings', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='foreignkey')
    
    # Drop tables
    op.drop_index(op.f('ix_recommendations_score'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_item_id'), table_name='recommendations')
    op.drop_index(op.f('ix_recommendations_user_id'), table_name='recommendations')
    op.drop_table('recommendations')
    
    op.drop_index(op.f('ix_embeddings_model'), table_name='embeddings')
    op.drop_index(op.f('ix_embeddings_item_id'), table_name='embeddings')
    op.drop_table('embeddings')
    
    op.drop_index(op.f('ix_events_occurred_at'), table_name='events')
    op.drop_index(op.f('ix_events_event_type'), table_name='events')
    op.drop_index(op.f('ix_events_provider_id'), table_name='events')
    op.drop_index(op.f('ix_events_item_id'), table_name='events')
    op.drop_index(op.f('ix_events_user_id'), table_name='events')
    op.drop_table('events')
    
    op.drop_index(op.f('ix_items_tmdb_id'), table_name='items')
    op.drop_index(op.f('ix_items_title'), table_name='items')
    op.drop_index(op.f('ix_items_source'), table_name='items')
    op.drop_index(op.f('ix_items_external_id'), table_name='items')
    op.drop_table('items')
    
    op.drop_index(op.f('ix_providers_name'), table_name='providers')
    op.drop_table('providers')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
