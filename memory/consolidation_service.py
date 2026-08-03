from memory.consolidation_policy import ConsolidationPolicy
from memory.consolidator import MemoryConsolidator
from memory.retriever import MemoryRetriever
from memory.writer import MemoryWriter


class MemoryConsolidationService:
    def __init__(self, retriever: MemoryRetriever, policy: ConsolidationPolicy, consolidator: MemoryConsolidator, writer:MemoryWriter):
        self.retriever = retriever
        self.policy = policy
        self.consolidator = consolidator
        self.writer = writer

    def process(self):
        memories = self.retriever.get_all_memory()
        groups = self.policy.select_groups(memories)
        for group in groups:
            result = self.consolidator.consolidate(group)

            if result is not None:
                self.writer.consolidate(result)
