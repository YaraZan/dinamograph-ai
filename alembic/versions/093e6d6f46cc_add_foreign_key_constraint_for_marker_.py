"""add foreign key constraint for marker_id in dnm table

Revision ID: 093e6d6f46cc
Revises: ddfe102fadb2
Create Date: 2024-01-23 16:42:45.912695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '093e6d6f46cc'
down_revision: Union[str, None] = 'ddfe102fadb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'dnm', 'markers', ['marker_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dnm', type ='foreignkey')
    # ### end Alembic commands ###