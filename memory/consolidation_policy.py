from collections import defaultdict

from config import MIN_CONSOLIDATION_GROUP_SIZE
from memory.status import MemoryStatus


def group_by_category(active_memories):
    groups = defaultdict(list)
    for memory in active_memories:
        groups[memory.category].append(memory)
    return list(groups.values())


class ConsolidationPolicy:
    def select_groups(self, memories):
        active_memories = [
            memory
            for memory in memories
            if memory.status == MemoryStatus.ACTIVE
            and not memory.is_expired()
        ]

        groups = group_by_category(active_memories)

        return [
            group
            for group in groups
            if len(group) >= MIN_CONSOLIDATION_GROUP_SIZE
        ]
