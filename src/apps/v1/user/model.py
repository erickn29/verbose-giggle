from base.model import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.v1.vacancy.model import Employee, Employer


class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(32), doc="Электронная почта", unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(512), doc="Пароль", nullable=False)
    is_active: Mapped[bool] = mapped_column(doc="Активен", default=True)
    is_admin: Mapped[bool] = mapped_column(doc="Админ", default=False)
    is_verified: Mapped[bool] = mapped_column(doc="Email подтвержден", default=False)
    coin: Mapped[int] = mapped_column(doc="Токены", default=0)
    
    recovery_tokens: Mapped[list["RecoveryToken"]] = relationship(
        back_populates="user", lazy="selectin"
    )

    employee: Mapped[Employee] = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined",
    )
    employer: Mapped[Employer] = relationship(
        "Employer",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="joined",
    )