from typing import TypeVar

from pydantic import BaseModel

from infrastructure.llm.models import LLMMessage, LLMResult
from infrastructure.llm.provider import LLMProvider


T = TypeVar("T", bound=BaseModel)


class LLMService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    @property
    def provider_name(self) -> str:
        return self._provider.name

    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResult[BaseModel]:
        return await self._provider.complete(system_prompt, user_prompt)

    async def structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> LLMResult[T]:
        return await self._provider.structured(system_prompt, user_prompt, response_model)

    async def structured_chat(
        self,
        messages: list[LLMMessage],
        response_model: type[T],
    ) -> T:
        system_prompt = "\n\n".join(
            message.content for message in messages if message.role == "system"
        )
        user_prompt = "\n\n".join(
            message.content for message in messages if message.role != "system"
        )
        result = await self.structured(system_prompt, user_prompt, response_model)
        if result.structured is None:
            raise ValueError("LLM provider returned no structured output")
        return result.structured
