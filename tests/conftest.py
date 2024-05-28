import asyncio

from collections.abc import AsyncGenerator, Generator
from typing import Any
from uuid import uuid4

import pytest

from httpx import AsyncClient
from main import app
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from core.config import cfg
from core.database import Base


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
    db_name = f"test_{uuid4().hex[:5]}"
    db_url = cfg.get_db_url(is_async=False, db_name=db_name)
    if not database_exists(db_url):
        create_database(db_url)

    yield db_name

    if database_exists(db_url):
        drop_database(db_url)


@pytest.fixture(scope="session")
async def session(create_and_drop_test_db) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        cfg.get_db_url(is_async=True, db_name=create_and_drop_test_db),
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_test = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_test() as test_session:
        yield test_session


@pytest.fixture(scope="session")
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=f"http://{cfg.HOST}:1001") as client:
        yield client


# @pytest.fixture(scope="function")
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
