from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from domain.prediction import WatchlistSymbol
from repositories.watchlist_repository import WatchlistRepository


class WatchlistService:
    default_symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS"]

    def __init__(self, repository: WatchlistRepository | None = None, db_path: str | Path | None = None) -> None:
        self._repository = repository or WatchlistRepository(db_path)

    def add_symbol(self, symbol: str, country: str | None = None) -> WatchlistSymbol:
        normalized_symbol = symbol.strip().upper()
        normalized_country = (country or self._infer_country(normalized_symbol)).strip().upper()
        existing = self._repository.get(normalized_symbol)
        now = datetime.utcnow()
        if existing:
            item = existing.model_copy(
                update={
                    "country": normalized_country,
                    "is_active": True,
                    "updated_at": now,
                }
            )
            return self._repository.save(item)
        item = WatchlistSymbol(
            id=str(uuid4()),
            symbol=normalized_symbol,
            country=normalized_country,
            is_active=True,
            created_at=now,
            updated_at=now,
            metadata={},
        )
        return self._repository.save(item)

    def remove_symbol(self, symbol: str) -> None:
        self._repository.deactivate(symbol)

    def list_active_symbols(self) -> list[WatchlistSymbol]:
        return self._repository.list_active()

    def seed_default_watchlist(self) -> list[WatchlistSymbol]:
        if self._repository.count_active() > 0:
            return self.list_active_symbols()
        return [self.add_symbol(symbol, "IN") for symbol in self.default_symbols]

    def _infer_country(self, symbol: str) -> str:
        if symbol.endswith((".NS", ".BO")):
            return "IN"
        return "US"
