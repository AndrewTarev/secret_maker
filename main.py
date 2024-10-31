from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from src.api.api_v1.routers import router
from src.core.database import Base
from src.core.database.db_helper import db_helper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Before request
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # After request
    await conn.engine.dispose()
    await conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
