"""Init 3

Revision ID: fcbc44d095d7
Revises: aef369591a5b
Create Date: 2025-03-07 18:06:57.472042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcbc44d095d7'
down_revision: Union[str, None] = 'aef369591a5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
