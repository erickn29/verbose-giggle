import factory

from utils.factory.base import BaseFactory
from v1.user.model.model import User
from v1.user.service.service import UserService


class UserFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    password = UserService.get_password_hash("password")
    is_active = True
    is_admin = False
