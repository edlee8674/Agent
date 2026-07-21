from openai import OpenAI

from config import API_KEY, BASE_URL, CHAT_MODEL, EMBEDDING_MODEL
from memory.embedding_cache import EmbeddingCache


class LLMClient:
    def __init__(self, embedding_cache: EmbeddingCache | None = None):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.embedding_cache = embedding_cache or EmbeddingCache()

    def chat(self, messages):
        return self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
        )

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
