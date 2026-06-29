from functools import lru_cache

from app.config import settings
from infrastructure.llm.client import OpenAILLMProvider
from infrastructure.llm.mock_provider import MockLLMProvider
from infrastructure.llm.provider import LLMProvider
from infrastructure.market.mock_provider import MockMarketDataProvider
from infrastructure.market.provider import MarketDataProvider
from infrastructure.news.mock_provider import MockNewsProvider
from infrastructure.news.provider import NewsProvider
from services.llm.service import LLMService


@lru_cache
def get_llm_provider() -> LLMProvider:
    if settings.enable_live_llm and settings.llm_provider.lower() == "openai" and settings.openai_api_key:
        return OpenAILLMProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model or settings.llm_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    return MockLLMProvider()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService(get_llm_provider())


@lru_cache
def get_market_provider() -> MarketDataProvider:
    return MockMarketDataProvider()


@lru_cache
def get_news_provider() -> NewsProvider:
    return MockNewsProvider()
