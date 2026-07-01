from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from domain.prediction import WatchlistSymbol
from repositories.db import get_connection, initialize_database


class WatchlistRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        initialize_database(db_path)

    def save(self, item: WatchlistSymbol) -> WatchlistSymbol:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO watchlist_symbols (
                    id, symbol, country, is_active, created_at, updated_at, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.id,
                    item.symbol,
                    item.country,
                    int(item.is_active),
                    item.created_at.isoformat(),
                    item.updated_at.isoformat(),
                    json.dumps(item.metadata),
                ),
            )
        return item

    def get(self, symbol: str) -> WatchlistSymbol | None:
        with get_connection(self._db_path) as connection:
            row = connection.execute(
                "SELECT * FROM watchlist_symbols WHERE symbol = ?",
                (symbol.upper(),),
            ).fetchone()
        return self._from_row(row) if row else None

    def list_active(self) -> list[WatchlistSymbol]:
        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM watchlist_symbols WHERE is_active = 1 ORDER BY symbol"
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def deactivate(self, symbol: str) -> None:
        now = datetime.utcnow().isoformat()
        with get_connection(self._db_path) as connection:
            connection.execute(
                "UPDATE watchlist_symbols SET is_active = 0, updated_at = ? WHERE symbol = ?",
                (now, symbol.upper()),
            )

    def count_active(self) -> int:
        with get_connection(self._db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM watchlist_symbols WHERE is_active = 1"
            ).fetchone()
        return int(row["count"])

    def _from_row(self, row) -> WatchlistSymbol:
        return WatchlistSymbol(
            id=row["id"],
            symbol=row["symbol"],
            country=row["country"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata_json"]),
        )
