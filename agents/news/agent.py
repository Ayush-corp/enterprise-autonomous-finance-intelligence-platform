from __future__ import annotations

from agents.base import BaseAgent
from agents.news.models import (
    NewsAgentInput,
    NewsAgentOutput,
)
from agents.news.prompt import NEWS_PROMPT
from infrastructure.news.provider import NewsProvider
from services.llm.service import LLMService
from infrastructure.llm.models import LLMMessage


class NewsAgent(
    BaseAgent[
        NewsAgentInput,
        NewsAgentOutput,
    ]
):

    def __init__(
        self,
        news_provider: NewsProvider,
        llm: LLMService,
    ):
        super().__init__()
        self.news_provider = news_provider
        self.llm = llm

    async def prepare(
        self,
        state: NewsAgentInput,
    ):

        news = await self.news_provider.fetch(
            symbol=state.symbol,
            company_name=state.company_name,
            limit=state.max_articles,
        )

        prompt = NEWS_PROMPT.render(
            symbol=state.symbol,
            news=news,
        )

        return prompt

    async def execute(
        self,
        prepared: str,
    ):

        return await self.llm.structured_chat(
            messages=[
                LLMMessage(
                    role="user",
                    content=prepared,
                )
            ],
            response_model=NewsAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> NewsAgentOutput:
        return result