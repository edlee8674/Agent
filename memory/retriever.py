
from llm import create_embedding
from memory.models import Memory
from memory.vector_store import query_memory


def search_memory(text):
    embedding = create_embedding(text)
    result = query_memory(embedding)
    return to_memory_list(result)

def search_memory_by_embedding(embedding):
    result = query_memory(embedding)
    print("result:",result)
    print("memories:",to_memory_list(result))
    return to_memory_list(result)

def to_memory_list(collection):
    memories = []
    for i in range(len(collection["ids"][0])):
        metadata = collection["metadatas"][0][i]
        distance = collection["distances"][0][i]
        memory = Memory.from_chroma(
            collection["ids"][0][i],
            collection["documents"][0][i],
            metadata,
            distance,
        )
        memories.append(memory)
    return memories

def format_vector_memory(memories):
    if not memories:
        return "无"
    result = []
    for memory in memories:
        if memory.is_expired():
            continue
        result.append(memory.fact)
    return "\n".join(result) or "无"

def format_short_memory(messages):
    return "\n".join(
        f"{message['role']}:\n{message['content']}"
        for message in messages
    )
