from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.config import get_settings
from app.core.logging import configure_logging
from repositories.db import initialize_database
from services.prediction_scheduler import PredictionScheduler

configure_logging()

_scheduler: PredictionScheduler | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler
    initialize_database()
    settings = get_settings()
    if settings.enable_scheduler:
        _scheduler = PredictionScheduler()
        _scheduler.start()
    try:
        yield
    finally:
        if _scheduler:
            _scheduler.stop()


app = FastAPI(
    title="Autonomous Investing Agent",
    version="2.0",
    lifespan=lifespan,
)

app.include_router(api_router)
