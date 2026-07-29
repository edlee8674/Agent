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
