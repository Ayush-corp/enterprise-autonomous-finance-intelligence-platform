from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from domain.prediction import PredictionAccuracySummary, PredictionHorizon
from repositories.accuracy_repository import AccuracyRepository
from repositories.prediction_repository import PredictionRepository


class AccuracyService:
    def __init__(
        self,
        prediction_repository: PredictionRepository | None = None,
        accuracy_repository: AccuracyRepository | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self._prediction_repository = prediction_repository or PredictionRepository(db_path)
        self._accuracy_repository = accuracy_repository or AccuracyRepository(db_path)

    def get_accuracy_summary(
        self,
        symbol: str | None = None,
        horizon: PredictionHorizon | None = None,
        days: int = 90,
    ) -> PredictionAccuracySummary:
        since = date.today() - timedelta(days=days)
        predictions = self._prediction_repository.list_predictions(symbol=symbol, horizon=horizon, limit=10_000)
        outcomes = self._accuracy_repository.list_outcomes_since(
            since,
            symbol=symbol,
            horizon=horizon.value if horizon else None,
        )

        evaluated = len(outcomes)
        open_predictions = len([prediction for prediction in predictions if prediction.status.value == "open"])
        directional_correct = sum(int(row["is_directionally_correct"]) for row in outcomes)
        market_beating = sum(int(row["is_market_beating"]) for row in outcomes)
        wins = sum(1 for row in outcomes if float(row["actual_return_pct"]) > 0)
        actual_returns = [float(row["actual_return_pct"]) for row in outcomes]
        alphas = [float(row["alpha_pct"]) for row in outcomes]

        return PredictionAccuracySummary(
            total_predictions=len(predictions),
            evaluated_predictions=evaluated,
            open_predictions=open_predictions,
            directional_accuracy_pct=self._pct(directional_correct, evaluated),
            market_beating_pct=self._pct(market_beating, evaluated),
            avg_actual_return_pct=self._avg(actual_returns),
            avg_alpha_pct=self._avg(alphas),
            win_rate_pct=self._pct(wins, evaluated),
            by_horizon=self._breakdown(outcomes, "horizon"),
            by_symbol=self._breakdown(outcomes, "symbol"),
        )

    def _breakdown(self, rows, key: str) -> dict[str, dict[str, float | int]]:
        grouped: dict[str, list] = {}
        for row in rows:
            grouped.setdefault(row[key], []).append(row)
        result: dict[str, dict[str, float | int]] = {}
        for group_key, group_rows in grouped.items():
            evaluated = len(group_rows)
            result[group_key] = {
                "evaluated_predictions": evaluated,
                "directional_accuracy_pct": self._pct(
                    sum(int(row["is_directionally_correct"]) for row in group_rows),
                    evaluated,
                ),
                "market_beating_pct": self._pct(
                    sum(int(row["is_market_beating"]) for row in group_rows),
                    evaluated,
                ),
                "avg_actual_return_pct": self._avg([float(row["actual_return_pct"]) for row in group_rows]),
                "avg_alpha_pct": self._avg([float(row["alpha_pct"]) for row in group_rows]),
            }
        return result

    def _pct(self, numerator: int, denominator: int) -> float:
        return round((numerator / denominator) * 100, 2) if denominator else 0.0

    def _avg(self, values: list[float]) -> float:
        return round(sum(values) / len(values), 4) if values else 0.0
