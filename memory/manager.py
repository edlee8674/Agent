from dataclasses import replace

from memory.action import MemoryAction
from memory.merger import merge_memory
from memory.models import Memory
from memory.retriever import search_memory, format_vector_memory
from memory.validator import MemoryValidator
from memory.writer import write


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
    write(memory,result)

def get_vector_memory(user_input):
    return search_memory(user_input)

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
