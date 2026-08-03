from datetime import date

from memory.action import MemoryAction
from memory.consolidation_result import ConsolidationResult
from memory.operation import ReflectionResult
from memory.repository import MemoryRepository
from memory.validator import ValidatorResult


class MemoryWriter:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def _add(self, memory):
        self.repository.add_memory(memory)

    def _update(self, memory_id, memory):
        self.repository.update_memory(memory_id, memory)

    def write(self, result: ValidatorResult):
        memory = result.new_memory
        if result.action == MemoryAction.ADD:
            self._add(memory)
        elif result.action == MemoryAction.UPDATE:
            if result.old_memory is None:
                raise ValueError("UPDATE action requires old_memory")
            self._update(result.old_memory.id, memory)

    def archive(self, memory_id, archived_at=None):
        self.repository.archive_memory(memory_id, archived_at or date.today())

    def forget(self,memory_id):
        self.repository.delete_memory(memory_id)

    def consolidate(self, result: ConsolidationResult):
        self._add(result.consolidated_memory)
        for memory_id in result.source_memory_ids:
            self.archive(memory_id)

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
            elif operation.action == MemoryAction.ARCHIVE:
                if not operation.target_ids:
                    raise ValueError("Reflection ARCHIVE requires target_ids")
                for memory_id in operation.target_ids:
                    self.archive(memory_id)
