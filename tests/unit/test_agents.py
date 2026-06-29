import pytest

from agents.market_agent import MarketAgent
from agents.news_agent import NewsAgent
from agents.technical_agent import TechnicalAgent
from domain.graph_state import GraphState
from domain.market import MarketSnapshot
from domain.news import NewsAnalysis
from infrastructure.llm.mock_provider import MockLLMProvider
from infrastructure.market.mock_provider import MockMarketDataProvider
from infrastructure.news.mock_provider import MockNewsProvider
from services.llm.service import LLMService


@pytest.mark.asyncio
async def test_market_agent_returns_domain_model():
    result = await MarketAgent(MockMarketDataProvider()).run("reliance.ns")

    assert isinstance(result, MarketSnapshot)
    assert result.symbol == "RELIANCE.NS"


@pytest.mark.asyncio
async def test_news_agent_returns_domain_model():
    result = await NewsAgent(MockNewsProvider()).run("reliance.ns")

    assert isinstance(result, NewsAnalysis)
    assert result.symbol == "RELIANCE.NS"


@pytest.mark.asyncio
async def test_technical_agent_uses_graph_state_and_llm_service():
    market = await MockMarketDataProvider().get_snapshot("RELIANCE.NS")
    state = GraphState(symbol="RELIANCE.NS", market=market)
    service = LLMService(MockLLMProvider())

    result = await TechnicalAgent(service).run(state)

    assert result.symbol == "RELIANCE.NS"
    assert result.confidence > 0
