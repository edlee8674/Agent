from dataclasses import replace

from memory.action import MemoryAction
from memory.models import Memory
from memory.status import MemoryStatus


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
        prompt_builder,
        token_compressor,
        final_token_validator,
        lifecycle,
        lifecycle_service
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
        self.token_compressor = token_compressor
        self.final_token_validator = final_token_validator
        self.lifecycle = lifecycle
        self.lifecycle_service = lifecycle_service

    def build_context(self, user_input):
        if self.runtime.should_run_lifecycle():
            self.lifecycle_service.process()
            self.runtime.after_lifecycle()
        return self.context_builder.build(user_input)

    def build_prompt(self, context):
        return self.prompt_builder.build(context)

    def prepare_messages(self, context):
        """构建满足最终 Token 限制的 Prompt。"""
        messages = self.build_prompt(context)
        while not self.final_token_validator.validate(messages):
            compressed_context = self.token_compressor.compress(context)
            if compressed_context == context:
                raise ValueError("上下文超过 Token 限制，且没有可压缩的长期记忆。")
            context = compressed_context
            messages = self.build_prompt(context)
        return messages

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
