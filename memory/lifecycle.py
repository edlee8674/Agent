import math
from datetime import date, datetime

from memory.models import Memory


class MemoryLifecycleManager:
    def is_expired(self, memory: Memory, today: date | None = None) -> bool:
        return memory.is_expired(today)

    def calculate_decay(self,memory,today=None,decay_days=180)-> float:
        today = today or date.today()
        age_days = (today - date.fromisoformat(memory.created_time)).days
        if age_days <= 0:
            return 1.0
        return math.exp(-age_days / decay_days)

    def should_archive(self, memory,today=None):

        if self.is_expired(memory,today):
            return True
        decay = self.calculate_decay(memory,today)
        return decay < 0.1