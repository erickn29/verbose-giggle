from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from v1.vacancy.model.model import Experience, Language, Speciality


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
    id: UUID
    created_at: datetime
    updated_at: datetime


class CompanyInputSchema(BaseModel):
    name: str
    description: str | None = None
    city_id: UUID | None = None


class CompanyOutputSchema(CompanyInputSchema):
    id: UUID
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
]


class VacancyInputSchema(BaseModel):
    title: str
    description: str | None = None
    language: LanguageLiteral
    speciality: SpecialityLiteral
    experience: ExperienceLiteral
    salary_from: int | None = None
    salary_to: int | None = None
    company_id: UUID | None = None


class VacancyOutputSchema(VacancyInputSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    tool: list[ToolOutputSchema] | None = []


class VacancyListOutputSchema(BaseModel):
    vacancies: list[VacancyOutputSchema]


class VacancyCreateSchema(BaseModel):
    city: CityInputSchema
    company: CompanyInputSchema
    vacancy: VacancyInputSchema
    tool: list[ToolInputSchema] | None = []
