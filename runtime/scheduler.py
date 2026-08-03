from datetime import datetime, timedelta

from config import REFLECT_INTERVAL_HOURS, REFLECT_MEMORY_THRESHOLD
from memory.lifecycle_service import MemoryLifecycleService
from runtime.state import RuntimeState


class RuntimeScheduler:

    def should_reflect(self, state: RuntimeState):
        if state.last_reflection_time is None:
            return True
        enough_time = datetime.now() - state.last_reflection_time >= timedelta(hours=REFLECT_INTERVAL_HOURS)
        enough_memory = state.memory_count- state.memory_count_after_reflection>= REFLECT_MEMORY_THRESHOLD

        return enough_time or enough_memory