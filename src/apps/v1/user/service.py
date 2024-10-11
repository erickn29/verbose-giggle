from collections.abc import Sequence
from typing import Any
from uuid import UUID

from apps.v1.user.model import User
from apps.v1.user.repository import UserRepository
from apps.v1.user.schema import (
    UserCreateInputSchema,
    UserUpdateData,
    UserUpdateVerifyData,
)
from base.service import BaseService
from core.settings import settings
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession


PWD_CONTEXT = settings.auth.PWD_CONTEXT


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserRepository)

    async def get(self, user_id: UUID) -> User | None:
        return await self.repository.get(user_id)

    async def create(self, data: UserCreateInputSchema) -> User:
        if data.password:
            data.password = self.get_password_hash(data.password)
        return await self.repository.create(data)

    async def delete(self, user_id: UUID) -> UUID:
        return await self.repository.delete(user_id)

    async def update(
        self, user_id: UUID, data: UserUpdateData | UserUpdateVerifyData
    ) -> User:
        if isinstance(data, UserUpdateData) and data.password:
            data.password = self.get_password_hash(data.password)
        return await self.repository.update(user_id, data)

    async def fetch(
        self, filters: dict | None = None
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        return await self.repository.fetch(filters)

    async def exists(self, user_id: UUID) -> bool:
        return await self.repository.exists(user_id)

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
