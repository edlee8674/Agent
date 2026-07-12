from memory.action import MemoryAction
from llm import create_embedding
from memory.models import Memory
from memory.validator import ValidatorResult
from memory.vector_store import add_memory, update_memory

def write(memory: Memory, result: ValidatorResult):
    embedding = create_embedding(memory.fact)
    metadata = memory.to_metadata()

    if result.action == MemoryAction.ADD:
        add_memory(memory.id, memory.fact, embedding, metadata)
    elif result.action == MemoryAction.UPDATE:
        if result.target_id is None:
            raise ValueError("UPDATE action requires target_id")
        update_memory(result.target_id, memory.fact, embedding, metadata)
    elif result.action == MemoryAction.IGNORE:
        pass
    elif result.action == MemoryAction.MERGE:
        pass
