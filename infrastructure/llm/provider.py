from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from infrastructure.llm.models import LLMResult


T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResult[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> LLMResult[T]:
        raise NotImplementedError
