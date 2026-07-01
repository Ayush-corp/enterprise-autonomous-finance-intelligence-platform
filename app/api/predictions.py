from fastapi import APIRouter
from pydantic import BaseModel, Field

from domain.prediction import PredictionHorizon, PredictionOutcome, PredictionRecord, PredictionRun, RunStatus
from repositories.prediction_repository import PredictionRepository
from services.prediction_evaluator import PredictionEvaluator
from services.prediction_scheduler import PredictionScheduler
from services.prediction_service import PredictionService
from services.watchlist_service import WatchlistService


router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])


class PredictionRunRequest(BaseModel):
    symbol: str | None = Field(default=None, min_length=1, max_length=32)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    horizons: list[PredictionHorizon] | None = None


@router.post("/run", response_model=list[PredictionRecord])
def run_predictions(request: PredictionRunRequest) -> list[PredictionRecord]:
    service = PredictionService()
    horizons = request.horizons or list(PredictionHorizon)
    if request.symbol:
        run = service.create_run("manual", len(horizons))
        records = [
            service.generate_prediction(request.symbol, request.country, horizon, run.id)
            for horizon in horizons
        ]
        service.finish_run(run, status=RunStatus.SUCCESS, symbols_completed=len(records))
        return records
    watchlist = WatchlistService().seed_default_watchlist()
    return service.generate_daily_predictions(watchlist, horizons)


@router.get("/latest", response_model=list[PredictionRecord])
def latest_predictions() -> list[PredictionRecord]:
    return PredictionRepository().latest_predictions()


@router.post("/evaluate-due", response_model=list[PredictionOutcome])
def evaluate_due_predictions() -> list[PredictionOutcome]:
    return PredictionEvaluator().evaluate_due_predictions()


@router.post("/{prediction_id}/evaluate", response_model=PredictionOutcome)
def evaluate_prediction(prediction_id: str) -> PredictionOutcome:
    return PredictionEvaluator().evaluate_prediction(prediction_id)


@router.post("/scheduler/run-daily", response_model=PredictionRun)
def run_scheduler_daily_job() -> PredictionRun:
    return PredictionScheduler().run_daily_prediction_job()


@router.get("/{symbol}/latest", response_model=list[PredictionRecord])
def latest_predictions_for_symbol(symbol: str) -> list[PredictionRecord]:
    return PredictionRepository().latest_predictions(symbol)


@router.get("/{symbol}", response_model=list[PredictionRecord])
def predictions_for_symbol(symbol: str) -> list[PredictionRecord]:
    return PredictionRepository().list_predictions(symbol=symbol, limit=500)
