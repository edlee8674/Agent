from dataclasses import dataclass, replace

from context.models import Context
from context.token_counter import TokenCounter
from memory.models import Memory


@dataclass(frozen=True)
class TokenBudgetConfig:
    context_window: int
    #模型上下文总容量
    reserved_output_tokens: int
    #为模型回答预留的空间
    safety_margin: int = 300
    #防止估算误差和消息结构额外开销

    #max_input_tokens 返回本次输入真正可以使用的Token数
    @property
    def max_input_tokens(self) -> int:
        return self.context_window - self.reserved_output_tokens - self.safety_margin

# 计算当前context还能放多少memory
class TokenBudgetManager:

    def __init__(self, token_counter: TokenCounter, config: TokenBudgetConfig):
        self.token_counter = token_counter
        self.config = config

    def apply(self,context: Context) -> Context:
        fixed_tokens = self._count_fixed_context(context)
        available_tokens = max(self.config.max_input_tokens - fixed_tokens, 0)
        selected_memories = self._select_memories(context.memories, available_tokens)
        return replace(context,memories=selected_memories)

    def _count_fixed_context(self, context: Context) -> int:
        total = self.token_counter.count(context.user_input)
        total += self.token_counter.count(context.summary_memory or "")
        total += sum(self.token_counter.count(message) for message in context.short_memory)
        return total

    def _select_memories(self, memories: list[Memory], available_tokens: int) -> list[Memory]:
        selected = []
        remaining_tokens = available_tokens
        for memory in memories:
            memory_token = self.token_counter.count(memory.fact)
            if memory_token <= remaining_tokens:
                selected.append(memory)
                remaining_tokens -= memory_token
        return selected

