from multiprocessing.util import Finalize

from context.builder import ContextBuilder
from context.compressor import ContextCompressor
from context.final_token_validator import FinalTokenValidator
from context.prompt_builder import PromptBuilder
from context.token_budget import TokenBudgetManager, TokenBudgetConfig
from infrastructure.chroma_repository import ChromaMemoryRepository
from infrastructure.embedding_service import EmbeddingService
from infrastructure.token_counter import TiktokenTokenCounter
from llm import LLMClient

from memory.application import MemoryApplication
from memory.consolidation_policy import ConsolidationPolicy
from memory.consolidation_service import MemoryConsolidationService
from memory.consolidator import MemoryConsolidator
from memory.embedding_cache import EmbeddingCache
from memory.extractor import MemoryExtractor
from memory.lifecycle import MemoryLifecycleManager
from memory.lifecycle_service import MemoryLifecycleService
from memory.ranker import MemoryRanker
from memory.scoring import MemoryScorer
from memory.short_memory import ShortMemory
from memory.summary_memory import SummaryMemory
from memory.validator import MemoryValidator
from memory.reflection import MemoryReflection
from memory.merger import MemoryMerger

from memory.retriever import MemoryRetriever
from memory.writer import MemoryWriter
from prompt.consolidation_prompt import ConsolidationPromptBuilder

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
    lifecycle = MemoryLifecycleManager()
    retriever = MemoryRetriever(repository,lifecycle)
    scorer = MemoryScorer(lifecycle)
    ranker = MemoryRanker(scorer, top_k=5)
    token_counter = TiktokenTokenCounter()
    token_config = TokenBudgetConfig(context_window=8000,reserved_output_tokens=1500,safety_margin=300)
    token_budget_manager = TokenBudgetManager(token_counter,token_config)
    final_token_validator = FinalTokenValidator(token_counter,max_tokens=10000)
    token_compressor = ContextCompressor(token_counter)
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
    lifecycle_service = MemoryLifecycleService(retriever, lifecycle, writer)
    consolidation_prompt_builder = ConsolidationPromptBuilder()
    consolidation_policy = ConsolidationPolicy()
    consolidator = MemoryConsolidator(llm, consolidation_prompt_builder)
    consolidation_service = MemoryConsolidationService(retriever, consolidation_policy, consolidator, writer)

    return MemoryApplication(
        consolidation_service = consolidation_service,
        lifecycle_service= lifecycle_service,
        lifecycle = lifecycle,
        token_compressor = token_compressor,
        final_token_validator = final_token_validator,
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
