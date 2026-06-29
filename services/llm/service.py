from __future__ import annotations

from typing import Sequence, Type

from pydantic import BaseModel

from infrastructure.llm.models import (
    LLMMessage,
    LLMResponse,
)
from infrastructure.llm.provider import LLMProvider


class LLMService:

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self._provider = provider

    async def chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        temperature: float = 0.0,
    ) -> LLMResponse:
        return await self._provider.chat(
            messages=messages,
            temperature=temperature,
        )

    async def structured_chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        response_model: Type[BaseModel],
        temperature: float = 0.0,
    ) -> BaseModel:
        return await self._provider.structured_chat(
            messages=messages,
            response_model=response_model,
            temperature=temperature,
        )