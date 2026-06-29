import pytest

from domain.technical import TechnicalAnalysis
from infrastructure.llm.mock_provider import MockLLMProvider
from services.llm.service import LLMService


@pytest.mark.asyncio
async def test_llm_service_returns_structured_domain_model():
    service = LLMService(MockLLMProvider())

    result = await service.structured(
        "system",
        "Symbol: RELIANCE.NS",
        TechnicalAnalysis,
    )

    assert result.structured is not None
    assert result.structured.symbol == "RELIANCE.NS"
    assert result.metadata["provider"] == "mock"
