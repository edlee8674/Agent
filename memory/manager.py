from dataclasses import replace
from datetime import datetime

from memory.action import MemoryAction
from memory.merger import merge_memory
from memory.models import Memory
from memory.reflection import MemoryReflection
from memory.retriever import search_memory, format_vector_memory, count_memories_by_retriever, get_all_memory
from memory.validator import MemoryValidator
from memory.writer import apply, write
from runtime.scheduler import RuntimeScheduler
from runtime.state import RuntimeState

runtime_state = RuntimeState()
runtime_scheduler = RuntimeScheduler()
memory_reflection = MemoryReflection()

def save_memory(memory: Memory):
    memories = search_memory(memory.fact)

    result = MemoryValidator().validate(memory, memories)
    if result.action == MemoryAction.MERGE:
        merged_memory = merge_memory(result.old_memory, result.new_memory)
        result = replace(
            result,
            action=MemoryAction.UPDATE,
            new_memory=merged_memory,
        )
    write(result)

    runtime_state.memory_count = count_memories_by_retriever()

    if runtime_scheduler.should_reflect(runtime_state):
        run_reflection(runtime_state)

def reflect_memory(memories: list[Memory]):
    result = memory_reflection.reflect(memories)

    apply(result)

def get_vector_memory(user_input):
    return search_memory(user_input)

def run_reflection(state: RuntimeState):
    memories = get_all_memory()
    result = memory_reflection.reflect(memories)
    apply(result)
    state.memory_count = count_memories_by_retriever()
    state.memory_count_after_reflection = state.memory_count
    state.last_reflection_time = datetime.now()
    state.reflection_count +=1

def build_context(user_input):

    vector = get_vector_memory(user_input)
    vector_text = format_vector_memory(vector)
    return [
        {
            "role":"system",
            "content":
            f"""
            相关记忆:
            {vector_text}
            """
        }
    ]
