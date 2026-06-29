from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class NewsAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(..., min_length=1)
    company_name: str | None = None
    max_articles: int = Field(default=20, ge=5, le=100)


class NewsItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    summary: str
    source: str
    url: str
    sentiment: str
    relevance_score: float


class NewsAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overall_sentiment: str
    confidence: float
    summary: str
    articles: list[NewsItem]