import math
from datetime import date, datetime, timedelta

from config import ARCHIVE_RETENTION_DAYS
from memory.category import MemoryCategory
from memory.models import Memory
from memory.status import MemoryStatus


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

    def should_forget(self, memory: Memory, today=None) -> bool:
        today = today or date.today()
        if memory.status != MemoryStatus.ARCHIVED:
            return False
        if memory.archived_at is None:
            return False

        if not self.is_archive_retention_elapsed(memory, today):
            return False

        if not self.is_low_value(memory, today):
            return False

        return self.is_forgettable_category(memory.category)

    def is_archive_retention_elapsed(self, memory, today):
        return today >= memory.archived_at + timedelta(ARCHIVE_RETENTION_DAYS)

    def is_low_value(self, memory, today):
        return self.calculate_decay(memory, today) < 0.05

    def is_forgettable_category(self, category):
        if category == MemoryCategory.PREFERENCE:
            return True
        if category == MemoryCategory.TEMPORARY_PREFERENCE:
            return True