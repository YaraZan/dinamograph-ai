"""Change default value for public_id

Revision ID: 345460bda0c2
Revises: 71a6c3ee6061
Create Date: 2024-01-31 07:08:43.221586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '345460bda0c2'
down_revision: Union[str, None] = '71a6c3ee6061'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('ai_models', 'public_id', server_default=None)
    op.alter_column('roles', 'public_id', server_default=None)
    op.alter_column('users', 'public_id', server_default=None)
    op.alter_column('api_keys', 'public_id', server_default=None)


def downgrade() -> None:
    op.alter_column('ai_models', 'public_id', server_default='uuid-ossp')
    op.alter_column('roles', 'public_id', server_default='uuid-ossp')
    op.alter_column('users', 'public_id', server_default='uuid-ossp')
    op.alter_column('api_keys', 'public_id', server_default='uuid-ossp')
