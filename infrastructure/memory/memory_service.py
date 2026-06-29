import uuid

from repositories.memory_repository import (
    MemoryRepository,
)

from services.memory import MemoryService


class DefaultMemoryService(
    MemoryService
):

    def __init__(
        self,
        repository: MemoryRepository,
    ):

        self.repository = repository

    async def save(
        self,
        key: str,
        value: str,
    ):

        await self.repository.save(
            id=str(uuid.uuid4()),
            document=value,
            metadata={
                "key": key,
            },
        )

    async def search(
        self,
        query: str,
        limit: int = 5,
    ):

        return await self.repository.search(
            query=query,
            limit=limit,
        )