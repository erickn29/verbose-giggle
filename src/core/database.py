import uuid

from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Annotated

from core.config import cfg
from sqlalchemy import UUID, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


DATABASE_URL = cfg.get_db_url(is_async=True)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# @asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    ),
]

created_at = Annotated[
    datetime,
    mapped_column(server_default=func.now(), doc="Дата создания"),
]

updated_at = Annotated[
    datetime,
    mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="Дата изменения",
    ),
]


class Base(DeclarativeBase):
    id: Mapped[uuid_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
