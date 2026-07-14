from memory.action import MemoryAction
from llm import create_embedding
from memory.operation import ReflectionResult
from memory.validator import ValidatorResult
from memory.vector_store import add_memory, update_memory, delete_memory


def _add(memory):
    embedding = create_embedding(memory.fact)
    metadata = memory.to_metadata()
    add_memory(memory.id, memory.fact, embedding, metadata)


def _update(memory_id, memory):
    embedding = create_embedding(memory.fact)
    metadata = memory.to_metadata()
    update_memory(memory_id, memory.fact, embedding, metadata)


def write(result: ValidatorResult):
    memory = result.new_memory

    if result.action == MemoryAction.ADD:
        _add(memory)
    elif result.action == MemoryAction.UPDATE:
        if result.old_memory is None:
            raise ValueError("UPDATE action requires old_memory")
        _update(result.old_memory.id, memory)
    elif result.action == MemoryAction.IGNORE:
        pass


def apply(result: ReflectionResult):
    for operation in result.operations:
        if operation.action == MemoryAction.ADD:
            if operation.memory is None:
                raise ValueError("Reflection ADD requires memory")
            _add(operation.memory)
        elif operation.action == MemoryAction.UPDATE:
            if operation.memory is None or not operation.target_ids:
                raise ValueError("Reflection UPDATE requires memory and target_ids")
            _update(operation.target_ids[0], operation.memory)
        elif operation.action == MemoryAction.DELETE:
            for memory_id in operation.target_ids:
                delete_memory(memory_id)
        elif operation.action == MemoryAction.MERGE:
            if operation.memory is None or not operation.target_ids:
                raise ValueError("Reflection MERGE requires memory and target_ids")
            _update(operation.target_ids[0], operation.memory)
            for memory_id in operation.target_ids[1:]:
                delete_memory(memory_id)
