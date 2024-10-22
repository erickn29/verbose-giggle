from apps.v1.user.model import User
from apps.v1.user.repository import UserRepository
from apps.v1.user.schema import (
    UserUpdateData,
)
from base.service import BaseService
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


PWD_CONTEXT = settings.auth.PWD_CONTEXT


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserRepository)

    @staticmethod
    async def __set_cache(user: User):
        from schemas.user import UserModelSchema
        from utils.cache import cache

        if user_schema := await cache.get_user(str(user.id)):
            user_schema = UserModelSchema(
                id=user.id,
                email=user.email,
                password=user.password,
                is_active=user.is_active,
                is_admin=user.is_admin,
                is_verified=user.is_verified,
                coin=user.coin,
                subscription=user.subscription,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            await cache.set_user(user_schema)

    async def create(self, **data) -> User:
        if data.get("password"):
            data["password"] = self.get_password_hash(data["password"])
        user = await self.repository.create(**data)
        # await self.__set_cache(user)
        return user

    async def update(self, user: User, **data) -> User:
        if isinstance(data, UserUpdateData) and data.password:
            data.password = self.get_password_hash(data.password)
        user_upd = await self.repository.update(user, **data)
        # await self.__set_cache(user)
        return user_upd

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        return PWD_CONTEXT.verify(
            settings.app.SECRET_KEY + plain_password, hashed_password
        )

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        return PWD_CONTEXT.hash(settings.app.SECRET_KEY + password)
