from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from domain.enums import Environment, Provider


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    APP_NAME: str = "Autonomous Investing Agent"
    ENVIRONMENT: Environment = Environment.DEV
    LOG_LEVEL: str = "INFO"
    OPENAI_API_KEY: str = Field(default="")
    LLM_PROVIDER: Provider = Provider.OPENAI
    CHROMA_PATH: str = "./data/chroma"
    MARKET_CACHE_TTL: int = 300


@lru_cache
def get_settings():
    return Settings()