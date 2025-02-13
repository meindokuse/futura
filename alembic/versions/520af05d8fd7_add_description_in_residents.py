"""Add description in residents

Revision ID: 520af05d8fd7
Revises: a36031124d40
Create Date: 2025-02-08 00:01:26.657819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '520af05d8fd7'
down_revision: Union[str, None] = 'a36031124d40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('residents', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('residents', 'description')
    # ### end Alembic commands ###
