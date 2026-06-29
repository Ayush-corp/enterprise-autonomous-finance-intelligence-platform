from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, Type

from pydantic import BaseModel

from infrastructure.llm.models import (
    LLMMessage,
    LLMResponse,
)


class LLMProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        temperature: float = 0.0,
    ) -> LLMResponse:
        ...

    @abstractmethod
    async def structured_chat(
        self,
        *,
        messages: Sequence[LLMMessage],
        response_model: Type[BaseModel],
        temperature: float = 0.0,
    ) -> BaseModel:
        ...