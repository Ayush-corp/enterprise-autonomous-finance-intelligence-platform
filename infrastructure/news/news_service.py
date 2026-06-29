from domain.news import (
    NewsAnalysis,
    NewsArticle,
)

from domain.enums import Sentiment

from services.news import NewsService


class DummyNewsService(NewsService):

    async def get_news(
        self,
        symbol: str,
    ) -> NewsAnalysis:

        article = NewsArticle(
            title=f"{symbol} market update",
            summary="No news provider connected yet.",
            source="Internal",
            published_at="",
            sentiment=Sentiment.NEUTRAL,
            confidence=0.5,
        )

        return NewsAnalysis(
            articles=[article],
            overall_sentiment=Sentiment.NEUTRAL,
            confidence=0.5,
        )