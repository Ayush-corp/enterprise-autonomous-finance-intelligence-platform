import pytest

from agents.base import BaseAgent
from app.core.exceptions import ExternalProviderError


class FlakyAgent(BaseAgent[str, str, str]):
    name = "flaky"

    def __init__(self) -> None:
        super().__init__(max_attempts=3)
        self.calls = 0

    async def execute(self, prepared_input: str) -> str:
        self.calls += 1
        if self.calls < 2:
            raise ExternalProviderError("temporary failure")
        return prepared_input.upper()


@pytest.mark.asyncio
async def test_base_agent_retries_external_provider_failures():
    agent = FlakyAgent()

    result = await agent.run("reliance.ns")

    assert result == "RELIANCE.NS"
    assert agent.calls == 2
