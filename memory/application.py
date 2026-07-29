from dataclasses import replace

from memory.action import MemoryAction
from memory.models import Memory
from memory.retriever import format_vector_memory


class MemoryApplication:
    def __init__(self, llm, retriever, validator, merger, reflection, writer, runtime, extractor):
        self.llm = llm
        self.retriever = retriever
        self.validator = validator
        self.merger = merger
        self.reflection = reflection
        self.writer = writer
        self.runtime = runtime
        self.extractor = extractor

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
