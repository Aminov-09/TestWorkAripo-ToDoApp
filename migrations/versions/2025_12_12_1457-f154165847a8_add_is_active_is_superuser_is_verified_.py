"""Add is_active, is_superuser, is_verified back

Revision ID: f154165847a8
Revises: 1dd985b54675
Create Date: 2025-12-12 14:57:18.786197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f154165847a8'
down_revision: Union[str, Sequence[str], None] = '1dd985b54675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))


def downgrade():
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_verified')

