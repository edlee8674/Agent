class MemoryLifecycleService:

    def __init__(self, retriever, lifecycle_manager, writer):
        self.retriever = retriever
        self.lifecycle_manager = lifecycle_manager
        self.writer = writer

    def process(self):
        memories = self.retriever.get_all_memory()

        for memory in memories:
            if self.lifecycle_manager.should_archive(memory):
                self.writer.archive(memory.id)