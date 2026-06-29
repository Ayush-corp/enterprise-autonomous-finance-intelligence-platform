from abc import ABC, abstractmethod

from domain.news import NewsAnalysis


class NewsProvider(ABC):
    name: str

    @abstractmethod
    async def analyze(self, symbol: str) -> NewsAnalysis:
        raise NotImplementedError
