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
from base.repository import BaseRepository
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class VacancyRepository(BaseRepository):
    model = Vacancy

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class ToolRepository(BaseRepository):
    model = Tool

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class CityRepository(BaseRepository):
    model = City

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class CompanyRepository(BaseRepository):
    model = Company

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class VacancyToolRepository(BaseRepository):
    model = VacancyTool

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )

    async def delete_vacancy_tools(self, vacancy_id: UUID):
        async with self.session.begin():
            query = delete(VacancyTool).where(VacancyTool.vacancy_id == vacancy_id)
            await self.session.execute(query)
            await self.session.commit()


class EmployerRepository(BaseRepository):
    model = Employer

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class EmployeeRepository(BaseRepository):
    model = Employee

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class ResumeRepository(BaseRepository):
    model = Resume

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class JobPlaceRepository(BaseRepository):
    model = JobPlace

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )


class ResumeToolRepository(BaseRepository):
    model = ResumeTool

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session,
        )

    async def delete_resume_tools(self, resume_id: UUID):
        async with self.session.begin():
            query = delete(ResumeTool).where(ResumeTool.resume_id == resume_id)
            await self.session.execute(query)
            await self.session.commit()
