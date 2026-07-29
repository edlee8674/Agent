from config import EMBEDDING_MODEL
from memory.embedding_cache import EmbeddingCache


class EmbeddingService:

    def __init__(self, client , embedding_cache: EmbeddingCache | None = None):
        self.client = client
        self.embedding_cache = embedding_cache or EmbeddingCache()

    def create_embedding(self, text: str) -> list[float]:
        embedding = self.embedding_cache.get(text)
        if embedding is not None:
            print("Embedding Cache Hit")
            return embedding

        print("Embedding API")
        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )
        embedding = response.data[0].embedding
        self.embedding_cache.save(text, embedding)
        return embedding