import json

import tiktoken
from context.token_counter import TokenCounter
class TiktokenTokenCounter(TokenCounter):
    def __init__(self, encoding_name: str = "cl100k_base"):
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count(self, text: str) -> int:
        if not text:
            return 0
        text = json.dumps(
            text,
            ensure_ascii=False
        )
        return len(self.encoding.encode(text))