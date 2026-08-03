from datetime import datetime, timedelta

from config import REFLECT_INTERVAL_HOURS, REFLECT_MEMORY_THRESHOLD, LIFECYCLE_INTERVAL_HOURS, \
    CONSOLIDATION_INTERVAL_HOURS
from runtime.state import RuntimeState


class RuntimeScheduler:

    def should_reflect(self, state: RuntimeState):
        if state.last_reflection_time is None:
            return True
        enough_time = datetime.now() - state.last_reflection_time >= timedelta(hours=REFLECT_INTERVAL_HOURS)
        enough_memory = state.memory_count- state.memory_count_after_reflection>= REFLECT_MEMORY_THRESHOLD

        return enough_time or enough_memory

    def should_run_lifecycle(self, state: RuntimeState):
        if state.last_lifecycle_run_time is None:
            return True
        enough_time =  datetime.now() - state.last_lifecycle_run_time >= timedelta(hours=LIFECYCLE_INTERVAL_HOURS)

        return enough_time

    def should_run_consolidation(self, state: RuntimeState):
        if state.last_consolidation_time is None:
            return True
        enough_time =  datetime.now() - state.last_consolidation_time >= timedelta(hours=CONSOLIDATION_INTERVAL_HOURS)

        return enough_time
