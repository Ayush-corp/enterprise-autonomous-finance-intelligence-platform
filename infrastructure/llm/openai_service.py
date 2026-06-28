from openai import AsyncOpenAI

from app.config.settings import get_settings

from services.llm import LLMService


class OpenAIService(LLMService):

    def __init__(self):

        settings = get_settings()

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    async def generate(
        self,
        prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content