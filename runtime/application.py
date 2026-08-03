from datetime import datetime

from runtime.scheduler import RuntimeScheduler
from runtime.state_store import RuntimeStateStore


class RuntimeApplication:
    def __init__(self, store=None, scheduler=None):
        self.store = store or RuntimeStateStore()
        self.scheduler = scheduler or RuntimeScheduler()
        self.state = self.store.load()

    def refresh_memory_count(self, memory_count: int):
        self.state.memory_count = memory_count
        self.store.save(self.state)

    def should_reflect(self):
        return self.scheduler.should_reflect(self.state)

    def after_reflection(self):
        self.state.memory_count_after_reflection = self.state.memory_count
        self.state.last_reflection_time = datetime.now()
        self.state.reflection_count += 1
        self.store.save(self.state)

    def should_run_lifecycle(self):
        return self.scheduler.should_run_lifecycle(self.state)

    def after_lifecycle(self):
        self.state.last_lifecycle_run_time = datetime.now()
        self.store.save(self.state)

    def should_run_consolidation(self):
        return self.scheduler.should_run_consolidation(self.state)

    def after_consolidation(self):
        self.state.last_consolidation_time = datetime.now()
        self.store.save(self.state)

    def close(self):
        self.store.close()
