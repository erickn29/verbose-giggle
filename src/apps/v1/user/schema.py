from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    is_active: bool
    is_active: bool
    coin: int
    created_at: datetime
    updated_at: datetime


class UserCreateInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str


class EmailVerifyInputSchema(BaseModel):
    token: str


class EmailVerifyOutputSchema(BaseModel):
    status: bool


class UserUpdateData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str | None = None
    password: str | None = None


class UserUpdateVerifyData(BaseModel):
    is_verified: bool


class UserUpdateInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    data: UserUpdateData


class UserDeleteInputSchema(BaseModel):
    id: UUID
