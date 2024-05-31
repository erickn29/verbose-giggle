from enum import Enum
from uuid import UUID

from sqlalchemy.dialects import postgresql

from core.database import Base
from sqlalchemy import ForeignKey, String, Text, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Language(Enum):
    python = "Python"
    javascript = "JavaScript"
    java = "Java"
    golang = "Go"
    php = "PHP"
    plus_plus = "C++"
    sharp = "C#"
    sql = "SQL"
    rust = "Rust"


class Experience(Enum):
    no_experience = "Без опыта"
    one_to_three = "От 1 до 3 лет"
    three_to_five = "От 3 до 5 лет"
    more_than_five = "Более 5 лет"


class Speciality(Enum):
    developer = "Developer"
    analyst = "Analyst"
    devops = "DevOps"
    system_administrator = "System Administrator"
    data_science = "Data Science"
    machine_learning = "Machine Learning"
    project_manager = "Project Management"
    team_lead = "Team Lead"
    architect = "Architect"


class Tool(Base):
    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
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
    __table_args__ = (UniqueConstraint('company_id', 'title', name='uq_company_title'),)

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(
        postgresql.ENUM(*[o.value for o in Language], name="language"),
        doc="Страница сайта",
    )
    speciality: Mapped[str] = mapped_column(
        postgresql.ENUM(*[o.value for o in Speciality], name="speciality"),
        doc="Страница сайта",
    )
    experience: Mapped[str] = mapped_column(
        postgresql.ENUM(*[o.value for o in Experience], name="experience"),
        doc="Страница сайта",
    )
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
