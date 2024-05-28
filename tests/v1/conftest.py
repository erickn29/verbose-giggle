import asyncio
from typing import Generator, Any, AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session(create_and_drop_test_db) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        cfg.get_db_url(is_async=True),
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_test = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_test() as test_session:
        yield test_session
