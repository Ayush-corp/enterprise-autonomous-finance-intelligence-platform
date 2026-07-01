from fastapi import APIRouter

from app.api.accuracy import router as accuracy_router
from app.api.analysis import router as analysis_router
from app.api.health import router as health_router
from app.api.predictions import router as predictions_router
from app.api.watchlist import router as watchlist_router

api_router = APIRouter()

api_router.include_router(analysis_router)
api_router.include_router(health_router)
api_router.include_router(watchlist_router)
api_router.include_router(predictions_router)
api_router.include_router(accuracy_router)
