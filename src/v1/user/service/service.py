from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from service.base import BaseService
from v1.user.repository.repository import UserRepository


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, repository=UserRepository)

    async def create(self, obj: UserCreateSchema):
        await self.repository.create(obj)

    async def get(self, id: UUID):
        await self.repository.get(id)

    async def delete(self, id: UUID):
        await self.repository.delete(id)

    async def update(self, id: UUID, data: UserUpdateSchema):
        await self.repository.update(id, data)

    async def all(self, order_by: list = None):
        await self.repository.all(order_by)

    async def filter(self, filters: dict, order_by: list = None):
        await self.repository.filter(filters, order_by)
