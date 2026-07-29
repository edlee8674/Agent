from abc import ABC, abstractmethod

from memory.models import Memory


class MemoryRepository(ABC):
    @abstractmethod
    def add_memory(self, memory: Memory) -> None:
        pass

    @abstractmethod
    def query_memory(self, text: str, top_k: int = 3):
        pass

    @abstractmethod
    def update_memory(self, memory_id: str, memory: Memory) -> None:
        pass

    @abstractmethod
    def delete_memory(self, memory_id: str) -> None:
        pass

    @abstractmethod
    def count_memories(self) -> int:
        pass

    @abstractmethod
    def get_all_memories(self):
        pass
