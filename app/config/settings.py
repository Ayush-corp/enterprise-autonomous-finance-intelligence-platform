from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Environment
    env: str = "development"

    # LLM
    llm_provider: str = "openai"
    llm_model: str = "gpt-5.5"

    openai_api_key: str = ""
    google_api_key: str = ""

    temperature: float = 0.2

    # Market

    market_provider: str = "yfinance"

    # News

    news_provider: str = "google"

    # Memory

    vector_db: str = "chroma"
    chroma_path: str = "data/chroma"

    # Logging

    log_level: str = "INFO"

    # Network

    request_timeout: int = 30
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()