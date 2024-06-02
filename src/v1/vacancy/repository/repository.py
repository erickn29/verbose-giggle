from repository.alchemy_orm import SQLAlchemyRepository
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
