import chromadb


class MemoryRepository:
    def __init__(self, path="./chromadb", collection_name="memory"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_memory(self, memory_id, text, embedding, metadata):
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id],
        )

    def query_memory(self, embedding, top_k=3):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def update_memory(self, memory_id, text, embedding, metadata):
        self.collection.update(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id],
        )

    def delete_memory(self, memory_id):
        self.collection.delete(ids=[memory_id])

    def count_memories(self):
        return self.collection.count()

    def get_all_memories(self):
        return self.collection.get()
