from uuid import UUID

from fastapi import HTTPException
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
    ToolOutputSchema,
    VacancyCreateSchema,
    VacancyListOutputSchema,
    VacancyOutputSchema,
    VacancyToolSchema,
)


class VacancyService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=VacancyRepository)

    async def get(self, vacancy_id: UUID):
        vacancy = await self.repository.get(vacancy_id)
        tool = vacancy.tools

        output = VacancyOutputSchema.from_orm(vacancy)
        output.tool = [t.tool for t in tool]
        return output

    async def create(self, vacancy_create_schema: VacancyCreateSchema):
        vacancy_schema = await self.get_vacancy_schema_object(vacancy_create_schema)

        tool_service = ToolService(session=self.session)
        tool = vacancy_create_schema.tool

        vacancy_obj: Vacancy = await self.repository.get_or_create(vacancy_schema)

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

    async def update(self, id: UUID, vacancy_update_schema: VacancyCreateSchema):
        if not self.repository.get(id):
            raise HTTPException(status_code=404, detail="Vacancy not found")

        vacancy_schema = await self.get_vacancy_schema_object(vacancy_update_schema)

        tool_service = ToolService(session=self.session)
        tool = vacancy_update_schema.tool

        vacancy_obj: Vacancy = await self.repository.update(id, vacancy_schema)

        if tool:
            vacancy_tool_service = VacancyToolService(session=self.session)
            await vacancy_tool_service.delete_vacancy_tools(vacancy_obj.id)

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

    async def delete(self, id: UUID):
        return await self.repository.delete(id)

    async def get_vacancy_schema_object(self, vacancy_schema: VacancyCreateSchema):
        city_service = CityService(session=self.session)
        company_service = CompanyService(session=self.session)

        city = vacancy_schema.city
        company = vacancy_schema.company
        vacancy = vacancy_schema.vacancy

        city_obj: City = await city_service.get_or_create(city)

        company.city_id = city_obj.id
        company_obj: Company = await company_service.get_or_create(company)

        vacancy.company_id = company_obj.id
        return vacancy

    async def all(self, order_by: list = None):
        vacancies: list[Vacancy] = await self.repository.all()
        vacancies_list: list[VacancyOutputSchema] = []
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

    async def delete_vacancy_tools(self, vacancy_id: UUID):
        await self.repository.delete_vacancy_tools(vacancy_id)
