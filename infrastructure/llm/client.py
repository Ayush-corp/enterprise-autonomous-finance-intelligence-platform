from typing import TypeVar

from pydantic import BaseModel

from app.core.exceptions import LLMProviderError
from infrastructure.llm.models import LLMResult, LLMUsage
from infrastructure.llm.provider import LLMProvider


T = TypeVar("T", bound=BaseModel)


class OpenAILLMProvider(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int) -> None:
        if not api_key:
            raise LLMProviderError("OpenAI API key is required for OpenAILLMProvider")
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResult[BaseModel]:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except Exception as exc:
            raise LLMProviderError(str(exc)) from exc

        usage = response.usage
        return LLMResult(
            content=response.choices[0].message.content or "",
            usage=LLMUsage(
                prompt_tokens=getattr(usage, "prompt_tokens", None),
                completion_tokens=getattr(usage, "completion_tokens", None),
                total_tokens=getattr(usage, "total_tokens", None),
            ),
            metadata={"model": self._model, "provider": self.name},
        )

    async def structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> LLMResult[T]:
        try:
            response = await self._client.beta.chat.completions.parse(
                model=self._model,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=response_model,
            )
        except Exception as exc:
            raise LLMProviderError(str(exc)) from exc

        message = response.choices[0].message
        parsed = message.parsed
        if parsed is None:
            raise LLMProviderError("OpenAI returned no parsed structured output")

        usage = response.usage
        return LLMResult(
            structured=parsed,
            usage=LLMUsage(
                prompt_tokens=getattr(usage, "prompt_tokens", None),
                completion_tokens=getattr(usage, "completion_tokens", None),
                total_tokens=getattr(usage, "total_tokens", None),
            ),
            metadata={"model": self._model, "provider": self.name},
        )
