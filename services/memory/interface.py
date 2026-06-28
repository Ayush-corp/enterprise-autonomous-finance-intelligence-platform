from abc import ABC, abstractmethod


class MemoryService(ABC):

    @abstractmethod
    def save(self, key: str, value: str):
        pass

    @abstractmethod
    def search(self, query: str):
        pass