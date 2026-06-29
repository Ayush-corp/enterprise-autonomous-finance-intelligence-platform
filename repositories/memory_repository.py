from abc import ABC, abstractmethod


class MemoryRepository(ABC):

    @abstractmethod
    async def save(self, id: str, document: str, metadata: dict):
        ...

    @abstractmethod
    async def search(self, query: str, limit: int = 5):
        ...