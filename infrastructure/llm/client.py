from __future__ import annotations

from typing import Type

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config.settings import settings


class LLMClient:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def structured_completion(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ):

        response = await self.client.responses.parse(
            model=settings.openai_model,
            input=prompt,
            text_format=schema,
        )

        return response.output_parsed

    async def complete(
        self,
        prompt: str,
    ):

        response = await self.client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )

        return response.output[0].content[0].parsed