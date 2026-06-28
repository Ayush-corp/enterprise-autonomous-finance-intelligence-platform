from fastapi import FastAPI

from app.api.router import api_router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Autonomous Investing Agent",
    version="2.0",
)

app.include_router(api_router)