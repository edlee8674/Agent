from openai import OpenAI
from memory.embedding_cache import EmbeddingCache
from config import EMBEDDING_MODEL, API_KEY, BASE_URL

client = OpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)
cache = EmbeddingCache()

def create_embedding(text: str):
    embedding = cache.get(text)

    if embedding is not None:
        print("Embedding Cache Hit")
        return embedding
    print("Embedding API")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response.data[0].embedding
    cache.save(text, embedding)
    return embedding



