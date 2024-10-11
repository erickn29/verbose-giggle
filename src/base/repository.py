from collections.abc import Sequence
from typing import Any
from uuid import UUID

from base.model import Base, ModelType
from sqlalchemy import Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute


class FilterCondition:
    EXACT = "exact"
    NOT_EXACT = "not_exact"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "gte"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    ILIKE = "ilike"
    BETWEEN = "between"

    @classmethod
    def get_by_expr(cls, expr: str = EXACT):
        conditions_map = {
            cls.EXACT: lambda column, value: column == value,
            cls.NOT_EXACT: lambda column, value: column != value,
            cls.GT: lambda column, value: column > value,
            cls.GTE: lambda column, value: column >= value,
            cls.LT: lambda column, value: column < value,
            cls.LTE: lambda column, value: column <= value,
            cls.IN: lambda column, value: column.in_(value),
            cls.NOT_IN: lambda column, value: column.not_in(value),
            cls.LIKE: lambda column, value: column.like(f"%{value}%"),
            cls.ILIKE: lambda column, value: column.ilike(f"%{value}%"),
            cls.BETWEEN: lambda column, value: column.between(*value),
        }
        return conditions_map.get(expr)

    @classmethod
    def get_filter(cls, value: Any, expr: str = EXACT):
        return {expr: value}


class BaseRepository:
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_filters(self, filters: dict):
        filter_conditions = []
        for key, value in filters.items():
            column = getattr(self.model, key)
            if not isinstance(value, dict):
                value = {FilterCondition.EXACT: value}
            for operator, operand in value.items():
                condition = FilterCondition.get_by_expr(operator)
                if condition and operand:
                    filter_conditions.append(condition(column, operand))
        return (
            and_(*filter_conditions)
            if len(filter_conditions) > 1
            else filter_conditions[0]
        )

    def get_statement(
        self,
        filters: dict[str, Any] | None = None,
        excludes: dict[InstrumentedAttribute, Any] | None = None,
        # select_related: list[relationship] | None = None,
        # prefetch_related: list[relationship] | None = None,
        order_by_: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        count: bool = False,
    ) -> Select:
        statement = (
            select(self.model)
            if not count
            else select(func.count()).select_from(self.model).group_by(self.model.id)
        )
        if filters:
            filter_query = self._get_filters(filters)
            statement = statement.filter(filter_query)
        if excludes:
            for field, value in excludes.items():
                statement = statement.where(field != value)
        # if select_related:
        #     statement = statement.options(
        #         *[joinedload(item) for item in select_related]
        #     )
        # if prefetch_related:
        #     statement = statement.options(
        #         *[selectinload(item) for item in prefetch_related]
        #     )
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        order_by: list = order_by_ or [self.model.created_at.desc()]
        statement = statement.order_by(*order_by)
        return statement

    def customize_filters(self, filters: dict[str, Any]):
        pass

    async def all(
        self,
        # select_related: list[relationship] | None = None,
        # prefetch_related: list[relationship] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
    ) -> Sequence[ModelType]:
        statement = self.get_statement(
            # select_related=select_related,
            # prefetch_related=prefetch_related,
            order_by_=order_by,
        )
        result = await self.session.scalars(statement=statement)
        return result.all()

    async def count(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> int:
        self.customize_filters(filters)
        statement = self.get_statement(
            filters=filters, excludes=exclude_data, count=True
        )
        result = await self.session.scalars(statement=statement)
        return len(result.all())

    async def exists(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
    ) -> bool:
        self.customize_filters(filters)
        subquery = self.get_statement(filters=filters, excludes=exclude_data)
        statement = select(1).where(subquery.exists())
        result = await self.session.scalar(statement=statement)
        return bool(result)

    async def filter(
        self,
        filters: dict[str, Any],
        exclude_data: dict[InstrumentedAttribute, Any] | None = None,
        # select_related: list[relationship] | None = None,
        # prefetch_related: list[relationship] | None = None,
        order_by: list[InstrumentedAttribute] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[ModelType]:
        self.customize_filters(filters)
        statement = self.get_statement(
            filters=filters,
            excludes=exclude_data,
            # select_related=select_related,
            # prefetch_related=prefetch_related,
            order_by_=order_by,
            limit=limit,
            offset=offset,
        )
        result = await self.session.scalars(statement=statement)
        return result.all()

    async def get(self, id: UUID) -> ModelType | None:
        result: ModelType | None = await self.session.get(self.model, id)
        return result

    async def create(self, **model_data) -> ModelType:
        instance: ModelType = self.model(**model_data)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, instance: ModelType, **model_data) -> ModelType:
        for key, value in model_data.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: Base) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def get_or_create(
        self, filters: dict[str, Any], **model_data
    ) -> tuple[ModelType, bool]:
        created = True
        if instance := await self.filter(filters=filters):
            if len(instance) > 1:
                raise ValueError("Multiple instances found with the same filters")
            created = False
            return instance[0], created
        model_data.update(filters)
        return await self.create(**model_data), created

    async def update_or_create(
        self, filters: dict[str, Any], **model_data
    ) -> tuple[ModelType, bool]:
        created = True
        if instance := await self.filter(filters=filters):
            if len(instance) > 1:
                raise ValueError("Multiple instances found with the same filters")
            created = False
            return await self.update(instance=instance[0], **model_data), created
        model_data.update(filters)
        return await self.create(**model_data), created
