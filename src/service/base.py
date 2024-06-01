from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from repository.alchemy_orm import SQLAlchemyRepository
from repository.base import BaseAsyncRepository


class BaseService(ABC):
    def __init__(self, session: AsyncSession, repository: BaseAsyncRepository):
        self.session = session
        self.repository = repository(session=session)

    @abstractmethod
    async def create(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id, data):
        raise NotImplementedError

    @abstractmethod
    async def all(self):
        raise NotImplementedError

    @abstractmethod
    async def filter(self, filters: dict, order_by: list = None):
        raise NotImplementedError
