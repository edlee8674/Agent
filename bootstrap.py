from infrastructure.chroma_repository import ChromaMemoryRepository
from infrastructure.embedding_service import EmbeddingService
from llm import LLMClient

from memory.application import MemoryApplication
from memory.embedding_cache import EmbeddingCache
from memory.extractor import MemoryExtractor
from memory.validator import MemoryValidator
from memory.reflection import MemoryReflection
from memory.merger import MemoryMerger

from memory.retriever import MemoryRetriever
from memory.writer import MemoryWriter

from runtime.application import RuntimeApplication
from runtime.scheduler import RuntimeScheduler
from runtime.state_store import RuntimeStateStore


def create_memory_application():
    embedding_cache = EmbeddingCache()
    llm = LLMClient(embedding_cache)
    embedding_service = EmbeddingService(llm.client, embedding_cache)
    runtime_store = RuntimeStateStore()
    runtime_scheduler = RuntimeScheduler()
    runtime = RuntimeApplication(runtime_store, runtime_scheduler)
    repository = ChromaMemoryRepository(embedding_service)
    retriever = MemoryRetriever(repository)
    writer = MemoryWriter(repository)
    validator = MemoryValidator(llm)
    merger = MemoryMerger(llm)
    reflection = MemoryReflection(llm)
    extractor = MemoryExtractor(llm)

    return MemoryApplication(
        llm=llm,
        retriever=retriever,
        validator=validator,
        merger=merger,
        reflection=reflection,
        writer=writer,
        runtime=runtime,
        extractor=extractor
    )
