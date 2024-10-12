import uuid

from datetime import datetime, timedelta

from apps.v1.auth.model import RecoveryToken
from apps.v1.auth.repository import RecoveryTokenRepository
from apps.v1.auth.schema import PasswordRecoveryEmail, RecoveryTokenInputSchema
from apps.v1.user.model import User
from base.service import BaseService
from core.exceptions import exception
from core.settings import settings
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from utils.mail import Mail


class RecoveryTokenUpdate(BaseModel):
    created_at: datetime = datetime(1970, 1, 1)
    user_id: uuid.UUID | str = ""
    is_used: bool = False


class RecoveryTokenService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = RecoveryTokenRepository(session=session)

    async def create(self, **data) -> tuple[RecoveryToken, bool]:
        token = await self.repository.create(**data)
        return token, token is not None

    async def get_obj_or_400(self, filters: dict) -> RecoveryToken:
        token = await self.repository.filter(filters)
        if not token:
            raise exception(400, msg="Ошибка", extra="Токен не найден")
        if token[0].is_used or datetime.utcnow() > token[0].created_at + timedelta(
            seconds=settings.auth.RECOVERY_TOKEN_EXPIRE,
        ):
            raise exception(
                400,
                msg="Ошибка",
                extra="Токен использован или срок использования истек",
            )
        return token[0]

    async def send_token(self, user: User, message: str, email: PasswordRecoveryEmail):
        status = False
        token = uuid.uuid4().hex
        recovery_token = RecoveryTokenInputSchema(token=token, user_id=user.id)
        message_ = message + token
        status = await self.create(**recovery_token.model_dump())
        if status:
            Mail().send_email(email.email, message_)
        return status
