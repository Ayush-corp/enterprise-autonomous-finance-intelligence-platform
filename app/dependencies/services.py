from functools import lru_cache

from app.config import get_settings
from infrastructure.llm.client import OpenAILLMProvider
from infrastructure.llm.mock_provider import MockLLMProvider
from infrastructure.llm.provider import LLMProvider
from infrastructure.market.country_router_provider import CountryRouterMarketDataProvider
from infrastructure.market.fallback_provider import FallbackMarketDataProvider
from infrastructure.market.massive_provider import MassiveMarketDataProvider
from infrastructure.market.mock_provider import MockMarketDataProvider
from infrastructure.market.provider import MarketDataProvider
from infrastructure.market.yfinance_provider import YFinanceMarketDataProvider
from infrastructure.news.mock_provider import MockNewsProvider
from infrastructure.news.newsapi_provider import NewsAPIProvider
from infrastructure.news.provider import NewsProvider
from services.llm.service import LLMService


@lru_cache
def get_llm_provider() -> LLMProvider:
    settings = get_settings()
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
    settings = get_settings()
    yfinance_provider = YFinanceMarketDataProvider()
    if settings.market_provider.lower() in {"yfinance", "yahoo", "yahoo_finance"}:
        return yfinance_provider
    if settings.market_provider.lower() in {"auto", "live"}:
        massive_provider = MassiveMarketDataProvider(
            api_key=settings.massive_api_key,
            base_url=settings.massive_base_url,
            timeout=settings.request_timeout,
        )
        return CountryRouterMarketDataProvider(
            us_provider=massive_provider,
            india_provider=yfinance_provider,
            default_provider=yfinance_provider,
        )
    if settings.market_provider.lower() in {"massive", "polygon"}:
        massive_provider = MassiveMarketDataProvider(
            api_key=settings.massive_api_key,
            base_url=settings.massive_base_url,
            timeout=settings.request_timeout,
        )
        return FallbackMarketDataProvider(
            [
                massive_provider,
                yfinance_provider,
            ]
        )
    return MockMarketDataProvider()


@lru_cache
def get_news_provider() -> NewsProvider:
    settings = get_settings()
    if settings.news_provider.lower() in {"newsapi", "news_api", "live"}:
        return NewsAPIProvider(
            api_key=settings.news_api_key,
            timeout=settings.request_timeout,
        )
    return MockNewsProvider()
