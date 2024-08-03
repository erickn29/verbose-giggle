from datetime import datetime
from uuid import UUID

from core.database import Base
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(32), doc="Электронная почта", unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(512), doc="Пароль", nullable=False)
    is_active: Mapped[bool] = mapped_column(doc="Активен", default=True)
    is_admin: Mapped[bool] = mapped_column(doc="Админ", default=False)

    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined"
    )
    employer = relationship(
        "Employer",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined"
    )
