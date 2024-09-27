from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserModelSchema(BaseModel):
    id: UUID | str
    email: str
    password: str
    is_active: bool
    is_admin: bool
    is_verified: bool
    coin: int
    subscription: datetime | None
    created_at: datetime | str
    updated_at: datetime | str
