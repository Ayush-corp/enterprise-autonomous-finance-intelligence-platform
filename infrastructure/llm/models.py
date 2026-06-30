from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T", bound=BaseModel)


class LLMUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class LLMMessage(BaseModel):
    role: str
    content: str


class LLMResult(BaseModel, Generic[T]):
    content: str | None = None
    structured: T | None = None
    usage: LLMUsage = Field(default_factory=LLMUsage)
    metadata: dict[str, Any] = Field(default_factory=dict)
