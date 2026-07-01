from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from domain.prediction import DataFreshnessRecord
from repositories.data_freshness_repository import DataFreshnessRepository


class DataFreshnessService:
    default_ttls = {
        "market": 24 * 60,
        "news": 240,
        "fundamental": 10080,
        "macro": 1440,
        "intelligence": 10080,
    }

    def __init__(
        self,
        repository: DataFreshnessRepository | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self._repository = repository or DataFreshnessRepository(db_path)

    def is_fresh(self, symbol: str, country: str | None, data_type: str) -> bool:
        record = self._repository.get(symbol, country or "US", data_type)
        return record is not None and record.fresh_until > datetime.utcnow()

    def mark_refreshed(
        self,
        symbol: str,
        country: str | None,
        data_type: str,
        source: str,
        ttl_minutes: int | None = None,
    ) -> DataFreshnessRecord:
        now = datetime.utcnow()
        ttl = ttl_minutes if ttl_minutes is not None else self.default_ttls.get(data_type, 1440)
        existing = self._repository.get(symbol, country or "US", data_type)
        record = DataFreshnessRecord(
            id=existing.id if existing else str(uuid4()),
            symbol=symbol.strip().upper(),
            country=(country or "US").strip().upper(),
            data_type=data_type,
            last_refreshed_at=now,
            fresh_until=now + timedelta(minutes=ttl),
            source=source,
            metadata={},
        )
        return self._repository.save(record)

    def freshness_metadata(self, symbol: str, country: str | None) -> dict[str, object]:
        metadata: dict[str, object] = {}
        for data_type in self.default_ttls:
            record = self._repository.get(symbol, country or "US", data_type)
            if record:
                metadata[data_type] = {
                    "source": record.source,
                    "last_refreshed_at": record.last_refreshed_at.isoformat(),
                    "fresh_until": record.fresh_until.isoformat(),
                    "is_fresh": record.fresh_until > datetime.utcnow(),
                }
        return metadata
