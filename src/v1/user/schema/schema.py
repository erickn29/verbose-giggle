from uuid import UUID

from fastapi.openapi.models import Schema
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    email: str | None = None
    password: str | None = None


class UserOutputSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: str


class UserListOutputSchema(BaseModel):
    users: list[UserOutputSchema]
