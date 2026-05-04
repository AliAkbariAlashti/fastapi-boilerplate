from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.core.logging import configure_logging, get_logger
from app.db.session import engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    logger.info("startup", environment=app.state.settings.ENVIRONMENT)

    # Optionally warm up DB connection pool
    async with engine.begin():
        pass

    yield

    # Teardown
    await engine.dispose()
    logger.info("shutdown")
