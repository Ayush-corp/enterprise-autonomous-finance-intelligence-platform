from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from domain.graph_state import GraphState
from repositories.db import get_connection, initialize_database


class AnalysisRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        initialize_database(db_path)

    def save_analysis(
        self,
        *,
        symbol: str,
        country: str,
        horizon: str,
        request_payload: dict[str, object],
        graph_state: GraphState,
    ) -> str:
        recommendation = graph_state.recommendation.action if graph_state.recommendation else ""
        confidence = graph_state.recommendation.confidence if graph_state.recommendation else 0.0
        analysis_id = str(uuid4())
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT INTO analysis_runs (
                    id, symbol, country, horizon, request_payload_json, graph_state_json,
                    recommendation, confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    analysis_id,
                    symbol,
                    country,
                    horizon,
                    json.dumps(request_payload),
                    graph_state.model_dump_json(),
                    recommendation,
                    confidence,
                    datetime.utcnow().isoformat(),
                ),
            )
        return analysis_id
