from llm import LLMClient
from memory.action import MemoryAction
from memory.operation import ReflectionResult
from memory.validator import ValidatorResult
from memory.vector_store import MemoryRepository


class MemoryWriter:
    def __init__(self, llm: LLMClient, repository: MemoryRepository):
        self.llm = llm
        self.repository = repository

    def _add(self, memory):
        embedding = self.llm.create_embedding(memory.fact)
        self.repository.add_memory(
            memory.id,
            memory.fact,
            embedding,
            memory.to_metadata(),
        )

    def _update(self, memory_id, memory):
        embedding = self.llm.create_embedding(memory.fact)
        self.repository.update_memory(
            memory_id,
            memory.fact,
            embedding,
            memory.to_metadata(),
        )

    def write(self, result: ValidatorResult):
        memory = result.new_memory
        if result.action == MemoryAction.ADD:
            self._add(memory)
        elif result.action == MemoryAction.UPDATE:
            if result.old_memory is None:
                raise ValueError("UPDATE action requires old_memory")
            self._update(result.old_memory.id, memory)

    def apply(self, result: ReflectionResult):
        for operation in result.operations:
            if operation.action == MemoryAction.ADD:
                if operation.memory is None:
                    raise ValueError("Reflection ADD requires memory")
                self._add(operation.memory)
            elif operation.action == MemoryAction.UPDATE:
                if operation.memory is None or not operation.target_ids:
                    raise ValueError("Reflection UPDATE requires memory and target_ids")
                self._update(operation.target_ids[0], operation.memory)
            elif operation.action == MemoryAction.DELETE:
                for memory_id in operation.target_ids:
                    self.repository.delete_memory(memory_id)
            elif operation.action == MemoryAction.MERGE:
                if operation.memory is None or not operation.target_ids:
                    raise ValueError("Reflection MERGE requires memory and target_ids")
                self._update(operation.target_ids[0], operation.memory)
                for memory_id in operation.target_ids[1:]:
                    self.repository.delete_memory(memory_id)
