from abc import ABC, abstractmethod

from domain.market import MarketSnapshot


class MarketDataProvider(ABC):
    name: str

    @abstractmethod
    async def get_snapshot(self, symbol: str, country: str = "US") -> MarketSnapshot:
        raise NotImplementedError
