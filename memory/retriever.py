from memory.models import Memory
from memory.repository import MemoryRepository


class MemoryRetriever:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def search_memory(self, text):
        return self.to_memory_list(self.repository.query_memory(text))

    def get_all_memory(self):
        return self.to_memory_list(self.repository.get_all_memories())

    def count_memories(self):
        return self.repository.count_memories()

    @staticmethod
    def to_memory_list(collection):
        ids = collection["ids"]
        documents = collection["documents"]
        metadatas = collection["metadatas"]
        distances = collection.get("distances")

        if ids and isinstance(ids[0], list):
            ids = ids[0]
            documents = documents[0]
            metadatas = metadatas[0]
            distances = distances[0]
        elif distances is None:
            distances = [None] * len(ids)

        return [
            Memory.from_chroma(ids[i], documents[i], metadatas[i], distances[i])
            for i in range(len(ids))
        ]


def format_vector_memory(memories):
    if not memories:
        return "无"
    facts = [memory.fact for memory in memories if not memory.is_expired()]
    return "\n".join(facts) or "无"


def format_short_memory(messages):
    return "\n".join(
        f"{message['role']}:\n{message['content']}"
        for message in messages
    )
