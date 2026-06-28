from abc import ABC, abstractmethod


class PortfolioService(ABC):

    @abstractmethod
    def evaluate(self, portfolio):
        pass