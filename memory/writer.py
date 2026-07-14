from memory.action import MemoryAction
from llm import create_embedding
from memory.models import Memory
from memory.reflection import ReflectionResult
from memory.validator import ValidatorResult
from memory.vector_store import add_memory, update_memory, delete_memory


def write(memory: Memory, result: ValidatorResult):
    embedding = create_embedding(memory.fact)
    metadata = memory.to_metadata()

    if result.action == MemoryAction.ADD:
        add_memory(memory.id, memory.fact, embedding, metadata)
    elif result.action == MemoryAction.UPDATE:
        if result.target_id is None:
            raise ValueError("UPDATE action requires target_id")
        update_memory(result.old_memory.id, memory.fact, embedding, metadata)
    elif result.action == MemoryAction.IGNORE:
        pass

def apply(result: ReflectionResult):
    for memory in result.add:
        add_memory(memory)

    for memory in result.update:
        update_memory(memory)

    for id in result.delete:
        delete_memory(id)