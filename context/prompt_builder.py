from context.models import Context


class PromptBuilder:
    def build(self,context: Context):
        return [
            {
                "role": "system",
                "content": self.build_system_prompt(context)
            },
            {
                "role": "user",
                "content": context.user_input
            }
        ]

    def build_system_prompt(self,context: Context):
        return f"""
        你是一个智能助手。
        用户相关信息：
        {self.format_summary(context)}
        相关长期记忆：
        {self.format_memories(context)}
        近期对话：
        {self.format_short_memory(context)}
        """

    def format_memories(self,context):
        result = []
        for memory in context.memories:
            result.append(
                f"""
                事实:
                {memory.fact}
                类别:
                {memory.category.value}
                """
            )
        return "\n".join(result)

    def format_summary(self,context):
        if context.summary_memory:
            return context.summary_memory
        return "暂无用户总结信息"

    def format_short_memory(self,context):
        return "\n".join(
            f"{message['role']}: {message['content']}"
            for message in context.short_memory
        )
