from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.base.model import Base

from base.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute


class BaseService:
    def __init__(self, session: AsyncSession, repository: BaseRepository):
        self.session = session
        self.repository = repository(session=session)

    async def create(self, **model_data) -> Base:
        return await self.repository.create(**model_data)

    async def get(self, id: UUID) -> Base:
        return await self.repository.get(id)

    async def delete(self, instance: Base) -> None:
        return await self.repository.delete(instance)

    async def update(self, instance: Base, **model_data) -> Base:
        return await self.repository.update(instance, **model_data)

    async def all(
        self, order_by: list[InstrumentedAttribute] | None = None
    ) -> Sequence[Base]:
        return await self.repository.all(order_by)

    async def filter(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[Base]:
        return await self.repository.filter(
            filters,
            order_by,
            exclude_data,
            limit,
            offset,
        )

    async def get_or_create(self, filters: dict[str, Any], **model_data) -> Base:
        return await self.repository.get_or_create(filters, **model_data)

    async def update_or_create(self, filters: dict[str, Any], **model_data) -> Base:
        return await self.repository.update_or_create(filters, **model_data)

    async def exists(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> bool:
        return await self.repository.exists(filters, exclude_data)

    async def count(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> int:
        return await self.repository.count(filters, exclude_data)
