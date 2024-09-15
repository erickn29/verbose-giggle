import uuid

from datetime import datetime, timedelta

from apps.v1.auth.model import RecoveryToken
from apps.v1.auth.repository import RecoveryTokenRepository
from apps.v1.auth.schema import PasswordRecoveryEmail, RecoveryTokenInputSchema
from apps.v1.user.model import User
from core.exceptions import exception
from core.settings import settings
from utils.mail import Mail

from pydantic import UUID4, BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class RecoveryTokenUpdate(BaseModel):
    created_at: datetime = datetime(1970, 1, 1)
    user_id: UUID4 = ""
    is_used: bool = False


class RecoveryTokenService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = RecoveryTokenRepository(session=session)

    async def create(self, data: RecoveryTokenInputSchema):
        return await self.repository.create(data) is not None

    async def get_obj_or_400(self, filters: dict | None = None) -> RecoveryToken:
        token = await self.repository.fetch(filters)
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

    async def update(self, id: UUID4, data: BaseModel):
        return await self.repository.update(id, data)

    async def send_token(self, user: User, message: str, email: PasswordRecoveryEmail):
        status = False
        token = uuid.uuid4().hex
        recovery_token = RecoveryTokenInputSchema(token=token, user_id=user.id)
        message_ = message + token
        status = await self.create(recovery_token)
        if status:
            Mail().send_email(email.email, message_)
        return status
