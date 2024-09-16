import factory

from apps.v1.user.model import User
from apps.v1.user.service import UserService
from utils.factory.base import BaseFactory


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
