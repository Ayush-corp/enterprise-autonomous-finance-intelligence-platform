from functools import lru_cache

from infrastructure.market.yfinance_service import (
    YFinanceMarketService,
)

from infrastructure.news.news_service import (
    DummyNewsService,
)

from infrastructure.llm.openai_service import (
    OpenAIService,
)

from infrastructure.memory.chroma_repository import (
    ChromaMemoryRepository,
)

from infrastructure.memory.memory_service import (
    DefaultMemoryService,
)


@lru_cache
def get_market_service():
    return YFinanceMarketService()


@lru_cache
def get_news_service():
    return DummyNewsService()


@lru_cache
def get_llm_service():
    return OpenAIService()


@lru_cache
def get_memory_service():

    repository = ChromaMemoryRepository()

    return DefaultMemoryService(
        repository,
    )