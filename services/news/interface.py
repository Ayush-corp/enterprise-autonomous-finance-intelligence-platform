from abc import ABC, abstractmethod

from domain import NewsArticle


class NewsService(ABC):

    @abstractmethod
    def get_news(self, symbol: str) -> list[NewsArticle]:
        pass