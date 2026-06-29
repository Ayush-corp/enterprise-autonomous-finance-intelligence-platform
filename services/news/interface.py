from abc import ABC, abstractmethod

from domain.news import NewsAnalysis


class NewsService(ABC):

    @abstractmethod
    async def get_news(self, symbol: str) -> NewsAnalysis:
        pass