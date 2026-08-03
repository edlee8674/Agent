class MemoryLifecycleService:

    def __init__(self, retriever, lifecycle_manager, writer):
        self.retriever = retriever
        self.lifecycle_manager = lifecycle_manager
        self.writer = writer

    def process(self):
        active_memories = self.retriever.get_all_memory(include_archived=False)
        for memory in active_memories:
            if self.lifecycle_manager.should_archive(memory):
                self.writer.archive(memory.id)

        archived_memories = self.retriever.get_all_memory(include_archived=True)
        for memory in archived_memories:
            if self.lifecycle_manager.should_forget(memory):
                self.writer.forget(memory.id)
