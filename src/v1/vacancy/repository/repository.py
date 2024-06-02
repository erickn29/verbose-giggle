from uuid import UUID

from repository.alchemy_orm import SQLAlchemyRepository
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from v1.vacancy.model.model import City, Company, Tool, Vacancy, VacancyTool


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
