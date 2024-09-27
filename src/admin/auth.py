from apps.v1.auth.utils.auth import JWTAuthenticationBackend as auth

# from model.user import UserRole
from apps.v1.user.service import UserService
from core.database import db_conn
from core.settings import settings
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str) -> None:
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        session_generator = db_conn.get_session()
        session = await anext(session_generator)
        async with session:
            auth_service = auth(session=session)
            token = await auth_service.login(username, password)
        if not token:
            return False

        request.session["token"] = token.refresh_token
        return True

    async def logout(self, request: Request) -> bool:
        if not request.session.get("token"):
            return False

        del request.session["token"]  # TODO удаляются все куки решить!
        return True

    async def authenticate(self, request: Request) -> bool:
        refresh_token = request.session.get("token")
        if not refresh_token:
            return False

        session_generator = db_conn.get_session()
        session = await anext(session_generator)

        async with session:
            auth_service = auth(session=session)
            jwt_dict = await auth_service.validate_token(refresh_token)

        async with session:
            user_service = UserService(session=session)
            if user := await user_service.get(jwt_dict.get("id")):
                return user.is_admin is True
            return False


authentication_backend = AdminAuth(secret_key=settings.app.SECRET_KEY)
