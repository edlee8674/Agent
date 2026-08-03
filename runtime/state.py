from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RuntimeState:

    memory_count: int = 0

    last_reflection_time: Optional[datetime] = None

    memory_count_after_reflection: int = 0

    reflection_count: int = 0

    last_lifecycle_run_time: Optional[datetime] = None