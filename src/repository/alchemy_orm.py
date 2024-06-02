from collections.abc import Sequence

from core.database import Base
from fastapi import HTTPException
from pydantic import UUID4, BaseModel
from repository.base import BaseAsyncRepository
from sqlalchemy import and_, insert, select
from sqlalchemy.exc import IntegrityError


class SQLAlchemyRepository(BaseAsyncRepository):

    async def create(self, obj: BaseModel) -> Base | None:
        stmt = insert(self.model).values(**obj.model_dump()).returning(self.model)
        try:
            async with self.session:
                result = await self.session.execute(stmt)
                await self.session.commit()
                return result.scalar_one_or_none()
        except IntegrityError:
            await self.session.rollback()
            await self.session.close()
            raise HTTPException(
                status_code=400,
                detail=f"Already Exists ({self.model.__name__})",
            )

    async def get(self, id: UUID4) -> Base | None:
        query = select(self.model).where(self.model.id == id)
        async with self.session:
            result = await self.session.execute(query)
        obj = result.scalars().first()
        return obj

    async def delete(self, id: UUID4):
        obj = await self.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not Found")
        async with self.session:
            await self.session.delete(obj)
            await self.session.commit()
        return id

    async def update(self, id: UUID4, data: BaseModel) -> Base | None:
        obj = await self.get(id)
        for field, value in data.dict(exclude_unset=True).items():
            if value:
                setattr(obj, field, value)
        try:
            async with self.session:
                await self.session.commit()
                return obj
        except IntegrityError as e:
            await self.session.rollback()
            await self.session.close()
            raise HTTPException(status_code=400, detail=e.args[0])

    async def all(self, order_by: list = None) -> Sequence[Base]:
        order_by = order_by or [self.model.created_at.desc()]
        query = select(self.model).order_by(*order_by)
        async with self.session.begin():
            result = await self.session.execute(query)
            return result.scalars().all()

    async def filter(self, filters: dict, order_by: list = None) -> Sequence[Base]:
        """
        filters = {
            "price": {"gt": 100, "lt": 200},
            "category": "electronics",
            "brand": {"in": ["Samsung", "Apple"]},
            "title": {"ilike": "phone"}
        }
        """
        operator_map = {
            "gt": lambda column, value: column > value,
            "gte": lambda column, value: column >= value,
            "lt": lambda column, value: column < value,
            "lte": lambda column, value: column <= value,
            "in": lambda column, value: column.in_(value),
            "like": lambda column, value: column.like(f"%{value}%"),
            "ilike": lambda column, value: column.ilike(f"%{value}%"),
        }
        order_by = order_by or [self.model.created_at.desc()]
        query = select(self.model)

        filter_list = []
        for key, value in filters.items():
            if not value:
                continue
            if isinstance(value, dict):
                column = getattr(self.model, key)
                for operator, operand in value.items():
                    condition = operator_map.get(operator)
                    if condition:
                        filter_list.append(condition(column, operand))
            else:
                filter_list.append(getattr(self.model, key) == value)
            query = select(self.model).filter(and_(*filter_list)).order_by(*order_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_or_create(self, obj: BaseModel) -> Base | None:
        obj_in_db = await self.filter(obj.model_dump())
        if obj_in_db:
            return obj_in_db[0]
        result = await self.create(obj)
        return result
