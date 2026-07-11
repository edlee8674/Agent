import chromadb

chroma_client  = chromadb.PersistentClient(
    path="./chromadb"
)

collections = chroma_client.get_or_create_collection(
    name="memory"
)

memory_data = []

def add_memory(id, text, embedding,metadata):

    collections.add(
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
        ids=[id]
    )
    print("add-collections:",collections)


def query_memory(embeddings,top_k=3):

    return collections.query(
        query_embeddings=[embeddings],
        n_results=top_k
    )


def update_memory(id, text, embedding,metadata):
    collections.update(
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
        ids=[id]
    )
    print("update-collections:", collections)


def delete_memory(id,embedding):
    collections.delete(
        ids=[id]
    )
