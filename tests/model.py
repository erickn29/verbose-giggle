import uuid

from datetime import datetime
from typing import Annotated

from core.settings import settings
from sqlalchemy import UUID, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    ),
]
created_at = Annotated[
    datetime,
    mapped_column(default=datetime.utcnow, doc="Дата создания"),
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
    metadata = MetaData(naming_convention=settings.db.naming_convention)
    __table_args__ = {'extend_existing': True}

    id: Mapped[uuid_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]