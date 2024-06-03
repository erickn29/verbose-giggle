import asyncio
import warnings

from collections.abc import AsyncGenerator, Generator
from typing import Any
from uuid import uuid4

import alembic
import pytest
import pytest_asyncio

from core.config import cfg
from core.database import Base, get_async_session
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database
from uvicorn import Config


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session")
def create_and_drop_test_db():
    async_db_url = cfg.get_db_url(is_async=True, db_name=f"test_wb_{uuid4().hex[:5]}")
    db_url = async_db_url.replace("postgresql+asyncpg", "postgresql")
    if not database_exists(db_url):
        create_database(db_url)

    yield async_db_url

    if database_exists(db_url):
        drop_database(db_url.replace("postgresql+asyncpg", "postgresql"))


@pytest_asyncio.fixture(scope="session")
async def engine(create_and_drop_test_db) -> AsyncGenerator:
    engine = create_async_engine(
        create_and_drop_test_db,
        echo=False,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_test = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_test() as test_session:
        yield test_session
        # await test_session.close()


@pytest_asyncio.fixture(scope="function")
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=f"http://{cfg.HOST}:1001") as client:

        async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
            async with session as test_session:
                yield test_session
                # await test_session.close()

        app.dependency_overrides[get_async_session] = override_get_session
        yield client


# @pytest_asyncio.fixture(scope="function")
# async def auth_headers(client, session):
#     UserFactory._meta.sqlalchemy_session = session
#     user: SQLAlchemyModelFactory = await UserFactory()
#
#     data = {
#         "username": user.email,
#         "password": "password",
#     }
#
#     response = await client.post("/api/v1/auth/login/", data=data)
#     return {"Authorization": f"Bearer {response.json()['access_token']}"}
