from __future__ import annotations

from typing import Sequence, Type

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config.settings import settings
from infrastructure.llm.models import (
    LLMMessage,
    LLMResponse,
    LLMUsage,
)
from infrastructure.llm.provider import LLMProvider


class LLMClient(LLMProvider):

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        temperature: float = 0.0,
    ) -> LLMResponse:

        response = await self._client.chat.completions.create(
            model=settings.openai_model,
            temperature=temperature,
            messages=[
                {
                    "role": m.role,
                    "content": m.content,
                }
                for m in messages
            ],
        )

        choice = response.choices[0]

        usage = response.usage

        return LLMResponse(
            model=response.model,
            finish_reason=choice.finish_reason,
            content=choice.message.content,
            usage=LLMUsage(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            ),
        )

    async def structured_chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        response_model: Type[BaseModel],
        temperature: float = 0.0,
    ) -> BaseModel:

        response = await self._client.beta.chat.completions.parse(
            model=settings.openai_model,
            temperature=temperature,
            messages=[
                {
                    "role": m.role,
                    "content": m.content,
                }
                for m in messages
            ],
            response_format=response_model,
        )

        return response.choices[0].message.parsed