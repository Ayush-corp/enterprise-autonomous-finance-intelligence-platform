from domain.news import NewsAnalysis
from infrastructure.news.provider import NewsProvider


class MockNewsProvider(NewsProvider):
    name = "mock_news"

    async def analyze(self, symbol: str) -> NewsAnalysis:
        normalized_symbol = symbol.upper()
        return NewsAnalysis(
            symbol=normalized_symbol,
            sentiment="neutral",
            key_risks=["Mock news provider is configured; no live headlines were fetched."],
            catalysts=["Provider wiring and graph orchestration are available for integration testing."],
            confidence=0.5,
            summary="Deterministic mock news analysis for local development and tests.",
            articles=[],
        )
