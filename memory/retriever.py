from memory.lifecycle import MemoryLifecycleManager
from memory.models import Memory
from memory.repository import MemoryRepository
from memory.status import MemoryStatus


class MemoryRetriever:
    def __init__(self, repository: MemoryRepository , lifecycle:MemoryLifecycleManager):
        self.repository = repository
        self.lifecycle = lifecycle

    def search_memory(self, text, include_archived=False):
        memories = self.to_memory_list(
            self.repository.query_memory(text, include_archived=include_archived)
        )
        valid_memories = [
            m
            for m in memories
            if (include_archived or m.status == MemoryStatus.ACTIVE)
            and not self.lifecycle.is_expired(m)
        ]
        return valid_memories

    def get_all_memory(self, include_archived=False):
        memories = self.to_memory_list(
            self.repository.get_all_memories(include_archived=include_archived)
        )
        if include_archived:
            return memories
        return [memory for memory in memories if memory.status == MemoryStatus.ACTIVE]

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
