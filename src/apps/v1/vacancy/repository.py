from uuid import UUID

from apps.v1.vacancy.model import (
    City,
    Company,
    Employee,
    Employer,
    JobPlace,
    Resume,
    ResumeTool,
    Tool,
    Vacancy,
    VacancyTool,
)
from repository.alchemy_orm import SQLAlchemyRepository

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class VacancyRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Vacancy)


class ToolRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tool)


class CityRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, City)


class CompanyRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Company)


class VacancyToolRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, VacancyTool)

    async def delete_vacancy_tools(self, vacancy_id: UUID):
        async with self.session.begin():
            query = delete(VacancyTool).where(VacancyTool.vacancy_id == vacancy_id)
            await self.session.execute(query)
            await self.session.commit()


class EmployerRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Employer)


class EmployeeRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Employee)


class ResumeRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Resume)


class JobPlaceRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, JobPlace)


class ResumeToolRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ResumeTool)

    async def delete_resume_tools(self, resume_id: UUID):
        async with self.session.begin():
            query = delete(ResumeTool).where(ResumeTool.resume_id == resume_id)
            await self.session.execute(query)
            await self.session.commit()
