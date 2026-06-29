from enum import Enum


class Trend(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"


class RecommendationAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Provider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"


class Environment(str, Enum):
    DEV = "development"
    TEST = "test"
    PROD = "production"