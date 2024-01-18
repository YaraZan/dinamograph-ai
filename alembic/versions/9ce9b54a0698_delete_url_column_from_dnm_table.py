"""Delete url column from dnm table

Revision ID: 9ce9b54a0698
Revises: f2d347b35b0c
Create Date: 2024-01-18 10:01:16.930192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ce9b54a0698'
down_revision: Union[str, None] = 'f2d347b35b0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('markers', 'url')
    # ### end Alembic commands ###


def downgrade() -> None:
    op.add_column('markers', sa.Column('url', sa.String(), nullable=True))
    # ### end Alembic commands ###
