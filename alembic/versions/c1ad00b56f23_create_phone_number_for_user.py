"""Create phone number for user

Revision ID: c1ad00b56f23
Revises: 
Create Date: 2024-02-19 18:36:09.710666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1ad00b56f23'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number',sa.String,nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number');
