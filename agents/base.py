import time
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import structlog
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.exceptions import AgentExecutionError, ExternalProviderError, LLMProviderError


InputT = TypeVar("InputT")
PreparedT = TypeVar("PreparedT")
OutputT = TypeVar("OutputT")


class BaseAgent(ABC, Generic[InputT, PreparedT, OutputT]):
    name: str

    def __init__(self, *, max_attempts: int = 3) -> None:
        self._max_attempts = max_attempts
        self._logger = structlog.get_logger(self.__class__.__name__)

    async def run(self, agent_input: InputT) -> OutputT:
        started_at = time.perf_counter()
        self._logger.info("agent_started", agent=self.name)
        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self._max_attempts),
                wait=wait_exponential(multiplier=0.2, min=0.2, max=2.0),
                retry=retry_if_exception_type((ExternalProviderError, LLMProviderError)),
                reraise=True,
            ):
                with attempt:
                    self.validate(agent_input)
                    prepared = await self.prepare(agent_input)
                    raw_output = await self.execute(prepared)
                    parsed = await self.parse(raw_output)
            latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
            self._logger.info("agent_succeeded", agent=self.name, latency_ms=latency_ms)
            return parsed
        except Exception as exc:
            latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
            self._logger.exception(
                "agent_failed",
                agent=self.name,
                latency_ms=latency_ms,
                error_type=type(exc).__name__,
            )
            if isinstance(exc, AgentExecutionError):
                raise
            raise AgentExecutionError(f"{self.name} failed: {exc}") from exc

    def validate(self, agent_input: InputT) -> None:
        return None

    async def prepare(self, agent_input: InputT) -> PreparedT:
        return agent_input  # type: ignore[return-value]

    @abstractmethod
    async def execute(self, prepared_input: PreparedT) -> object:
        raise NotImplementedError

    async def parse(self, raw_output: object) -> OutputT:
        return raw_output  # type: ignore[return-value]
