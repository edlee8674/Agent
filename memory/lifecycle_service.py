class MemoryLifecycleService:

    def __init__(self,repository,lifecycle_manager,writer):
        self.repository = repository
        self.lifecycle_manager = lifecycle_manager
        self.writer = writer

    def process(self):
        memories = self.repository.get_all_memories()

        for memory in memories:
            if self.lifecycle_manager.should_archive(memory):
                self.writer.archive(memory.id)