from __future__ import annotations

from abc import ABC, abstractmethod


class MarketDataProvider(ABC):

    @abstractmethod
    async def technical_indicators(
        self,
        symbol: str,
    ) -> str:
        ...

    @abstractmethod
    async def fundamentals(
        self,
        symbol: str,
    ) -> str:
        ...

    @abstractmethod
    async def macro_data(
        self,
    ) -> str:
        ...

    @abstractmethod
    async def quote(
        self,
        symbol: str,
    ) -> str:
        ...