from pydantic import BaseModel
from domain.enums import Sentiment


class NewsArticle(BaseModel):
    title: str
    summary: str
    source: str
    published_at: str
    sentiment: Sentiment
    confidence: float


class NewsAnalysis(BaseModel):
    articles: list[NewsArticle]
    overall_sentiment: Sentiment
    confidence: float