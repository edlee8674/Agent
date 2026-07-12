import json

from llm import chat
from memory.models import Memory

def merge_memory(old_memory: Memory, new_memory: Memory) -> Memory:
    prompt = f"""
合并两条关于同一用户的长期记忆，输出 JSON：
{{
  "fact": "",
  "category": "",
  "importance": 0.0,
  "ttl": null
}}

旧记忆：{old_memory}
新记忆：{new_memory}
"""

    response = chat([{"role": "user", "content": prompt}])
    data = json.loads(response.choices[0].message.content)

    return Memory(
        id=old_memory.id,
        fact=data["fact"],
        category=data["category"],
        importance=data["importance"],
        ttl=data["ttl"],
        created_time=old_memory.created_time,
    )