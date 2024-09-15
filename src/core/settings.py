from pathlib import Path
from tkinter import N

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_HOSTS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


class AppConfig(BaseModel):
    FRONT_URL: str = "https://test.ru"
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = False
    SECRET_KEY: str = "123"
    SENTRY_DSN: str = ""


class AuthConfig(BaseModel):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)

    ACCESS_TOKEN_EXPIRE: int = 3 * 60
    REFRESH_TOKEN_EXPIRE: int = 60 * 24 * 7 * 60
    RECOVERY_TOKEN_EXPIRE: int = 60 * 60 * 24
    TOKEN_TYPE: str = "Bearer"
    ALGORITHM: str = "HS256"
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer("/api/v1/auth/token/")


class EmailConfig(BaseModel):
    HOST: str = "smtp.gmail.com"
    USER: str = "main@gmail.com"
    PASSWORD: str = "aaaa bbbb cccc dddd"
    PORT: int = 465


class DatabaseConfig(BaseModel):
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: str = "5432"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 30
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    def url(self, db_name: str | None = None) -> str:
        db_name = db_name or self.name
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{db_name}"
        )


class RedisConfig(BaseModel):
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 3


class CorsConfig(BaseModel):
    ALLOWED_HOSTS: str | list = []
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: str = "*"
    ALLOWED_HEADERS: str | list = ["*"]

    @field_validator("ALLOWED_HOSTS", mode="before", check_fields=False)
    @classmethod
    def split_allowed_hosts(cls, value):
        if isinstance(value, str):
            lst = value.split(",")
            lst.extend(DEFAULT_HOSTS)
            return lst
        return value

    @property
    def get_list_allowed_methods(self) -> list[str]:
        return self.ALLOWED_METHODS.split(",")

    @field_validator("ALLOWED_HEADERS", mode="before", check_fields=False)
    @classmethod
    def split_allowed_headers(cls, value):
        if isinstance(value, str):
            lst = value.split(",")
            return lst
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).resolve().parent.parent.parent}/secrets/.envfile",
        case_sensitive=False,
        env_nested_delimiter="__",
        arbitrary_types_allowed=True,
        env_ignore_empty=True,
        extra="ignore",
    )
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    auth: AuthConfig = AuthConfig()
    email: EmailConfig = EmailConfig()
    cors: CorsConfig = CorsConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
