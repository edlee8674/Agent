from context.builder import ContextBuilder
from context.prompt_builder import PromptBuilder
from context.token_budget import TokenBudgetManager, TokenBudgetConfig
from infrastructure.chroma_repository import ChromaMemoryRepository
from infrastructure.embedding_service import EmbeddingService
from infrastructure.token_counter import TiktokenTokenCounter
from llm import LLMClient

from memory.application import MemoryApplication
from memory.embedding_cache import EmbeddingCache
from memory.extractor import MemoryExtractor
from memory.ranker import MemoryRanker
from memory.scoring import MemoryScorer
from memory.short_memory import ShortMemory
from memory.summary_memory import SummaryMemory
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
    scorer = MemoryScorer()
    ranker = MemoryRanker(scorer, top_k=5)
    token_counter = TiktokenTokenCounter()
    token_config = TokenBudgetConfig(context_window=8000,reserved_output_tokens=1500,safety_margin=300)
    token_budget_manager = TokenBudgetManager(token_counter,token_config)
    context_builder = ContextBuilder(
        retriever,
        ShortMemory(),
        SummaryMemory(),
        ranker,
        token_budget_manager
    )
    prompt_builder = PromptBuilder()
    writer = MemoryWriter(repository)
    validator = MemoryValidator(llm)
    merger = MemoryMerger(llm)
    reflection = MemoryReflection(llm)
    extractor = MemoryExtractor(llm)

    return MemoryApplication(
        context_builder = context_builder,
        prompt_builder = prompt_builder,
        llm=llm,
        retriever=retriever,
        validator=validator,
        merger=merger,
        reflection=reflection,
        writer=writer,
        runtime=runtime,
        extractor=extractor
    )
