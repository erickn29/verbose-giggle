from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
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
