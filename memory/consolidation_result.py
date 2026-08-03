from dataclasses import dataclass

from memory.models import Memory


@dataclass
class ConsolidationResult:
    consolidated_memory: Memory
    source_memory_ids: list[str]
    reason: str