from datetime import datetime

from apps.v1.auth.model import RecoveryToken
from apps.v1.interview.model import Chat
from base.model import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(256), doc="Электронная почта", unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(512), doc="Пароль", nullable=False)
    is_active: Mapped[bool] = mapped_column(doc="Активен", default=True)
    is_admin: Mapped[bool] = mapped_column(doc="Админ", default=False)
    is_verified: Mapped[bool] = mapped_column(doc="Email подтвержден", default=False)
    coin: Mapped[int] = mapped_column(doc="Токены", default=0)
    subscription: Mapped[datetime] = mapped_column(doc="Подписка до", nullable=True)

    recovery_tokens: Mapped[list["RecoveryToken"]] = relationship(
        back_populates="user", lazy="selectin"
    )
    chats: Mapped[list[Chat]] = relationship(
        "Chat", back_populates="user", lazy="selectin"
    )
    answers = relationship("Answer", back_populates="user", lazy="selectin")
    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined",
    )
    employer = relationship(
        "Employer",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined",
    )
