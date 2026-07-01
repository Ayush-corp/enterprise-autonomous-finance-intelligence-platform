from __future__ import annotations

from datetime import UTC, datetime

import httpx

from app.core.exceptions import NewsServiceError
from domain.news import NewsAnalysis, NewsArticle
from infrastructure.news.provider import NewsProvider


class NewsAPIProvider(NewsProvider):
    name = "newsapi"

    def __init__(self, api_key: str, *, timeout: float = 30.0) -> None:
        if not api_key:
            raise NewsServiceError("NEWS_API_KEY is required for live news")
        self._api_key = api_key
        self._timeout = timeout

    async def analyze(self, symbol: str) -> NewsAnalysis:
        ticker = symbol.strip().upper()
        params = {
            "q": ticker,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": self._api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get("https://newsapi.org/v2/everything", params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:
            raise NewsServiceError(f"NewsAPI request failed for {ticker}: {exc}") from exc

        if payload.get("status") != "ok":
            raise NewsServiceError(payload.get("message") or "NewsAPI returned a non-ok response")

        articles = [
            self._article_from_payload(item)
            for item in payload.get("articles", [])
            if item.get("title")
        ]
        if not articles:
            return NewsAnalysis(
                symbol=ticker,
                sentiment="neutral",
                key_risks=["No recent live news articles were returned for this symbol."],
                catalysts=[],
                confidence=0.25,
                summary=f"No recent NewsAPI articles were found for {ticker}.",
                articles=[],
            )

        average_score = sum(article.score for article in articles) / len(articles)
        sentiment = self._sentiment_label(average_score)
        positive_titles = [article.title for article in articles if article.score > 0.2][:3]
        negative_titles = [article.title for article in articles if article.score < -0.2][:3]

        return NewsAnalysis(
            symbol=ticker,
            sentiment=sentiment,
            key_risks=negative_titles,
            catalysts=positive_titles,
            confidence=min(0.85, 0.35 + (len(articles) / 20)),
            summary=(
                f"Live NewsAPI scan found {len(articles)} recent article(s) for {ticker}; "
                f"aggregate sentiment is {sentiment}."
            ),
            articles=articles,
        )

    def _article_from_payload(self, item: dict[str, object]) -> NewsArticle:
        title = str(item.get("title") or "")
        description = str(item.get("description") or "")
        score = self._score_text(f"{title} {description}")
        source = item.get("source") or {}
        if isinstance(source, dict):
            source_name = str(source.get("name") or "Unknown")
        else:
            source_name = "Unknown"

        published_at = str(item.get("publishedAt") or datetime.now(UTC).isoformat())
        return NewsArticle(
            title=title,
            source=source_name,
            published_at=published_at,
            sentiment=self._sentiment_label(score),
            score=score,
        )

    def _score_text(self, text: str) -> float:
        normalized = text.lower()
        positive_words = (
            "beat",
            "beats",
            "growth",
            "gain",
            "gains",
            "surge",
            "rally",
            "upgrade",
            "profit",
            "record",
            "strong",
            "bullish",
        )
        negative_words = (
            "miss",
            "falls",
            "fall",
            "drop",
            "drops",
            "loss",
            "downgrade",
            "weak",
            "probe",
            "lawsuit",
            "bearish",
            "risk",
        )
        positives = sum(1 for word in positive_words if word in normalized)
        negatives = sum(1 for word in negative_words if word in normalized)
        score = (positives - negatives) / max(positives + negatives, 1)
        return max(-1.0, min(1.0, score))

    def _sentiment_label(self, score: float) -> str:
        if score > 0.2:
            return "positive"
        if score < -0.2:
            return "negative"
        return "neutral"
