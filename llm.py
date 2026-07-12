#将client职责单独放入一个文件中，弃用embedding.py，其他文件不需要知道openai
from openai import OpenAI

from config import (
    API_KEY,
    BASE_URL,
    CHAT_MODEL,
    EMBEDDING_MODEL
)
from memory.embedding_cache import EmbeddingCache

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
_cache = EmbeddingCache()

def chat(messages):
    return client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages
    )

def create_embedding(text: str)-> list[float]:
    embedding = _cache.get(text)

    if embedding is not None:
        print("Embedding Cache Hit")
        return embedding

    print("Embedding API")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response.data[0].embedding
    _cache.save(text, embedding)
    return embedding
