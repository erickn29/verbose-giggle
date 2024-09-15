from datetime import datetime

from src.apps.v1.vacancy.model import Employee, Employer, JobPlace, Resume
from tests.factory.base import BaseFactory

import factory


class EmployerFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Employer
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user_id: str = None
    company_id: str = None


class EmployeeFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Employee
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user_id: str = None
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    patronymic: str = factory.Faker("patronymic")
    dob: datetime = factory.Faker("date_of_birth")
    sex: bool = True


class ResumeFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Resume
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    employee_id: str = None
    position: str = factory.Faker("word")
    speciality: str = "разработка"
    description: str = factory.Faker("word")
    is_publish: bool = True


class JobPlaceFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = JobPlace
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    company: str = factory.Faker("company")
    resume_id: str = None
    position: str = factory.Faker("word")
    speciality: str = "разработка"
    description: str = factory.Faker("word")
    end_date = None
