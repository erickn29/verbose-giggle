from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(32), doc="Имя")
    last_name: Mapped[str] = mapped_column(String(32), doc="Фамилия")
    patronymic: Mapped[str] = mapped_column(String(32), default="", doc="Отчество")
    email: Mapped[str] = mapped_column(String(32), doc="Электронная почта", unique=True)
    password: Mapped[str] = mapped_column(String(512), doc="Пароль")
    is_active: Mapped[bool] = mapped_column(doc="Активен", default=True)
