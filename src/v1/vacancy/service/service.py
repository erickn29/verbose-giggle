from typing import List

from service.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from v1.vacancy.model.model import City, Company, Tool, Vacancy
from v1.vacancy.repository.repository import (
    CityRepository,
    CompanyRepository,
    ToolRepository,
    VacancyRepository,
    VacancyToolRepository,
)
from v1.vacancy.schema.schema import (
    VacancyCreateSchema,
    VacancyListOutputSchema,
    VacancyOutputSchema,
    VacancyToolSchema, ToolOutputSchema, ToolInputSchema,
)


class VacancyService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=VacancyRepository)

    async def create(self, vacancy_create_schema: VacancyCreateSchema):
        city_service = CityService(session=self.session)
        company_service = CompanyService(session=self.session)
        tool_service = ToolService(session=self.session)

        city = vacancy_create_schema.city
        company = vacancy_create_schema.company
        vacancy = vacancy_create_schema.vacancy
        tool = vacancy_create_schema.tool

        city_obj: City = await city_service.get_or_create(city)

        company.city_id = city_obj.id
        company_obj: Company = await company_service.get_or_create(company)

        vacancy.company_id = company_obj.id
        vacancy_obj: Vacancy = await self.repository.get_or_create(vacancy)

        if tool:
            # TODO bulk create
            vacancy_tool_service = VacancyToolService(session=self.session)
            tool_obj_list: list[Tool] = [
                await tool_service.get_or_create(t) for t in tool
            ]
            [
                await vacancy_tool_service.get_or_create(
                    VacancyToolSchema(
                        vacancy_id=vacancy_obj.id,
                        tool_id=t.id,
                    )
                )
                for t in tool_obj_list
            ]
        output = VacancyOutputSchema.from_orm(vacancy_obj)
        output.tool = tool
        return output

    async def all(self, order_by: list = None):
        vacancies: List[Vacancy] = await self.repository.all()
        vacancies_list: List[VacancyOutputSchema] = []
        for vacancy in vacancies:
            obj = VacancyOutputSchema.from_orm(vacancy)
            if vacancy.tools:
                obj.tool = [ToolOutputSchema.from_orm(o.tool) for o in vacancy.tools]
            vacancies_list.append(obj)
        return VacancyListOutputSchema(vacancies=vacancies_list)


class ToolService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=ToolRepository)


class CityService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=CityRepository)


class CompanyService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=CompanyRepository)


class VacancyToolService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=VacancyToolRepository)
