from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base


class BaseAsyncRepository(ABC):

    def __init__(self, session: AsyncSession, model: Base) -> None:
        self.session = session
        self.model = model

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
