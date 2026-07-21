from dataclasses import replace

from llm import LLMClient
from memory.action import MemoryAction
from memory.extractor import MemoryExtractor
from memory.merger import MemoryMerger
from memory.models import Memory
from memory.reflection import MemoryReflection
from memory.retriever import MemoryRetriever, format_vector_memory
from memory.validator import MemoryValidator
from memory.vector_store import MemoryRepository
from memory.writer import MemoryWriter
from runtime.application import RuntimeApplication


class MemoryApplication:
    def __init__(self, llm=None, repository=None, runtime=None):
        self.llm = llm or LLMClient()
        self.repository = repository or MemoryRepository()
        self.writer = MemoryWriter(self.llm, self.repository)
        self.retriever = MemoryRetriever(self.llm, self.repository)
        self.extractor = MemoryExtractor(self.llm)
        self.validator = MemoryValidator(self.llm)
        self.merger = MemoryMerger(self.llm)
        self.reflection = MemoryReflection(self.llm)
        self.runtime = runtime or RuntimeApplication()

    def extract_memory(self, user_input, assistant_content):
        return self.extractor.extract_memory(user_input, assistant_content)

    def save_memory(self, memory: Memory):
        memories = self.retriever.search_memory(memory.fact)
        result = self.validator.validate(memory, memories)
        if result.action == MemoryAction.MERGE:
            merged_memory = self.merger.merge_memory(result.old_memory, result.new_memory)
            result = replace(
                result,
                action=MemoryAction.UPDATE,
                new_memory=merged_memory,
            )
        self.writer.write(result)
        self.runtime.refresh_memory_count(self.retriever.count_memories())

        if self.runtime.should_reflect():
            self.run_reflection()

    def run_reflection(self):
        memories = self.retriever.get_all_memory()
        self.reflect_memories(memories)
        self.runtime.refresh_memory_count(self.retriever.count_memories())
        self.runtime.after_reflection()

    def reflect_memories(self, memories: list[Memory]):
        result = self.reflection.reflect(memories)
        self.writer.apply(result)

    def build_context(self, user_input):
        vector_text = format_vector_memory(self.retriever.search_memory(user_input))
        return [{
            "role": "system",
            "content": f"相关记忆:\n{vector_text}",
        }]

    def close(self):
        self.runtime.close()
