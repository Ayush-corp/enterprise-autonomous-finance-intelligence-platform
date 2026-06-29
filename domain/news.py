from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    title: str
    source: str
    published_at: str
    sentiment: str
    score: float


class NewsAnalysis(BaseModel):
    symbol: str
    sentiment: str
    key_risks: list[str]
    catalysts: list[str]
    confidence: float
    summary: str
    articles: list[NewsArticle] = Field(default_factory=list)
