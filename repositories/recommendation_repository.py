from __future__ import annotations

from pathlib import Path

from domain.prediction import PredictionRecord
from repositories.prediction_repository import PredictionRepository


class RecommendationRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._prediction_repository = PredictionRepository(db_path)

    def latest(self, symbol: str | None = None) -> list[PredictionRecord]:
        return self._prediction_repository.latest_predictions(symbol)
