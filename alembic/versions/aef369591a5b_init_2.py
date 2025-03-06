"""Init 2

Revision ID: aef369591a5b
Revises: 520af05d8fd7
Create Date: 2025-03-07 00:53:42.549499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aef369591a5b'
down_revision: Union[str, None] = '520af05d8fd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
