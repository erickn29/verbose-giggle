from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_HOSTS = [
    "http://127.0.0.1:3000",
    "http://localhost:5173",
]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).resolve().parent.parent.parent}" f"/secret/.envfile"
    )

    # main
    DEBUG: bool = False
    FRONT_URL: str = "https://test.ru"
    HOST: str = "localhost"
    PORT: str = "8000"
    SECRET_KEY: str = "123"

    # Auth settings
    ACCESS_TOKEN_EXPIRE: int = 5 * 60
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 7
    RECOVERY_TOKEN_EXPIRE: int = 60 * 60 * 24
    TOKEN_TYPE: str = "Bearer"
    ALGORITHM: str = "HS256"
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer("/api/v1/auth/token/")

    # DB
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    # Testing
    TEST_MODE: bool = False

    # CORS
    CORS_ALLOWED_HOSTS: list[str] = []
    CORS_ALLOWED_HOSTS.extend(DEFAULT_HOSTS)
    # CORS_ALLOWED_HOSTS_REGEX: str = (
    #     "(https?://[^/]*\dom\.(ru|tech))|(http://(localhost|127.0.0.1):[1-9][0-9]{3})"
    # )
    CORS_ALLOWED_CREDENTIALS: bool = True
    CORS_ALLOWED_METHODS: list[str] = ["*"]
    CORS_ALLOWED_HEADERS: list[str] = ["*"]

    # EMAIL
    EMAIL_HOST: str = ""
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    EMAIL_PORT: str = ""

    def get_db_url(self, is_async: bool = False, db_name: str = None) -> str:
        suffix = "postgresql+asyncpg://" if is_async else "postgresql://"
        db_name = db_name or self.POSTGRES_DB

        return (
            f"{suffix}"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"
        )


cfg = Settings()
