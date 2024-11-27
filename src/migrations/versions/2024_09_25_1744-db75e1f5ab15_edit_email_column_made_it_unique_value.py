"""edit email column: made it unique value

Revision ID: db75e1f5ab15
Revises: 3a0e08fc940e
Create Date: 2024-09-25 17:44:41.034907

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "db75e1f5ab15"
down_revision: Union[str, None] = "3a0e08fc940e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
