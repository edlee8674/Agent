from dataclasses import replace

from context.models import Context


class ContextCompressor:
    def __init__(self,token_counter):
        self.token_counter = token_counter

    # 每次移除排序最低的一条长期记忆，使用 replace 返回新 Context。
    def compress(self,context: Context) -> Context:
        return replace(context, memories=context.memories[:-1])
