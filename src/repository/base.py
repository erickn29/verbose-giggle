from abc import ABC, abstractmethod


class BaseAsyncRepository(ABC):
    model = None

    @abstractmethod
    async def create(self, model):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id, model):
        raise NotImplementedError

    @abstractmethod
    async def fetch(
        self, filters: dict = None, order_by: list = None, paginate: dict = None
    ):
        raise NotImplementedError
