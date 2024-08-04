from datetime import datetime
from enum import Enum
from uuid import UUID

from core.database import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects import postgresql
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
    resumes: Mapped[list["ResumeTool"]] = relationship(
        "ResumeTool",
        back_populates="tool",
        lazy="selectin",
    )


class City(Base):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    companies: Mapped[list["Company"]] = relationship(
        "Company",
        back_populates="city",
        lazy="selectin",
    )


class Company(Base):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
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
    employer = relationship(
        "Employer",
        back_populates="company",
        lazy="joined",
        uselist=False,
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
    is_publish: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
        nullable=False,
    )
    company: Mapped["Company"] = relationship(
        "Company", back_populates="vacancies", lazy="selectin"
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


class ResumeTool(Base):
    __tablename__ = "resume_tool"

    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resume.id", ondelete="CASCADE"),
        nullable=False,
    )
    tool_id: Mapped[UUID] = mapped_column(
        ForeignKey("tool.id", ondelete="CASCADE"),
        nullable=False,
    )
    resume: Mapped["Resume"] = relationship(
        "Resume", back_populates="tools", lazy="joined"
    )
    tool: Mapped["Tool"] = relationship("Tool", back_populates="resumes", lazy="joined")


class Employer(Base):
    __tablename__ = "employer"
    __table_args__ = (
        UniqueConstraint("company_id", "user_id", name="uq_company_user"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("User", back_populates="employer", uselist=False, lazy="joined")
    company = relationship(
        "Company", back_populates="employer", uselist=False, lazy="joined"
    )


class Employee(Base):
    __tablename__ = "employee"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(32), doc="Имя")
    last_name: Mapped[str] = mapped_column(String(32), doc="Фамилия")
    patronymic: Mapped[str] = mapped_column(String(32), default="", doc="Отчество")
    dob: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    sex: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="employee", uselist=False, lazy="joined")
    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="employee",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Resume(Base):
    __tablename__ = "resume"

    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )
    position: Mapped[str] = mapped_column(Text, nullable=False)
    speciality: Mapped[str] = mapped_column(
        postgresql.ENUM(*[s.value for s in Speciality], name="speciality"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_publish: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tools: Mapped[list["ResumeTool"]] = relationship(
        "ResumeTool",
        back_populates="resume",
        lazy="selectin",
    )
    job_places: Mapped[list["JobPlace"]] = relationship(
        "JobPlace",
        back_populates="resume",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    employee: Mapped[Employee] = relationship(
        Employee, back_populates="resumes", uselist=False, lazy="joined"
    )


class JobPlace(Base):
    __tablename__ = "job_place"

    company: Mapped[str] = mapped_column(Text, nullable=False)
    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resume.id", ondelete="CASCADE"),
        nullable=False,
    )
    position: Mapped[str] = mapped_column(Text, nullable=False)
    speciality: Mapped[str] = mapped_column(
        postgresql.ENUM(*[s.value for s in Speciality], name="speciality"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=True,
    )

    resume: Mapped["Resume"] = relationship(
        "Resume", back_populates="job_places", lazy="joined"
    )
