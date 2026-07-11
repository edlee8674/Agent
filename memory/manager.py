from memory.models import Memory
from memory.retriever import search_memory, format_vector_memory
from memory.writer import save


def save_memory(memory: Memory):
    save(memory)

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