import uuid

from typing import Annotated

from apps.v1.auth.schema import (
    AccessTokenRequest,
    PasswordRecoveryData,
    PasswordRecoveryEmail,
    RecoveryTokenInputSchema,
    UserPassword,
)
from apps.v1.auth.service import RecoveryTokenService
from apps.v1.auth.utils.auth import JWTAuthenticationBackend as auth
from apps.v1.user.schema import UserCreateInputSchema
from apps.v1.user.service import UserService
from core.database import db_conn
from core.exceptions import exception
from core.settings import settings
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils.mail import Mail


router = APIRouter()


@router.post("/login/")
async def login_for_access_token(
    form_data: UserCreateInputSchema,
    session: Annotated[
        AsyncSession,
        Depends(db_conn.get_session),
    ],
):
    return await auth(session=session).login(form_data.email, form_data.password)


@router.post("/token/refresh/")
async def get_new_tokens(
    token: AccessTokenRequest,
    session: Annotated[
        AsyncSession,
        Depends(db_conn.get_session),
    ],
):
    return await auth(session=session).get_token(token.token)


@router.post("/password-reset/")
async def password_reset_request(
    email: PasswordRecoveryEmail,
    session: Annotated[
        AsyncSession,
        Depends(db_conn.get_session),
    ],
):
    user_service = UserService(session=session)
    recovery_service = RecoveryTokenService(session=session)
    status = False
    if user := await user_service.filter({"email": email.email}):
        token = uuid.uuid4().hex
        recovery_token = RecoveryTokenInputSchema(token=token, user_id=user[0].id)
        message = (
            f"Перейдите по ссылке для восстановления пароля\n"
            f"https://{settings.app.FRONT_URL}/password-recovery?token={token}"
        )
        _, status = await recovery_service.create(**recovery_token.model_dump())
        Mail().send_email(email.email, message)

    return {"status": status}


@router.post("/password-recovery/")
async def password_recovery(
    data: PasswordRecoveryData,
    session: Annotated[
        AsyncSession,
        Depends(db_conn.get_session),
    ],
):
    user_service = UserService(session=session)
    recovery_service = RecoveryTokenService(session=session)
    token = await recovery_service.get_obj_or_400({"token": data.token})
    user = await user_service.filter({"id": token.user_id})
    if len(user) != 1:
        raise exception(404, extra=str(token.user_id))

    user_base = UserPassword(password=data.password)
    status = await user_service.update(user[0], **user_base.model_dump()) is not None
    await recovery_service.update(token, is_used=True)
    return {"status": status}
