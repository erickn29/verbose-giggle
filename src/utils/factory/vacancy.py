import random

import factory

from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from v1.vacancy.model.model import (
    Vacancy,
    Speciality,
    Language,
    Experience,
    City,
    Company,
    Tool,
    VacancyTool,
)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = None
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
        return await instance

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        obj = model_class(*args, **kwargs)
        session.add(obj)
        await session.commit()
        return obj

    # @property
    # def meta_session(self):
    #     return self._meta
    #
    # @meta_session.setter
    # def meta_session(self, session: AsyncSession):
    #     self._meta.sqlalchemy_session = session


class ToolFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Tool
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("word")


class CityFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = City
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("city")


class CompanyFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Company
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("company")
    city_id = None


class VacancyFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Vacancy
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("word")
    description = factory.Faker("word")
    language = Language.python.value
    speciality = Speciality.developer.value
    experience = Experience.one_to_three.value
    salary_from = random.randint(50000, 100000)
    salary_to = random.randint(101000, 200000)
    company_id = None


class VacancyToolFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = VacancyTool
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    vacancy_id = None
    tool_id = None
