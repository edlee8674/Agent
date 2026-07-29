import chromadb

from infrastructure.embedding_service import EmbeddingService
from memory.repository import MemoryRepository


class ChromaMemoryRepository(MemoryRepository):

    def __init__(self, embedding_service: EmbeddingService, path="./chromadb", collection_name="memory"):
        self.embedding_service = embedding_service
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_memory(self, memory):
        embedding = self.embedding_service.create_embedding(memory.fact)
        self.collection.add(
            embeddings=[embedding],
            documents=[memory.fact],
            metadatas=[memory.to_metadata()],
            ids=[memory.id],
        )

    def query_memory(self, text, top_k=3):
        embedding = self.embedding_service.create_embedding(text)
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

    def update_memory(self, memory_id, memory):
        embedding = self.embedding_service.create_embedding(memory.fact)
        self.collection.update(
            embeddings=[embedding],
            documents=[memory.fact],
            metadatas=[memory.to_metadata()],
            ids=[memory_id],
        )

    def delete_memory(self, memory_id):
        self.collection.delete(ids=[memory_id])

    def count_memories(self):
        return self.collection.count()

    def get_all_memories(self):
        return self.collection.get()
