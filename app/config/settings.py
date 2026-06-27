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

    llm_provider: str

    llm_model: str

    openai_api_key: str = ""

    google_api_key: str = ""

    temperature: float

    max_tokens: int

    # ----------------------------
    # Market
    # ----------------------------

    market_provider: str

    # ----------------------------
    # News
    # ----------------------------

    news_provider: str

    # ----------------------------
    # Memory
    # ----------------------------

    vector_db: str

    chroma_path: str

    # ----------------------------
    # Network
    # ----------------------------

    request_timeout: int

    max_retries: int

    # ----------------------------
    # Logging
    # ----------------------------

    log_level: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()