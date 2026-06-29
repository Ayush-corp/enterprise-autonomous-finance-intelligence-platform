from __future__ import annotations

from abc import ABC, abstractmethod


class NewsProvider(ABC):

    @abstractmethod
    async def fetch(
        self,
        *,
        symbol: str,
        company_name: str | None,
        limit: int,
    ) -> str:
        """
        Returns serialized news context
        ready for prompt injection.
        """