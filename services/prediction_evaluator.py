from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from app.config import get_settings
from app.dependencies.services import get_market_provider
from domain.prediction import PredictionOutcome, PredictionStatus
from repositories.accuracy_repository import AccuracyRepository
from repositories.prediction_repository import PredictionRepository


class PredictionEvaluator:
    def __init__(
        self,
        prediction_repository: PredictionRepository | None = None,
        accuracy_repository: AccuracyRepository | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self._prediction_repository = prediction_repository or PredictionRepository(db_path)
        self._accuracy_repository = accuracy_repository or AccuracyRepository(db_path)

    def evaluate_due_predictions(self) -> list[PredictionOutcome]:
        due = self._prediction_repository.due_predictions(date.today())
        outcomes: list[PredictionOutcome] = []
        for prediction in due:
            outcomes.append(self.evaluate_prediction(prediction.id))
        return outcomes

    def evaluate_prediction(self, prediction_id: str) -> PredictionOutcome:
        prediction = self._prediction_repository.get_prediction(prediction_id)
        if prediction is None:
            raise ValueError(f"Prediction not found: {prediction_id}")
        existing = self._accuracy_repository.get_outcome_for_prediction(prediction_id)
        if existing:
            return existing

        market_provider = get_market_provider()
        exit_snapshot = asyncio.run(market_provider.get_snapshot(prediction.symbol, prediction.country))
        benchmark_symbol = get_settings().default_benchmark_symbol
        benchmark_snapshot = asyncio.run(market_provider.get_snapshot(benchmark_symbol, "IN"))
        benchmark_entry_price = float(
            prediction.graph_state.get("metadata", {}).get(
                "benchmark_entry_price",
                benchmark_snapshot.current_price,
            )
        )

        actual_return_pct = ((exit_snapshot.current_price - prediction.entry_price) / prediction.entry_price) * 100
        benchmark_return_pct = ((benchmark_snapshot.current_price - benchmark_entry_price) / benchmark_entry_price) * 100
        alpha_pct = actual_return_pct - benchmark_return_pct
        action = prediction.recommendation.upper()
        is_directionally_correct = (
            (action == "BUY" and actual_return_pct > 0)
            or (action == "SELL" and actual_return_pct < 0)
            or (action == "HOLD" and abs(actual_return_pct) <= 2)
            or (action == "AVOID" and actual_return_pct <= 0)
        )
        is_market_beating = alpha_pct > 0
        is_risk_adjusted_success = is_directionally_correct and (
            is_market_beating or prediction.risk_level.lower() in {"low", "medium", "moderate"}
        )

        outcome = PredictionOutcome(
            id=str(uuid4()),
            prediction_id=prediction.id,
            evaluation_date=date.today(),
            exit_price=exit_snapshot.current_price,
            actual_return_pct=actual_return_pct,
            benchmark_symbol=benchmark_symbol,
            benchmark_return_pct=benchmark_return_pct,
            alpha_pct=alpha_pct,
            is_directionally_correct=is_directionally_correct,
            is_market_beating=is_market_beating,
            is_risk_adjusted_success=is_risk_adjusted_success,
            evaluated_at=datetime.utcnow(),
            metadata={},
        )
        saved = self._accuracy_repository.save_outcome(outcome)
        self._prediction_repository.update_prediction_status(prediction.id, PredictionStatus.EVALUATED)
        return saved
