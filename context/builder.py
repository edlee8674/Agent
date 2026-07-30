from context.models import Context

class ContextBuilder:

    def __init__(self, retriever, short_memory, summary_memory, ranker, token_budget_manager):
        self.retriever = retriever
        self.short_memory = short_memory
        self.summary_memory = summary_memory
        self.ranker = ranker
        self.token_budget_manager = token_budget_manager

    def build(self, user_input: str) -> Context:
        memories = self.retriever.search_memory(user_input)
        ranked_memories = self.ranker.rank(memories)
        short_memory = self.short_memory.get()
        summary_memory = self.summary_memory.get()
        context = Context(
            user_input=user_input,
            memories=ranked_memories,
            short_memory=short_memory,
            summary_memory=summary_memory
        )
        return self.token_budget_manager.apply(context)
