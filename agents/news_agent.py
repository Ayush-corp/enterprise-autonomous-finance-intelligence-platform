from agents.base import BaseAgent
from domain.news import NewsAnalysis
from infrastructure.news.provider import NewsProvider


class NewsAgent(BaseAgent[str, str, NewsAnalysis]):
    name = "news"

    def __init__(self, provider: NewsProvider) -> None:
        super().__init__()
        self._provider = provider

    def validate(self, agent_input: str) -> None:
        if not agent_input.strip():
            raise ValueError("symbol is required")

    async def execute(self, prepared_input: str) -> NewsAnalysis:
        return await self._provider.analyze(prepared_input.upper())
