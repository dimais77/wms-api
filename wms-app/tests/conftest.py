from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from models import Base
from core.config import settings
from db import DatabaseHelper, db_helper
from main import app

test_db_helper = DatabaseHelper()

url = str(settings.db.url)
engine_test = create_async_engine(url, echo=True)
session_factory = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
Base.metadata.bind = engine_test


async def override_transactional_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


app.dependency_overrides[db_helper.get_transactional_session] = (
    override_transactional_session
)


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        async with session.begin():
            yield session
        await session.rollback()
