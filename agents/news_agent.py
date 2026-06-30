from agents.base import BaseAgent
from domain.news import NewsAnalysis
from infrastructure.news.provider import NewsProvider


class NewsAgent(BaseAgent[str, str, NewsAnalysis]):
    name = "news"

    def __init__(self, news_provider: NewsProvider) -> None:
        super().__init__()
        self.news_provider = news_provider

    async def execute(self, prepared_input: str) -> NewsAnalysis:
        return await self.news_provider.analyze(prepared_input.strip().upper())
