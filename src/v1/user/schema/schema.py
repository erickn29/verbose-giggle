from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    email: str | None = None
    password: str | None = None


class UserOutputSchema(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime


class UserListOutputSchema(BaseModel):
    users: list[UserOutputSchema]
