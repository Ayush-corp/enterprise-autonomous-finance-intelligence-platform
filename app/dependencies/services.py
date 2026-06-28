from infrastructure.market.yfinance_service import YFinanceMarketService
from infrastructure.llm.openai_service import OpenAIService
from infrastructure.memory.chroma_service import ChromaMemoryService

_market_service = None
_llm_service = None
_memory_service = None


def get_market_service():
    global _market_service

    if _market_service is None:
        _market_service = YFinanceMarketService()

    return _market_service


def get_llm_service():
    global _llm_service

    if _llm_service is None:
        _llm_service = OpenAIService()

    return _llm_service


def get_memory_service():
    global _memory_service

    if _memory_service is None:
        _memory_service = ChromaMemoryService()

    return _memory_service