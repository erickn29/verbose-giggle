import uuid

from pydantic import UUID4, BaseModel, EmailStr


class User(BaseModel):
    id: uuid.UUID
    first_name: str = ""
    last_name: str = ""
    patronymic: str = ""
    email: str


class RecoveryTokenInputSchema(BaseModel):
    token: str
    user_id: UUID4


class PasswordRecoveryEmail(BaseModel):
    email: EmailStr


class PasswordRecoveryData(BaseModel):
    token: str
    password: str


class UserPassword(BaseModel):
    password: str


class AccessTokenRequest(BaseModel):
    token: str
