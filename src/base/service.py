from uuid import UUID

from base.repository import BaseRepository

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, session: AsyncSession, repository: BaseRepository):
        self.session = session
        self.repository = repository(session=session)

    async def create(self, obj: BaseModel):
        return await self.repository.create(obj)

    async def get(self, id: UUID):
        return await self.repository.get(id)

    async def delete(self, id: UUID):
        return await self.repository.delete(id)

    async def update(self, id: UUID, data: BaseModel):
        return await self.repository.update(id, data)

    async def get_all(self, order_by: list = None):
        return await self.repository.all(order_by)

    async def fetch(self, filters: dict, order_by: list = None):
        return await self.repository.fetch(filters, order_by)

    async def get_or_create(self, obj: BaseModel):
        return await self.repository.get_or_create(obj)
