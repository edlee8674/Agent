from dataclasses import dataclass, field
from typing import Any, Optional

from memory.models import Memory

@dataclass
class Context:

    user_input: str
    memories: list[Memory] = field(default_factory=list)
    short_memory: list[dict[str, Any]] = field(default_factory=list)
    summary_memory: Optional[str] = None
