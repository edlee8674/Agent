import chromadb

from infrastructure.embedding_service import EmbeddingService
from memory.repository import MemoryRepository
from memory.status import MemoryStatus


class ChromaMemoryRepository(MemoryRepository):

    def __init__(self, embedding_service: EmbeddingService, path="./chromadb", collection_name="memory"):
        self.embedding_service = embedding_service
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine"
            }
        )
    #    self._migrate_legacy_status()

    # def _migrate_legacy_status(self):
    #     """为 status 字段引入前保存的记忆补上默认状态。"""
    #     records = self.collection.get(include=["metadatas"])
    #     for memory_id, metadata in zip(records["ids"], records["metadatas"]):
    #         if metadata is not None and "status" not in metadata:
    #             self.collection.update(
    #                 ids=[memory_id],
    #                 metadatas=[{"status": MemoryStatus.ACTIVE.value}],
    #             )

    def add_memory(self, memory):
        embedding = self.embedding_service.create_embedding(memory.fact)
        self.collection.add(
            embeddings=[embedding],
            documents=[memory.fact],
            metadatas=[memory.to_metadata()],
            ids=[memory.id],
        )

    def query_memory(self, text, include_archived=False, top_k=3):
        embedding = self.embedding_service.create_embedding(text)
        query_args = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }
        if not include_archived:
            query_args["where"] = {"status": MemoryStatus.ACTIVE.value}
        return self.collection.query(**query_args)

    def update_memory(self, memory_id, memory):
        embedding = self.embedding_service.create_embedding(memory.fact)
        self.collection.update(
            embeddings=[embedding],
            documents=[memory.fact],
            metadatas=[memory.to_metadata()],
            ids=[memory_id],
        )

    def archive_memory(self, memory_id, archived_at):
        self.collection.update(
            ids=[memory_id],
            metadatas=[
                {
                    "status": MemoryStatus.ARCHIVED.value,
                    "archived_at": archived_at.isoformat(),
                }
            ],
        )

    def delete_memory(self, memory_id):
        self.collection.delete(ids=[memory_id])

    def count_memories(self):
        return self.collection.count()

    def get_all_memories(self, include_archived=False):
        get_args = {}
        if not include_archived:
            get_args["where"] = {"status": MemoryStatus.ACTIVE.value}
        return self.collection.get(**get_args)
