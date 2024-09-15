from tests.factory.vacancy import (
    CityFactory,
    CompanyFactory,
    ToolFactory,
    VacancyFactory,
    VacancyToolFactory,
)

import pytest


@pytest.fixture(scope="session")
async def vacancy_status(session):
    ToolFactory._meta.sqlalchemy_session = session
    CityFactory._meta.sqlalchemy_session = session
    CompanyFactory._meta.sqlalchemy_session = session
    VacancyFactory._meta.sqlalchemy_session = session
    VacancyToolFactory._meta.sqlalchemy_session = session

    city = await CityFactory()
    company = await CompanyFactory(city_id=city.id)
    vacancy = await VacancyFactory(company_id=company.id)

    return vacancy


@pytest.fixture(scope="session")
async def vacancy_output(session):
    ToolFactory._meta.sqlalchemy_session = session
    CityFactory._meta.sqlalchemy_session = session
    CompanyFactory._meta.sqlalchemy_session = session
    VacancyFactory._meta.sqlalchemy_session = session
    VacancyToolFactory._meta.sqlalchemy_session = session

    city = await CityFactory()
    company = await CompanyFactory(city_id=city.id)
    vacancy = await VacancyFactory(company_id=company.id)

    return vacancy
