# ruff: noqa: B008
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt

from apps.v1.user.model import User
from apps.v1.user.service import UserService
from core.database import db_conn
from core.exceptions import exception
from core.settings import settings
from fastapi import Depends
from jwt import DecodeError, ExpiredSignatureError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from schemas.user import UserModelSchema
from utils.cache import cache


class Token(BaseModel):
    token_type: str
    access_token: str | None = None
    refresh_token: str | None = None


class TokenData(BaseModel):
    id: str | None = None
    email: str | None = None


async def get_request(request: Request):
    return request


class JWTAuthenticationBackend:
    def __init__(
        self,
        session: AsyncSession,
        algorithm: str = settings.auth.ALGORITHM,
        access_token_expire: int = settings.auth.ACCESS_TOKEN_EXPIRE,
        refresh_token_expire: int = settings.auth.REFRESH_TOKEN_EXPIRE,
        secret_key: str = settings.app.SECRET_KEY,
        # request: Request | None = None,
    ):
        self.algorithm = algorithm
        self.access_token_expire = access_token_expire
        self.refresh_token_expire = refresh_token_expire
        self.secret_key = secret_key
        # self.request: Request = request
        self.user_service = UserService(session=session)

    async def __call__(self, request: Request) -> UserModelSchema:
        """Метод вызывает проверку активности пользователя"""
        if not request or not request.headers.get("Authorization"):
            raise exception(401, extra="Заголовок авторизации отсутствует")
        self.request = request
        return await self._check_user_is_active()

    async def _create_token(
        self,
        data: dict,
        type_: str,
        expires_delta: timedelta,
    ) -> str:
        """Принимает payload и дату истечения времени жизни токена, возвращает jwt"""
        to_encode = data.copy()
        to_encode.update({"type": type_, "exp": datetime.now(UTC) + expires_delta})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def _get_token_data(self, user) -> Token:
        """Возвращает access refresh токены фронту"""
        token_data = Token(token_type=settings.auth.TOKEN_TYPE)
        if not user:
            raise exception(
                400,
                msg="Ошибка аутентификации",
                extra="Некорректные имя пользователя или пароль",
            )
        refresh_token_expires = timedelta(seconds=self.refresh_token_expire)
        token_data.refresh_token = await self._create_token(
            data={"id": str(user.id)},
            type_="refresh",
            expires_delta=refresh_token_expires,
        )

        access_token_expires = timedelta(seconds=self.access_token_expire)
        token_data.access_token = await self._create_token(
            data={"id": str(user.id)},
            type_="access",
            expires_delta=access_token_expires,
        )
        return token_data

    async def login(
        self,
        email: str,
        password: str,
    ) -> Token:
        """Токены после логина юзера"""
        user = await self._get_user_from_db("email", email)
        if not self.user_service.verify_password(password, user.password):
            raise exception(
                400,
                msg="Ошибка аутентификации",
                extra="Некорректные имя пользователя или пароль",
            )
        return await self._get_token_data(user)

    async def validate_token(self, token) -> dict[str, str]:
        """Проверка валидности токена и времени жизни"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except (ExpiredSignatureError, DecodeError):
            return {}

    async def get_token(self, token: str) -> Token:
        """Токены после запроса refresh"""
        token_: dict[str, str] = await self.validate_token(token)
        if not token_:
            raise exception(401, extra="Невалидный токен")
        user = await self._get_user_from_db("id", token_.get("id", ""))
        return await self._get_token_data(user)

    async def _get_user_from_db(self, field_name: str, field_value: str) -> User:
        """Метод возвращает объект пользователя из БД"""
        user_list = await self.user_service.fetch({field_name: field_value})
        if len(user_list) != 1:
            raise exception(401, extra="Некорректные имя пользователя или пароль")
        return user_list[0]

    async def _get_current_user(
        self,
        token: Annotated[str, Depends(settings.auth.OAUTH2_SCHEME)],
    ) -> UserModelSchema:
        """Возвращает текущего пользователя"""
        payload = await self.validate_token(token)
        if not payload:
            raise exception(401)
        user_id: str = payload.get("id", "")
        if user_id is None:
            raise exception(401)
        if user_schema := await cache.get_user(user_id):
            return user_schema
        token_data = TokenData(id=user_id)
        user = await self._get_user_from_db("id", token_data.id)
        if str(user.id) != token_data.id:
            raise exception(401)
        user_schema = UserModelSchema(
                id=user.id,
                email=user.email,
                password=user.password,
                is_active=user.is_active,
                is_admin=user.is_admin,
                is_verified=user.is_verified,
                coin=user.coin,
                subscription=user.subscription,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        await cache.set_user(user_schema)
        return user_schema

    async def _check_user_is_active(self) -> UserModelSchema:
        """Проверяет статус пользователя"""
        current_user = await self._get_current_user(
            await settings.auth.OAUTH2_SCHEME(self.request)
        )
        if not current_user.is_active:
            raise exception(
                400, msg="Ошибка авторизации", extra="Пользователь неактивен"
            )
        return current_user


def get_jwt_auth_backend(
    session: AsyncSession = Depends(db_conn.get_session),
) -> JWTAuthenticationBackend:
    return JWTAuthenticationBackend(session=session)


async def is_authenticated(
    request: Request,
    auth: JWTAuthenticationBackend = Depends(get_jwt_auth_backend),
) -> UserModelSchema:
    return await auth(request)
