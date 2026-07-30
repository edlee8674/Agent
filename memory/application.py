from dataclasses import replace

from memory.action import MemoryAction
from memory.models import Memory


class MemoryApplication:
    def __init__(
        self,
        llm,
        retriever,
        validator,
        merger,
        reflection,
        writer,
        runtime,
        extractor,
        context_builder,
        prompt_builder
    ):
        self.llm = llm
        self.retriever = retriever
        self.validator = validator
        self.merger = merger
        self.reflection = reflection
        self.writer = writer
        self.runtime = runtime
        self.extractor = extractor
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

    def build_context(self, user_input):
        return self.context_builder.build(user_input)

    def build_prompt(self, context):
        return self.prompt_builder.build(context)

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

    def close(self):
        self.runtime.close()
