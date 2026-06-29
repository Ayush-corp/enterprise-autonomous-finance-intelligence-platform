import chromadb

from app.config.settings import get_settings

from repositories.memory_repository import (
    MemoryRepository,
)


class ChromaMemoryRepository(
    MemoryRepository
):

    def __init__(self):

        settings = get_settings()

        client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH
        )

        self.collection = client.get_or_create_collection(
            "investor_memory"
        )

    async def save(
        self,
        id: str,
        document: str,
        metadata: dict,
    ):

        self.collection.add(
            ids=[id],
            documents=[document],
            metadatas=[metadata],
        )

    async def search(
        self,
        query: str,
        limit: int = 5,
    ):

        return self.collection.query(
            query_texts=[query],
            n_results=limit,
        )