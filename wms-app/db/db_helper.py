from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from core import settings


class DatabaseHelper:
    def __init__ (
            self,
            url: str = "postgresql+asyncpg://user:password@localhost:5432/dbname",
            echo: bool = False,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url = url,
            echo = echo,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind = self.engine,
            autoflush = False,
            expire_on_commit = False,
        )
    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
)
