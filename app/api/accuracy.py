from fastapi import APIRouter, Query

from domain.prediction import PredictionAccuracySummary, PredictionHorizon
from services.accuracy_service import AccuracyService


router = APIRouter(prefix="/api/v1/accuracy", tags=["Accuracy"])


@router.get("", response_model=PredictionAccuracySummary)
def accuracy_summary(
    horizon: PredictionHorizon | None = None,
    days: int = Query(default=90, ge=1, le=3650),
) -> PredictionAccuracySummary:
    return AccuracyService().get_accuracy_summary(horizon=horizon, days=days)


@router.get("/{symbol}", response_model=PredictionAccuracySummary)
def accuracy_summary_for_symbol(
    symbol: str,
    horizon: PredictionHorizon | None = None,
    days: int = Query(default=90, ge=1, le=3650),
) -> PredictionAccuracySummary:
    return AccuracyService().get_accuracy_summary(symbol=symbol, horizon=horizon, days=days)
