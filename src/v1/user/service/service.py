from uuid import UUID

from service.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from v1.user.repository.repository import UserRepository
from v1.user.schema.schema import (
    UserCreateSchema,
    UserListOutputSchema,
    UserOutputSchema,
    UserUpdateSchema,
)


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=UserRepository)

    async def create(self, obj: UserCreateSchema):
        obj = await self.repository.create(obj)
        return UserOutputSchema(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            patronymic=obj.patronymic,
            email=obj.email,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )

    async def get(self, id: UUID):
        return await self.repository.get(id)

    async def delete(self, id: UUID):
        return await self.repository.delete(id)

    async def update(self, id: UUID, data: UserUpdateSchema):
        return await self.repository.update(id, data)

    async def all(self, order_by: list = None):
        res = await self.repository.all(order_by)
        return UserListOutputSchema(
            users=[
                UserOutputSchema(
                    id=obj.id,
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    patronymic=obj.patronymic,
                    email=obj.email,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at,
                )
                for obj in res
            ]
        )

    async def filter(self, filters: dict, order_by: list = None):
        return await self.repository.filter(filters, order_by)
