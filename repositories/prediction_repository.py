from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from domain.prediction import PredictionHorizon, PredictionRecord, PredictionRun, PredictionStatus, RunStatus
from repositories.db import get_connection, initialize_database


class PredictionRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        initialize_database(db_path)

    def save_run(self, run: PredictionRun) -> PredictionRun:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO prediction_runs (
                    id, run_type, started_at, finished_at, status, symbols_requested,
                    symbols_completed, error_message, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.id,
                    run.run_type,
                    run.started_at.isoformat(),
                    run.finished_at.isoformat() if run.finished_at else None,
                    run.status.value,
                    run.symbols_requested,
                    run.symbols_completed,
                    run.error_message,
                    json.dumps(run.metadata),
                ),
            )
        return run

    def get_run(self, run_id: str) -> PredictionRun | None:
        with get_connection(self._db_path) as connection:
            row = connection.execute("SELECT * FROM prediction_runs WHERE id = ?", (run_id,)).fetchone()
        return self._run_from_row(row) if row else None

    def save_prediction(self, prediction: PredictionRecord) -> PredictionRecord:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO predictions (
                    id, run_id, symbol, country, horizon, prediction_date, evaluation_due_date,
                    entry_price, predicted_price, predicted_return_pct, recommendation,
                    confidence, risk_level, reasoning_summary, graph_state_json, created_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    prediction.id,
                    prediction.run_id,
                    prediction.symbol,
                    prediction.country,
                    prediction.horizon.value,
                    prediction.prediction_date.isoformat(),
                    prediction.evaluation_due_date.isoformat(),
                    prediction.entry_price,
                    prediction.predicted_price,
                    prediction.predicted_return_pct,
                    prediction.recommendation,
                    prediction.confidence,
                    prediction.risk_level,
                    prediction.reasoning_summary,
                    json.dumps(prediction.graph_state),
                    prediction.created_at.isoformat(),
                    prediction.status.value,
                ),
            )
        return prediction

    def get_prediction(self, prediction_id: str) -> PredictionRecord | None:
        with get_connection(self._db_path) as connection:
            row = connection.execute("SELECT * FROM predictions WHERE id = ?", (prediction_id,)).fetchone()
        return self._prediction_from_row(row) if row else None

    def list_predictions(
        self,
        symbol: str | None = None,
        horizon: PredictionHorizon | None = None,
        status: PredictionStatus | None = None,
        limit: int = 100,
    ) -> list[PredictionRecord]:
        clauses: list[str] = []
        params: list[object] = []
        if symbol:
            clauses.append("symbol = ?")
            params.append(symbol.upper())
        if horizon:
            clauses.append("horizon = ?")
            params.append(horizon.value)
        if status:
            clauses.append("status = ?")
            params.append(status.value)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        params.append(limit)
        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                f"SELECT * FROM predictions {where} ORDER BY created_at DESC LIMIT ?",
                params,
            ).fetchall()
        return [self._prediction_from_row(row) for row in rows]

    def latest_predictions(self, symbol: str | None = None) -> list[PredictionRecord]:
        params: list[object] = []
        where = ""
        if symbol:
            where = "WHERE p.symbol = ?"
            params.append(symbol.upper())
        query = f"""
            SELECT p.* FROM predictions p
            JOIN (
                SELECT symbol, horizon, MAX(created_at) AS max_created_at
                FROM predictions
                {'WHERE symbol = ?' if symbol else ''}
                GROUP BY symbol, horizon
            ) latest
            ON p.symbol = latest.symbol
            AND p.horizon = latest.horizon
            AND p.created_at = latest.max_created_at
            {where}
            ORDER BY p.symbol, p.horizon
        """
        if symbol:
            params = [symbol.upper(), symbol.upper()]
        with get_connection(self._db_path) as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._prediction_from_row(row) for row in rows]

    def due_predictions(self, due_date: date) -> list[PredictionRecord]:
        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                """
                SELECT * FROM predictions
                WHERE evaluation_due_date <= ? AND status = ?
                ORDER BY evaluation_due_date ASC
                """,
                (due_date.isoformat(), PredictionStatus.OPEN.value),
            ).fetchall()
        return [self._prediction_from_row(row) for row in rows]

    def update_prediction_status(self, prediction_id: str, status: PredictionStatus) -> None:
        with get_connection(self._db_path) as connection:
            connection.execute(
                "UPDATE predictions SET status = ? WHERE id = ?",
                (status.value, prediction_id),
            )

    def _run_from_row(self, row) -> PredictionRun:
        return PredictionRun(
            id=row["id"],
            run_type=row["run_type"],
            started_at=datetime.fromisoformat(row["started_at"]),
            finished_at=datetime.fromisoformat(row["finished_at"]) if row["finished_at"] else None,
            status=RunStatus(row["status"]),
            symbols_requested=row["symbols_requested"],
            symbols_completed=row["symbols_completed"],
            error_message=row["error_message"],
            metadata=json.loads(row["metadata_json"]),
        )

    def _prediction_from_row(self, row) -> PredictionRecord:
        confidence = float(row["confidence"])
        return PredictionRecord(
            id=row["id"],
            run_id=row["run_id"],
            symbol=row["symbol"],
            country=row["country"],
            horizon=PredictionHorizon(row["horizon"]),
            prediction_date=date.fromisoformat(row["prediction_date"]),
            evaluation_due_date=date.fromisoformat(row["evaluation_due_date"]),
            entry_price=float(row["entry_price"]),
            predicted_price=float(row["predicted_price"]),
            predicted_return_pct=float(row["predicted_return_pct"]),
            recommendation=row["recommendation"],
            confidence=confidence,
            risk_level=row["risk_level"],
            reasoning_summary=row["reasoning_summary"],
            graph_state=json.loads(row["graph_state_json"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            status=PredictionStatus(row["status"]),
            response_metadata={
                "disclaimer": "This is not financial advice. Use for research and education only.",
                "data_freshness": {},
                **({"confidence_warning": "Low confidence prediction"} if confidence < 0.6 else {}),
            },
        )
