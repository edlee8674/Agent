from memory.scoring import MemoryScorer

# 将memory按价值排序
class MemoryRanker:
    def __init__(self, scorer: MemoryScorer, top_k=5):
        self.scorer = scorer
        self.top_k = top_k

    def rank(self, memories):
        valid_memories = [memory for memory in memories if not memory.is_expired()]
        return sorted(
            valid_memories,
            key=self.scorer.score,
            reverse=True,
        )[:self.top_k]
