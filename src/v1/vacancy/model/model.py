from enum import Enum
from uuid import UUID

from core.database import Base
from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Language(Enum):
    python = "python"
    javascript = "javascript"
    java = "java"
    golang = "go"
    php = "php"
    plus_plus = "c++"
    sharp = "c#"
    sql = "sql"
    rust = "rust"


class Experience(Enum):
    no_experience = "без опыта"
    one_to_three = "от 1 до 3 лет"
    three_to_five = "от 3 до 5 лет"
    more_than_five = "более 5 лет"


class Speciality(Enum):
    developer = "разработка"
    analyst = "аналитика"
    devops = "devops"
    system_administrator = "системное администрирование"
    data_science = "дата-инженерия"
    machine_learning = "машинное обучение"
    project_manager = "управление проектами"
    team_lead = "руководство разработкой"
    architect = "архитектура проектов"
    cyber_security = "информационная безопасность"
    qa = "тестирование"


class Tool(Base):
    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    vacancies: Mapped[list["VacancyTool"]] = relationship(
        "VacancyTool",
        back_populates="tool",
    )


class City(Base):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    companies: Mapped[list["Company"]] = relationship(
        "Company",
        back_populates="city",
        lazy="selectin",
    )


class Company(Base):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    city_id: Mapped[UUID] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE"),
        nullable=False,
    )
    city: Mapped["City"] = relationship(
        "City", back_populates="companies", lazy="joined"
    )
    vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy",
        back_populates="company",
        lazy="selectin",
    )


class Vacancy(Base):
    __tablename__ = "vacancy"
    __table_args__ = (UniqueConstraint("company_id", "title", name="uq_company_title"),)

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(16), nullable=False)
    speciality: Mapped[str] = mapped_column(String(32), nullable=False)
    experience: Mapped[str] = mapped_column(String(32), nullable=False)
    salary_from: Mapped[int] = mapped_column(Integer, nullable=True)
    salary_to: Mapped[int] = mapped_column(Integer, nullable=True)
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
        nullable=False,
    )
    company: Mapped["Company"] = relationship(
        "Company", back_populates="vacancies", lazy="joined"
    )
    tools: Mapped[list["VacancyTool"]] = relationship(
        "VacancyTool",
        back_populates="vacancy",
        lazy="selectin",
    )
    link: Mapped[str] = mapped_column(Text, nullable=True)


class VacancyTool(Base):
    __tablename__ = "vacancy_tool"

    vacancy_id: Mapped[UUID] = mapped_column(
        ForeignKey("vacancy.id", ondelete="CASCADE"),
        nullable=False,
    )
    tool_id: Mapped[UUID] = mapped_column(
        ForeignKey("tool.id", ondelete="CASCADE"),
        nullable=False,
    )
    vacancy: Mapped["Vacancy"] = relationship(
        "Vacancy", back_populates="tools", lazy="joined"
    )
    tool: Mapped["Tool"] = relationship(
        "Tool", back_populates="vacancies", lazy="joined"
    )
