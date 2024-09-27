"""add_evals

Revision ID: fb7b557a82cf
Revises: 8a1e70418147
Create Date: 2024-09-27 11:37:10.464519

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fb7b557a82cf"
down_revision: Union[str, None] = "8a1e70418147"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "evaluation",
        sa.Column("answer_id", sa.UUID(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["answer_id"],
            ["answer.id"],
            name=op.f("fk_evaluation_answer_id_answer"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_evaluation")),
        sa.UniqueConstraint("id", name=op.f("uq_evaluation_id")),
    )
    op.add_column("message", sa.Column("type", sa.String(), nullable=False))
    op.drop_column("message", "is_user_message")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "message",
        sa.Column(
            "is_user_message",
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("message", "type")
    op.drop_table("evaluation")
    # ### end Alembic commands ###