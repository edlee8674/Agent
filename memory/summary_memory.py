import tiktoken
import json

from config import MAX_TOKEN, SYSTEM_PROMPT
from llm import LLMClient

def count_tokens(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    text = json.dumps(
        messages,
        ensure_ascii=False
    )
    return len(encoding.encode(text))

def trim_messages_by_tokens(llm: LLMClient, messages):
    print(count_tokens(messages))

    while count_tokens(messages) > MAX_TOKEN:

        messages_for_summary = [
            m for m in messages
            if not (
                    m.get("role") == "system"
                    and m.get("name") == "memory"
            )
        ]

        summary = summarize(llm, messages_for_summary)
        recent_messages = messages[-6:]
        messages = [
                       {
                           "role": "system",
                           "content": SYSTEM_PROMPT
                       },
                       {
                           "role": "system",
                           "content": f"历史摘要：\n{summary}"
                       }
                   ] + recent_messages
    return messages

def summarize(llm: LLMClient, messages):
    response = llm.chat(
        messages + [
            {
                "role": "user",
                "name": "memory",
                "content": """
                    请总结以上聊天。
                
                    要求：
                    保留重要事实。
                    保留用户偏好。
                    200字以内。
                    """
            }
        ]
    )

    return response.choices[0].message.content
