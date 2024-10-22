import asyncio

from collections.abc import AsyncGenerator, Generator
from typing import Any
from uuid import uuid4

# from src.tests.factory.factory import UserFactory
import pytest
import pytest_asyncio

from apps.v1.user.service import UserService
from base.model import Base
from core.database import db_conn
from core.settings import settings
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_and_drop_test_db():
    async_db_url = settings.db.url(db_name=f"test_db_{uuid4().hex[:5]}")
    db_url = async_db_url.replace("postgresql+asyncpg", "postgresql")
    if not database_exists(db_url):
        print(db_url)
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

    async with session_test() as test_session:  # type: ignore
        yield test_session
        # await test_session.close()


@pytest_asyncio.fixture(scope="session")
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=app, base_url=f"http://{settings.app.HOST}:1001"
    ) as client:

        async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
            async with session as test_session:
                yield test_session
                # await test_session.close()

        app.dependency_overrides[db_conn.get_session] = override_get_session
        yield client


# @pytest_asyncio.fixture(scope="session")
# async def auth_headers_admin(client, session):
#     UserFactory._meta.sqlalchemy_session = session
#     user: SQLAlchemyModelFactory = await UserFactory()

#     data = {
#         "username": user.email,
#         "password": "password",
#     }

#     response = await client.post("/api/v1/auth/login/", data=data)
#     return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest_asyncio.fixture(scope="session")
async def auth_headers(client, session):
    returned_data = {}
    user_service = UserService(session)
    user = await user_service.create(
        email="user_base@example.com",
        password="test_password",
    )
    data = {
        "email": user.email,
        "password": "test_password",
    }
    await user_service.update(user, is_verified=True)

    response = await client.post("/api/v1/auth/login/", json=data)
    returned_data.update(
        {
            "refresh_token": response.json()["refresh_token"],
            "access_token": response.json()["access_token"],
            "auth_headers": {
                "Authorization": f"Bearer {response.json()['access_token']}"
            },
            "user": user,
        }
    )
    user2 = await user_service.create(
        email="user_base2@example.com",
        password="test_password",
    )
    data = {
        "email": user2.email,
        "password": "test_password",
    }
    await user_service.update(user2, is_verified=True)

    response = await client.post("/api/v1/auth/login/", json=data)
    returned_data.update(
        {
            "auth_headers2": {
                "Authorization": f"Bearer {response.json()['access_token']}"
            },
            "user2": user2,
        }
    )
    user3 = await user_service.create(
        email="user_base3@example.com",
        password="test_password",
    )
    data = {
        "email": user3.email,
        "password": "test_password",
    }

    response = await client.post("/api/v1/auth/login/", json=data)
    returned_data.update(
        {
            "auth_headers3": {
                "Authorization": f"Bearer {response.json()['access_token']}"
            },
            "user3": user3,
        }
    )
    user4 = await user_service.create(
        email="user_base4@example.com",
        password="test_password",
    )
    data = {
        "email": user4.email,
        "password": "test_password",
    }
    await user_service.update(user4, is_verified=True)

    response = await client.post("/api/v1/auth/login/", json=data)
    returned_data.update(
        {
            "auth_headers4": {
                "Authorization": f"Bearer {response.json()['access_token']}"
            },
            "user4": user4,
        }
    )
    return returned_data
