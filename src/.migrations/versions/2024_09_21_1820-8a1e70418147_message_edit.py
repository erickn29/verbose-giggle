"""message_edit

Revision ID: 8a1e70418147
Revises: d11b03287664
Create Date: 2024-09-21 18:20:40.086192

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a1e70418147"
down_revision: Union[str, None] = "d11b03287664"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f("uq_chat_id"), "chat", ["id"])
    op.add_column(
        "message", sa.Column("is_user_message", sa.Boolean(), nullable=False)
    )
    op.create_unique_constraint(op.f("uq_message_id"), "message", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_message_id"), "message", type_="unique")
    op.drop_column("message", "is_user_message")
    op.drop_constraint(op.f("uq_chat_id"), "chat", type_="unique")
    # ### end Alembic commands ###
