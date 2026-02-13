"""created post table

Revision ID: 16a19e68c497
Revises: 
Create Date: 2026-02-14 01:09:27.251909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a19e68c497'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id",sa.Integer(), nullable = False , primary_key = True),
                    sa.Column("title",sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
