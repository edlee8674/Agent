
from llm import create_embedding
from memory.models import Memory
from memory.vector_store import query_memory, get_all_memories, count_memories


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
    ids = collection["ids"]
    documents = collection["documents"]
    metadatas = collection["metadatas"]
    distances = collection.get("distances")

    if ids and isinstance(ids[0], list):
        ids = ids[0]
        documents = documents[0]
        metadatas = metadatas[0]
        distances = distances[0]
    elif distances is None:
        distances = [None] * len(ids)

    memories = []
    for i in range(len(ids)):
        metadata = metadatas[i]
        distance = distances[i]
        memory = Memory.from_chroma(
            ids[i],
            documents[i],
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

def get_all_memory():
    return to_memory_list(get_all_memories())

def count_memories_by_retriever():
    return count_memories()
