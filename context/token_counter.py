from abc import ABC, abstractmethod
class TokenCounter(ABC):
    @abstractmethod
    def count(self, text: str) -> int:
        pass