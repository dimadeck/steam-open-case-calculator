"""Added models to DB

Revision ID: feedd99c7de0
Revises: 
Create Date: 2022-07-22 18:39:50.172728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feedd99c7de0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('profile_id', sa.BigInteger(), nullable=True),
    sa.Column('asset_id', sa.BigInteger(), nullable=False),
    sa.Column('class_id', sa.BigInteger(), nullable=True),
    sa.Column('instance_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('item_type', sa.String(), nullable=True),
    sa.Column('weapon', sa.String(), nullable=True),
    sa.Column('exterior', sa.String(), nullable=True),
    sa.Column('rarity', sa.String(), nullable=True),
    sa.Column('rarity_color', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('item_float', sa.Numeric(), nullable=True),
    sa.Column('is_shown', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('asset_id')
    )
    op.create_index(op.f('ix_items_profile_id'), 'items', ['profile_id'], unique=False)
    op.create_table('observed_profiles',
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.Column('last_asset_id', sa.BigInteger(), nullable=True),
    sa.Column('is_observed', sa.Boolean(), nullable=True),
    sa.Column('last_modified_date', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Numeric(), nullable=True),
    sa.Column('total_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('profile_id')
    )
    op.create_index(op.f('ix_observed_profiles_profile_id'), 'observed_profiles', ['profile_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_observed_profiles_profile_id'), table_name='observed_profiles')
    op.drop_table('observed_profiles')
    op.drop_index(op.f('ix_items_profile_id'), table_name='items')
    op.drop_table('items')
    # ### end Alembic commands ###
