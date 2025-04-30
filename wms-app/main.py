from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from core import settings
from api import router as api_router
from db import db_helper
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    async with db_helper.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(Base.metadata.drop_all)
    yield
    # shutdown
    await db_helper.dispose()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
