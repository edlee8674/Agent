from dataclasses import dataclass, field
from typing import Optional

from memory.action import MemoryAction
from memory.models import Memory


@dataclass
class MemoryOperation:
    action: MemoryAction
    memory: Optional[Memory] = None
    target_ids: list[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class ReflectionResult:
    operations: list[MemoryOperation] = field(default_factory=list)