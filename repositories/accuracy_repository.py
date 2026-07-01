from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from domain.prediction import PredictionOutcome
from repositories.db import get_connection, initialize_database


class AccuracyRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        initialize_database(db_path)

    def save_outcome(self, outcome: PredictionOutcome) -> PredictionOutcome:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO prediction_outcomes (
                    id, prediction_id, evaluation_date, exit_price, actual_return_pct,
                    benchmark_symbol, benchmark_return_pct, alpha_pct,
                    is_directionally_correct, is_market_beating, is_risk_adjusted_success,
                    evaluated_at, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    outcome.id,
                    outcome.prediction_id,
                    outcome.evaluation_date.isoformat(),
                    outcome.exit_price,
                    outcome.actual_return_pct,
                    outcome.benchmark_symbol,
                    outcome.benchmark_return_pct,
                    outcome.alpha_pct,
                    int(outcome.is_directionally_correct),
                    int(outcome.is_market_beating),
                    int(outcome.is_risk_adjusted_success),
                    outcome.evaluated_at.isoformat(),
                    json.dumps(outcome.metadata),
                ),
            )
        return outcome

    def get_outcome_for_prediction(self, prediction_id: str) -> PredictionOutcome | None:
        with get_connection(self._db_path) as connection:
            row = connection.execute(
                "SELECT * FROM prediction_outcomes WHERE prediction_id = ?",
                (prediction_id,),
            ).fetchone()
        return self._from_row(row) if row else None

    def list_outcomes_since(self, since: date, symbol: str | None = None, horizon: str | None = None):
        query = """
            SELECT o.*, p.symbol, p.horizon, p.status
            FROM prediction_outcomes o
            JOIN predictions p ON p.id = o.prediction_id
            WHERE o.evaluation_date >= ?
        """
        params: list[object] = [since.isoformat()]
        if symbol:
            query += " AND p.symbol = ?"
            params.append(symbol.upper())
        if horizon:
            query += " AND p.horizon = ?"
            params.append(horizon)
        with get_connection(self._db_path) as connection:
            return connection.execute(query, params).fetchall()

    def _from_row(self, row) -> PredictionOutcome:
        return PredictionOutcome(
            id=row["id"],
            prediction_id=row["prediction_id"],
            evaluation_date=date.fromisoformat(row["evaluation_date"]),
            exit_price=float(row["exit_price"]),
            actual_return_pct=float(row["actual_return_pct"]),
            benchmark_symbol=row["benchmark_symbol"],
            benchmark_return_pct=float(row["benchmark_return_pct"]),
            alpha_pct=float(row["alpha_pct"]),
            is_directionally_correct=bool(row["is_directionally_correct"]),
            is_market_beating=bool(row["is_market_beating"]),
            is_risk_adjusted_success=bool(row["is_risk_adjusted_success"]),
            evaluated_at=datetime.fromisoformat(row["evaluated_at"]),
            metadata=json.loads(row["metadata_json"]),
        )
