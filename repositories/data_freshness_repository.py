from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from domain.prediction import DataFreshnessRecord
from repositories.db import get_connection, initialize_database


class DataFreshnessRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        initialize_database(db_path)

    def get(self, symbol: str, country: str, data_type: str) -> DataFreshnessRecord | None:
        with get_connection(self._db_path) as connection:
            row = connection.execute(
                """
                SELECT * FROM data_freshness
                WHERE symbol = ? AND country = ? AND data_type = ?
                """,
                (symbol.upper(), country.upper(), data_type),
            ).fetchone()
        return self._from_row(row) if row else None

    def save(self, record: DataFreshnessRecord) -> DataFreshnessRecord:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO data_freshness (
                    id, symbol, country, data_type, last_refreshed_at,
                    fresh_until, source, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.symbol,
                    record.country,
                    record.data_type,
                    record.last_refreshed_at.isoformat(),
                    record.fresh_until.isoformat(),
                    record.source,
                    json.dumps(record.metadata),
                ),
            )
        return record

    def _from_row(self, row) -> DataFreshnessRecord:
        return DataFreshnessRecord(
            id=row["id"],
            symbol=row["symbol"],
            country=row["country"],
            data_type=row["data_type"],
            last_refreshed_at=datetime.fromisoformat(row["last_refreshed_at"]),
            fresh_until=datetime.fromisoformat(row["fresh_until"]),
            source=row["source"],
            metadata=json.loads(row["metadata_json"]),
        )
