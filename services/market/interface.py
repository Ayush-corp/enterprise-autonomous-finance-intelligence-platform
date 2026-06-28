from abc import ABC, abstractmethod

from domain import MarketSnapshot


class MarketDataService(ABC):

    @abstractmethod
    def get_market_snapshot(self, symbol: str) -> MarketSnapshot:
        pass