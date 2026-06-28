from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Generic, TypeVar

from structlog.stdlib import BoundLogger
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.logging import get_logger

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseAgent(ABC, Generic[InputT, OutputT]):
    """
    Base class for every production agent.
    """

    def __init__(self) -> None:
        self._logger: BoundLogger = get_logger().bind(
            agent=self.__class__.__name__
        )

    async def run(self, state: InputT) -> OutputT:
        started = perf_counter()

        self._logger.info("agent.started")

        self.validate(state)

        prepared = await self.prepare(state)

        try:
            async for attempt in AsyncRetrying(
                wait=wait_exponential(multiplier=1, min=1, max=16),
                stop=stop_after_attempt(3),
                retry=retry_if_exception_type(Exception),
                reraise=True,
            ):
                with attempt:
                    raw = await self.execute(prepared)

            result = await self.parse(raw)

            latency = (perf_counter() - started) * 1000

            self._logger.info(
                "agent.completed",
                latency_ms=round(latency, 2),
            )

            return result

        except RetryError:
            self._logger.exception("agent.retry_exhausted")
            raise

        except Exception:
            self._logger.exception("agent.failed")
            raise

    def validate(self, state: InputT) -> None:
        """
        Override if validation is required.
        """

    async def prepare(self, state: InputT):
        return state

    @abstractmethod
    async def execute(self, prepared):
        ...

    @abstractmethod
    async def parse(self, result) -> OutputT:
        ...