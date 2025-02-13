"""Update big

Revision ID: d65515d1f98a
Revises: 5f253486fcfb
Create Date: 2025-01-27 20:40:48.117308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd65515d1f98a'
down_revision: Union[str, None] = '5f253486fcfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('employer', sa.Column('location_id', sa.Integer(), nullable=True))
    op.drop_column('employer', 'is_active')
    op.add_column('employer_in_work_day', sa.Column('employer_fio', sa.Integer(), nullable=False))
    op.drop_column('employer_in_work_day', 'employer_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employer_in_work_day', sa.Column('employer_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'employer_in_work_day', type_='foreignkey')
    op.create_foreign_key('employer_in_work_day_employer_id_fkey', 'employer_in_work_day', 'employer', ['employer_id'], ['id'])
    op.drop_column('employer_in_work_day', 'employer_fio')
    op.add_column('employer', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'employer', type_='foreignkey')
    op.drop_column('employer', 'location_id')
    op.drop_table('location')
    # ### end Alembic commands ###
