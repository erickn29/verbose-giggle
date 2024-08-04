import random

import factory

from utils.factory.base import BaseFactory
from v1.vacancy.model.model import (
    City,
    Company,
    Experience,
    Language,
    Speciality,
    Tool,
    Vacancy,
    VacancyTool,
)


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
    is_publish = True
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
