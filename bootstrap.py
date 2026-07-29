from llm import LLMClient

from memory.application import MemoryApplication
from memory.embedding_cache import EmbeddingCache
from memory.extractor import MemoryExtractor
from memory.validator import MemoryValidator
from memory.reflection import MemoryReflection
from memory.merger import MemoryMerger

from memory.retriever import MemoryRetriever
from memory.vector_store import MemoryRepository
from memory.writer import MemoryWriter

from runtime.application import RuntimeApplication
from runtime.scheduler import RuntimeScheduler
from runtime.state_store import RuntimeStateStore


def create_memory_application():
    embedding_cache = EmbeddingCache()
    llm = LLMClient(embedding_cache)
    runtime_store = RuntimeStateStore()
    runtime_scheduler = RuntimeScheduler()
    runtime = RuntimeApplication(runtime_store, runtime_scheduler)
    repository = MemoryRepository()
    retriever = MemoryRetriever(llm, repository)
    writer = MemoryWriter(llm, repository)
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
