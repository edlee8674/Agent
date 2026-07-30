import math
from datetime import datetime

from memory.models import Memory


class MemoryScorer:

    def __init__(
        self,
        similarity_weight=0.5,
        importance_weight=0.3,
        recency_weight=0.2,
        decay_days=30
    ):
        self.similarity_weight = similarity_weight
        self.importance_weight = importance_weight
        self.recency_weight = recency_weight
        self.decay_days = decay_days

    def score(self, memory: Memory):
        if memory.is_expired():
            return 0

        similarity = self.calculate_similarity(memory.distance)
        importance = memory.importance
        recency = self.calculate_recency(memory.created_time)
        return (
                self.similarity_weight * similarity
                +
                self.importance_weight * importance
                +
                self.recency_weight * recency
        )

    def calculate_recency(self,created_time: str):
        created = datetime.fromisoformat(created_time)
        age_days = max((datetime.now() - created).days,0)
        return math.exp(-age_days / self.decay_days)

    def calculate_similarity(self,distance: float | None):
        if distance is None:
            return 0

        return 1 - distance