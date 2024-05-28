from abc import ABC


class BaseAsyncRepository(ABC):
    model = None

    async def create(self, model):
        raise NotImplementedError

    async def get(self, id):
        raise NotImplementedError

    async def delete(self, id):
        raise NotImplementedError

    async def update(self, id, model):
        raise NotImplementedError

    async def fetch(
        self, filters: dict = None, order_by: list = None, paginate: dict = None
    ):
        raise NotImplementedError
