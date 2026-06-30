from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ----------------------------
    # Application
    # ----------------------------

    app_name: str = Field(default="Autonomous Investing Agent")
    app_version: str = Field(default="2.0.0")

    environment: str = "development"

    debug: bool = True

    # ----------------------------
    # LLM
    # ----------------------------

    llm_provider: str = "mock"

    llm_model: str = "gpt-4o-mini"
    openai_model: str = "gpt-4o-mini"

    openai_api_key: str = ""

    google_api_key: str = ""

    enable_live_llm: bool = False

    temperature: float = 0.2

    max_tokens: int = 1500

    # ----------------------------
    # Market
    # ----------------------------

    market_provider: str = "mock"

    # ----------------------------
    # News
    # ----------------------------

    news_provider: str = "mock"

    # ----------------------------
    # Memory
    # ----------------------------

    vector_db: str = "chroma"

    chroma_path: str = "./.chroma"

    # ----------------------------
    # Network
    # ----------------------------

    request_timeout: int = 30

    max_retries: int = 3

    # ----------------------------
    # Logging
    # ----------------------------

    log_level: str = "INFO"

    langsmith_api_key: str = ""
    langsmith_project: str = ""
    redis_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def __getattr__(name: str):
    return getattr(settings, name)
