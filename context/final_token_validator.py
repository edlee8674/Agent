class FinalTokenValidator:
    def __init__(self,token_counter,max_tokens):
        self.token_counter = token_counter
        self.max_tokens = max_tokens

    def validate(self, messages):
        return self.count_messages_tokens(messages) <= self.max_tokens

    def count_messages_tokens(self, messages):
        total = 0
        for message in messages:
            total += self.token_counter.count(message["content"])
        return total
