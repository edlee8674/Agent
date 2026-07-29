from context.models import Context

class ContextBuilder:

    def __init__(self,retriever, short_memory, summary_memory ):
        self.retriever = retriever
        self.short_memory = short_memory
        self.summary_memory = summary_memory

    def build(self, user_input: str) -> Context:
        memories = self.retriever.search_memory(user_input)

        short_memory = self.short_memory.get()
        summary_memory = self.summary_memory.get()

        return Context(
            user_input=user_input,
            memories=memories,
            short_memory=short_memory,
            summary_memory=summary_memory
        )