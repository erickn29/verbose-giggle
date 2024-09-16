from uuid import UUID

from base.model import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RecoveryToken(Base):
    __tablename__ = "recovery_token"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        doc="Пользователь",
    )
    token: Mapped[str] = mapped_column(String(32), doc="Токен")
    is_used: Mapped[bool] = mapped_column(doc="Использован", default=False)

    user = relationship("User", back_populates="recovery_tokens", lazy="joined")
