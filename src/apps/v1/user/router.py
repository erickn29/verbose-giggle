from typing import Annotated
from uuid import UUID

from apps.v1.auth.schema import PasswordRecoveryEmail
from apps.v1.auth.service import RecoveryTokenService
from apps.v1.auth.utils.auth import is_authenticated
from apps.v1.user.schema import (
    EmailVerifyInputSchema,
    EmailVerifyOutputSchema,
    UserCreateInputSchema,
    UserOutputSchema,
    UserUpdateData,
    UserUpdateVerifyData,
)
from apps.v1.user.service import UserService
from core.database import db_conn
from core.exceptions import exception
from core.settings import settings
from fastapi import APIRouter, Depends
from schemas.user import UserModelSchema
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/", response_model=UserOutputSchema, status_code=201)
async def create_user(
    schema: UserCreateInputSchema,
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
):
    user_service = UserService(session=session)
    recovery_service = RecoveryTokenService(session=session)
    user = await user_service.create(**schema.model_dump())
    msg = f"Confirm email\n" f"{settings.app.FRONT_URL}/verify-email/"
    await recovery_service.send_token(
        user=user,
        message=msg,
        email=PasswordRecoveryEmail(email=user.email),
    )
    return user


@router.post("/verify-email/", response_model=EmailVerifyOutputSchema)
async def verify_email(
    schema: EmailVerifyInputSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_conn.get_session),
    ],
):
    status = False
    user_service = UserService(session=session)
    recovery_service = RecoveryTokenService(session=session)
    if token := await recovery_service.get_obj_or_400({"token": schema.token}):
        status = True
    user = await user_service.filter({"id": token.user_id})
    if len(user) != 1:
        raise exception(404, extra=str(token.user_id))
    await user_service.update(
        user[0], **UserUpdateVerifyData(is_verified=True).model_dump()
    )
    return EmailVerifyOutputSchema(status=status)


@router.put("/", response_model=UserOutputSchema, status_code=201)
async def update_user(
    schema: UserUpdateData,
    session: Annotated[AsyncSession, Depends(db_conn.get_session)],
    user: Annotated[UserModelSchema, Depends(is_authenticated)],
):
    user_service = UserService(session=session)
    user_id = user.id if isinstance(user.id, UUID) else UUID(user.id)
    if user_obj := await user_service.get(user_id):
        return await user_service.update(user_obj, **schema.model_dump())
    raise exception(404, extra=str(user.id))


@router.get("/me/", response_model=UserOutputSchema)
async def get_user(user: Annotated[UserModelSchema, Depends(is_authenticated)]):
    return user
