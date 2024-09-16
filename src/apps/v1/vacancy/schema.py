from datetime import datetime
from typing import Literal
from uuid import UUID

from apps.v1.vacancy.model import Experience, Language, Speciality
from utils.pagination import PaginationSchema

from pydantic import BaseModel, ConfigDict


class ToolInputSchema(BaseModel):
    name: str


class ToolOutputSchema(ToolInputSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    name: str


class VacancyToolSchema(BaseModel):
    vacancy_id: UUID
    tool_id: UUID


class CityInputSchema(BaseModel):
    name: str


class CityOutputSchema(CityInputSchema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


class CompanyInputSchema(BaseModel):
    name: str
    description: str | None = None
    city_id: UUID | None = None


class CompanyOutputSchema(CompanyInputSchema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    city: CityOutputSchema
    created_at: datetime
    updated_at: datetime


LanguageLiteral = Literal[
    Language.python.value,
    Language.javascript.value,
    Language.java.value,
    Language.golang.value,
    Language.php.value,
    Language.plus_plus.value,
    Language.sharp.value,
    Language.sql.value,
    Language.rust.value,
]

ExperienceLiteral = Literal[
    Experience.no_experience.value,
    Experience.no_experience.value,
    Experience.one_to_three.value,
    Experience.three_to_five.value,
    Experience.more_than_five.value,
]

SpecialityLiteral = Literal[
    Speciality.developer.value,
    Speciality.analyst.value,
    Speciality.devops.value,
    Speciality.system_administrator.value,
    Speciality.data_science.value,
    Speciality.machine_learning.value,
    Speciality.project_manager.value,
    Speciality.team_lead.value,
    Speciality.architect.value,
    Speciality.qa.value,
    Speciality.cyber_security.value,
]


class VacancyInputSchema(BaseModel):
    title: str
    description: str | None = None
    language: LanguageLiteral
    speciality: SpecialityLiteral
    experience: ExperienceLiteral
    is_publish: bool = True
    salary_from: int | None = None
    salary_to: int | None = None
    company_id: UUID | None = None


class VacancyOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    experience: str
    language: str
    speciality: str
    salary_from: int | None = None
    salary_to: int | None = None
    description: str | None = None
    is_publish: bool
    company: CompanyOutputSchema
    created_at: datetime
    updated_at: datetime
    tool: list[ToolOutputSchema] | None = []


class VacancyListOutputSchema(BaseModel):
    vacancies: list[VacancyOutputSchema]
    pagination: PaginationSchema


class VacancyCreateSchema(BaseModel):
    city: CityInputSchema
    company: CompanyInputSchema
    vacancy: VacancyInputSchema
    tool: list[ToolInputSchema] | None = []


class EmployeeInputSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = ""
    dob: datetime
    sex: bool


class ResumeToolSchema(BaseModel):
    resume_id: UUID
    tool_id: UUID


class ResumeInputSchema(BaseModel):
    position: str
    speciality: SpecialityLiteral
    description: str | None = None
    is_publish: bool = True


class JobPlaceInputSchema(BaseModel):
    company: str
    position: str
    speciality: str
    description: str | None = None
    start_date: datetime
    end_date: datetime | None = None


class JobPlaceOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company: str
    position: str
    speciality: str
    description: str = ""
    start_date: datetime
    end_date: datetime | None = None


class ResumeCreateSchema(BaseModel):
    resume: ResumeInputSchema
    job_place: list[JobPlaceInputSchema]
    tool: list[ToolInputSchema]


class ResumeOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    position: str
    speciality: str
    description: str
    is_publish: bool
    job_place: list[JobPlaceOutputSchema] = []
    tool: list[ToolOutputSchema] = []


class ResumeListOutputSchema(BaseModel):
    resumes: list[ResumeOutputSchema]
