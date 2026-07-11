from embedding import create_embedding
from memory.retriever import search_memory_by_embedding
from memory.vector_store import add_memory, update_memory


def save(memory):
    embedding = create_embedding(memory.fact)
    metadata = memory.to_metadata()
    memories = search_memory_by_embedding(embedding)

    if not memories:
        add_memory(
            id = memory.id,
            text= memory.fact,
            embedding= embedding,
            metadata= metadata
        )
        return
    top = memories[0]

    if top.distance < 0.1:
        update_memory(
            id=top.id,
            text=memory.fact,
            embedding=embedding,
            metadata=metadata
        )

        return

    add_memory(
        id=memory.id,
        text=memory.fact,
        embedding=embedding,
        metadata=metadata
    )